# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QEvent, SIGNAL

from library.Utils import forceRef, forceBool
from library.crbcombobox import CRBComboBox

from Ui_MKBExSubclassPopup import Ui_MKBExSubclassPopup

__all__ = ( 'CMKBExSubclassPopup',
          )

class CMKBExSubclassPopup(QtGui.QFrame, Ui_MKBExSubclassPopup):
    def __init__(self, parent = None):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self.combo = parent
        self.setupUi(self)
        opt = self.comboStyleOption()
        self.setFrameStyle(parent.style().styleHint(QtGui.QStyle.SH_ComboBox_PopupFrameStyle, opt, parent))
        self.setFocusProxy(self.cmbC6)
        for combo in self.cmbC6, self.cmbC7, self.cmbC8, self.cmbC9, self.cmbC10:
            combo.installEventFilter(self)
            combo.setShowFields(CRBComboBox.showCode)
        self.connect(self.cmbC6, SIGNAL('currentIndexChanged(int)'), self.on_cmbC6_currentIndexChanged)
        self.connect(self.cmbC7, SIGNAL('currentIndexChanged(int)'), self.on_cmbC7_currentIndexChanged)
        self.connect(self.cmbC8, SIGNAL('currentIndexChanged(int)'), self.on_cmbC8_currentIndexChanged)
        self.connect(self.cmbC9, SIGNAL('currentIndexChanged(int)'), self.on_cmbC9_currentIndexChanged)
        self.connect(self.cmbC10, SIGNAL('currentIndexChanged(int)'), self.on_cmbC10_currentIndexChanged)
        self.MKB = None
        self.endDate = None
        self.tempValue = []


    def setInitComboPopupEnabled(self):
        self.setComboEnabled([self.cmbC7, self.cmbC8, self.cmbC9, self.cmbC10], forceBool(forceRef(self.cmbC6.value())))


    def comboStyleOption(self):
        opt = QtGui.QStyleOptionComboBox()
        opt.initFrom(self.combo)
        opt.subControls = QtGui.QStyle.SC_All
        opt.activeSubControls = QtGui.QStyle.SC_None
        opt.editable = False
        return opt


    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape):
                self.combo.hidePopup()
                return True
        return QtGui.QFrame.eventFilter(self, obj, event)


    def setEndDate(self, date):
        self.endDate = date


    def setTempValue(self, value):
        self.tempValue = value


    def updateItemsComboBoxes(self, MKB):
        db = QtGui.qApp.db
        tableMKBExSC = db.table('rbMKBExSubclass')
        tableMKBExSCItem = db.table('rbMKBExSubclass_Item')
        tableMKB_ExSubclass = db.table('MKB_ExSubclass')
        tableMKB = db.table('MKB')
        queryTable = tableMKB.innerJoin(tableMKB_ExSubclass, tableMKB_ExSubclass['master_id'].eq(tableMKB['id']))
        queryTable = queryTable.innerJoin(tableMKBExSC, tableMKBExSC['id'].eq(tableMKB_ExSubclass['exSubclass_id']))
        queryTable = queryTable.innerJoin(tableMKBExSCItem, tableMKBExSCItem['master_id'].eq(tableMKBExSC['id']))

        def getExSubclassIdList(MKBF, position):
            cond = [tableMKB['DiagID'].like(MKBF),
                    tableMKBExSC['position'].eq(position)]
#            if self.endDate:
#                cond.append(db.joinOr([tableF['endDate'].isNull(),
#                                        tableF['endDate'].dateGe(self.endDate)]))
            return db.getDistinctIdList(queryTable, [tableMKB_ExSubclass['exSubclass_id']], cond)

        def setTableExSC(cmbC, MKBF, MKBS, position):
            exSubclassIdList = []
            filter = u'id IN (NULL)'
            if len(MKBF) > 3:
                MKBF = MKBF[:5] if len(MKBF) > 5 else MKBF
                exSubclassIdList = getExSubclassIdList(MKBF, position)
                if exSubclassIdList:
                    filter = u'master_id IN (%s)'%(u','.join(str(exId) for exId in exSubclassIdList if exId))
            if not exSubclassIdList:
                exSubclassIdList = getExSubclassIdList(MKBS, position)
                if exSubclassIdList:
                    filter = u'master_id IN (%s)'%(u','.join(str(exId) for exId in exSubclassIdList if exId))
            cmbC.setTable('rbMKBExSubclass_Item', True, filter, u','.join(n for n in [tableMKBExSCItem['code'].name(), tableMKBExSCItem['name'].name()]))

        isValid = True
        self.cmbC6.clear()
        self.cmbC7.clear()
        self.cmbC8.clear()
        self.cmbC9.clear()
        self.cmbC10.clear()

        self.MKB = MKB[:3] if (MKB and len(MKB) > 3) else (MKB if MKB else None)
        if self.MKB:
            setTableExSC(self.cmbC6, MKB, self.MKB, 6)
            setTableExSC(self.cmbC7, MKB, self.MKB, 7)
            setTableExSC(self.cmbC8, MKB, self.MKB, 8)
            setTableExSC(self.cmbC9, MKB, self.MKB, 9)
            setTableExSC(self.cmbC10, MKB, self.MKB, 10)
        else:
            self.cmbC6.setTable('rbMKBExSubclass_Item', True, 'False')
            self.cmbC7.setTable('rbMKBExSubclass_Item', True, 'False')
            self.cmbC8.setTable('rbMKBExSubclass_Item', True, 'False')
            self.cmbC9.setTable('rbMKBExSubclass_Item', True, 'False')
            self.cmbC10.setTable('rbMKBExSubclass_Item', True, 'False')

        isValid = isValid and (self.cmbC6.model().searchCode(self.tempValue[0]) >= 0)
        isValid = isValid and (self.cmbC7.model().searchCode(self.tempValue[1]) >= 0)
        isValid = isValid and (self.cmbC8.model().searchCode(self.tempValue[2]) >= 0)
        isValid = isValid and (self.cmbC9.model().searchCode(self.tempValue[3]) >= 0)
        isValid = isValid and (self.cmbC10.model().searchCode(self.tempValue[4]) >= 0)

        if isValid:
            self.setValue(self.tempValue)
        else:
            self.setInitComboPopupEnabled()


    def setValue(self, d):
        def setComboValue(combo, value):
            blocked = combo.blockSignals(True)
            try:
                for i in xrange(combo.count()):
                    if unicode(combo.itemText(i)) == value:
                        combo.setCurrentIndex(i)
                        return
                combo.setCurrentIndex(0)
            finally:
                combo.blockSignals(blocked)

        setComboValue(self.cmbC6, d[0])
        setComboValue(self.cmbC7, d[1])
        setComboValue(self.cmbC8, d[2])
        setComboValue(self.cmbC9, d[3])
        setComboValue(self.cmbC10, d[4])
        self.setComboEnabled([self.cmbC7, self.cmbC8, self.cmbC9, self.cmbC10], forceBool(forceRef(self.cmbC6.value())))


    def getValue(self):
        codeList =  [unicode(self.cmbC6.code()),
                     unicode(self.cmbC7.code()),
                     unicode(self.cmbC8.code()),
                     unicode(self.cmbC9.code()),
                     unicode(self.cmbC10.code())
                    ]
        return codeList


    def onAnyCurrentIndexChanged(self, index):
        self.combo.updateValueFromPopup()


    def setComboEnabled(self, widgets, valPrev=False):
        for i, combo in enumerate(widgets):
            isEnable = valPrev
            if not valPrev and forceBool(forceRef(widgets[i].value())):
                combo.setValue(None)
            if i > 0:
                valPrev = forceBool(forceRef(widgets[i-1].value()))
                isEnable = valPrev
            combo.setEnabled(isEnable)


    def on_cmbC6_currentIndexChanged(self, index):
        self.onAnyCurrentIndexChanged(index)
        val = forceRef(self.cmbC6.value())
        widgets = [self.cmbC7, self.cmbC8, self.cmbC9, self.cmbC10]
        self.setComboEnabled(widgets, forceBool(val))


    def on_cmbC7_currentIndexChanged(self, index):
        self.onAnyCurrentIndexChanged(index)
        val = forceRef(self.cmbC7.value())
        widgets = [self.cmbC8, self.cmbC9, self.cmbC10]
        self.setComboEnabled(widgets, forceBool(val))


    def on_cmbC8_currentIndexChanged(self, index):
        self.onAnyCurrentIndexChanged(index)
        val = forceRef(self.cmbC8.value())
        widgets = [self.cmbC9, self.cmbC10]
        self.setComboEnabled(widgets, forceBool(val))


    def on_cmbC9_currentIndexChanged(self, index):
        self.onAnyCurrentIndexChanged(index)
        val = forceRef(self.cmbC9.value())
        if forceRef(self.cmbC9.value()):
            self.cmbC10.setEnabled(True)
        else:
            widgets = [self.cmbC10]
            self.setComboEnabled(widgets, forceBool(val))


    def on_cmbC10_currentIndexChanged(self, index):
        self.onAnyCurrentIndexChanged(index)

