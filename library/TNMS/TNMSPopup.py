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
from PyQt4.QtCore import Qt, SIGNAL, QEvent

from library.crbcombobox import CRBComboBox

from Ui_TNMSPopup import Ui_TNMSPopup

__all__ = ( 'CTNMSPopup',
          )

class CTNMSPopup(QtGui.QFrame, Ui_TNMSPopup):
    def __init__(self, parent = None):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self.combo = parent
        self.setupUi(self)
        opt = self.comboStyleOption()
        self.setFrameStyle(parent.style().styleHint(QtGui.QStyle.SH_ComboBox_PopupFrameStyle, opt, parent))
        self.setFocusProxy(self.cmbCTumor)

        for combo in self.cmbCTumor, self.cmbCNodus, self.cmbCMetastasis, self.cmbCStage, self.cmbPTumor, self.cmbPNodus, self.cmbPMetastasis, self.cmbPStage:
            combo.installEventFilter(self)
            self.connect(combo, SIGNAL('currentIndexChanged(int)'), self.onAnyCurrentIndexChanged)
        self.MKB = None
        self.isTest = False
        self.endDate = None
        self.tempValue = {}
        self.tempValueIdDict = {}
        self.cmbCTumor.setShowFields(CRBComboBox.showCode)
        self.cmbCNodus.setShowFields(CRBComboBox.showCode)
        self.cmbCMetastasis.setShowFields(CRBComboBox.showCode)
        self.cmbCStage.setShowFields(CRBComboBox.showCode, isTrim=True)
        self.cmbPTumor.setShowFields(CRBComboBox.showCode)
        self.cmbPNodus.setShowFields(CRBComboBox.showCode)
        self.cmbPMetastasis.setShowFields(CRBComboBox.showCode)
        self.cmbPStage.setShowFields(CRBComboBox.showCode, isTrim=True)


    def comboStyleOption(self):
        opt = QtGui.QStyleOptionComboBox()
        opt.initFrom(self.combo)
        opt.subControls = QtGui.QStyle.SC_All
        opt.activeSubControls = QtGui.QStyle.SC_None
        opt.editable = False # self.combo.isEditable()
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
        self.tempValue = value[0]
        self.tempValueIdDict = value[1]

    def updateItemsComboBoxes(self, MKB, isTest=False):
        def getCond(MKBF, tableF, dbF):
            cond = [tableF['MKB'].like(MKBF)]
            if self.endDate:
                cond.append(db.joinAnd([db.joinOr([tableF['endDate'].isNull(),
                                       tableF['endDate'].dateGe(self.endDate)]),
                                        db.joinOr([tableF['begDate'].isNull(),
                                                   tableF['begDate'].dateLe(self.endDate)])
                                        ]))
            return cond, db.joinAnd(cond)
        self.isTest = isTest
        isValid = True
        self.cmbCTumor.clear()
        self.cmbCNodus.clear()
        self.cmbCMetastasis.clear()
        self.cmbCStage.clear()
        self.cmbPTumor.clear()
        self.cmbPNodus.clear()
        self.cmbPMetastasis.clear()
        self.cmbPStage.clear()
        db = QtGui.qApp.db
        tableTumor = db.table('rbTumor')           # T
        tableNodus = db.table('rbNodus')           # N
        tableMetastasis = db.table('rbMetastasis') # M
        tableTNMphase = db.table('rbTNMphase')     # S
        self.MKB = MKB[:3] if (MKB and len(MKB) > 3) else (MKB if MKB else None)
        if self.MKB:
            # T
            TRecords = []
            if len(MKB) > 3:
                condT, filterT = getCond(MKB, tableTumor, db)
                self.cmbCTumor.setTable('rbTumor', True, filterT, u','.join(n for n in [tableTumor['code'].name(), tableTumor['name'].name()]))
                self.cmbPTumor.setTable('rbTumor', True, filterT, u','.join(n for n in [tableTumor['code'].name(), tableTumor['name'].name()]))
                TRecords = db.getRecordListGroupBy(tableTumor, ['DISTINCT RIGHT(rbTumor.code, LENGTH(rbTumor.code)-1) AS codeT, rbTumor.name AS nameT, rbTumor.id AS idT'], condT, 'codeT, nameT, idT', [tableTumor['code'].name(), tableTumor['name'].name()])
            if not TRecords:
                condT, filterT = getCond(self.MKB, tableTumor, db)
                self.cmbCTumor.setTable('rbTumor', True, filterT, u','.join(n for n in [tableTumor['code'].name(), tableTumor['name'].name()]))
                self.cmbPTumor.setTable('rbTumor', True, filterT, u','.join(n for n in [tableTumor['code'].name(), tableTumor['name'].name()]))
                TRecords = db.getRecordListGroupBy(tableTumor, ['DISTINCT RIGHT(rbTumor.code, LENGTH(rbTumor.code)-1) AS codeT, rbTumor.name AS nameT, rbTumor.id AS idT'], condT, 'codeT, nameT, idT', [tableTumor['code'].name(), tableTumor['name'].name()])
            if not TRecords and (MKB[:1] == 'C' or MKB[:2] == "D0"):
                condT, filterT = getCond('', tableTumor, db)
                self.cmbCTumor.setTable('rbTumor', True, filterT, u','.join(n for n in [tableTumor['code'].name(), tableTumor['name'].name()]))
                self.cmbPTumor.setTable('rbTumor', True, filterT, u','.join(n for n in [tableTumor['code'].name(), tableTumor['name'].name()]))
                TRecords = db.getRecordListGroupBy(tableTumor, ['DISTINCT RIGHT(rbTumor.code, LENGTH(rbTumor.code)-1) AS codeT, rbTumor.name AS nameT, rbTumor.id AS idT'], condT, 'codeT, nameT, idT', [tableTumor['code'].name(), tableTumor['name'].name()])
            # N
            NRecords = []
            if len(MKB) > 3:
                condN, filterN = getCond(MKB, tableNodus, db)
                self.cmbCNodus.setTable('rbNodus', True, filterN, u','.join(n for n in [tableNodus['code'].name(), tableNodus['name'].name()]))
                self.cmbPNodus.setTable('rbNodus', True, filterN, u','.join(n for n in [tableNodus['code'].name(), tableNodus['name'].name()]))
                NRecords = db.getRecordListGroupBy(tableNodus, ['DISTINCT RIGHT(rbNodus.code, LENGTH(rbNodus.code)-1) AS N'], condN, 'N', tableNodus['code'].name())
            if not NRecords:
                condN, filterN = getCond(self.MKB, tableNodus, db)
                self.cmbCNodus.setTable('rbNodus', True, filterN, u','.join(n for n in [tableNodus['code'].name(), tableNodus['name'].name()]))
                self.cmbPNodus.setTable('rbNodus', True, filterN, u','.join(n for n in [tableNodus['code'].name(), tableNodus['name'].name()]))
                NRecords = db.getRecordListGroupBy(tableNodus, ['DISTINCT RIGHT(rbNodus.code, LENGTH(rbNodus.code)-1) AS N'], condN, 'N', tableNodus['code'].name())
            if not NRecords and (MKB[:1] == 'C' or MKB[:2] == "D0"):
                condN, filterN = getCond('', tableNodus, db)
                self.cmbCNodus.setTable('rbNodus', True, filterN, u','.join(n for n in [tableNodus['code'].name(), tableNodus['name'].name()]))
                self.cmbPNodus.setTable('rbNodus', True, filterN, u','.join(n for n in [tableNodus['code'].name(), tableNodus['name'].name()]))
                NRecords = db.getRecordListGroupBy(tableNodus, ['DISTINCT RIGHT(rbNodus.code, LENGTH(rbNodus.code)-1) AS N'], condN, 'N', tableNodus['code'].name())
            # M
            MRecords = []
            if len(MKB) > 3:
                condM, filterM = getCond(MKB, tableMetastasis, db)
                self.cmbCMetastasis.setTable('rbMetastasis', True, filterM, u','.join(n for n in [tableMetastasis['code'].name(), tableMetastasis['name'].name()]))
                self.cmbPMetastasis.setTable('rbMetastasis', True, filterM, u','.join(n for n in [tableMetastasis['code'].name(), tableMetastasis['name'].name()]))
                MRecords = db.getRecordListGroupBy(tableMetastasis, ['DISTINCT RIGHT(rbMetastasis.code, LENGTH(rbMetastasis.code)-1) AS M'], condM, 'M', tableMetastasis['code'].name())
            if not MRecords:
                condM, filterM = getCond(self.MKB, tableMetastasis, db)
                self.cmbCMetastasis.setTable('rbMetastasis', True, filterM, u','.join(n for n in [tableMetastasis['code'].name(), tableMetastasis['name'].name()]))
                self.cmbPMetastasis.setTable('rbMetastasis', True, filterM, u','.join(n for n in [tableMetastasis['code'].name(), tableMetastasis['name'].name()]))
                MRecords = db.getRecordListGroupBy(tableMetastasis, ['DISTINCT RIGHT(rbMetastasis.code, LENGTH(rbMetastasis.code)-1) AS M'], condM, 'M', tableMetastasis['code'].name())
            if not MRecords and (MKB[:1] == 'C' or MKB[:2] == "D0"):
                condM, filterM = getCond('', tableMetastasis, db)
                self.cmbCMetastasis.setTable('rbMetastasis', True, filterM, u','.join(n for n in [tableMetastasis['code'].name(), tableMetastasis['name'].name()]))
                self.cmbPMetastasis.setTable('rbMetastasis', True, filterM, u','.join(n for n in [tableMetastasis['code'].name(), tableMetastasis['name'].name()]))
                MRecords = db.getRecordListGroupBy(tableMetastasis, ['DISTINCT RIGHT(rbMetastasis.code, LENGTH(rbMetastasis.code)-1) AS M'], condM, 'M', tableMetastasis['code'].name())
            # S
            SRecords = []
            if len(MKB) > 3:
                condS, filterS = getCond(MKB, tableTNMphase, db)
                self.cmbCStage.setTable('rbTNMphase', True, filterS, u','.join(n for n in [tableTNMphase['code'].name(), tableTNMphase['name'].name()]))
                self.cmbPStage.setTable('rbTNMphase', True, filterS, u','.join(n for n in [tableTNMphase['code'].name(), tableTNMphase['name'].name()]))
                SRecords = db.getRecordListGroupBy(tableTNMphase, ['DISTINCT rbTNMphase.code AS S'], condS, 'S', tableTNMphase['code'].name())
            if not SRecords:
                condS, filterS = getCond(self.MKB, tableTNMphase, db)
                self.cmbCStage.setTable('rbTNMphase', True, filterS, u','.join(n for n in [tableTNMphase['code'].name(), tableTNMphase['name'].name()]))
                self.cmbPStage.setTable('rbTNMphase', True, filterS, u','.join(n for n in [tableTNMphase['code'].name(), tableTNMphase['name'].name()]))
                SRecords = db.getRecordListGroupBy(tableTNMphase, ['DISTINCT rbTNMphase.code AS S'], condS, 'S', tableTNMphase['code'].name())
            if not SRecords and (MKB[:1] == 'C' or MKB[:2] == "D0"):
                condS, filterS = getCond('', tableTNMphase, db)
                self.cmbCStage.setTable('rbTNMphase', True, filterS, u','.join(n for n in [tableTNMphase['code'].name(), tableTNMphase['name'].name()]))
                self.cmbPStage.setTable('rbTNMphase', True, filterS, u','.join(n for n in [tableTNMphase['code'].name(), tableTNMphase['name'].name()]))
                SRecords = db.getRecordListGroupBy(tableTNMphase, ['DISTINCT rbTNMphase.code AS S'], condS, 'S', tableTNMphase['code'].name())
        elif self.isTest:
            self.cmbCTumor.setTable('rbTumor', True, order=u','.join(n for n in [tableTumor['code'].name(), tableTumor['name'].name()]))
            self.cmbPTumor.setTable('rbTumor', True, order=u','.join(n for n in [tableTumor['code'].name(), tableTumor['name'].name()]))
            self.cmbCNodus.setTable('rbNodus', True, order=u','.join(n for n in [tableNodus['code'].name(), tableNodus['name'].name()]))
            self.cmbPNodus.setTable('rbNodus', True, order=u','.join(n for n in [tableNodus['code'].name(), tableNodus['name'].name()]))
            self.cmbCMetastasis.setTable('rbMetastasis', True, order=u','.join(n for n in [tableMetastasis['code'].name(), tableMetastasis['name'].name()]))
            self.cmbPMetastasis.setTable('rbMetastasis', True, order=u','.join(n for n in [tableMetastasis['code'].name(), tableMetastasis['name'].name()]))
            self.cmbCStage.setTable('rbTNMphase', True, order=u','.join(n for n in [tableTNMphase['code'].name(), tableTNMphase['name'].name()]))
            self.cmbPStage.setTable('rbTNMphase', True, order=u','.join(n for n in [tableTNMphase['code'].name(), tableTNMphase['name'].name()]))
        if self.isTest:
            def findComboValue(combo, value, isStage=False):
                blocked = combo.blockSignals(True)
                try:
                    if isStage:
                        for i in xrange(combo.count()):
                            if unicode(combo.itemText(i)) == value:
                                return True
                    else:
                        for i in xrange(combo.count()):
                            if unicode(combo.itemText(i).right(combo.itemText(i).length()-1)) == value:
                                return True
                    return False
                finally:
                    combo.blockSignals(blocked)
            isValid = isValid and findComboValue(self.cmbCTumor, self.tempValue.get('cT',''))
            isValid = isValid and findComboValue(self.cmbCNodus, self.tempValue.get('cN',''))
            isValid = isValid and findComboValue(self.cmbCMetastasis, self.tempValue.get('cM',''))
            isValid = isValid and findComboValue(self.cmbCStage, self.tempValue.get('cS',''), isStage=True)

            isValid = isValid and findComboValue(self.cmbPTumor, self.tempValue.get('pT',''))
            isValid = isValid and findComboValue(self.cmbPNodus, self.tempValue.get('pN',''))
            isValid = isValid and findComboValue(self.cmbPMetastasis, self.tempValue.get('pM',''))
            isValid = isValid and findComboValue(self.cmbPStage, self.tempValue.get('pS',''), isStage=True)

            if isValid:
                self.setValue(self.tempValue)
        else:
            isValid = isValid and (self.cmbCTumor.model().searchId(self.tempValueIdDict.get('cT', None)) >= 0)
            isValid = isValid and (self.cmbCNodus.model().searchId(self.tempValueIdDict.get('cN', None)) >= 0)
            isValid = isValid and (self.cmbCMetastasis.model().searchId(self.tempValueIdDict.get('cM', None)) >= 0)
            isValid = isValid and (self.cmbCStage.model().searchId(self.tempValueIdDict.get('cS', None)) >= 0)

            isValid = isValid and (self.cmbPTumor.model().searchId(self.tempValueIdDict.get('pT', None)) >= 0)
            isValid = isValid and (self.cmbPNodus.model().searchId(self.tempValueIdDict.get('pN', None)) >= 0)
            isValid = isValid and (self.cmbPMetastasis.model().searchId(self.tempValueIdDict.get('pM', None)) >= 0)
            isValid = isValid and (self.cmbPStage.model().searchId(self.tempValueIdDict.get('pS', None)) >= 0)

            if isValid:
                self.setValue(self.tempValueIdDict)


    def setValue(self, d):
        if self.isTest:
            def setComboValue(combo, value, isStage=False):
                blocked = combo.blockSignals(True)
                try:
                    if isStage:
                        for i in xrange(combo.count()):
                            if unicode(combo.itemText(i)) == value:
                                combo.setCurrentIndex(i)
                                return
                    else:
                        for i in xrange(combo.count()):
                            if unicode(combo.itemText(i).right(combo.itemText(i).length() - 1)) == value:
                                combo.setCurrentIndex(i)
                                return
                    combo.setCurrentIndex(0)
                finally:
                    combo.blockSignals(blocked)

            setComboValue(self.cmbCTumor, d.get('cT', ''))
            setComboValue(self.cmbCNodus, d.get('cN', ''))
            setComboValue(self.cmbCMetastasis, d.get('cM', ''))
            setComboValue(self.cmbCStage, d.get('cS', ''), isStage=True)

            setComboValue(self.cmbPTumor, d.get('pT', ''))
            setComboValue(self.cmbPNodus, d.get('pN', ''))
            setComboValue(self.cmbPMetastasis, d.get('pM', ''))
            setComboValue(self.cmbPStage, d.get('pS', ''), isStage=True)
        else:
            self.cmbCTumor.setValue(d.get('cT', None))
            self.cmbCNodus.setValue(d.get('cN', None))
            self.cmbCMetastasis.setValue(d.get('cM', None))
            self.cmbCStage.setValue(d.get('cS', None))

            self.cmbPTumor.setValue(d.get('pT', None))
            self.cmbPNodus.setValue(d.get('pN', None))
            self.cmbPMetastasis.setValue(d.get('pM', None))
            self.cmbPStage.setValue(d.get('pS', None))


    def getValue(self):
        cTumorCode = self.cmbCTumor.currentText()
        cNodusCode = self.cmbCNodus.currentText()
        cMetastasisCode = self.cmbCMetastasis.currentText()
        cStageCode = self.cmbCStage.currentText()
        pTumorCode = self.cmbPTumor.currentText()
        pNodusCode = self.cmbPNodus.currentText()
        pMetastasisCode = self.cmbPMetastasis.currentText()
        pStageCode = self.cmbPStage.currentText()

        codeList = {
            'cT': unicode(cTumorCode),
            'cN': unicode(cNodusCode),
            'cM': unicode(cMetastasisCode),
            'cS': unicode(cStageCode),

            'pT': unicode(pTumorCode),
            'pN': unicode(pNodusCode),
            'pM': unicode(pMetastasisCode),
            'pS': unicode(pStageCode),
        }
        idList = {
            'cT': self.cmbCTumor.value(),
            'cN': self.cmbCNodus.value(),
            'cM': self.cmbCMetastasis.value(),
            'cS': self.cmbCStage.value(),

            'pT': self.cmbPTumor.value(),
            'pN': self.cmbPNodus.value(),
            'pM': self.cmbPMetastasis.value(),
            'pS': self.cmbPStage.value(),
        }
        return codeList, idList


    def onAnyCurrentIndexChanged(self, index):
        self.combo.updateValueFromPopup()
