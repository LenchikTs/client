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

from PyQt4 import QtGui, QtSql
from PyQt4.QtCore import Qt, pyqtSignature, QDate, QVariant


from DataCheck.EventsListDialog import CEventsListDialog
from Reports.Report             import normalizeMKB
from Orgs.Utils                 import getOrgStructureNetId

from library.Utils              import forceDate, forceInt, forceRef, forceString, toVariant
from library.AgeSelector        import parseAgeSelector


from DataCheck.Ui_LogicalControlDiagnosis import Ui_Dialog


class CControlDiagnosis(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.rows = 0
        self.errorStr = u''
        self.abortProcess = False
        self.checkRun = False
        self.prbControlDiagnosis.setFormat('%v')
        self.prbControlDiagnosis.setValue(0)
        self.lblCountLine.setText(u'всего строк: 0')
        self.diagnosisTypeMSIListId = self.getDiagnosisTypeMSIListId()
        self.diagnosisTypeMSIStr = u','.join(str(diagnosisTypeMSIId) for diagnosisTypeMSIId in self.diagnosisTypeMSIListId if diagnosisTypeMSIId)
        self.duration = 0
        self.recordBuffer = []
        self.recordBufferError = []
        self.recordBufferCorrect = []
        self.recordBufferClientId = []
        self.recordBufferErrorClientId = []
        self.recordBufferCorrectClientId = []
        self.bufferCorrectClientIds = []
        self.setDefaultAge()
        self.recSelectCorrect = u''
        self.recSelectClient = u''
        self.diagnosisId = None
        self.listResultControlDiagnosis.createPopupMenu()


    def getDiagnosisTypeMSIListId(self):
        db = QtGui.qApp.db
        tableDiagnosisType = db.table('rbDiagnosisType')
        return db.getDistinctIdList(tableDiagnosisType, [tableDiagnosisType['id']], where='''TRIM(rbDiagnosisType.code) IN ('51', '52', '53', '54')''')


    def getDiagnosisTypeMSICond(self, tableName):
        diagnosisTypeMSICond = u''
        if self.diagnosisTypeMSIListId:
            diagnosisTypeMSICond = u''' AND %s.diagnosisType_id NOT IN (%s) ''' % (tableName, self.diagnosisTypeMSIStr)
        return diagnosisTypeMSICond


    def setDefaultAge(self):
        db = QtGui.qApp.db

        netId = None
        currentOrgStructureId = QtGui.qApp.currentOrgStructureId()
        if currentOrgStructureId:
            netId = getOrgStructureNetId(currentOrgStructureId)
        else:
            netId = forceRef(db.translate('Organisation', 'id', QtGui.qApp.currentOrgId(), 'net_id'))

        if netId:
            ageSelector = forceString(db.translate('rbNet', 'id', netId, 'age'))
        else:
            ageSelector = ''

        (begUnit, begCount, endUnit, endCount) = parseAgeSelector(ageSelector)
        self.ageFrom = begCount if begUnit == 4 else 0
        self.ageTo   = endCount if endUnit == 4 else 150

        self.edtAgeFrom.setValue(self.ageFrom)
        self.edtAgeTo.setValue(self.ageTo)


    @pyqtSignature('')
    def on_btnEndControl_clicked(self):
        if self.checkRun:
            self.abortProcess = True
            self.listResultControlDiagnosis.reset()
            self.lblCountLine.setText(u'всего строк: %d' % self.listResultControlDiagnosis.count())
        else:
            self.close()
            QtGui.qApp.emitCurrentClientInfoChanged()


    @pyqtSignature('bool')
    def on_chkMKB_clicked(self, checked):
        self.edtMKBFrom.setEnabled(checked)
        self.edtMKBTo.setEnabled(checked)


    @pyqtSignature('')
    def on_btnStartControl_clicked(self):
        self.duration = 0
        self.recordBuffer = []
        self.recordBufferError = []
        self.recordBufferCorrect = []
        self.recordBufferClientId = []
        self.recordBufferErrorClientId = []
        self.recordBufferCorrectClientId = []
        self.bufferCorrectClientIds = []
        self.setDefaultAge()
        self.recSelectCorrect = u''
        self.recSelectClient = u''
        self.diagnosisId = None
        self.checkRun = False
        self.abortProcess = False
        self.btnCorrectControl.setText(u'исправить')
        self.dateBeginPeriod.setEnabled(False)
        self.dateEndPeriod.setEnabled(False)
        self.edtAgeFrom.setEnabled(False)
        self.edtAgeTo.setEnabled(False)
        self.chkMKB.setEnabled(False)
        self.edtMKBFrom.setEnabled(self.chkMKB.isChecked())
        self.edtMKBTo.setEnabled(self.chkMKB.isChecked())
        self.chkIgnoreCorrectionUser.setEnabled(False)
        self.chkAccountChronicDisease.setEnabled(False)
        self.chkAccountAcuteDisease.setEnabled(False)
        self.chkControlIntegrity.setEnabled(False)
        self.chkCodingMKBEx.setEnabled(False)
        self.chkCodingMKB.setEnabled(False)
        self.chkCodingTraumaType.setEnabled(False)
        self.chkDiseaseDiagnostic.setEnabled(False)
        self.chkDataDiagnosis.setEnabled(False)
        self.chkCharacterChronicFirstDisease.setEnabled(False)
        self.chkCharacterChronicKnowDisease.setEnabled(False)
        self.chkChronicAcuteDisease.setEnabled(False)
        try:
            self.loadDataDiagnosis()
        finally:
            self.dateBeginPeriod.setEnabled(True)
            self.dateEndPeriod.setEnabled(True)
            self.edtAgeFrom.setEnabled(True)
            self.edtAgeTo.setEnabled(True)
            self.chkMKB.setEnabled(True)
            self.edtMKBFrom.setEnabled(self.chkMKB.isChecked())
            self.edtMKBTo.setEnabled(self.chkMKB.isChecked())
            self.chkIgnoreCorrectionUser.setEnabled(True)
            self.chkAccountChronicDisease.setEnabled(True)
            self.chkAccountAcuteDisease.setEnabled(True)
            self.chkControlIntegrity.setEnabled(True)
            self.chkCodingMKBEx.setEnabled(True)
            self.chkCodingMKB.setEnabled(True)
            self.chkCodingTraumaType.setEnabled(True)
            self.chkDiseaseDiagnostic.setEnabled(True)
            self.chkDataDiagnosis.setEnabled(True)
            self.chkCharacterChronicFirstDisease.setEnabled(True)
            self.chkCharacterChronicKnowDisease.setEnabled(True)
            self.chkChronicAcuteDisease.setEnabled(True)


    @pyqtSignature('')
    def on_btnCorrectControl_clicked(self):
        if self.checkRun:
            self.abortProcess = True
        else:
            self.checkRun = True
            self.btnCorrectControl.setFocus(Qt.OtherFocusReason)
            self.btnCorrectControl.setText(u'прервать исправление')
            self.btnStartControl.setEnabled(False)
            QtGui.qApp.callWithWaitCursor(self, self.correctDataDiagnosis)
            self.btnCorrectControl.setText(u'исправить')
            self.checkRun = False
            self.abortProcess = False
            self.btnStartControl.setEnabled(True)
            self.prbControlDiagnosis.setText(u'готово')


    @pyqtSignature('QModelIndex')
    def on_listResultControlDiagnosis_doubleClicked(self, index):
        if self.checkRun:
            self.abortProcess = True
        else:
            self.checkRun = True
            self.btnCorrectControl.setFocus(Qt.OtherFocusReason)
            self.btnCorrectControl.setText(u'прервать исправление')
            self.btnStartControl.setEnabled(False)
            self.correctDataDiagnosisEvent()
            QtGui.qApp.callWithWaitCursor(self, self.changeDataClientsId)
            self.btnCorrectControl.setText(u'исправить')
            self.checkRun = False
            self.abortProcess = False
            self.btnStartControl.setEnabled(True)


    def recordReadChronicDisease(self, clientId, MKB, MKBEx, traumaTypeId, characterId):
        db = QtGui.qApp.db
        stmt = None
        stmtCharacterId = None
        records = []
        characterId = forceRef(characterId)
        clientId = forceRef(clientId)
        stringMKB = forceString(MKB)
        stringMKBEx = forceString(MKBEx)
        if characterId is None:
            stmtCharacterId = u'''character_id IS NULL'''
        else:
            stmtCharacterId = u'''character_id = %d''' % (characterId)
        if stmtCharacterId:
            #Min setDate
            stmt = u'''SELECT D2.setDate, D2.endDate, D2.id AS id, D2.client_id, D2.MKB, D2.character_id
                       FROM Diagnosis AS D2
                       WHERE D2.deleted = 0%s AND IF((SELECT MIN(IF (D1.setDate IS NULL, 0, D1.setDate)) AS setDate
                                 FROM Diagnosis AS D1
                                 WHERE D1.deleted = 0%s AND D1.`client_id`= %d AND D1.`MKB`= \'%s\' AND D1.`MKBEx`= \'%s\' AND D1.%s) = 0, D2.setDate IS NULL, D2.setDate = (SELECT MIN(D3.setDate)
                                               FROM Diagnosis AS D3
                                               WHERE D3.deleted = 0 AND D3.`client_id`= %d AND D3.`MKB`= \'%s\' AND D3.`MKBEx`= \'%s\' AND D3.%s)
)
                             AND (D2.`client_id`= %d AND D2.`MKB`= \'%s\' AND D2.`MKBEx`= \'%s\' AND D2.%s)
                       ORDER BY D2.id
                       LIMIT 0,1''' % (self.getDiagnosisTypeMSICond('D2'), self.getDiagnosisTypeMSICond('D1'), clientId, stringMKB, stringMKBEx, stmtCharacterId, clientId, stringMKB, stringMKBEx, stmtCharacterId, clientId, stringMKB, stringMKBEx, stmtCharacterId)
            if stmt:
                result = db.query(stmt)
                while result.next():
                    records.append(result.record())
            #MAX endDate
            stmt = u'''SELECT D2.endDate, D2.setDate, D2.id AS id, D2.client_id, D2.MKB, D2.character_id
                       FROM Diagnosis AS D2
                       WHERE D2.deleted = 0%s AND (D2.endDate = (SELECT MAX(D1.endDate) AS endDate
                                            FROM Diagnosis AS D1
                                            WHERE D1.deleted = 0%s AND (D1.`client_id`= %d AND D1.`MKB`= \'%s\' AND D1.`MKBEx`= \'%s\' AND D1.%s))
                              AND (D2.`client_id`= %d AND D2.`MKB`= \'%s\' AND D2.`MKBEx`= \'%s\' AND D2.%s))
                       ORDER BY D2.id
                       LIMIT 0,1''' % (self.getDiagnosisTypeMSICond('D2'), self.getDiagnosisTypeMSICond('D1'), clientId, stringMKB, stringMKBEx, stmtCharacterId, clientId, stringMKB, stringMKBEx, stmtCharacterId)
            if stmt:
                result = db.query(stmt)
                while result.next():
                    records.append(result.record())
        return records


    def recordReadAcuteDisease(self, clientId, MKB, MKBEx, traumaTypeId, characterId, setDateBuffer, endDateBuffer):
        db = QtGui.qApp.db
        tableDiagnosis = db.table('Diagnosis')

        cols = [tableDiagnosis['id'],
                tableDiagnosis['client_id'],
                tableDiagnosis['MKB'],
                tableDiagnosis['character_id'],
                tableDiagnosis['setDate'],
                tableDiagnosis['endDate']
                ]

        cond = [tableDiagnosis['deleted'].eq(0),
                tableDiagnosis['client_id'].eq(clientId),
                tableDiagnosis['MKB'].eq(MKB),
                tableDiagnosis['MKBEx'].eq(MKBEx)
                ]
        characterId = forceRef(characterId)
        if characterId is None:
            cond.append(u'Diagnosis.character_id IS NULL')
        else:
            cond.append(tableDiagnosis['character_id'].eq(characterId))
        durationMKB = self.setDurationMKB(MKB)
        durationDate = forceDate(endDateBuffer)
        if durationDate:
            durationEndDate = durationDate.addDays(durationMKB)
        else:
            durationEndDate = durationDate
        durationEndDateString = forceString(durationEndDate.toString('yyyy-MM-dd'))
        setDateFormat = forceDate(setDateBuffer)
        endDateFormat = forceDate(endDateBuffer)
        setDate = forceString(setDateFormat.toString('yyyy-MM-dd'))
        endDate = forceString(endDateFormat.toString('yyyy-MM-dd'))
        if self.diagnosisTypeMSIListId:
            cond.append(tableDiagnosis['diagnosisType_id'].notInlist(self.diagnosisTypeMSIListId))

        cond.append(u'''(Diagnosis.setDate IS NOT NULL AND ((Diagnosis.setDate < \'%s\' AND Diagnosis.endDate > \'%s\') OR ((Diagnosis.setDate < \'%s\' AND (Diagnosis.endDate >= \'%s\' OR (ADDDATE(Diagnosis.endDate, %d) >= \'%s\'))) OR (Diagnosis.endDate > \'%s\' AND (Diagnosis.setDate <= \'%s\' OR Diagnosis.setDate <= \'%s\')))))
        OR (Diagnosis.setDate IS NULL AND ((0 < \'%s\' AND Diagnosis.endDate > \'%s\') OR ((0 < \'%s\' AND (Diagnosis.endDate >= \'%s\' OR (ADDDATE(Diagnosis.endDate, %d) >= \'%s\'))) OR (Diagnosis.endDate > \'%s\' AND (0 <= \'%s\' OR 0 <= \'%s\')))))''' % (setDate, endDate, setDate, setDate, durationMKB, setDate, endDate, endDate, durationEndDateString, setDate, endDate, setDate, setDate, durationMKB, setDate, endDate, endDate, durationEndDateString))
        records = db.getRecordList(tableDiagnosis, cols, cond, tableDiagnosis['client_id'].name() +' ASC, ' + tableDiagnosis['MKB'].name() + ' ASC')
        return records


    def setDurationMKB(self, MKB = None):
        durationMKB = 0
        if MKB:
            durationMKB = forceInt(QtGui.qApp.db.translate('MKB', 'DiagID', MKB, 'duration'))
            if not durationMKB:
                durationMKB = self.duration
        return durationMKB


    def messageInsertDiagnosis(self, correctDiagnosId, clientId, MKB, MKBEx):
        message = self.recSelectClient + u'\n\nОбнаружен диагноз с интервалом, превышающим среднюю продолжительность заболевания, до следующего диагноза:\n' + self.recSelectCorrect + u'\n\n Создать отдельную запись в ЛУД?'
        res = QtGui.QMessageBox.warning(self,
                                        u'Внимание!',
                                        message,
                                        QtGui.QMessageBox.Ok|QtGui.QMessageBox.Ignore|QtGui.QMessageBox.Cancel|QtGui.QMessageBox.Abort,
                                        QtGui.QMessageBox.Cancel)
        if res == QtGui.QMessageBox.Ok:
            db = QtGui.qApp.db
            tableDiagnostic = db.table('Diagnostic')
            tableDiagnosis = db.table('Diagnosis')
            cols = [tableDiagnostic['deleted'],
                    tableDiagnostic['diagnosisType_id'],
                    tableDiagnostic['character_id'],
                    tableDiagnostic['dispanser_id'],
                    tableDiagnostic['traumaType_id'],
                    tableDiagnostic['setDate'],
                    tableDiagnostic['endDate'],
                    tableDiagnostic['person_id']
                    ]
            recordDiagnostic = db.getRecordList(tableDiagnostic, cols, [tableDiagnostic['deleted'].eq(0), tableDiagnostic['id'].eq(correctDiagnosId)])
            for recordIns in recordDiagnostic:
                insertRecordDiagnosis  = tableDiagnosis.newRecord()
                insertRecordDiagnosis.setValue('deleted', toVariant(forceDate(recordIns.value('deleted'))))
                insertRecordDiagnosis.setValue('client_id', toVariant(clientId))
                insertRecordDiagnosis.setValue('diagnosisType_id', toVariant(forceRef(recordIns.value('diagnosisType_id'))))
                insertRecordDiagnosis.setValue('character_id', toVariant(forceRef(recordIns.value('character_id'))))
                insertRecordDiagnosis.setValue('MKB', toVariant(MKB))
                insertRecordDiagnosis.setValue('MKBEx', toVariant(MKBEx))
                insertRecordDiagnosis.setValue('dispanser_id', toVariant(forceRef(recordIns.value('dispanser_id'))))
                insertRecordDiagnosis.setValue('traumaType_id', toVariant(forceRef(recordIns.value('traumaType_id'))))
                insertSetDate = forceDate(recordIns.value('setDate'))
                insertEndDate = forceDate(recordIns.value('endDate'))
                insertRecordDiagnosis.setValue('setDate', toVariant(forceString(insertSetDate.toString('yyyy-MM-dd'))))
                insertRecordDiagnosis.setValue('endDate', toVariant(forceString(insertEndDate.toString('yyyy-MM-dd'))))
                insertRecordDiagnosis.setValue('mod_id', toVariant(None))
                insertRecordDiagnosis.setValue('person_id', toVariant(forceRef(recordIns.value('person_id'))))
                insertId = db.insertRecord(tableDiagnosis, insertRecordDiagnosis)
                if insertId:
                    db.updateRecords(tableDiagnostic, tableDiagnostic['diagnosis_id'].eq(insertId), [tableDiagnostic['id'].eq(correctDiagnosId), tableDiagnostic['deleted'].eq(0)])
            self.listResultControlDiagnosis.reset()
            self.lblCountLine.setText(u'всего строк: %d' % self.listResultControlDiagnosis.count())
        return res


    def updateDateAcuteChronicDisease(self, recordCorrectBuffer = [], row = -1):
        if recordCorrectBuffer != []:
            correctDiagnosId = forceRef(recordCorrectBuffer.value('diagnostic_id'))
            correctDiagnosisId = forceRef(recordCorrectBuffer.value('diagnosis_id'))
            correctClientId = forceString(recordCorrectBuffer.value('client_id'))
            correctMKB = forceString(recordCorrectBuffer.value('MKB'))
            correctMKBEx = forceString(recordCorrectBuffer.value('MKBEx'))
#            correctCharacterId = forceRef(recordCorrectBuffer.value('character_id'))
            diagnosticCharacterId = forceRef(recordCorrectBuffer.value('diagnosticCharacterId'))
            correctSetDate = forceDate(recordCorrectBuffer.value('setDate'))
            correctSetDateString = forceString(correctSetDate.toString('yyyy-MM-dd'))
            correctEndDate = forceDate(recordCorrectBuffer.value('endDate'))
            correctEndDateString = forceString(correctEndDate.toString('yyyy-MM-dd'))
            if correctSetDate <= correctEndDate:
                db = QtGui.qApp.db
                tableDiagnosis = db.table('Diagnosis')
                cols = [tableDiagnosis['id'],
                        tableDiagnosis['setDate'],
                        tableDiagnosis['endDate']
                        ]
                cond = [tableDiagnosis['deleted'].eq(0), tableDiagnosis['id'].eq(correctDiagnosisId)]
                records = db.getRecordList(tableDiagnosis, cols, cond)
                for record in records:
                    diagnosisId = forceRef(record.value('id'))
                    if correctDiagnosisId == diagnosisId:
                        setDateDiagnosis = forceDate(record.value('setDate'))
                        endDateDiagnosis = forceDate(record.value('endDate'))
                        if correctSetDate < setDateDiagnosis and correctEndDate > endDateDiagnosis:
                            #в Diagnosis уменьшаем SetDate до SetDate Diagnostic
                            db.updateRecords(tableDiagnosis, tableDiagnosis['setDate'].eq(correctSetDateString), [tableDiagnosis['id'].eq(correctDiagnosisId), tableDiagnosis['deleted'].eq(0)])
                            #в Diagnosis увеличиваем EndDate до EndDate Diagnostic
                            db.updateRecords(tableDiagnosis, tableDiagnosis['endDate'].eq(correctEndDateString), [tableDiagnosis['id'].eq(correctDiagnosisId), tableDiagnosis['deleted'].eq(0)])
                        else:
                            if correctSetDate < setDateDiagnosis:
                                if diagnosticCharacterId < 2:
                                    durationMKB = self.setDurationMKB(correctMKB)
                                    if correctEndDate.addDays(durationMKB) < setDateDiagnosis:
                                        if not self.chkIgnoreCorrectionUser.isChecked():
                                            self.viewMessageInsertDiagnosisEvent(recordCorrectBuffer, row)
                                            QtGui.qApp.restoreOverrideCursor()
                                            try:
                                                messageButtonClick = self.messageInsertDiagnosis(correctDiagnosId, correctClientId, correctMKB, correctMKBEx)
                                            finally:
                                                QtGui.qApp.setWaitCursor()
                                            if messageButtonClick == QtGui.QMessageBox.Ignore:
                                                #в Diagnosis уменьшаем SetDate до SetDate Diagnostic
                                                db.updateRecords(tableDiagnosis, tableDiagnosis['setDate'].eq(correctSetDateString), [tableDiagnosis['id'].eq(correctDiagnosisId), tableDiagnosis['deleted'].eq(0)])
                                            elif messageButtonClick == QtGui.QMessageBox.Cancel:
                                                return False
                                            elif messageButtonClick == QtGui.QMessageBox.Abort:
                                                self.abortProcess = True
                                                return False
                                    else:
                                        #в Diagnosis уменьшаем SetDate до SetDate Diagnostic
                                        db.updateRecords(tableDiagnosis, tableDiagnosis['setDate'].eq(correctSetDateString), [tableDiagnosis['id'].eq(correctDiagnosisId), tableDiagnosis['deleted'].eq(0)])
                                else:
                                    #в Diagnosis уменьшаем SetDate до SetDate Diagnostic
                                    db.updateRecords(tableDiagnosis, tableDiagnosis['setDate'].eq(correctSetDateString), [tableDiagnosis['id'].eq(correctDiagnosisId), tableDiagnosis['deleted'].eq(0)])
                            else:
                                if correctEndDate > endDateDiagnosis:
                                    if diagnosticCharacterId < 2:
                                        durationMKB = self.setDurationMKB(correctMKB)
                                        if endDateDiagnosis.addDays(durationMKB) < correctSetDate:
                                            if not self.chkIgnoreCorrectionUser.isChecked():
                                                self.viewMessageInsertDiagnosisEvent(recordCorrectBuffer, row)
                                                QtGui.qApp.restoreOverrideCursor()
                                                try:
                                                    messageButtonClick = self.messageInsertDiagnosis(correctDiagnosId, correctClientId, correctMKB, correctMKBEx)
                                                finally:
                                                    QtGui.qApp.setWaitCursor()
                                                if messageButtonClick == QtGui.QMessageBox.Ignore:
                                                    #в Diagnosis увеличиваем EndDate до EndDate Diagnostic
                                                    db.updateRecords(tableDiagnosis, tableDiagnosis['endDate'].eq(correctEndDateString), [tableDiagnosis['id'].eq(correctDiagnosisId), tableDiagnosis['deleted'].eq(0)])
                                                elif messageButtonClick == QtGui.QMessageBox.Cancel:
                                                    return False
                                                elif messageButtonClick == QtGui.QMessageBox.Abort:
                                                    self.abortProcess = True
                                                    return False
                                        else:
                                            #в Diagnosis увеличиваем EndDate до EndDate Diagnostic
                                            db.updateRecords(tableDiagnosis, tableDiagnosis['endDate'].eq(correctEndDateString), [tableDiagnosis['id'].eq(correctDiagnosisId), tableDiagnosis['deleted'].eq(0)])
                                    else:
                                        #в Diagnosis увеличиваем EndDate до EndDate Diagnostic
                                        db.updateRecords(tableDiagnosis, tableDiagnosis['endDate'].eq(correctEndDateString), [tableDiagnosis['id'].eq(correctDiagnosisId), tableDiagnosis['deleted'].eq(0)])
        return True


#controlIntegrity(dateBeginPeriod, dateEndPeriod)           # 1 Нет целостности.
#controlCodingMKBEx(dateBeginPeriod, dateEndPeriod)         # 2 Различие в шифрах доп.секции.
#controlCodingMKB(dateBeginPeriod, dateEndPeriod)           # 3 Одинаковые блоки MKB.
#controlCodingTraumaType(dateBeginPeriod, dateEndPeriod)    # 4 Несоответствие типа травмы.
#controlDiseaseDiagnostic(character_id)                     # 5 Минимальная дата начала. Максимальная дата окончания.
#controlCharacterChronicFirstDisease()                      # 6 Некорректная дата начала хронического заболевания.
#loadDataDiagnosis()                                        # 7 Проблема длительности периода.
#controlCharacterChronicKnowDisease()                       # 8 Некорректный характер хронического заболевания.
#controlDiseaseDiagnostic(character_id)                     # 9 Минимальная дата окончания.
#controlChronicAcuteDisease(dateBeginPeriod, dateEndPeriod) # 10 Нарушена хронология острого и хронического заболевания.


    def correctDataDiagnosis(self):
        self.bufferCorrectClientIds = []
        booleanActionsCorrect = False
        listItemsSelectControl = self.listResultControlDiagnosis.selectedItems()
        listItemsSelectControl.sort()
        correctSelect = []
        resSelect = []
        itemsSelect = []
#        resetClientId = []
        rowList = -1
        self.prbControlDiagnosis.setFormat('%v')
        self.prbControlDiagnosis.setValue(0)
        prbControlPercent = 0
        lenStr = len(listItemsSelectControl)
        if lenStr > 1:
            self.prbControlDiagnosis.setMaximum(lenStr - 1)
        for itemsSelect in listItemsSelectControl:
            rowList = self.listResultControlDiagnosis.row(itemsSelect)
            correctSelect.append([self.recordBuffer[rowList], rowList])
        for resSelect, row in correctSelect:
            QtGui.qApp.processEvents()
            if self.abortProcess:
                self.checkRun = False
                self.prbControlDiagnosis.setValue(lenStr - 1)
                break
            self.prbControlDiagnosis.setValue(prbControlPercent)
            prbControlPercent += 1
            correctDiagnosId = forceString(resSelect.value('id'))
            correctDiagnosisId = forceRef(resSelect.value('diagnosis_id'))
            correctClientId = forceRef(resSelect.value('client_id'))
            if correctClientId not in self.bufferCorrectClientIds:
                self.bufferCorrectClientIds.append(correctClientId)
#            correctMKB = forceString(resSelect.value('MKB'))
#            correctMKBEx = forceString(resSelect.value('MKBEx'))
#            correctTraumaType_id = forceRef(resSelect.value('traumaType_id'))
            correctCharacterId = forceRef(resSelect.value('character_id'))
            correctSetDate = forceDate(resSelect.value('setDate'))
            correctEndDate = forceDate(resSelect.value('endDate'))
            db = QtGui.qApp.db
            tableDiagnosis = db.table('Diagnosis')
            tableDiagnostic = db.table('Diagnostic')
            tableTempInvalid_Period = db.table('TempInvalid_Period')
            tableTempInvalid = db.table('TempInvalid')

            if self.recordBufferCorrect[row] == 1: # 1 Нет целостности.
                #удаляем запись из {Diagnosis}
                booleanActionsCorrect = True
                deleteDiagnosId = forceString(resSelect.value('id'))
                db.deleteRecord(tableDiagnosis, tableDiagnosis['id'].eq(deleteDiagnosId))
                self.listWidgetItemEnabled(row)

            if self.recordBufferCorrect[row] == 2 or self.recordBufferCorrect[row] == 3 or self.recordBufferCorrect[row] == 9 or self.recordBufferCorrect[row] == 10:
                # 2 Различие в шифрах доп.секции. # 3 Одинаковые блоки MKB. # 9 Минимальная дата окончания. # 10 Нарушена хронология острого и хронического заболевания.
                if not self.chkIgnoreCorrectionUser.isChecked():
                    booleanActionsCorrect = True
                    QtGui.qApp.restoreOverrideCursor()
                    try:
                        self.viewDiagnosisEvent(resSelect, row, 0, True)
                    finally:
                        QtGui.qApp.setWaitCursor()

            if self.recordBufferCorrect[row] == 4: # 4 Несоответствие типа травмы.
                booleanActionsCorrect = True
                recordTraumaType = db.getIdList(tableDiagnosis, 'traumaType_id', [tableDiagnosis['deleted'].eq(0), tableDiagnosis['id'].eq(correctDiagnosisId)])
                traumaTypeId = forceRef(recordTraumaType[0]) if recordTraumaType else None
                # Заменяем traumaType_id в {Diagnostic} в соответствии с traumaType_id из {Diagnosis}
                if (traumaTypeId is not None) or (traumaTypeId > 0):
                    db.updateRecords(tableDiagnostic, tableDiagnostic['traumaType_id'].eq(traumaTypeId), [tableDiagnostic['id'].eq(correctDiagnosId), tableDiagnostic['deleted'].eq(0)])
                self.listWidgetItemEnabled(row)

            if self.recordBufferCorrect[row] == 5: # 5 Минимальная дата начала. Максимальная дата окончания.
                booleanActionsCorrect = True
                if self.updateDateAcuteChronicDisease(resSelect, row):
                    self.listWidgetItemEnabled(row)

            if self.recordBufferCorrect[row] == 6: # 6 Некорректная дата начала.
                # Заменяем setDate в {Diagnosis} в соответствии с хроническим впервые установленным setDate из {Diagnostic}
                booleanActionsCorrect = True
                setDateModif = None
                setDateModif = forceString(correctSetDate.toString('yyyy-MM-dd'))
                if setDateModif:
                    db.updateRecords(tableDiagnosis, tableDiagnosis['setDate'].eq(setDateModif), [tableDiagnosis['id'].eq(correctDiagnosisId), tableDiagnosis['deleted'].eq(0)])
                    condDateModif = [tableDiagnostic['deleted'].eq(0), tableDiagnostic['diagnosis_id'].eq(correctDiagnosisId)]
                    recordModif = db.getRecordList(tableDiagnostic, 'MIN(Diagnostic.setDate) AS setDate, Diagnostic.character_id', condDateModif)
                    recordDateModif = recordModif[0]
                    minSetDateDiagnostic = forceDate(recordDateModif.value('setDate'))
                    minCharacterId = forceInt(recordDateModif.value('character_id'))
                    if minSetDateDiagnostic and (correctSetDate > minSetDateDiagnostic and minCharacterId > 1):
                        db.updateRecords(tableDiagnostic, tableDiagnostic['character_id'].eq(3), [tableDiagnostic['id'].eq(correctDiagnosId), tableDiagnostic['deleted'].eq(0)])
                    self.listWidgetItemEnabled(row)

            if self.recordBufferCorrect[row] == 8: # 8 Некорректный характер хронического заболевания.
                # Заменяем хроническое впервые установленное на хроническое известное
                booleanActionsCorrect = True
                db.updateRecords(tableDiagnostic, tableDiagnostic['character_id'].eq(3), [tableDiagnostic['id'].eq(correctDiagnosId), tableDiagnostic['deleted'].eq(0)])
                self.listWidgetItemEnabled(row)

            if self.recordBufferCorrect[row] == 7: # 7 Проблема длительности периода.
                booleanActionsCorrect = True
                minSetDate = None
                minSetDateId = None
                maxEndDate = None
                maxEndDateId = None
                listDiagnosId = []
                if correctCharacterId == 1:
                    records = self.recordReadAcuteDisease(resSelect.value('client_id'), resSelect.value('MKB'), resSelect.value('MKBEx'), resSelect.value('traumaType_id'), resSelect.value('character_id'), resSelect.value('setDate'), resSelect.value('endDate'))
                else:
                    if correctCharacterId > 1:
                        records = self.recordReadChronicDisease(resSelect.value('client_id'), resSelect.value('MKB'), resSelect.value('MKBEx'), resSelect.value('traumaType_id'), resSelect.value('character_id'))
                for record in records:
                    diagnos_id = forceString(record.value('id'))
#                    clientId = forceString(record.value('client_id'))
#                    MKB = forceString(record.value('MKB'))
#                    characterId = forceString(record.value('character_id'))
                    setDate = forceDate(record.value('setDate'))
                    endDate = forceDate(record.value('endDate'))
                    if forceRef(record.value('id')) and forceRef(record.value('client_id')):
                        if minSetDate:
                            if minSetDate > setDate:
                                minSetDate = setDate
                                minSetDateId = diagnos_id
                        else:
                            if minSetDate is None:
                                minSetDate = setDate
                                minSetDateId = diagnos_id

                        if maxEndDate:
                            if maxEndDate < endDate:
                                maxEndDate = endDate
                                maxEndDateId = diagnos_id
                        else:
                            if maxEndDate is None:
                                maxEndDate = endDate
                                maxEndDateId = diagnos_id

                if correctDiagnosId != maxEndDateId:
                    if minSetDate > correctSetDate:
                        minSetDate = correctSetDate
                        minSetDateId = correctDiagnosId
                    else:
                        listDiagnosId.append(correctDiagnosId)

                if correctCharacterId > 1:
                    setDateModif = None
                    if minSetDate == correctSetDate and maxEndDate == correctEndDate:
                        cond = [tableDiagnostic['deleted'].eq(0),
                                tableDiagnostic['diagnosis_id'].eq(correctDiagnosId),
                                tableDiagnostic['character_id'].gt(1)
                                ]
                        minDiagnostic = db.getRecordEx(tableDiagnostic, 'MIN(setDate) AS setDate, character_id AS minCharacter_id', cond)
                        maxDiagnostic = db.getRecordEx(tableDiagnostic, 'MAX(endDate) AS endDate', cond)
                        if minDiagnostic and maxDiagnostic:
                            setDateDiagnostic = forceDate(minDiagnostic.value('setDate'))
                            characterIdMinSetDate = forceRef(minDiagnostic.value('minCharacter_id'))
                            endDateDiagnostic = forceDate(maxDiagnostic.value('endDate'))
#                            correctdiagnosIdBuffer = None
                            if characterIdMinSetDate > 2:
                                if setDateDiagnostic < correctSetDate:
                                    setDateModif = forceString(setDateDiagnostic.toString('yyyy-MM-dd'))
                                    db.updateRecords(tableDiagnosis, tableDiagnosis['setDate'].eq(setDateModif), [tableDiagnosis['id'].eq(correctDiagnosId), tableDiagnosis['deleted'].eq(0)])
                                    minSetDate = setDateDiagnostic
#                                    correctdiagnosIdBuffer = minSetDateId
                                    minSetDateId = correctDiagnosId
                            else:
                                if characterIdMinSetDate == 2:
                                    if setDateDiagnostic != correctSetDate:
                                        setDateModif = forceString(setDateDiagnostic.toString('yyyy-MM-dd'))
                                        db.updateRecords(tableDiagnosis, tableDiagnosis['setDate'].eq(setDateModif), [tableDiagnosis['id'].eq(correctDiagnosId), tableDiagnosis['deleted'].eq(0)])
                                        minSetDate = setDateDiagnostic
#                                        correctdiagnosIdBuffer = minSetDateId
                                        minSetDateId = correctDiagnosId
                            if endDateDiagnostic > correctEndDate:
                                endDateModif = forceString(endDateDiagnostic.toString('yyyy-MM-dd'))
                                db.updateRecords(tableDiagnosis, tableDiagnosis['endDate'].eq(endDateModif), [tableDiagnosis['id'].eq(correctDiagnosId), tableDiagnosis['deleted'].eq(0)])
                                maxEndDate = endDateDiagnostic
#                                correctdiagnosIdBuffer = maxEndDateId
                                maxEndDateId = correctDiagnosId
                            if maxEndDateId == correctDiagnosId and minSetDateId == correctDiagnosId:
                                listDiagnosId = []

                if minSetDateId and maxEndDateId:
                    if minSetDateId != maxEndDateId:
                        if minSetDateId != correctDiagnosId and maxEndDateId != correctDiagnosId:
                            #изменяем correctDiagnosId на maxEndDateId в {Diagnostic}, {TempInvalid_Period}, {TempInvalid}.
                            db.updateRecords(tableDiagnostic, tableDiagnostic['diagnosis_id'].eq(maxEndDateId), [tableDiagnostic['diagnosis_id'].eq(correctDiagnosId), tableDiagnostic['deleted'].eq(0)])
                            db.updateRecords(tableTempInvalid_Period, tableTempInvalid_Period['diagnosis_id'].eq(maxEndDateId), tableTempInvalid_Period['diagnosis_id'].eq(correctDiagnosId))
                            db.updateRecords(tableTempInvalid, tableTempInvalid['diagnosis_id'].eq(maxEndDateId), [tableTempInvalid['diagnosis_id'].eq(correctDiagnosId), tableTempInvalid['deleted'].eq(0)])
                            #удаляем запись из {Diagnosis}
                            db.deleteRecord(tableDiagnosis, tableDiagnosis['id'].eq(correctDiagnosId))
                        else:
                            #в maxEndDateId уменьшаем SetDate до minSetDateId
                            minSetDateString = forceString(minSetDate.toString('yyyy-MM-dd'))
                            db.updateRecords(tableDiagnosis, tableDiagnosis['setDate'].eq(minSetDateString), [tableDiagnosis['id'].eq(maxEndDateId), tableDiagnosis['deleted'].eq(0)])
                            #изменяем minSetDateId на maxEndDateId в {Diagnostic}, {TempInvalid_Period}, {TempInvalid}.
                            db.updateRecords(tableDiagnostic, tableDiagnostic['diagnosis_id'].eq(maxEndDateId), [tableDiagnostic['diagnosis_id'].eq(minSetDateId), tableDiagnostic['deleted'].eq(0)])
                            db.updateRecords(tableTempInvalid_Period, tableTempInvalid_Period['diagnosis_id'].eq(maxEndDateId), tableTempInvalid_Period['diagnosis_id'].eq(minSetDateId))
                            db.updateRecords(tableTempInvalid, tableTempInvalid['diagnosis_id'].eq(maxEndDateId), [tableTempInvalid['diagnosis_id'].eq(minSetDateId), tableTempInvalid['deleted'].eq(0)])
                            #удаляем запись из {Diagnosis}
                            db.deleteRecord(tableDiagnosis, tableDiagnosis['id'].eq(minSetDateId))
                    else:
                        if listDiagnosId != []:
                            for DiagnosId in listDiagnosId:
                                #изменяем correctDiagnosId на maxEndDateId в {Diagnostic}, {TempInvalid_Period}, {TempInvalid}.
                                db.updateRecords(tableDiagnostic, tableDiagnostic['diagnosis_id'].eq(maxEndDateId), [tableDiagnostic['diagnosis_id'].eq(DiagnosId), tableDiagnostic['deleted'].eq(0)])
                                db.updateRecords(tableTempInvalid_Period, tableTempInvalid_Period['diagnosis_id'].eq(maxEndDateId), tableTempInvalid_Period['diagnosis_id'].eq(DiagnosId))
                                db.updateRecords(tableTempInvalid, tableTempInvalid['diagnosis_id'].eq(maxEndDateId), [tableTempInvalid['diagnosis_id'].eq(DiagnosId), tableTempInvalid['deleted'].eq(0)])
                                #удаляем запись из {Diagnosis}
                                db.deleteRecord(tableDiagnosis, tableDiagnosis['id'].eq(DiagnosId))
                self.listWidgetItemEnabled(row)
            self.listResultControlDiagnosis.reset()
            self.lblCountLine.setText(u'всего строк: %d' % self.listResultControlDiagnosis.count())
        if booleanActionsCorrect:
            self.changeDataClientsId()
        else:
            self.bufferCorrectClientIds = []


    def changeDataClientsId(self):
        if self.bufferCorrectClientIds != []:
            self.dateBeginPeriod.setEnabled(False)
            self.dateEndPeriod.setEnabled(False)
            self.edtAgeFrom.setEnabled(False)
            self.edtAgeTo.setEnabled(False)
            self.chkMKB.setEnabled(False)
            self.edtMKBFrom.setEnabled(self.chkMKB.isChecked())
            self.edtMKBTo.setEnabled(self.chkMKB.isChecked())
            self.chkIgnoreCorrectionUser.setEnabled(False)
            self.chkAccountChronicDisease.setEnabled(False)
            self.chkAccountAcuteDisease.setEnabled(False)
            self.chkControlIntegrity.setEnabled(False)
            self.chkCodingMKBEx.setEnabled(False)
            self.chkCodingMKB.setEnabled(False)
            self.chkCodingTraumaType.setEnabled(False)
            self.chkDiseaseDiagnostic.setEnabled(False)
            self.chkDataDiagnosis.setEnabled(False)
            self.chkCharacterChronicFirstDisease.setEnabled(False)
            self.chkCharacterChronicKnowDisease.setEnabled(False)
            self.chkChronicAcuteDisease.setEnabled(False)
            if self.chkMKB.isChecked():
                MKBFrom = normalizeMKB(self.edtMKBFrom.text())
                MKBTo = normalizeMKB(self.edtMKBTo.text())
            else:
                MKBFrom = None
                MKBTo = None
            for clientId in self.bufferCorrectClientIds:
                self.recordBufferClientId = []
                self.recordBufferErrorClientId = []
                self.recordBufferCorrectClientId = []
                findLikeStings = []
                self.controlDiseaseLUD(clientId, MKBFrom, MKBTo)
                stringClientId = forceString(clientId)
                if stringClientId != u'':
                    findLikeStings = self.listResultControlDiagnosis.findItems(stringClientId, Qt.MatchContains)
                    for likeString in findLikeStings:
                        row = self.listResultControlDiagnosis.row(likeString)
                        if forceRef(self.recordBuffer[row].value('client_id')) == clientId:
                            if len(self.recordBuffer) > row and len(self.recordBufferCorrect) > row and len(self.recordBufferError) > row:
                                if (int(likeString.flags()) & Qt.NoItemFlags) == 0:
                                    likeString.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsEnabled)
                                self.listResultControlDiagnosis.takeItem(row)
                                self.recordBuffer.pop(row)
                                self.recordBufferCorrect.pop(row)
                                self.recordBufferError.pop(row)
                    findLikeStings = []
                    for bufferCorrectClientId, bufferClientId, bufferErrorClientId in zip(self.recordBufferCorrectClientId, self.recordBufferClientId, self.recordBufferErrorClientId):
                        resultStr = u''
                        resultStr = self.aggregateString(bufferClientId, bufferErrorClientId)
                        findLikeStings = self.listResultControlDiagnosis.findItems(bufferErrorClientId, Qt.MatchContains)
                        if findLikeStings != []:
                            rowCurrentError = -1
                            rowCurrentError = self.listResultControlDiagnosis.row(findLikeStings[0])
                            if rowCurrentError >= 0:
                                self.listResultControlDiagnosis.insertItem(rowCurrentError, resultStr)
                                self.recordBuffer.insert(rowCurrentError, bufferClientId)
                                self.recordBufferCorrect.insert(rowCurrentError, bufferCorrectClientId)
                                self.recordBufferError.insert(rowCurrentError, bufferErrorClientId)
                            else:
                                self.listResultControlDiagnosis.addItem(resultStr)
                                self.recordBuffer.append(bufferClientId)
                                self.recordBufferCorrect.append(bufferCorrectClientId)
                                self.recordBufferError.append(bufferErrorClientId)
                        else:
                            self.listResultControlDiagnosis.addItem(resultStr)
                            self.recordBuffer.append(bufferClientId)
                            self.recordBufferCorrect.append(bufferCorrectClientId)
                            self.recordBufferError.append(bufferErrorClientId)
                self.listResultControlDiagnosis.reset()
                self.rows = self.listResultControlDiagnosis.count()
                self.lblCountLine.setText(u'всего строк: %d' % self.rows)
            self.checkRun = False
            self.abortProcess = False
            self.dateBeginPeriod.setEnabled(True)
            self.dateEndPeriod.setEnabled(True)
            self.edtAgeFrom.setEnabled(True)
            self.edtAgeTo.setEnabled(True)
            self.chkMKB.setEnabled(True)
            self.edtMKBFrom.setEnabled(self.chkMKB.isChecked())
            self.edtMKBTo.setEnabled(self.chkMKB.isChecked())
            self.chkIgnoreCorrectionUser.setEnabled(True)
            self.chkAccountChronicDisease.setEnabled(True)
            self.chkAccountAcuteDisease.setEnabled(True)
            self.chkControlIntegrity.setEnabled(True)
            self.chkCodingMKBEx.setEnabled(True)
            self.chkCodingMKB.setEnabled(True)
            self.chkCodingTraumaType.setEnabled(True)
            self.chkDiseaseDiagnostic.setEnabled(True)
            self.chkDataDiagnosis.setEnabled(True)
            self.chkCharacterChronicFirstDisease.setEnabled(True)
            self.chkCharacterChronicKnowDisease.setEnabled(True)
            self.chkChronicAcuteDisease.setEnabled(True)


    def aggregateString(self, record = None, recordError = None):
        resultStr = u''
        if record and recordError:
            characterId = u''
            clientId = u''
            lastName = u''
            firstName = u''
            patrName = u''
            birthDate = u''
            MKB = u''
            MKBEx = u''
            traumaTypeId = u''
            setDate = u''
            endDate = u''
            recordBufferError = u''
            lastName = forceString(record.value('lastName'))
            firstName = forceString(record.value('firstName'))
            patrName = forceString(record.value('patrName'))
            birthDate = forceString(record.value('birthDate'))
            clientId = forceString(record.value('client_id'))
#            diagnos_id = forceString(record.value('id'))
            MKB = forceString(record.value('MKB'))
            MKBEx = forceString(record.value('MKBEx'))
            characterId = forceString(record.value('character_id'))
            traumaTypeId = forceString(record.value('name'))
            setDate = forceString(forceDate(record.value('setDate')))
            endDate = forceString(forceDate(record.value('endDate')))
            recordBufferError = recordError
            strCharacter = self.createCharacterLine(characterId)
            resultStr = u''
            resultStr = u' Клиент: ' + clientId + u'(' + lastName + ' ' + firstName + ' ' + patrName + u' ,' + birthDate + u')'
            if MKB != u'':
                resultStr += u'  MKB: ' + MKB
            if MKBEx != u'':
                resultStr += u'  MKBEx: ' + MKBEx
            if traumaTypeId != u'':
                resultStr += u'  тип травмы: ' + traumaTypeId
            if  setDate != u'':
                resultStr += u'  Начальная дата: ' + setDate
            if  endDate != u'':
                resultStr += u'  Конечная дата: ' + endDate
            resultStr += recordBufferError + ' '+strCharacter
        return resultStr


    def correctDataDiagnosisEvent(self):
        self.bufferCorrectClientIds = []
        listItemsSelectControl = self.listResultControlDiagnosis.selectedItems()
        listItemsSelectControl.sort()
        correctSelect = []
        resSelect = []
        itemsSelect = []
        rowList = -1
        for itemsSelect in listItemsSelectControl:
            rowList = self.listResultControlDiagnosis.row(itemsSelect)
            correctSelect.append([self.recordBuffer[rowList], rowList])
        for resSelect, row in correctSelect:
            QtGui.qApp.processEvents()
            if self.abortProcess:
                self.checkRun = False
                break
            if self.recordBufferCorrect[row] > 1:
                self.viewDiagnosisEvent(resSelect, row, self.recordBufferCorrect[row], False)


    def createCharacterLine(self, characterId):
        strCharacter = forceString(QtGui.qApp.db.translate('rbDiseaseCharacter', 'id', characterId, 'name'))
        return u' Характер заболевания: ' + strCharacter


    def assembleLine(self, resSelect = None, row = -1):
        self.diagnosisId = None
        self.diagnosticId = None
        self.diagnosisId = forceRef(resSelect.value('id'))
        strCharacter = self.createCharacterLine(forceString(resSelect.value('character_id')))
        self.recSelectCorrect = u''
        self.recSelectClient = u''
        self.recSelectClient = u'Клиент: ' + forceString(resSelect.value('client_id')) + u'(' + forceString(resSelect.value('lastName')) + u' ' + forceString(resSelect.value('firstName')) + u' ' + forceString(resSelect.value('patrName')) + u' ,' + forceString(resSelect.value('birthDate')) + u')'
        self.recSelectCorrect = u''
        eventMKB = forceString(resSelect.value('MKB'))
        eventMKBEx = forceString(resSelect.value('MKBEx'))
        eventTrauma = forceString(resSelect.value('name'))
        eventSetDate = forceString(forceDate(resSelect.value('setDate')))
        eventEndDate = forceString(forceDate(resSelect.value('endDate')))
        if eventMKB != u'':
            self.recSelectCorrect += u'  MKB: ' + eventMKB
        if eventMKBEx != u'':
            self.recSelectCorrect += u'  MKBEx: ' + eventMKBEx
        if eventTrauma != u'':
            self.recSelectCorrect += u'  Тип травмы: ' + eventTrauma
        if eventSetDate != u'':
            self.recSelectCorrect += u'  Начальная дата: ' + eventSetDate
        if eventEndDate != u'':
            self.recSelectCorrect += u'  Конечная дата: ' + eventEndDate
        self.recSelectCorrect += self.recordBufferError[row] + strCharacter


    def viewMessageInsertDiagnosisEvent(self, resSelect = None, row = -1):
        if resSelect and row > -1:
            self.assembleLine(resSelect, row)
            self.diagnosticId = forceRef(resSelect.value('diagnostic_id'))
            db = QtGui.qApp.db
            tableDiagnosis = db.table('Diagnosis')
            record = db.getRecordEx(tableDiagnosis, 'Diagnosis.*', [tableDiagnosis['id'].eq(forceRef(resSelect.value('diagnosis_id'))), tableDiagnosis['deleted'].eq(0)])
            if record:
                eventMKB = forceString(record.value('MKB'))
                eventMKBEx = forceString(record.value('MKBEx'))
                eventTrauma = forceString(record.value('name'))
                eventSetDate = forceString(forceDate(record.value('setDate')))
                eventEndDate = forceString(forceDate(record.value('endDate')))
                self.recSelectCorrect += u'\nСуществующая запись в ЛУДе:\n'
                if eventMKB != u'':
                    self.recSelectCorrect += u'  MKB: ' + eventMKB
                if eventMKBEx != u'':
                    self.recSelectCorrect += u'  MKBEx: ' + eventMKBEx
                if eventTrauma != u'':
                    self.recSelectCorrect += u'  Тип травмы: ' + eventTrauma
                if eventSetDate != u'':
                    self.recSelectCorrect += u'  Начальная дата: ' + eventSetDate
                if eventEndDate != u'':
                    self.recSelectCorrect += u'  Конечная дата: ' + eventEndDate
                strCharacter = self.createCharacterLine(forceString(record.value('character_id')))
                self.recSelectCorrect += strCharacter


    def viewDiagnosisEvent(self, resSelect = None, row = -1, valueBufferCorrect = 0, booleanActionsCorrect = False):
        if resSelect and row > -1:
            self.assembleLine(resSelect, row)
            db = QtGui.qApp.db
            table = db.table('Diagnostic')
            if  valueBufferCorrect == 4 or valueBufferCorrect == 6 or valueBufferCorrect == 8:
                cond = [table['id'].eq(self.diagnosisId), table['deleted'].eq(0)]
            else:
                cond = [table['diagnosis_id'].eq(self.diagnosisId), table['deleted'].eq(0)]
            eventIdList = db.getIdList(table, 'event_id', cond, 'event_id')
            if eventIdList:
                if not booleanActionsCorrect:
                    clientId = forceRef(resSelect.value('client_id'))
                    if clientId not in self.bufferCorrectClientIds:
                        self.bufferCorrectClientIds.append(clientId)
                correctListWidgetView = CEventsListDialog(self, eventIdList)
                correctListWidgetView.exec_()
                if correctListWidgetView.booleanRowEnabled:
                    self.listWidgetItemEnabled(row)
                self.abortProcess = correctListWidgetView.booleanCloseCorrect


    def listWidgetItemEnabled(self, row = -1):
        if row > -1:
            listWidgetItem = self.listResultControlDiagnosis.item(row)
            if listWidgetItem:
                listWidgetItem.setFlags(Qt.NoItemFlags)


    def controlIntegrity(self, dateBeginPeriod = None, dateEndPeriod = None, clientId = None, MKBFrom = None, MKBTo = None):
        #Проверка целостности.
        db = QtGui.qApp.db
        currentDate = QDate.currentDate()
        if clientId:
            factorClient = u'Diagnosis.client_id = %d AND ' % (clientId)
        else:
            factorClient = u''
        stmt = u'''SELECT Diagnosis.client_id, Diagnosis.MKB, Diagnosis.MKBEx, Diagnosis.id, Diagnosis.character_id, Diagnosis.traumaType_id, rbTraumaType.name, Diagnosis.setDate, Diagnosis.endDate, Client.lastName,
        Client.firstName, Client.patrName, Client.birthDate
FROM Diagnosis LEFT JOIN Client ON Diagnosis.client_id = Client.id LEFT JOIN rbTraumaType ON Diagnosis.traumaType_id = rbTraumaType.id
WHERE %s((Diagnosis.setDate IS NULL OR (Diagnosis.setDate >= \'%s\' AND Diagnosis.setDate < \'%s\' )) AND (Diagnosis.endDate <= \'%s\' AND Diagnosis.endDate > \'%s\'))
%s
AND (%s)
AND Diagnosis.deleted = 0
AND (NOT EXISTS (SELECT  DS.id FROM Diagnosis AS DS WHERE DS.mod_id = Diagnosis.id)
AND NOT EXISTS (SELECT  Diagnostic.id FROM Diagnostic WHERE Diagnostic.diagnosis_id = Diagnosis.id AND Diagnostic.deleted = 0)
AND NOT EXISTS (SELECT  TempInvalid.id FROM TempInvalid WHERE TempInvalid.diagnosis_id = Diagnosis.id AND TempInvalid.deleted = 0)
AND NOT EXISTS (SELECT  TempInvalid_Period.id FROM TempInvalid_Period WHERE TempInvalid_Period.diagnosis_id = Diagnosis.id))%s
ORDER BY Diagnosis.client_id ASC, Diagnosis.MKB ASC''' % (factorClient, dateBeginPeriod, dateEndPeriod, dateEndPeriod, dateBeginPeriod, self.getDiagnosisTypeMSICond('Diagnosis'), 'Diagnosis.MKB >= \'%s\' AND Diagnosis.MKB <= \'%s\''%(MKBFrom, MKBTo) if MKBFrom and MKBTo else 'Diagnosis.MKB >= \'A\' AND Diagnosis.MKB < \'U\'', u' AND (age(Client.birthDate, %s) >= %d AND age(Client.birthDate, %s) <= %d)'%(db.formatDate(currentDate), self.ageFrom, db.formatDate(currentDate), self.ageTo))
        query = db.query(stmt)
        if clientId:
            while query.next():
                self.recordBufferClientId.append(query.record())
                self.recordBufferErrorClientId.append(u' Нет целостности. ')
                self.recordBufferCorrectClientId.append(1)
        else:
            while query.next():
                self.recordBuffer.append(query.record())
                self.recordBufferError.append(u' Нет целостности. ')
                self.recordBufferCorrect.append(1)


    def controlCharacterChronicFirstDisease(self, dateBeginPeriod = None, dateEndPeriod = None, clientId = None, MKBFrom = None, MKBTo = None):
        #Проверка даты начала хронического заболевания.
        db = QtGui.qApp.db
        currentDate = QDate.currentDate()
        stmtCharacterChronicDisease = None
        if clientId:
            factorClient = u'A.client_id = %d AND ' % (clientId)
        else:
            factorClient = u''
        stmtCharacterChronicDisease = u'''SELECT B.setDate, B.endDate, B.diagnosis_id, B.id, B.character_id, A.client_id, A.MKB, A.MKBEx, T.name, Client.lastName,Client.firstName,Client.patrName,Client.birthDate
FROM Diagnosis AS A INNER JOIN Diagnostic AS B ON A.id = B.diagnosis_id
                    INNER JOIN Client ON A.client_id = Client.id
                    LEFT JOIN rbTraumaType AS T ON A.traumaType_id = T.id
WHERE %s((A.setDate IS NULL OR (A.setDate >= \'%s\' AND A.setDate < \'%s\' )) AND (A.endDate <= \'%s\' AND A.endDate > \'%s\'))
      AND A.deleted = 0
      AND B.deleted = 0
      %s
      %s
      AND Client.deleted = 0%s
      AND (%s)
      AND (B.character_id = 2
      AND ((A.setDate != B.setDate OR (A.setDate IS NULL AND B.setDate != 0))
      AND B.setDate <= (SELECT MIN(B2.setDate)
                        FROM Diagnostic AS B2
                        WHERE B2.deleted = 0%s AND B.deleted = 0 AND B2.diagnosis_id = B.diagnosis_id AND (B2.character_id = 3 OR B2.character_id = 4))))
ORDER BY B.diagnosis_id ASC''' % (factorClient, dateBeginPeriod, dateEndPeriod, dateEndPeriod, dateBeginPeriod, self.getDiagnosisTypeMSICond('A'),  self.getDiagnosisTypeMSICond('B'), u' AND (age(Client.birthDate, %s) >= %d AND age(Client.birthDate, %s) <= %d)'%(db.formatDate(currentDate), self.ageFrom, db.formatDate(currentDate), self.ageTo), 'A.MKB >= \'%s\' AND A.MKB <= \'%s\''%(MKBFrom, MKBTo) if MKBFrom and MKBTo else 'A.MKB >= \'A\' AND A.MKB < \'U\'',  self.getDiagnosisTypeMSICond('B2'))
        if stmtCharacterChronicDisease:
            query = db.query(stmtCharacterChronicDisease)
            if clientId:
                while query.next():
                    self.recordBufferClientId.append(query.record())
                    self.recordBufferErrorClientId.append(u' Некорректная дата начала. ')
                    self.recordBufferCorrectClientId.append(6)
            else:
                while query.next():
                    self.recordBuffer.append(query.record())
                    self.recordBufferError.append(u' Некорректная дата начала. ')
                    self.recordBufferCorrect.append(6)


    def controlCharacterChronicKnowDisease(self, dateBeginPeriod = None, dateEndPeriod = None, clientId = None, MKBFrom = None, MKBTo = None):
        #Проверка характера хронического заболевания.
        db = QtGui.qApp.db
        currentDate = QDate.currentDate()
        stmtCharacterChronicKnowDisease = None
        if clientId:
            factorClient = u'A.client_id = %d AND ' % (clientId)
        else:
            factorClient = u''
        stmtCharacterChronicKnowDisease = u'''SELECT B.setDate, B.endDate, B.diagnosis_id, B.id, B.character_id,A.client_id, A.MKB, A.MKBEx, T.name, Client.lastName,Client.firstName,Client.patrName,Client.birthDate
FROM Diagnosis AS A INNER JOIN Diagnostic AS B ON A.id = B.diagnosis_id
                    INNER JOIN Client ON A.client_id = Client.id
                    LEFT JOIN rbTraumaType AS T ON A.traumaType_id = T.id
WHERE %s((A.setDate IS NULL OR (A.setDate >= \'%s\' AND A.setDate < \'%s\' )) AND (A.endDate <= \'%s\' AND A.endDate > \'%s\'))
      AND A.deleted = 0
      AND B.deleted = 0
      %s
      %s
      AND Client.deleted = 0%s
      AND (%s)
      AND (B.character_id = 2
      AND ((A.setDate != B.setDate OR (A.setDate IS NULL AND B.setDate != 0))
      AND B.setDate > (SELECT MIN(B2.setDate)
                       FROM Diagnostic AS B2
                       WHERE B2.deleted = 0%s AND B.deleted = 0 AND B2.diagnosis_id = B.diagnosis_id AND (B2.character_id = 3 OR B2.character_id = 4))))
ORDER BY B.diagnosis_id ASC''' % (factorClient, dateBeginPeriod, dateEndPeriod, dateEndPeriod, dateBeginPeriod, self.getDiagnosisTypeMSICond('A'),  self.getDiagnosisTypeMSICond('B'), u' AND (age(Client.birthDate, %s) >= %d AND age(Client.birthDate, %s) <= %d)'%(db.formatDate(currentDate), self.ageFrom, db.formatDate(currentDate), self.ageTo), 'A.MKB >= \'%s\' AND A.MKB <= \'%s\''%(MKBFrom, MKBTo) if MKBFrom and MKBTo else 'A.MKB >= \'A\' AND A.MKB < \'U\'',  self.getDiagnosisTypeMSICond('B2'))
        if stmtCharacterChronicKnowDisease:
            query = db.query(stmtCharacterChronicKnowDisease)
            if clientId:
                while query.next():
                    self.recordBufferClientId.append(query.record())
                    self.recordBufferErrorClientId.append(u' Некорректный характер хронического заболевания. ')
                    self.recordBufferCorrectClientId.append(8)
            else:
                while query.next():
                    self.recordBuffer.append(query.record())
                    self.recordBufferError.append(u' Некорректный характер хронического заболевания. ')
                    self.recordBufferCorrect.append(8)


    def controlChronicAcuteDisease(self, dateBeginPeriod = None, dateEndPeriod = None,  clientId = None, MKBFrom = None, MKBTo = None):
        #Проверка на хронологию(острое заболевание - хроническое).
        db = QtGui.qApp.db
        currentDate = QDate.currentDate()
        stmtChronicAcuteDisease = None
        if clientId:
            factorClient = u'D1.client_id = %d AND ' % (clientId)
        else:
            factorClient = u''
        stmtChronicAcuteDisease = u'''SELECT D1.client_id, D1.MKB, D1.MKBEx, D1.id, D1.character_id, D1.setDate, T.name, D1.endDate, C.lastName, C.firstName, C.patrName, C.birthDate
FROM Diagnosis AS D1 LEFT JOIN Client AS C ON D1.client_id = C.id LEFT JOIN rbTraumaType AS T ON D1.traumaType_id = T.id, Diagnosis AS D2
WHERE %s((D1.setDate IS NULL OR D1.setDate >= \'%s\' AND D1.setDate < \'%s\') AND (D1.endDate <= \'%s\' AND D1.endDate > \'%s\'))
AND D1.deleted = 0
AND C.deleted = 0%s
AND D2.deleted = 0
AND D1.id != D2.id
AND D1.client_id = D2.client_id
AND (D1.MKB = D2.MKB
AND %s)
%s
AND (D1.character_id IS NOT NULL
AND ((D1.character_id != D2.character_id
AND((D1.character_id = 1 AND D2.setDate IS NULL AND D1.setDate IS NOT NULL)
OR ((D1.character_id = 1 AND D2.setDate IS NOT NULL AND D1.setDate IS NOT NULL)
AND (D1.endDate >= D2.setDate OR D1.setDate >= D2.setDate))
OR ((D1.character_id = 1 AND D1.setDate IS NOT NULL) AND (D1.setDate >= D2.endDate OR D1.endDate >= D2.endDate))
OR ((D1.character_id = 1 AND D1.setDate IS NULL) AND (D1.endDate >= D2.endDate OR (D2.setDate IS NOT NULL AND D1.endDate >= D2.setDate)))
))))
ORDER BY D1.client_id ASC, D1.MKB ASC'''% (factorClient, dateBeginPeriod, dateEndPeriod, dateEndPeriod, dateBeginPeriod, u' AND (age(C.birthDate, %s) >= %d AND age(C.birthDate, %s) <= %d)'%(db.formatDate(currentDate), self.ageFrom, db.formatDate(currentDate), self.ageTo), 'D1.MKB >= \'%s\' AND D1.MKB <= \'%s\''%(MKBFrom, MKBTo) if MKBFrom and MKBTo else 'D1.MKB >= \'A\' AND D1.MKB < \'U\'', self.getDiagnosisTypeMSICond('D1'))
        if stmtChronicAcuteDisease:
            query = QtGui.qApp.db.query(stmtChronicAcuteDisease)
            if clientId:
                while query.next():
                    self.recordBufferClientId.append(query.record())
                    self.recordBufferErrorClientId.append(u' Нарушена хронология острого и хронического заболевания. ')
                    self.recordBufferCorrectClientId.append(10)
            else:
                while query.next():
                    self.recordBuffer.append(query.record())
                    self.recordBufferError.append(u' Нарушена хронология острого и хронического заболевания. ')
                    self.recordBufferCorrect.append(10)


    def controlDiseaseDiagnostic(self, characterId = u'', dateBeginPeriod = None, dateEndPeriod = None, clientId = None, MKBFrom = None, MKBTo = None):
        currentDate = QDate.currentDate()
        db = QtGui.qApp.db
        stmtDiagnosticSetDate = None
        if clientId:
            factorClient = u' AND Diagnosis.client_id = %d ' % (clientId)
        else:
            factorClient = u''
        stmtDiagnosticSetDate = u'''SELECT MIN(Diagnostic.setDate) AS setDate, Diagnostic.endDate, Diagnostic.diagnosis_id, Diagnosis.id, Diagnostic.id AS diagnostic_id, Diagnosis.character_id, Diagnostic.character_id AS diagnosticCharacterId, Diagnosis.client_id, Diagnosis.MKB, Diagnosis.MKBEx, Diagnosis.traumaType_id, rbTraumaType.name, Client.lastName, Client.firstName, Client.patrName, Client.birthDate
FROM Diagnosis INNER JOIN Diagnostic ON Diagnostic.diagnosis_id = Diagnosis.id AND ((Diagnosis.setDate IS NULL OR Diagnosis.setDate >= \'%s\' AND Diagnosis.setDate < \'%s\') AND (Diagnosis.endDate <= \'%s\' AND Diagnosis.endDate > \'%s\')) AND (Diagnosis.setDate IS NOT NULL AND Diagnostic.setDate < Diagnosis.setDate) AND (%s)
AND (Diagnosis.character_id = \'%s\')
INNER JOIN Client ON Diagnosis.client_id = Client.id
LEFT JOIN rbTraumaType ON Diagnosis.traumaType_id = rbTraumaType.id
WHERE Diagnosis.deleted = 0 AND Diagnostic.deleted = 0 AND Client.deleted = 0 %s%s%s%s
GROUP BY Diagnosis.id
ORDER BY Diagnosis.client_id ASC, Diagnosis.MKB ASC''' % (dateBeginPeriod, dateEndPeriod, dateEndPeriod, dateBeginPeriod, 'Diagnosis.MKB >= \'%s\' AND Diagnosis.MKB <= \'%s\''%(MKBFrom, MKBTo) if MKBFrom and MKBTo else 'Diagnosis.MKB >= \'A\' AND Diagnosis.MKB < \'U\'', characterId, factorClient, u' AND (age(Client.birthDate, %s) >= %d AND age(Client.birthDate, %s) <= %d)'%(db.formatDate(currentDate), self.ageFrom, db.formatDate(currentDate), self.ageTo), self.getDiagnosisTypeMSICond('Diagnosis'), self.getDiagnosisTypeMSICond('Diagnostic'))
        if stmtDiagnosticSetDate:
            queryDiagnosticSetDate = db.query(stmtDiagnosticSetDate)
            if clientId:
                while queryDiagnosticSetDate.next():
                    self.recordBufferClientId.append(queryDiagnosticSetDate.record())
                    self.recordBufferErrorClientId.append(u' Минимальная дата начала. ')
                    self.recordBufferCorrectClientId.append(5)
            else:
                while queryDiagnosticSetDate.next():
                    self.recordBuffer.append(queryDiagnosticSetDate.record())
                    self.recordBufferError.append(u' Минимальная дата начала. ')
                    self.recordBufferCorrect.append(5)

        stmtDiagnosticMinEndDate = None
        stmtDiagnosticMinEndDate = u'''SELECT Diagnostic.setDate, MIN(Diagnostic.endDate) AS endDate, Diagnostic.diagnosis_id, Diagnosis.id, Diagnostic.id AS diagnostic_id, Diagnosis.character_id, Diagnosis.client_id, Diagnosis.MKB, Diagnosis.MKBEx, Diagnosis.traumaType_id, rbTraumaType.name, Client.lastName, Client.firstName, Client.patrName, Client.birthDate
FROM Diagnosis INNER JOIN Diagnostic ON Diagnostic.diagnosis_id = Diagnosis.id AND ((Diagnosis.setDate IS NULL OR Diagnosis.setDate >= \'%s\' AND Diagnosis.setDate < \'%s\') AND (Diagnosis.endDate <= \'%s\' AND Diagnosis.endDate > \'%s\')) AND (Diagnostic.endDate IS NOT NULL AND Diagnostic.endDate < Diagnosis.endDate AND Diagnostic.endDate < Diagnostic.setDate) AND (%s) AND (Diagnosis.character_id = \'%s\')
INNER JOIN Client ON Diagnosis.client_id = Client.id
LEFT JOIN rbTraumaType ON Diagnosis.traumaType_id = rbTraumaType.id
WHERE Diagnosis.deleted = 0 AND Diagnostic.deleted = 0 AND Client.deleted = 0 %s%s%s%s
GROUP BY Diagnosis.id
ORDER BY Diagnosis.client_id ASC, Diagnosis.MKB ASC''' % (dateBeginPeriod, dateEndPeriod, dateEndPeriod, dateBeginPeriod, 'Diagnosis.MKB >= \'%s\' AND Diagnosis.MKB <= \'%s\''%(MKBFrom, MKBTo) if MKBFrom and MKBTo else 'Diagnosis.MKB >= \'A\' AND Diagnosis.MKB < \'U\'', characterId, factorClient, u' AND (age(Client.birthDate, %s) >= %d AND age(Client.birthDate, %s) <= %d)'%(db.formatDate(currentDate), self.ageFrom, db.formatDate(currentDate), self.ageTo), self.getDiagnosisTypeMSICond('Diagnosis'), self.getDiagnosisTypeMSICond('Diagnostic'))
        if stmtDiagnosticMinEndDate:
            queryDiagnosticMinEndDate = db.query(stmtDiagnosticMinEndDate)
            if clientId:
                while queryDiagnosticMinEndDate.next():
                    self.recordBufferClientId.append(queryDiagnosticMinEndDate.record())
                    self.recordBufferErrorClientId.append(u' Минимальная дата окончания. ')
                    self.recordBufferCorrectClientId.append(9)
            else:
                while queryDiagnosticMinEndDate.next():
                    self.recordBuffer.append(queryDiagnosticMinEndDate.record())
                    self.recordBufferError.append(u' Минимальная дата окончания. ')
                    self.recordBufferCorrect.append(9)

        stmtDiagnosticMaxEndDate = None
        stmtDiagnosticMaxEndDate = u'''SELECT Diagnostic.setDate, MAX(Diagnostic.endDate) AS endDate, Diagnostic.diagnosis_id, Diagnosis.id, Diagnostic.id AS diagnostic_id, Diagnosis.character_id, Diagnostic.character_id AS diagnosticCharacterId, Diagnosis.client_id, Diagnosis.MKB, Diagnosis.MKBEx, Diagnosis.traumaType_id, rbTraumaType.name, Client.lastName, Client.firstName, Client.patrName, Client.birthDate
FROM Diagnosis INNER JOIN Diagnostic ON Diagnostic.diagnosis_id = Diagnosis.id AND ((Diagnosis.setDate IS NULL OR Diagnosis.setDate >= \'%s\' AND Diagnosis.setDate < \'%s\') AND (Diagnosis.endDate <= \'%s\' AND Diagnosis.endDate > \'%s\')) AND (Diagnostic.endDate IS NOT NULL AND Diagnostic.endDate > Diagnosis.endDate) AND (%s)
AND (Diagnosis.character_id = \'%s\')
INNER JOIN Client ON Diagnosis.client_id = Client.id
LEFT JOIN rbTraumaType ON Diagnosis.traumaType_id = rbTraumaType.id
WHERE Diagnosis.deleted = 0 AND Diagnostic.deleted = 0 AND Client.deleted = 0 %s%s%s%s
GROUP BY Diagnosis.id
ORDER BY Diagnosis.client_id ASC, Diagnosis.MKB ASC''' % (dateBeginPeriod, dateEndPeriod, dateEndPeriod, dateBeginPeriod, 'Diagnosis.MKB >= \'%s\' AND Diagnosis.MKB <= \'%s\''%(MKBFrom, MKBTo) if MKBFrom and MKBTo else 'Diagnosis.MKB >= \'A\' AND Diagnosis.MKB < \'U\'', characterId, factorClient, u' AND (age(Client.birthDate, %s) >= %d AND age(Client.birthDate, %s) <= %d)'%(db.formatDate(currentDate), self.ageFrom, db.formatDate(currentDate), self.ageTo), self.getDiagnosisTypeMSICond('Diagnosis'), self.getDiagnosisTypeMSICond('Diagnostic'))
        if stmtDiagnosticMaxEndDate:
            queryDiagnosticMaxEndDate = db.query(stmtDiagnosticMaxEndDate)
            if clientId:
                while queryDiagnosticMaxEndDate.next():
                    self.recordBufferClientId.append(queryDiagnosticMaxEndDate.record())
                    self.recordBufferErrorClientId.append(u' Максимальная дата окончания. ')
                    self.recordBufferCorrectClientId.append(5)
            else:
                while queryDiagnosticMaxEndDate.next():
                    self.recordBuffer.append(queryDiagnosticMaxEndDate.record())
                    self.recordBufferError.append(u' Максимальная дата окончания. ')
                    self.recordBufferCorrect.append(5)


    def controlCodingTraumaType(self, dateBeginPeriod = None, dateEndPeriod = None, clientId = None):
        #Проверка несоответствия типа травмы.
        db = QtGui.qApp.db
        currentDate = QDate.currentDate()
        stmtDiagnosticTraumaType = None
        if clientId:
            factorClient = u'Diagnosis.client_id = %d AND ' % (clientId)
        else:
            factorClient = u''
        stmtDiagnosticTraumaType = u'''SELECT Diagnosis.client_id, Diagnosis.MKB, Diagnosis.MKBEx, Diagnostic.diagnosis_id, Diagnostic.id, Diagnosis.character_id, Diagnostic.traumaType_id, rbTraumaType.name, Diagnostic.event_id, Diagnostic.setDate, Diagnostic.endDate, Client.lastName, Client.firstName, Client.patrName, Client.birthDate
FROM Diagnostic INNER JOIN Diagnosis ON Diagnostic.diagnosis_id = Diagnosis.id INNER JOIN Client ON Diagnosis.client_id = Client.id INNER JOIN Event ON Diagnostic.event_id = Event.id LEFT JOIN rbTraumaType ON Diagnostic.traumaType_id = rbTraumaType.id
WHERE %s((Diagnosis.setDate IS NULL OR (Diagnosis.setDate >= \'%s\' AND Diagnosis.setDate < \'%s\')) AND (Diagnosis.endDate <= \'%s\' AND Diagnosis.endDate > \'%s\')) AND Diagnosis.traumaType_id IS NOT NULL AND Diagnosis.traumaType_id != Diagnostic.traumaType_id AND Diagnosis.deleted = 0 AND Diagnostic.deleted = 0 AND Client.deleted = 0%s%s%s
GROUP BY Diagnostic.id
ORDER BY Diagnosis.client_id ASC, Diagnosis.MKB ASC''' % (factorClient, dateBeginPeriod, dateEndPeriod, dateEndPeriod, dateBeginPeriod, u' AND (age(Client.birthDate, %s) >= %d AND age(Client.birthDate, %s) <= %d)'%(db.formatDate(currentDate), self.ageFrom, db.formatDate(currentDate), self.ageTo), self.getDiagnosisTypeMSICond('Diagnosis'), self.getDiagnosisTypeMSICond('Diagnostic'))
        if stmtDiagnosticTraumaType:
            queryDiagnosticTraumaType = db.query(stmtDiagnosticTraumaType)
            if clientId:
               while queryDiagnosticTraumaType.next():
                    self.recordBufferClientId.append(queryDiagnosticTraumaType.record())
                    self.recordBufferErrorClientId.append(u' Несоответствие типа травмы. ')
                    self.recordBufferCorrectClientId.append(4)
            else:
                while queryDiagnosticTraumaType.next():
                    self.recordBuffer.append(queryDiagnosticTraumaType.record())
                    self.recordBufferError.append(u' Несоответствие типа травмы. ')
                    self.recordBufferCorrect.append(4)


    def controlCodingMKBEx(self, dateBeginPeriod = None, dateEndPeriod = None, clientId = None, MKBFrom = None, MKBTo = None):
        db = QtGui.qApp.db
        currentDate = QDate.currentDate()
        stmtDiagnosisMKBEx = None
        if clientId:
            factorClient = u'D1.client_id = %d AND ' % (clientId)
        else:
            factorClient = u''
        stmtDiagnosisMKBEx = u'''SELECT D1.client_id, D1.MKB, D1.MKBEx, D1.id, D1.character_id, D1.traumaType_id, T1.name, D1.setDate, D1.endDate, D2.client_id AS client_id2, D2.MKB AS MKB2, D2.MKBEx AS MKBEx2, D2.id AS id2, D2.character_id AS character_id2, D2.traumaType_id AS traumaType_id2, T2.name AS name2, D2.setDate AS setDate2, D2.endDate AS endDate2, C.lastName, C.firstName, C.patrName, C.birthDate
FROM Diagnosis AS D1 INNER JOIN Client AS C ON D1.client_id = C.id LEFT JOIN rbTraumaType AS T1 ON D1.traumaType_id = T1.id, Diagnosis AS D2 LEFT JOIN rbTraumaType AS T2 ON D2.traumaType_id = T2.id
WHERE %s((D1.setDate IS NULL OR (D1.setDate >= \'%s\' AND D1.setDate < \'%s\')) AND (D1.endDate <= \'%s\' AND D1.endDate > \'%s\'))
AND D1.deleted = 0
%s
%s
AND C.deleted = 0%s
AND D2.deleted = 0
AND D1.id > D2.id
AND D1.client_id = D2.client_id
AND (D1.MKB = D2.MKB AND (%s))
AND (D1.character_id IS NOT NULL
AND ((D1.character_id = D2.character_id AND (D1.character_id = 3 AND ((D1.endDate <= D2.endDate) OR (((D1.setDate IS NOT NULL AND D2.setDate IS NOT NULL) AND (D1.setDate >= D2.setDate)) OR (D1.setDate IS NULL AND D2.setDate IS NULL) OR (D1.setDate IS NOT NULL AND D2.setDate IS NULL AND D1.setDate != 0))
)))
OR (D1.character_id = D2.character_id
AND (
    D1.character_id = 1 AND
    (
    (D1.endDate <= D2.endDate AND (((D1.setDate IS NOT NULL AND D2.setDate IS NOT NULL) AND (D1.setDate >= D2.setDate)) OR (D1.setDate IS NULL AND D2.setDate IS NULL) OR (D1.setDate IS NOT NULL AND D2.setDate IS NULL AND D1.setDate != 0)))
    OR ((D1.endDate <= D2.endDate AND ((D2.setDate IS NOT NULL AND D1.endDate >= D2.setDate) OR (D2.setDate IS NULL AND D1.endDate >= 0))) AND
    (
    (D1.setDate IS NOT NULL AND D2.setDate IS NOT NULL AND D1.setDate <= D2.setDate)
    OR (D1.setDate IS NULL AND D2.setDate IS NULL)
    OR (D1.setDate IS NULL AND D2.setDate IS NOT NULL AND D2.setDate != 0)
    )
    )
    OR (D1.endDate >= D2.endDate AND (((D1.setDate IS NOT NULL AND D2.setDate IS NOT NULL AND (D1.setDate >= D2.setDate)) OR (D1.setDate IS NULL AND D2.setDate IS NULL) OR (D1.setDate IS NOT NULL AND D2.setDate IS NULL AND D1.setDate != 0)) AND (
    (D1.setDate IS NOT NULL AND D1.setDate <= D2.endDate) OR D1.setDate IS NULL
    )))
    )
    OR((D2.setDate IS NOT NULL AND ((D2.endDate > (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d)))
AND (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d))) > D2.setDate)
OR (D1.endDate < D2.endDate AND D2.endDate < (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d)))
AND (D2.endDate - D1.endDate) < (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
(SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB), %d))))

OR (D2.setDate IS NULL AND ((D2.endDate > (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d)))
AND (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0, ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)),
ADDDATE(D1.endDate, %d))) > 0)
OR (D1.endDate < D2.endDate AND D2.endDate < (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d)))
AND (D2.endDate - D1.endDate) < (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
(SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB), %d))))))
    )
    ) OR (D1.character_id != D2.character_id AND
         (

         ((D1.character_id = 1 AND D2.setDate IS NOT NULL) AND (D1.endDate >= D2.setDate OR D1.setDate >= D2.setDate))
         OR ((D1.character_id = 1 AND D1.setDate IS NOT NULL) AND (D1.setDate >= D2.endDate OR D1.endDate >= D2.endDate))
         )
         )
    ) AND (D1.MKBEx != D2.MKBEx)
    ))
ORDER BY D1.client_id ASC, D1.MKB ASC''' % (factorClient, dateBeginPeriod, dateEndPeriod, dateEndPeriod, dateBeginPeriod, self.getDiagnosisTypeMSICond('D1'), self.getDiagnosisTypeMSICond('D2'), u' AND (age(C.birthDate, %s) >= %d AND age(C.birthDate, %s) <= %d)'%(db.formatDate(currentDate), self.ageFrom, db.formatDate(currentDate), self.ageTo), 'D1.MKB >= \'%s\' AND D1.MKB <= \'%s\''%(MKBFrom, MKBTo) if MKBFrom and MKBTo else 'D1.MKB >= \'A\' AND D1.MKB < \'U\'', self.duration, self.duration, self.duration, self.duration, self.duration, self.duration, self.duration, self.duration)

        if stmtDiagnosisMKBEx:
            queryDiagnosisMKBEx = db.query(stmtDiagnosisMKBEx)
            if clientId:
                while queryDiagnosisMKBEx.next():
                    valRecord = QtSql.QSqlRecord()
                    valRecord2 = QtSql.QSqlRecord()
#                    valRecord.clear()
#                    valRecord2.clear()
                    bufvalRecord =[]
                    bufvalRecord.append(queryDiagnosisMKBEx.record())
                    self.recordBufferClientId.append(self.createBufferField(valRecord,  bufvalRecord, 1))
                    self.recordBufferErrorClientId.append(u' Различие в шифрах доп.секции. ')
                    self.recordBufferCorrectClientId.append(2)

                    self.recordBufferClientId.append(self.createBufferField(valRecord2,  bufvalRecord, 2))
                    self.recordBufferErrorClientId.append(u' Различие в шифрах доп.секции. ')
                    self.recordBufferCorrectClientId.append(2)
            else:
                while queryDiagnosisMKBEx.next():
                    valRecord = QtSql.QSqlRecord()
                    valRecord2 = QtSql.QSqlRecord()
#                    valRecord.clear()
#                    valRecord2.clear()
                    bufvalRecord =[]
                    bufvalRecord.append(queryDiagnosisMKBEx.record())
                    self.recordBuffer.append(self.createBufferField(valRecord,  bufvalRecord, 1))
                    self.recordBufferError.append(u' Различие в шифрах доп.секции. ')
                    self.recordBufferCorrect.append(2)

                    self.recordBuffer.append(self.createBufferField(valRecord2,  bufvalRecord, 2))
                    self.recordBufferError.append(u' Различие в шифрах доп.секции. ')
                    self.recordBufferCorrect.append(2)


    def controlCodingMKB(self, dateBeginPeriod = None, dateEndPeriod = None, clientId = None, MKBFrom = None, MKBTo = None):
        db = QtGui.qApp.db
        currentDate = QDate.currentDate()
        stmtDiagnosisMKB = None
        if clientId:
            factorClient = u'D1.client_id = %d AND ' % (clientId)
        else:
            factorClient = u''
        stmtDiagnosisMKB = u'''SELECT D1.client_id, D1.MKB, D1.MKBEx, D1.id, D1.character_id, D1.traumaType_id, T1.name, D1.setDate, D1.endDate, D2.client_id AS client_id2, D2.MKB AS MKB2, D2.MKBEx AS MKBEx2, D2.id AS id2, D2.character_id AS character_id2, D2.traumaType_id AS traumaType_id2, T2.name AS name2, D2.setDate AS setDate2, D2.endDate AS endDate2, C.lastName, C.firstName, C.patrName, C.birthDate
FROM Diagnosis AS D1 INNER JOIN Client AS C ON D1.client_id = C.id LEFT JOIN rbTraumaType AS T1 ON D1.traumaType_id = T1.id, Diagnosis AS D2 LEFT JOIN rbTraumaType AS T2 ON D2.traumaType_id = T2.id
WHERE %s((D1.setDate IS NULL OR (D1.setDate >= \'%s\' AND D1.setDate < \'%s\')) AND (D1.endDate <= \'%s\' AND D1.endDate > \'%s\'))
AND D1.deleted = 0
%s
%s
AND C.deleted = 0%s
AND D2.deleted = 0
AND D1.id < D2.id
AND D1.client_id = D2.client_id
AND ((LEFT( D1.MKB, 3 ) = LEFT( D2.MKB, 3 )) AND (%s))
AND (D1.character_id IS NOT NULL
AND ((D1.character_id = D2.character_id AND (D1.character_id = 3 AND ((D1.endDate <= D2.endDate) OR (((D1.setDate IS NOT NULL AND D2.setDate IS NOT NULL AND (D1.setDate >= D2.setDate)) OR (D1.setDate IS NULL AND D2.setDate IS NULL) OR (D1.setDate IS NOT NULL AND D2.setDate IS NULL AND D1.setDate != 0))))))
OR (D1.character_id = D2.character_id
AND (
    D1.character_id = 1 AND
    (
    (D1.endDate <= D2.endDate AND ((D1.setDate IS NOT NULL AND D2.setDate IS NOT NULL AND (D1.setDate >= D2.setDate)) OR (D1.setDate IS NULL AND D2.setDate IS NULL) OR (D1.setDate IS NOT NULL AND D2.setDate IS NULL AND D1.setDate != 0)))
    OR ((D1.endDate <= D2.endDate AND ((D2.setDate IS NOT NULL AND D1.endDate >= D2.setDate) OR (D2.setDate IS NULL AND D1.endDate >= 0))) AND ((D1.setDate IS NOT NULL AND D2.setDate IS NOT NULL AND D1.setDate <= D2.setDate) OR (D1.setDate IS NULL AND D2.setDate IS NULL) OR (D1.setDate IS NULL AND D2.setDate IS NOT NULL AND D2.setDate != 0)))
    OR (D1.endDate >= D2.endDate AND (((D1.setDate IS NOT NULL AND D2.setDate IS NOT NULL AND (D1.setDate >= D2.setDate)) OR (D1.setDate IS NULL AND D2.setDate IS NULL) OR (D1.setDate IS NOT NULL AND D2.setDate IS NULL AND D1.setDate != 0)) AND ((D1.setDate IS NOT NULL AND D1.setDate <= D2.endDate) OR D1.setDate IS NULL)))
    )
    OR((D2.setDate IS NOT NULL AND ((D2.endDate > (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d)))
AND (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d))) > D2.setDate)
OR (D1.endDate < D2.endDate AND D2.endDate < (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d)))
AND (D2.endDate - D1.endDate) < (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
(SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB), %d))))

OR (D2.setDate IS NULL AND ((D2.endDate > (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d)))
AND (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0, ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)),
ADDDATE(D1.endDate, %d))) > 0)
OR (D1.endDate < D2.endDate AND D2.endDate < (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d)))
AND (D2.endDate - D1.endDate) < (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
(SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB), %d))))))
    )
    ) OR (D1.character_id != D2.character_id AND
         (

         ((D1.character_id = 1 AND D2.setDate IS NOT NULL) AND (((D2.setDate IS NOT NULL AND D1.endDate >= D2.setDate) OR (D2.setDate IS NULL AND D1.endDate >= 0)) OR D1.setDate >= D2.setDate))
         OR ((D1.character_id = 1 AND D1.setDate IS NOT NULL) AND (D1.setDate >= D2.endDate OR D1.endDate >= D2.endDate))
         )
         )
    )
    ))
ORDER BY D1.client_id ASC, D1.MKB ASC''' % (factorClient, dateBeginPeriod, dateEndPeriod, dateEndPeriod, dateBeginPeriod, self.getDiagnosisTypeMSICond('D1'), self.getDiagnosisTypeMSICond('D2'), u' AND (age(C.birthDate, %s) >= %d AND age(C.birthDate, %s) <= %d)'%(db.formatDate(currentDate), self.ageFrom, db.formatDate(currentDate), self.ageTo), 'D1.MKB >= \'%s\' AND D1.MKB <= \'%s\''%(MKBFrom, MKBTo) if MKBFrom and MKBTo else 'D1.MKB >= \'A\' AND D1.MKB < \'U\'', self.duration, self.duration, self.duration, self.duration, self.duration, self.duration, self.duration, self.duration)

        if stmtDiagnosisMKB:
            queryDiagnosisMKB = db.query(stmtDiagnosisMKB)
            if clientId:
                while queryDiagnosisMKB.next():
                    valRecord = QtSql.QSqlRecord()
                    valRecord2 = QtSql.QSqlRecord()
#                    valRecord.clear()
#                    valRecord2.clear()
                    bufvalRecord =[]
                    bufvalRecord.append(queryDiagnosisMKB.record())
                    self.recordBufferClientId.append(self.createBufferField(valRecord,  bufvalRecord, 1))
                    self.recordBufferErrorClientId.append(u' Одинаковые блоки MKB. ')
                    self.recordBufferCorrectClientId.append(3)

                    self.recordBufferClientId.append(self.createBufferField(valRecord2,  bufvalRecord, 2))
                    self.recordBufferErrorClientId.append(u' Одинаковые блоки MKB. ')
                    self.recordBufferCorrectClientId.append(3)
            else:
                while queryDiagnosisMKB.next():
                    valRecord = QtSql.QSqlRecord()
                    valRecord2 = QtSql.QSqlRecord()
#                    valRecord.clear()
#                    valRecord2.clear()
                    bufvalRecord =[]
                    bufvalRecord.append(queryDiagnosisMKB.record())
                    self.recordBuffer.append(self.createBufferField(valRecord,  bufvalRecord, 1))
                    self.recordBufferError.append(u' Одинаковые блоки MKB. ')
                    self.recordBufferCorrect.append(3)

                    self.recordBuffer.append(self.createBufferField(valRecord2,  bufvalRecord, 2))
                    self.recordBufferError.append(u' Одинаковые блоки MKB. ')
                    self.recordBufferCorrect.append(3)


    def createBufferField(self, valRecord = None,  bufvalRecord = None, indexVariant = 1):
        if bufvalRecord and valRecord is not None:
            for bufRecord in bufvalRecord:
                if indexVariant == 1:
                    valRecord.append(QtSql.QSqlField('client_id',     QVariant.Int))
                    valRecord.setValue('client_id', toVariant(bufRecord.value('client_id')))
                    valRecord.append(QtSql.QSqlField('MKB',           QVariant.String))
                    valRecord.setValue('MKB', toVariant(bufRecord.value('MKB')))
                    valRecord.append(QtSql.QSqlField('MKBEx',         QVariant.String))
                    valRecord.setValue('MKBEx', toVariant(bufRecord.value('MKBEx')))
                    valRecord.append(QtSql.QSqlField('id',            QVariant.Int))
                    valRecord.setValue('id', toVariant(bufRecord.value('id')))
                    valRecord.append(QtSql.QSqlField('character_id',  QVariant.Int))
                    valRecord.setValue('character_id', toVariant(bufRecord.value('character_id')))
                    valRecord.append(QtSql.QSqlField('traumaType_id',  QVariant.Int))
                    valRecord.setValue('traumaType_id', toVariant(bufRecord.value('traumaType_id')))
                    valRecord.append(QtSql.QSqlField('name',          QVariant.String))
                    valRecord.setValue('name', toVariant(bufRecord.value('name')))
                    valRecord.append(QtSql.QSqlField('setDate',       QVariant.DateTime))
                    valRecord.setValue('setDate', toVariant(bufRecord.value('setDate')))
                    valRecord.append(QtSql.QSqlField('endDate',       QVariant.DateTime))
                    valRecord.setValue('endDate', toVariant(bufRecord.value('endDate')))
                    valRecord.append(QtSql.QSqlField('lastName',      QVariant.String))
                    valRecord.setValue('lastName', toVariant(bufRecord.value('lastName')))
                    valRecord.append(QtSql.QSqlField('firstName',     QVariant.String))
                    valRecord.setValue('firstName', toVariant(bufRecord.value('firstName')))
                    valRecord.append(QtSql.QSqlField('patrName',      QVariant.String))
                    valRecord.setValue('patrName', toVariant(bufRecord.value('patrName')))
                    valRecord.append(QtSql.QSqlField('birthDate',     QVariant.DateTime))
                    valRecord.setValue('birthDate', toVariant(bufRecord.value('birthDate')))
                    return valRecord
                else:
                  if indexVariant == 2:
                        valRecord.append(QtSql.QSqlField('client_id',     QVariant.Int))
                        valRecord.setValue('client_id', toVariant(bufRecord.value('client_id2')))
                        valRecord.append(QtSql.QSqlField('MKB',           QVariant.String))
                        valRecord.setValue('MKB', toVariant(bufRecord.value('MKB2')))
                        valRecord.append(QtSql.QSqlField('MKBEx',         QVariant.String))
                        valRecord.setValue('MKBEx', toVariant(bufRecord.value('MKBEx2')))
                        valRecord.append(QtSql.QSqlField('id',            QVariant.Int))
                        valRecord.setValue('id', toVariant(bufRecord.value('id2')))
                        valRecord.append(QtSql.QSqlField('character_id',  QVariant.Int))
                        valRecord.setValue('character_id', toVariant(bufRecord.value('character_id2')))
                        valRecord.append(QtSql.QSqlField('traumaType_id',  QVariant.Int))
                        valRecord.setValue('traumaType_id', toVariant(bufRecord.value('traumaType_id2')))
                        valRecord.append(QtSql.QSqlField('name',          QVariant.String))
                        valRecord.setValue('name', toVariant(bufRecord.value('name2')))
                        valRecord.append(QtSql.QSqlField('setDate',       QVariant.DateTime))
                        valRecord.setValue('setDate', toVariant(bufRecord.value('setDate2')))
                        valRecord.append(QtSql.QSqlField('endDate',       QVariant.DateTime))
                        valRecord.setValue('endDate', toVariant(bufRecord.value('endDate2')))
                        valRecord.append(QtSql.QSqlField('lastName',      QVariant.String))
                        valRecord.setValue('lastName', toVariant(bufRecord.value('lastName')))
                        valRecord.append(QtSql.QSqlField('firstName',     QVariant.String))
                        valRecord.setValue('firstName', toVariant(bufRecord.value('firstName')))
                        valRecord.append(QtSql.QSqlField('patrName',      QVariant.String))
                        valRecord.setValue('patrName', toVariant(bufRecord.value('patrName')))
                        valRecord.append(QtSql.QSqlField('birthDate',     QVariant.DateTime))
                        valRecord.setValue('birthDate', toVariant(bufRecord.value('birthDate')))
                        return valRecord
        else:
            return None


#controlIntegrity(dateBeginPeriod, dateEndPeriod)           # 1 Нет целостности.
#controlCodingMKBEx(dateBeginPeriod, dateEndPeriod)         # 2 Различие в шифрах доп.секции.
#controlCodingMKB(dateBeginPeriod, dateEndPeriod)           # 3 Одинаковые блоки MKB.
#controlCodingTraumaType(dateBeginPeriod, dateEndPeriod)    # 4 Несоответствие типа травмы.
#controlDiseaseDiagnostic(character_id)                     # 5 Минимальная дата начала. Максимальная дата окончания.
#controlCharacterChronicFirstDisease()                      # 6 Некорректная дата начала хронического заболевания.
#loadDataDiagnosis()                                        # 7 Проблема длительности периода.
#controlCharacterChronicKnowDisease()                       # 8 Некорректный характер хронического заболевания.
#controlDiseaseDiagnostic(character_id)                     # 9 Минимальная дата окончания.
#controlChronicAcuteDisease(dateBeginPeriod, dateEndPeriod) # 10 Нарушена хронология острого и хронического заболевания.


    def controlDiseaseLUD(self, clientId = None, MKBFrom = None, MKBTo = None):
        dateBeginPeriod = forceString(self.dateBeginPeriod.date().toString('yyyy-MM-dd'))
        dateEndPeriod = forceString(self.dateEndPeriod.date().toString('yyyy-MM-dd'))
        self.ageFrom = self.edtAgeFrom.value()
        self.ageTo = self.edtAgeTo.value()
        if self.duration == 0:
            self.duration = QtGui.qApp.averageDuration()
        if self.chkControlIntegrity.isChecked():
            self.checkRun = True
            self.controlIntegrity(dateBeginPeriod, dateEndPeriod, clientId, MKBFrom, MKBTo) # 1
        if self.chkAccountChronicDisease.isChecked() or self.chkAccountAcuteDisease.isChecked():
            self.checkRun = True
            db = QtGui.qApp.db
            currentDate = QDate.currentDate()
            if self.chkCodingMKBEx.isChecked():
                self.controlCodingMKBEx(dateBeginPeriod, dateEndPeriod, clientId, MKBFrom, MKBTo)       # 2
            if self.chkCodingMKB.isChecked():
                self.controlCodingMKB(dateBeginPeriod, dateEndPeriod, clientId, MKBFrom, MKBTo)         # 3
            if self.chkCodingTraumaType.isChecked():
                self.controlCodingTraumaType(dateBeginPeriod, dateEndPeriod, clientId)  # 4
            if clientId:
                factorClient = u'D1.client_id = %d AND ' % (clientId)
            else:
                factorClient = u''
            stmt = u'''SELECT D1.client_id, D1.MKB, D1.MKBEx, D1.id, D1.character_id, D1.setDate, D1.traumaType_id, T.name, D1.endDate, C.lastName, C.firstName, C.patrName, C.birthDate
                        FROM Diagnosis AS D1 LEFT JOIN Client AS C ON D1.client_id = C.id LEFT JOIN rbTraumaType AS T ON D1.traumaType_id = T.id, Diagnosis AS D2
                        WHERE %s((D1.setDate IS NULL OR (D1.setDate >= \'%s\' AND D1.setDate < \'%s\')) AND (D1.endDate <= \'%s\' AND D1.endDate > \'%s\')) AND
                        D1.deleted = 0
                        %s
                        AND C.deleted = 0%s AND
                        C.deleted = 0%s AND
                        D2.deleted = 0 AND
                        D1.id != D2.id AND
                        D1.client_id = D2.client_id AND
                        (D1.MKB = D2.MKB AND
                        %s) AND

                        (D1.character_id IS NOT NULL AND

                        ('''% (factorClient, dateBeginPeriod, dateEndPeriod, dateEndPeriod, dateBeginPeriod, self.getDiagnosisTypeMSICond('D1'), u' AND (age(C.birthDate, %s) >= %d AND age(C.birthDate, %s) <= %d)'%(db.formatDate(currentDate), self.ageFrom, db.formatDate(currentDate), self.ageTo), 'D1.MKB >= \'%s\' AND D1.MKB <= \'%s\''%(MKBFrom, MKBTo) if MKBFrom and MKBTo else 'D1.MKB >= \'A\' AND D1.MKB < \'U\'') #D1.MKB >= 'A' AND D1.MKB < 'U'
            if self.chkAccountChronicDisease.isChecked():
                #хронические заболевания
                if self.chkCharacterChronicFirstDisease.isChecked():
                    self.controlCharacterChronicFirstDisease(dateBeginPeriod, dateEndPeriod, clientId, MKBFrom, MKBTo) # 6
                if self.chkCharacterChronicKnowDisease.isChecked():
                    self.controlCharacterChronicKnowDisease(dateBeginPeriod, dateEndPeriod, clientId, MKBFrom, MKBTo)  # 8
                if self.chkChronicAcuteDisease.isChecked():
                    self.controlChronicAcuteDisease(dateBeginPeriod, dateEndPeriod, clientId, MKBFrom, MKBTo)          # 10
                if self.chkDiseaseDiagnostic.isChecked():
                    self.controlDiseaseDiagnostic(u'2', dateBeginPeriod, dateEndPeriod, clientId, MKBFrom, MKBTo)      # 5, 9
                stmt += u'''(D1.character_id = D2.character_id AND (D1.character_id = 3 AND ((D1.endDate <= D2.endDate) OR ((D1.setDate IS NOT NULL AND D2.setDate IS NOT NULL AND (D1.setDate >= D2.setDate)) OR (D1.setDate IS NULL AND D2.setDate IS NULL) OR (D1.setDate IS NOT NULL AND D2.setDate IS NULL AND D1.setDate != 0)))))'''

            else:
                if self.chkAccountAcuteDisease.isChecked():
                    #острые заболевания
                    if self.chkDiseaseDiagnostic.isChecked():
                        self.controlDiseaseDiagnostic(u'1', dateBeginPeriod, dateEndPeriod, clientId, MKBFrom, MKBTo) # 5, 9
                    stmt += u'''(D1.character_id = D2.character_id AND
                    (
                    D1.character_id = 1 AND
                    (
                    (D1.endDate <= D2.endDate AND ((D1.setDate IS NOT NULL AND D2.setDate IS NOT NULL AND (D1.setDate >= D2.setDate)) OR (D1.setDate IS NULL AND D2.setDate IS NULL) OR (D1.setDate IS NOT NULL AND D2.setDate IS NULL AND D1.setDate != 0)))
                    OR ((D1.endDate <= D2.endDate AND ((D2.setDate IS NOT NULL AND D1.endDate >= D2.setDate) OR (D2.setDate IS NULL AND D1.endDate >= 0))) AND ((D1.setDate IS NOT NULL AND D2.setDate IS NOT NULL AND D1.setDate <= D2.setDate) OR (D1.setDate IS NULL AND D2.setDate IS NULL) OR (D1.setDate IS NULL AND D2.setDate IS NOT NULL AND D2.setDate != 0)))
                    OR (D1.endDate >= D2.endDate AND (((D1.setDate IS NOT NULL AND D2.setDate IS NOT NULL AND (D1.setDate >= D2.setDate)) OR (D1.setDate IS NULL AND D2.setDate IS NULL) OR (D1.setDate IS NOT NULL AND D2.setDate IS NULL AND D1.setDate != 0)) AND ((D1.setDate IS NOT NULL AND D1.setDate <= D2.endDate) OR D1.setDate IS NULL)))
                    )
                    OR ((D2.setDate IS NOT NULL AND ((D2.endDate > (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d)))
AND (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d))) > D2.setDate)
OR (D1.endDate < D2.endDate AND D2.endDate < (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d)))
AND (D2.endDate - D1.endDate) < (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
(SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB), %d))))

OR (D2.setDate IS NULL AND ((D2.endDate > (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d)))
AND (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0, ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)),
ADDDATE(D1.endDate, %d))) > 0)
OR (D1.endDate < D2.endDate AND D2.endDate < (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d)))
AND (D2.endDate - D1.endDate) < (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
(SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB), %d))))))
                    )
                    ))'''% (self.duration, self.duration, self.duration, self.duration, self.duration, self.duration, self.duration, self.duration)
            if (self.chkAccountChronicDisease.isChecked() and self.chkAccountAcuteDisease.isChecked()):
                #острые заболевания, если и хронические и острые заболевания
                if self.chkDiseaseDiagnostic.isChecked():
                    self.controlDiseaseDiagnostic(u'1', dateBeginPeriod, dateEndPeriod, clientId, MKBFrom, MKBTo) # 5, 9
                stmt += u''' OR (D1.character_id = D2.character_id AND
                    (
                    D1.character_id = 1 AND
                    (
                    (D1.endDate <= D2.endDate AND ((D1.setDate IS NOT NULL AND D2.setDate IS NOT NULL AND (D1.setDate >= D2.setDate)) OR (D1.setDate IS NULL AND D2.setDate IS NULL) OR (D1.setDate IS NOT NULL AND D2.setDate IS NULL AND D1.setDate != 0)))
                    OR ((D1.endDate <= D2.endDate AND ((D2.setDate IS NOT NULL AND D1.endDate >= D2.setDate) OR (D2.setDate IS NULL AND D1.endDate >= 0))) AND ((D1.setDate IS NOT NULL AND D2.setDate IS NOT NULL AND D1.setDate <= D2.setDate) OR (D1.setDate IS NULL AND D2.setDate IS NULL) OR (D1.setDate IS NULL AND D2.setDate IS NOT NULL AND D2.setDate != 0)))
                    OR (D1.endDate >= D2.endDate AND (((D1.setDate IS NOT NULL AND D2.setDate IS NOT NULL AND (D1.setDate >= D2.setDate)) OR (D1.setDate IS NULL AND D2.setDate IS NULL) OR (D1.setDate IS NOT NULL AND D2.setDate IS NULL AND D1.setDate != 0)) AND ((D1.setDate IS NOT NULL AND D1.setDate <= D2.endDate) OR D1.setDate IS NULL)))
                    )
                    OR ((D2.setDate IS NOT NULL AND ((D2.endDate > (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d)))
AND (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d))) > D2.setDate)
OR (D1.endDate < D2.endDate AND D2.endDate < (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d)))
AND (D2.endDate - D1.endDate) < (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
(SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB), %d))))

OR (D2.setDate IS NULL AND ((D2.endDate > (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d)))
AND (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0, ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)),
ADDDATE(D1.endDate, %d))) > 0)
OR (D1.endDate < D2.endDate AND D2.endDate < (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
ADDDATE(D1.endDate, (SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB)), ADDDATE(D1.endDate, %d)))
AND (D2.endDate - D1.endDate) < (IF((SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB) != 0,
(SELECT MKB.duration FROM MKB WHERE MKB.DiagID = D1.MKB), %d))))))
                    )
                    ))'''% (self.duration, self.duration, self.duration, self.duration, self.duration, self.duration, self.duration, self.duration)

            stmt += u'''))
                    GROUP BY D1.id
                    ORDER BY D1.client_id ASC, D1.MKB ASC'''
            if self.chkDataDiagnosis.isChecked():
                query = db.query(stmt)
                if clientId:
                    while query.next():
                        self.recordBufferClientId.append(query.record())
                        self.recordBufferErrorClientId.append(u' Проблема длительности периода. ')
                        self.recordBufferCorrectClientId.append(7)                           # 7
                else:
                    while query.next():
                        self.recordBuffer.append(query.record())
                        self.recordBufferError.append(u' Проблема длительности периода. ')
                        self.recordBufferCorrect.append(7)                           # 7


    def loadDataDiagnosis(self):
        self.listResultControlDiagnosis.checkRunListWidget = False
        self.listResultControlDiagnosis.selectAll()
        self.listResultControlDiagnosis.clear()
        self.rows = 0
        self.lblCountLine.setText(u'всего строк: 0')
        self.btnCorrectControl.setEnabled(False)
        self.prbControlDiagnosis.setFormat('%v')
        self.prbControlDiagnosis.setValue(0)
        self.btnEndControl.setText(u'прервать')
        self.btnStartControl.setEnabled(False)
        lenStr = 0
        try:
            if self.chkMKB.isChecked():
                MKBFrom = normalizeMKB(self.edtMKBFrom.text())
                MKBTo = normalizeMKB(self.edtMKBTo.text())
            else:
                MKBFrom = None
                MKBTo = None
            QtGui.qApp.callWithWaitCursor(self, self.controlDiseaseLUD, None, MKBFrom, MKBTo)
            self.lblCountLine.setText(u'всего строк: %d' % len(self.recordBuffer))
            lenStr = self.selectDataDiagnosis(self.recordBuffer)
#        except Exception, e:
        except:
            self.abortProcess = True

        if self.abortProcess:
            self.listResultControlDiagnosis.reset()
            self.lblCountLine.setText(u'всего строк: %d' % self.listResultControlDiagnosis.count())
        self.prbControlDiagnosis.setText(u'прервано' if self.abortProcess else u'готово')
        self.btnEndControl.setText(u'закрыть')
        if lenStr > 0:
           self.btnCorrectControl.setEnabled(True)
        self.btnStartControl.setEnabled(True)
        self.checkRun = False
        self.abortProcess = False
        self.listResultControlDiagnosis.recordBufferCorrectLW = self.recordBufferCorrect
        self.listResultControlDiagnosis.checkRunListWidget = True


    def printDataDiagnosis(self, valStr):
        self.listResultControlDiagnosis.addItem(self.errorStr + valStr)
        item = self.listResultControlDiagnosis.item(self.rows)
        self.listResultControlDiagnosis.scrollToItem(item)
        self.rows += 1


    def selectDataDiagnosis(self, records):
        prbControlPercent = 0
        lenStr = len(records)
        if lenStr > 1:
            self.prbControlDiagnosis.setMaximum(lenStr - 1)
        i = 0
        for record in records:
            QtGui.qApp.processEvents()
            if self.abortProcess:
                self.checkRun = False
                break
            self.prbControlDiagnosis.setValue(prbControlPercent)
            prbControlPercent += 1
            lastName = forceString(record.value('lastName'))
            firstName = forceString(record.value('firstName'))
            patrName = forceString(record.value('patrName'))
            birthDate = forceString(record.value('birthDate'))
            clientId = forceString(record.value('client_id'))
            diagnos_id = forceString(record.value('id'))
            MKB = forceString(record.value('MKB'))
            MKBEx = forceString(record.value('MKBEx'))
            characterId = forceString(record.value('character_id'))
            traumaTypeId = forceString(record.value('name'))
            setDate = forceString(forceDate(record.value('setDate')))
            endDate = forceString(forceDate(record.value('endDate')))
            self.createStrDiagnosis(characterId, clientId, lastName, firstName, patrName, birthDate, diagnos_id, MKB, MKBEx, traumaTypeId, setDate, endDate, self.recordBufferError[i])
            i += 1
        return lenStr


    def createStrDiagnosis(self, characterId = u'', clientId = u'', lastName = u'', firstName = u'', patrName = u'', birthDate = u'', diagnos_id = u'', MKB = u'', MKBEx = u'', traumaTypeId = u'', setDate = u'', endDate = u'', recordBufferError = u''):
        strCharacter = self.createCharacterLine(characterId)
        resultStr = u''
        resultStr = u' Клиент: ' + clientId + u'(' + lastName + ' ' + firstName + ' ' + patrName + u' ,' + birthDate + u')'
        if MKB != u'':
            resultStr += u'  MKB: ' + MKB
        if MKBEx != u'':
            resultStr += u'  MKBEx: ' + MKBEx
        if traumaTypeId != u'':
            resultStr += u'  тип травмы: ' + traumaTypeId
        if  setDate != u'':
            resultStr += u'  Начальная дата: ' + setDate
        if  endDate != u'':
            resultStr += u'  Конечная дата: ' + endDate
        resultStr += recordBufferError + ' '+strCharacter
        self.printDataDiagnosis(resultStr)
