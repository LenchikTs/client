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
import json

from PyQt4 import QtGui
from PyQt4.QtCore import QVariant

from library.InDocTable import CInDocTableView
from library.Utils      import getPref, setPref, forceString, forceInt


class CSourceItemDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)


    def createEditor(self, parent, option, index):
        editor = QtGui.QToolButton(parent)
        editor.setText(u'...')
        return editor


    def setEditorData(self, editor, index):
        pass


    def setModelData(self, editor, model, index):
        pass


class CTreatmentSchemeInDocTableView(CInDocTableView):
    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self.setItemDelegate(CSourceItemDelegate(self))


    def loadPreferences(self, preferences):
        model = self.model()
        horizontalHeader = self.horizontalHeader()
        headerCount = horizontalHeader.count()
        charWidth = self.fontMetrics().width('A0')/2
        for col in range(0, headerCount):
            actionTypeId = model.headers[col][0]
            if actionTypeId:
                title = forceString(model.headers[col][1])
            else:
                title = forceString(u'00:00 - 00:00')
            width = forceInt(getPref(preferences, unicode('width ' + title.lower()), horizontalHeader.sectionSize(col)*charWidth))
            if width:
                self.setColumnWidth(col, width)
        self.horizontalHeader().setStretchLastSection(True)
        state = getPref(preferences, 'headerState', QVariant()).toByteArray()
        if state:
            header = self.horizontalHeader()
            try:
                state = json.loads(forceString(state))
            except:
                header.restoreState(state)
                return
            maxVIndex = 0
            for col in range(0, headerCount):
                actionTypeId = model.headers[col][0]
                if actionTypeId:
                    title = forceString(model.headers[col][1])
                else:
                    title = forceString(u'00:00 - 00:00')
                name = title.lower()
                curVIndex = header.visualIndex(col)
                if name in state:
                    vIndex = state[name][0]
                    isHidden = state[name][1]
                    if vIndex > maxVIndex:
                        maxVIndex = vIndex
                    if vIndex != curVIndex:
                        header.moveSection(curVIndex, vIndex)
                    if isHidden:
                        header.setSectionHidden(col, True)
                else:
                    header.moveSection(curVIndex, headerCount-1)


    def savePreferences(self):
        preferences = {}
        model = self.model()
        horizontalHeader = self.horizontalHeader()
        headerCount = horizontalHeader.count()
        for col in range(0, headerCount):
            width = self.columnWidth(col)
            actionTypeId = model.headers[col][0]
            if actionTypeId:
                title = forceString(model.headers[col][1])
            else:
                title = forceString(u'00:00 - 00:00')
            setPref(preferences, unicode('width ' + title.lower()), QVariant(width))
        header = self.horizontalHeader()
        if header.isMovable() or self.headerColsHidingAvailable():
            params = {}
            needSave = False
            for col in range(0, headerCount):
                if col != header.visualIndex(col)  or header.isSectionHidden(col):
                    needSave = True
                    break
            if needSave:
                for col in range(0, headerCount):
                    actionTypeId = model.headers[col][0]
                    if actionTypeId:
                        title = forceString(model.headers[col][1])
                    else:
                        title = forceString(u'00:00 - 00:00')
                    name = title.lower()
                    params[name] = (header.visualIndex(col), header.isSectionHidden(col))
            setPref(preferences, 'headerState', QVariant(json.dumps(params)))
        return preferences

