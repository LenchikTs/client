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
from PyQt4.QtCore import Qt, QVariant

from library.InDocTable import CInDocTableView
from library.Utils      import forceString, forceInt, getPref, setPref, pyDate


class CAmbCardMonitoringInDocTableView(CInDocTableView):
    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self.hideRowList = []


    def headerMenu(self, pos):
        pos2 = QtGui.QCursor().pos()
        header = self.horizontalHeader()
        menu = QtGui.QMenu()
        checkedActions = []
        for i, col in enumerate(self.model().headers):
            action = QtGui.QAction(forceString(col[1]), self)
            action.setCheckable(True)
            action.setData(i)
            action.setEnabled(col[2])
            if not header.isSectionHidden(i):
                action.setChecked(True)
                checkedActions.append(action)
            menu.addAction(action)
        if len(checkedActions) == 1:
            checkedActions[0].setEnabled(False)
        selectedItem = menu.exec_(pos2)
        if selectedItem:
            section = forceInt(selectedItem.data())
            if header.isSectionHidden(section):
                header.showSection(section)
            else:
                header.hideSection(section)
            isHideRow = False
            for row, d in enumerate(self.model().dates):
                for i, col in enumerate(self.model().headers):
                    if i > 0 and col and col[0] and (pyDate(d), col[0]) in self.model().items.keys():
                        isHideRow = header.isSectionHidden(i)
                if isHideRow and row not in self.hideRowList:
                    self.hideRow(row)
                    self.hideRowList.append(row)
                elif not isHideRow and row in self.hideRowList:
                    self.showRow(row)
                    self.hideRowList.remove(row)


    def loadPreferences(self, preferences):
        model = self.model()
        charWidth = self.fontMetrics().width('A0')/2
        cols = model.headers
        i = 0
        for j, col in enumerate(cols):
            width = forceInt(getPref(preferences, unicode('width '+forceString(col[1])), self.horizontalHeader().sectionSize(j)*charWidth))
            if width:
                self.setColumnWidth(i, width)
            i += 1
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
            colsLen = len(self.model().headers)
            for i, col in enumerate(self.model().headers):
                name = forceString(col[1])
                curVIndex = header.visualIndex(i)
                if name in state:
                    vIndex = state[name][0]
                    isHidden = state[name][1]
                    if vIndex > maxVIndex:
                        maxVIndex = vIndex
                    if vIndex != curVIndex:
                        header.moveSection(curVIndex, vIndex)
                    if isHidden:
                        header.setSectionHidden(i, True)
                else:
                    header.moveSection(curVIndex, colsLen-1)


    def savePreferences(self):
        preferences = {}
        model = self.model()
        cols = model.headers
        i = 0
        for j, col in enumerate(cols):
            width = self.columnWidth(i)
            setPref(preferences, unicode('width '+forceString(col[1])), QVariant(width))
            i += 1
        header = self.horizontalHeader()
        if header.isMovable() or self.headerColsHidingAvailable():
            params = {}
            needSave = False
            for i, col in enumerate(self.model().headers):
                if i != header.visualIndex(i)  or header.isSectionHidden(i):
                    needSave = True
                    break
            if needSave:
                for i, col in enumerate(self.model().headers):
                    name = forceString(col[1])
                    params[name] = (header.visualIndex(i), header.isSectionHidden(i))
            setPref(preferences, 'headerState', QVariant(json.dumps(params)))
        return preferences

