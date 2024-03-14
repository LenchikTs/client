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

from PyQt4                  import QtGui
from PyQt4.QtCore           import QVariant

from library.MKBExCustomComboBoxLike import CMKBExCustomComboBoxLike
from library.MKBExSubclassPopup import CMKBExSubclassPopup
from library.InDocTable     import CInDocTableCol
from library.Utils          import forceString, forceRef, getExSubclassItemLastName, forceStringEx
#from library.adjustPopup    import adjustPopupToWidget

__all__ = ( 'CMKBExSubclassComboBox',
            'CMKBExSubclassCol',
          )


class CMKBExSubclassComboBox(CMKBExCustomComboBoxLike):
    def __init__(self, parent = None):
        CMKBExCustomComboBoxLike.__init__(self, parent)
        self.MKB = None
        self.endDate = None


    def showPopup(self):
        if self._popup is None:
            self._popup = self.createPopup()
        self._popup.installEventFilter(self)
        pos = self.rect().bottomLeft()
        pos2 = self.rect().topLeft()
        pos = self.mapToGlobal(pos)
        pos2 = self.mapToGlobal(pos2)
        size=self._popup.sizeHint()
        screen = QtGui.QApplication.desktop().availableGeometry(pos)
        size.setWidth(screen.width()/4)
        pos.setX( max(min(pos.x(), screen.right()-size.width()), screen.left()) )
        pos.setY( max(min(pos.y(), screen.bottom()-size.height()), screen.top()) )
        self._popup.move(pos)
        self._popup.resize(size)
        self._popup.setEndDate(self.endDate)
        self._popup.setTempValue(CMKBExCustomComboBoxLike.getValue(self))
        self._popup.updateItemsComboBoxes(self.MKB)
        self.updateValueFromPopup()
        #self._popup.setInitComboPopupEnabled()
        self._popup.show()
        self._popup.setFocus()


#    def showPopup(self):
#        if self._popup is None:
#            self._popup = self.createPopup()
#        self._popup.installEventFilter(self)
#        adjustPopupToWidget(self, self._popup)
#        self._popup.setEndDate(self.endDate)
#        self._popup.setTempValue(CMKBExCustomComboBoxLike.getValue(self))
#        self._popup.updateItemsComboBoxes(self.MKB)
#        self.updateValueFromPopup()
#        self._popup.show()
#        self._popup.setFocus()


    def setEndDate(self, date):
        self.endDate = date


    def setMKB(self, value):
        self.MKB = value


    def setValue(self, MKBExSubclassString):
        value = convertMKBExSubclassStringToList(unicode(forceString(MKBExSubclassString)))
        CMKBExCustomComboBoxLike.setValue(self, value)


    def valueAsString(self, value):
        return convertMKBExSubclassListToString(value)


    def getValue(self):
        valueMKBExSubclass = CMKBExCustomComboBoxLike.getValue(self)
        return convertMKBExSubclassListToString(valueMKBExSubclass)


    def createPopup(self):
        return CMKBExSubclassPopup(self)


    def setValueToPopup(self):
        valueMKBExSubclass = CMKBExCustomComboBoxLike.getValue(self)
        self._popup.setValue(valueMKBExSubclass)


    def updateValueFromPopup(self):
        CMKBExCustomComboBoxLike.setValue(self, self._popup.getValue())


def convertMKBExSubclassStringToList(s):
    d = list(s)
    step = 5 - len(d)
    if step > 0:
        for i in range(0, step):
            d.append(u'')
    if not d or len(d) > 5:
        d = [u'', u'', u'', u'', u'']
    return d


def convertMKBExSubclassListToString(d):
    return u''.join(s for s in d) if d else u''


def convertMKBExSubclassDictToId(s, mkb):
    def getMKBExSubclassId(val, mkb, position):
        if val:
            db = QtGui.qApp.db
            tableMKB = db.table('MKB_ExSubclass')
            tableMKB_ExSubclass = db.table('MKB_ExSubclass')
            tableMKBExSubclass = db.table('rbMKBExSubclass')
            tableMKBExSubclassItem = db.table('rbMKBExSubclass_Item')
            queryTable = tableMKB.innerJoin(tableMKB_ExSubclass, tableMKB_ExSubclass['master_id'].eq(tableMKB['id']))
            queryTable = queryTable.innerJoin(tableMKBExSubclass, tableMKBExSubclass['id'].eq(tableMKB_ExSubclass['exSubclass_id']))
            queryTable = queryTable.innerJoin(tableMKBExSubclassItem, tableMKBExSubclassItem['master_id'].eq(tableMKBExSubclass['id']))
            cond = [tableMKB['MKB'].like(mkb),
                    tableMKBExSubclass['position'].eq(position)]
            cond.append('''rbMKBExSubclass_Item.code LIKE '%s' '''%(val))
            record = db.getRecordEx(tableMKBExSubclass, tableMKBExSubclassItem['id'], cond, 'id')
            id = forceRef(record.value('id')) if record else None
            if not id and len(mkb) > 3:
                id = getMKBExSubclassId(val, mkb[:3], position)
            return id
        return None
    d = convertMKBExSubclassStringToList(s)
    if d and mkb:
        c6Id = getMKBExSubclassId(d[0], mkb, 6)
        c7Id = getMKBExSubclassId(d[1], mkb, 7)
        c8Id = getMKBExSubclassId(d[2], mkb, 8)
        c9Id = getMKBExSubclassId(d[3], mkb, 9)
        c10Id = getMKBExSubclassId(d[4], mkb, 10)
        return [c6Id, c7Id, c8Id, c9Id, c10Id]
    else:
        return [None]*5


class CMKBExSubclassCol(CInDocTableCol):
    def __init__(self, title, fieldName, width, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)
        self.MKB = None
        self.cache = {}


    def setMKB(self, MKB):
        self.MKB = MKB


    def toString(self, val, record):
        return QVariant(forceString(val))


    def createEditor(self, parent):
        editor = CMKBExSubclassComboBox(parent)
        editor.setMKB(self.MKB)
        return editor


    def setEditorData(self, editor, value, record):
        editor.setValue(value)


    def getEditorData(self, editor):
        return QVariant(editor.getValue())


    def toStatusTip(self, val, record):
        if self.cache.has_key(val):
            descr = self.cache[val]
        else:
            descr = getExSubclassItemLastName(forceStringEx(val), forceStringEx(record.value('MKB'))) if val else ''
            self.cache[val] = descr
        return QVariant(descr if val else '')

