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
from PyQt4.QtCore import QVariant, SIGNAL, Qt

from library.InDocTable import CInDocTableView
from library.Utils import forceRef, forceString


class CDiagnosticsInDocTableView(CInDocTableView):
    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self.addPopupDelRow()
        self.setDelRowsChecker(self._delChecker)
        self.__actCopyDiagnosisToFinal = None
        self._diagnisticsBridge = None
        self.connect(self._popupMenu, SIGNAL('aboutToShow()'), self.on_aboutToShow)

    def on_aboutToShow(self):
        if self.__actCopyDiagnosisToFinal:
            canCopyDiagnosisToFinal = bool(self._diagnisticsBridge) and self._diagnisticsBridge.canCopyDiagnosisToFinal(self.currentIndex())
            self.__actCopyDiagnosisToFinal.setEnabled(canCopyDiagnosisToFinal)


    def addCopyDiagnosisToFinal(self, editor):
        self._diagnisticsBridge = createDiagnosticBridge(editor, self.model())
        if self._diagnisticsBridge:
            if self._popupMenu is None:
                self.createPopupMenu()
            self.__actCopyDiagnosisToFinal = QtGui.QAction(u'Копировать в заключительный диагноз', self)
            self._popupMenu.addAction(self.__actCopyDiagnosisToFinal)
            self.connect(self.__actCopyDiagnosisToFinal, SIGNAL('triggered()'), self.on_copyDiagnosisToFinal)


    def _delChecker(self, rows):
        canRemove = False
        for row in rows:
            canRemove = self.model().payStatus(row) == 0
            if not canRemove:
                break
        return canRemove


    def on_deleteRows(self):
        rows = self.getSelectedRows()
        rows.sort(reverse=True)
        for row in rows:
            self.model().removeRowEx(row)

    def on_copyDiagnosisToFinal(self):
        if self._diagnisticsBridge:
            self._diagnisticsBridge.copyDiagnosisToFinal(self.currentIndex())


    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key_Return, Qt.Key_Enter):
            QtGui.QTableView.keyPressEvent(self, event)
        else:
            CInDocTableView.keyPressEvent(self, event)



def createDiagnosticBridge(eventEditor, currentModel):
    modelFinalDiagnostics = modelPreliminaryDiagnostics = None
    if hasattr(eventEditor, 'modelPreliminaryDiagnostics'):
        modelPreliminaryDiagnostics = getattr(eventEditor, 'modelPreliminaryDiagnostics')
    if hasattr(eventEditor, 'modelFinalDiagnostics'):
        modelFinalDiagnostics = getattr(eventEditor, 'modelFinalDiagnostics')

    if not (modelFinalDiagnostics and modelPreliminaryDiagnostics) or currentModel != modelPreliminaryDiagnostics:
        return

    return CDiagnosticBridge(modelPreliminaryDiagnostics, modelFinalDiagnostics, eventEditor)


class CDiagnosticBridge(object):
    mainPreliminaryDiagnosisTypeId = None
    finalDiagnosisTypeId = None
    preliminaryDeathDiagnosisTypeId = None # for F106
    finalDeathDiagnosisTypeId = None
    def __init__(self, modelPreliminaryDiagnostics, modelFinalDiagnostics, eventEditor):
        self.modelPreliminaryDiagnostics = modelPreliminaryDiagnostics
        self.modelFinalDiagnostics = modelFinalDiagnostics
        self.eventEditor = eventEditor
        self._setProperties()

    @classmethod
    def _setProperties(cls):
        if cls.mainPreliminaryDiagnosisTypeId is None:
            cls.mainPreliminaryDiagnosisTypeId = forceRef(QtGui.qApp.db.translate('rbDiagnosisType', 'code', '7', 'id'))
        if cls.finalDiagnosisTypeId is None:
            cls.finalDiagnosisTypeId = forceRef(QtGui.qApp.db.translate('rbDiagnosisType', 'code', '1', 'id'))
        if cls.preliminaryDeathDiagnosisTypeId is None:
            cls.preliminaryDeathDiagnosisTypeId = forceRef(QtGui.qApp.db.translate('rbDiagnosisType', 'code', '8', 'id'))
        if cls.finalDeathDiagnosisTypeId is None:
            cls.finalDeathDiagnosisTypeId = forceRef(QtGui.qApp.db.translate('rbDiagnosisType', 'code', '4', 'id'))

    def copyDiagnosisToFinal(self, preliminaryIndex):
        if preliminaryIndex.isValid():
            preliminaryRow = preliminaryIndex.row()
            preliminaryRecord = self.modelPreliminaryDiagnostics.items()[preliminaryRow]
            newFinalRecord = self.modelFinalDiagnostics.getEmptyRecord()

            for idx in xrange(newFinalRecord.count()):
                fieldName = forceString(newFinalRecord.fieldName(idx))
                if fieldName == 'id':
                    value = QVariant()
                elif fieldName == 'person_id':
                    value = QVariant(self.eventEditor.getExecPersonId())
                elif fieldName == 'diagnosisType_id':
                    value = QVariant(self.getFinalDiagnosisTypeId())
                else:
                    value = preliminaryRecord.value(fieldName)
                newFinalRecord.setValue(fieldName, value)
            self.modelFinalDiagnostics.addRecord(newFinalRecord)
            self.modelFinalDiagnostics.emitAllChanged()


    def canCopyDiagnosisToFinal(self, preliminaryIndex):
        if preliminaryIndex.isValid():
            preliminaryRow = preliminaryIndex.row()
            if 0 <= preliminaryRow < len(self.modelPreliminaryDiagnostics.items()):
                preliminaryRecord = self.modelPreliminaryDiagnostics.items()[preliminaryRow]
                if forceRef(preliminaryRecord.value('diagnosisType_id')) == self.getMainPreliminaryDiagnosisTypeId():
                    eixistFinalDiagnosisTypeId = False
                    finalDiagnosisTypeId = self.getFinalDiagnosisTypeId()
                    for finalRecord in self.modelFinalDiagnostics.items():
                        if forceRef(finalRecord.value('diagnosisType_id')) == finalDiagnosisTypeId:
                            eixistFinalDiagnosisTypeId = True
                            break
                    return not eixistFinalDiagnosisTypeId
        return False


    def getMainPreliminaryDiagnosisTypeId(self):
        try:
            if self.modelPreliminaryDiagnostics.deathDiagnosisTypes:
                return CDiagnosticBridge.preliminaryDeathDiagnosisTypeId
        except:
            return CDiagnosticBridge.mainPreliminaryDiagnosisTypeId


    def getFinalDiagnosisTypeId(self):
        try:
            if self.modelFinalDiagnostics.deathDiagnosisTypes:
                return CDiagnosticBridge.finalDeathDiagnosisTypeId
        except:
            return CDiagnosticBridge.finalDiagnosisTypeId
