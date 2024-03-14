# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2018-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## основное MDI (и я надеюсь, единственное) окно обмена с СФР.
## MDI вроде как излишество, но я пока ленюсь придумывать интерфейс
## чтобы была и форма и верхнее меню, и чтобы хлопот было поменьше.
##
#############################################################################

#import time

from PyQt4                    import QtGui
from PyQt4.QtCore             import pyqtSignature, QDate, QDateTime, QMetaObject, QVariant

from library.database         import CTableRecordCache
from library.DialogBase       import CConstructHelperMixin
from library.MSCAPI           import MSCApi
from library.PreferencesMixin import CDialogPreferencesMixin
from library.RecordLock       import CRecordLockMixin
from library.TableModel       import ( CTableModel,
                                       CCol,
                                       CBoolCol,
                                       CDateCol,
                                       CDateTimeCol,
                                       CDesignationCol,
#                                       CEnumCol,
#                                       CRefBookCol,
#                                       CSumCol,
                                       CTextCol,
                                     )

from library.Utils            import (exceptionToUnicode,
                                      forceRef,
                                      formatName,
                                      formatNum,
                                      withWaitCursor,
                                     )
from Users.Rights import urFsselnEditPerson
from .ProgressWithLogDialog    import CProgressWithLogDialog
from .selectReadyTempInvalidDocumentIds   import selectReadyTempInvalidDocumentIds
from .selectExpiredTempInvalidDocumentIds import selectExpiredTempInvalidDocumentIds
from .Ui_WorkSpace             import Ui_CWorkSpace



class CWorkSpaceWindow(QtGui.QMdiSubWindow, Ui_CWorkSpace, CConstructHelperMixin, CDialogPreferencesMixin, CRecordLockMixin):
    u"""
    """
    def __init__(self, parent):
        QtGui.QMdiSubWindow.__init__(self, parent)
        CRecordLockMixin.__init__(self)

        self.addModels('NumbersRegistry', CNumbersRegistryModel(self))
        self.addModels('ReadyTempInvalidDocuments',   CReadyTempInvalidDocumentsModel(self))
        self.addModels('TempInvalidDocumentExports',  CTempInvalidDocumentExportsModel(self))
        self.addModels('ExpiredTempInvalidDocuments', CExpiredTempInvalidDocumentsModel(self))

        self.internal = QtGui.QWidget(self)
        self.setWidget(self.internal)

        self.addObject('actSelectAllReadyTempInvalidDocuments', QtGui.QAction(u'Выбрать все', self))
        self.addObject('actSelectAllExpiredTempInvalidDocuments', QtGui.QAction(u'Выбрать все', self))

        self.setupUi(self.internal)

        self.tblNumbersRegistry.setModel(self.modelNumbersRegistry)
        self.tblNumbersRegistry.setSelectionModel(self.selectionModelNumbersRegistry)

        self.tblReadyTempInvalidDocuments.setModel(self.modelReadyTempInvalidDocuments)
        self.tblReadyTempInvalidDocuments.setSelectionModel(self.selectionModelReadyTempInvalidDocuments)

        self.tblReadyTempInvalidDocuments.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblReadyTempInvalidDocuments.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tblReadyTempInvalidDocuments.addPopupAction(self.actSelectAllReadyTempInvalidDocuments)

        self.tblTempInvalidDocumentExports.setModel(self.modelTempInvalidDocumentExports)
        vh = self.tblTempInvalidDocumentExports.verticalHeader()
        vh.setResizeMode(vh.ResizeToContents)

        self.tblExpiredTempInvalidDocuments.setModel(self.modelExpiredTempInvalidDocuments)
        self.tblExpiredTempInvalidDocuments.setSelectionModel(self.selectionModelExpiredTempInvalidDocuments)
        self.tblExpiredTempInvalidDocuments.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblExpiredTempInvalidDocuments.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tblExpiredTempInvalidDocuments.addPopupAction(self.actSelectAllExpiredTempInvalidDocuments)

        QMetaObject.connectSlotsByName(self) # т.к. в setupUi параметр не self

        self.readyFilter = None
        self.historyFilter = None
        self.expiredFilter = None

        self.cmbReadyPerson.addNotSetValue()
        self.cmbHistoryPerson.addNotSetValue()

        self.updateNumbersRegistry()


    #######################################################################
    ##
    ## всякие потроха, навалом
    ##

    #######################################################################
    ##
    ## страница "реестр номеров"
    ##

    def registerNumbers(self, numbers):
        qApp = QtGui.qApp
        db = qApp.db
        userId = qApp.userId
        now = QDateTime.currentDateTime()
        today = now.date()
        docTypeId = qApp.getTempInvalidBlankTypeId()
        orgId  = qApp.getCurrentOrgId()

        table = db.table('BlankTempInvalid_Party')
        db.transaction()
        try:
            for number in numbers:
                record = table.newRecord()
                record.setValue('createDatetime',  now)
                record.setValue('createPerson_id', userId)
                record.setValue('modifyDatetime',  now)
                record.setValue('modifyPerson_id', userId)
                record.setValue('date',            today)
                record.setValue('doctype_id',      docTypeId)
                record.setValue('org_id',          orgId)
                record.setValue('serial',          '')
                record.setValue('numberFrom',      number)
                record.setValue('numberTo',        number)
                record.setValue('amount',          1)
                record.setValue('balance',         1)
                record.setValue('isElectronic',    1)
                db.insertRecord(table, record)
            db.commit()
        except:
            db.rollback()
            raise


    @withWaitCursor
    def updateNumbersRegistry(self):
        self.lblSizeOfNumbersRegistry.setText(u'…')
        db = QtGui.qApp.db
        table = db.table('BlankTempInvalid_Party')
        idList = db.getIdList(table,
                              idCol='id',
                              where=db.joinAnd( [ table['deleted'].eq(0),
                                                  table['doctype_id'].eq( QtGui.qApp.getTempInvalidBlankTypeId() ),
                                                  table['org_id'].eq(QtGui.qApp.getCurrentOrgId()),
#                                                  db.joinOr([
#                                                              table['org_id'].eq(None),
#                                                              table['org_id'].eq(QtGui.qApp.getCurrentOrgId()),
#                                                            ]),
                                                  table['isElectronic'].eq(1),
                                                  table['used'].eq(0)
                                                ]
                                              ),
                              order='date, numberFrom')
        self.modelNumbersRegistry.setIdList(idList)
        cnt = len(idList)
        if cnt == 0:
            message = u'Список пуст'
        else:
            message = u'В списке %s ЭЛН' % formatNum(cnt, (u'номер', u'номера',  u'номеров'))
        self.lblSizeOfNumbersRegistry.setText(message)


    #######################################################################
    ##
    ## страница "Готовые к передаче документы"
    ##

    def resetReadyFilter(self):
        self.cmbReadyOrgStructure.setValue(QtGui.qApp.getCurrentOrgStructureId())
        if QtGui.qApp.userSpecialityId:
            self.cmbReadyPerson.setValue(QtGui.qApp.userId)
            self.cmbReadyPerson.setEnabled(QtGui.qApp.userHasRight(urFsselnEditPerson))
        else:
            self.cmbReadyPerson.setValue(None)
            self.cmbReadyPerson.setEnabled(True)
        self.edtReadyNumber.setText('')
#        self.edtReadyBegDate.setDate(QDate.currentDate().addDays(-1))
        self.edtReadyBegDate.setDate(QDate.currentDate().addDays(-100))
        self.edtReadyEndDate.setDate(QDate.currentDate())


    def initialiseReadyFilter(self):
        self.readyFilter = { 'orgStructureId' : self.cmbReadyOrgStructure.value(),
                             'personId'       : self.cmbReadyPerson.value() if self.cmbReadyPerson.value()>0 else None,
                             'number'         : unicode(self.edtReadyNumber.text()),
                             'begDate'        : self.edtReadyBegDate.date(),
                             'endDate'        : self.edtReadyEndDate.date(),
                           }


    @withWaitCursor
    def updateReadyTempInvalidDocuments(self):
        self.lblRowsInReadyTempInvalidDocuments.setText(u'…')
        idList = selectReadyTempInvalidDocumentIds(self.readyFilter)
        self.modelReadyTempInvalidDocuments.setIdList(idList)
        self.tblReadyTempInvalidDocuments.selectAll()
        self.btnSend.setEnabled(self.selectionModelReadyTempInvalidDocuments.hasSelection())
        cnt = len(idList)
        if cnt == 0:
            message = u'Список пуст'
        else:
            message = u'В списке %s' % formatNum(cnt, (u'документ', u'документа',  u'документов'))
        self.lblRowsInReadyTempInvalidDocuments.setText(message)

    #######################################################################
    ##
    ## страница "Контроль открытых ЭЛН"
    ##

    def resetExpiredFilter(self):
        self.cmbExpiredOrgStructure.setValue(QtGui.qApp.getCurrentOrgStructureId())
        if QtGui.qApp.userSpecialityId:
            self.cmbExpiredPerson.setValue(QtGui.qApp.userId)
            self.cmbExpiredPerson.setEnabled(QtGui.qApp.userHasRight(urFsselnEditPerson))
        else:
            self.cmbExpiredPerson.setValue(None)
            self.cmbExpiredPerson.setEnabled(True)
        self.edtExpiredDays.setValue(30)
        self.edtExpiredFullName.setText('')


    def initialiseExpiredFilter(self):
        self.expiredFilter = { 'orgStructureId' : self.cmbExpiredOrgStructure.value(),
                               'personId'       : self.cmbExpiredPerson.value(),
                               'days'           : self.edtExpiredDays.value(),
                               'fullName'       : self.edtExpiredFullName.text()
                             }


    @withWaitCursor
    def updateExpiredTempInvalidDocuments(self):
        self.lblRowsInExpiredTempInvalidDocuments.setText(u'…')
        idList = selectExpiredTempInvalidDocumentIds(self.expiredFilter)
        self.modelExpiredTempInvalidDocuments.setIdList(idList)
        self.tblExpiredTempInvalidDocuments.selectAll()
        self.btnCheckExpiredDocuments.setEnabled(self.selectionModelExpiredTempInvalidDocuments.hasSelection())
        cnt = len(idList)
        if cnt == 0:
            message = u'Список пуст'
        else:
            message = u'В списке %s' % formatNum(cnt, (u'документ', u'документа',  u'документов'))
        self.lblRowsInExpiredTempInvalidDocuments.setText(message)


    #######################################################################
    ##
    ## страница "История обмена"
    ##

    def resetHistoryFilter(self):
        self.cmbHistoryOrgStructure.setValue( QtGui.qApp.getCurrentOrgStructureId() )
        if QtGui.qApp.userSpecialityId:
            self.cmbHistoryPerson.setValue(QtGui.qApp.userId)
            self.cmbHistoryPerson.setEnabled(QtGui.qApp.userHasRight(urFsselnEditPerson))
        else:
            self.cmbHistoryPerson.setValue(None)
            self.cmbHistoryPerson.setEnabled(True)
        self.edtHistoryNumber.setText('')
        self.edtHistoryBegDate.setDate(QDate.currentDate().addDays(-1))
        self.edtHistoryEndDate.setDate(QDate.currentDate())


    def initialiseHistoryFilter(self):
        self.historyFilter = { 'orgStructureId' : self.cmbHistoryOrgStructure.value(),
                               'personId'       : self.cmbHistoryPerson.value() if self.cmbHistoryPerson.value()>0 else None,
                               'number'         : unicode(self.edtHistoryNumber.text()),
                               'begDate'        : self.edtHistoryBegDate.date(),
                               'endDate'        : self.edtHistoryEndDate.date(),
                             }


    @withWaitCursor
    def updateHistoryTempInvalidDocuments(self):
       idList = selectTempInvalidDocumentExportIds(self.historyFilter)
       self.modelTempInvalidDocumentExports.setIdList(idList)


    #######################################################################
    ##
    ## обработчики сигналов
    ##


    @pyqtSignature('int')
    def on_tabMain_currentChanged(self, index):
        if index == 0:
            self.updateNumbersRegistry()
        elif index == 1:
            if self.readyFilter is None:
                self.resetReadyFilter()
                self.initialiseReadyFilter()
            self.updateReadyTempInvalidDocuments()
        elif index == 2:
            if self.expiredFilter is None:
                self.resetExpiredFilter()
                self.initialiseExpiredFilter()
            self.updateExpiredTempInvalidDocuments()
        elif index == 3:
            if self.historyFilter is None:
                self.resetHistoryFilter()
                self.initialiseHistoryFilter()
            self.updateHistoryTempInvalidDocuments()


    #######################################################################
    ##
    ## страница "реестр номеров"
    ##


    @pyqtSignature('')
    def on_btnRequestNumbers_clicked(self):
        def _requestNumbers():
            QtGui.qApp.getTempInvalidBlankTypeId()  # Для проверки существования записи
            api = MSCApi(QtGui.qApp.getCsp())
            cert = QtGui.qApp.getUserCert(api)
            with cert.provider() as master:  # для исключения массового запроса пароля
                assert master  # silence pyflakes
                numbers = QtGui.qApp.requestNumbers()
                self.registerNumbers(numbers)
                self.updateNumbersRegistry()
        QtGui.qApp.call(self, _requestNumbers)

    #######################################################################
    ##
    ## страница "готовые к передаче документы"
    ##

    @pyqtSignature('int')
    def on_cmbReadyOrgStructure_currentIndexChanged(self, index):
        value = self.cmbReadyOrgStructure.value()
        self.cmbReadyPerson.setOrgStructureId(value)


    @pyqtSignature('QAbstractButton*')
    def on_buttonBoxReady_clicked(self, button):
        buttonCode = self.buttonBoxReady.standardButton(button)
        if buttonCode == self.buttonBoxReady.Apply:
            self.initialiseReadyFilter()
            self.updateReadyTempInvalidDocuments()
        elif buttonCode == self.buttonBoxReady.Reset:
            self.resetReadyFilter()
            self.initialiseReadyFilter()
            self.updateReadyTempInvalidDocuments()


    @pyqtSignature('')
    def on_actSelectAllReadyTempInvalidDocuments_triggered(self):
        self.tblReadyTempInvalidDocuments.selectAll()


    @pyqtSignature('QItemSelection, QItemSelection')
    def on_selectionModelReadyTempInvalidDocuments_selectionChanged(self, selected, deselected):
        self.btnSend.setEnabled(self.selectionModelReadyTempInvalidDocuments.hasSelection())


    @pyqtSignature('')
    def on_btnSend_clicked(self):
        def _send():
            idList = self.tblReadyTempInvalidDocuments.selectedItemIdList()
            def stepIterator(progressDialog):
                for id in idList:
                    try:
                        lockId, message = self.tryLock('TempInvalidDocument', id)
                        if lockId:
                            try:
                                ok, number, message = QtGui.qApp.sendDocument(id)
                            finally:
                                self.releaseLock(lockId)
                            progressDialog.log(number, message)
                        else:
                            progressDialog.log('#%d' % id, message)
                    except Exception, e:
                        progressDialog.log('#%d' % id, exceptionToUnicode(e))
                        QtGui.qApp.logCurrentException()
                    yield 1

            api = MSCApi(QtGui.qApp.getCsp())
            cert = QtGui.qApp.getUserCert(api)
            with cert.provider() as master:  # для исключения массового запроса пароля
                assert master  # silence pyflakes
                pd = CProgressWithLogDialog(self)
                pd.setWindowTitle(u'Журнал передачи ЭЛН в СФР')
                pd.setFormat(u'%v из %m')
                pd.setStepCount(len(idList))
                pd.setAutoStart(True)
                pd.setAutoClose(False)
                pd.setStepIterator(stepIterator)
                pd.exec_()
            self.updateReadyTempInvalidDocuments()
        QtGui.qApp.call(self, _send)



    #######################################################################
    ##
    ## страница "Контроль открытых ЭЛН"
    ##

    @pyqtSignature('int')
    def on_cmbExpiredOrgStructure_currentIndexChanged(self, index):
        value = self.cmbExpiredOrgStructure.value()
        self.cmbExpiredPerson.setOrgStructureId(value)


    @pyqtSignature('QAbstractButton*')
    def on_buttonBoxExpired_clicked(self, button):
        buttonCode = self.buttonBoxExpired.standardButton(button)
        if buttonCode == self.buttonBoxExpired.Apply:
            self.initialiseExpiredFilter()
            self.updateExpiredTempInvalidDocuments()
        elif buttonCode == self.buttonBoxExpired.Reset:
            self.resetExpiredFilter()
            self.initialiseExpiredFilter()
            self.updateExpiredTempInvalidDocuments()


    @pyqtSignature('')
    def on_actSelectAllExpiredTempInvalidDocuments_triggered(self):
        self.tblExpiredTempInvalidDocuments.selectAll()


    @pyqtSignature('QItemSelection, QItemSelection')
    def on_selectionModelExpiredTempInvalidDocuments_selectionChanged(self, selected, deselected):
        self.btnCheckExpiredDocuments.setEnabled(self.selectionModelExpiredTempInvalidDocuments.hasSelection())


    @pyqtSignature('')
    def on_btnCheckExpiredDocuments_clicked(self):
        def _checkDocs():
            idList = self.tblExpiredTempInvalidDocuments.selectedItemIdList()
            def stepIterator(progressDialog):
                for id in idList:
                    try:
                        ok, number, message = QtGui.qApp.checkExpiredDocument(id)
    #                    ok, number, message = False, '0'*10, u'Не реализовано'
                        progressDialog.log(number, message)
                    except Exception, e:
                        progressDialog.log('#%d' % id, exceptionToUnicode(e))
                        QtGui.qApp.logCurrentException()
                    yield 1

            api = MSCApi(QtGui.qApp.getCsp())
            cert = QtGui.qApp.getUserCert(api)
            with cert.provider() as master:  # для исключения массового запроса пароля
                assert master  # silence pyflakes
                pd = CProgressWithLogDialog(self)
                pd.setWindowTitle(u'Журнал проверки ЭЛН в СФР')
                pd.setFormat(u'%v из %m')
                pd.setStepCount(len(idList))
                pd.setAutoStart(True)
                pd.setAutoClose(False)
                pd.setStepIterator(stepIterator)
                pd.exec_()
            self.updateExpiredTempInvalidDocuments()

        QtGui.qApp.call(self, _checkDocs)


    #######################################################################
    ##
    ## страница "История обмена"
    ##

    @pyqtSignature('int')
    def on_cmbHistoryOrgStructure_currentIndexChanged(self, index):
        value = self.cmbHistoryOrgStructure.value()
        self.cmbHistoryPerson.setOrgStructureId(value)


    @pyqtSignature('QAbstractButton*')
    def on_buttonBoxHistory_clicked(self, button):
        buttonCode = self.buttonBoxHistory.standardButton(button)
        if buttonCode == self.buttonBoxHistory.Apply:
            self.initialiseHistoryFilter()
            self.updateHistoryTempInvalidDocuments()
        elif buttonCode == self.buttonBoxHistory.Reset:
            self.resetHistoryFilter()
            self.initialiseHistoryFilter()
            self.updateHistoryTempInvalidDocuments()



class CNumbersRegistryModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent, [
            CDateCol(u'Дата',    ['date'],    10),
            CTextCol(u'Номер',   ['numberFrom'], 20),
            ], 'BlankTempInvalid_Party' )


class CClientCol(CCol):
    def __init__(self, title, fields, defaultWidth):
        CCol.__init__(self, title, fields, defaultWidth, 'l')
        db = QtGui.qApp.db
        self.tempInvalidCache = CTableRecordCache(db, 'TempInvalid', 'client_id')
        self.clientCache = CTableRecordCache(db, 'Client', 'lastName, firstName, patrName') #', birthDate, sex, SNILS')


    def format(self, values):
        tempInvalidId  = forceRef(values[0])
        tempInvalidRecord = self.tempInvalidCache.get(tempInvalidId)
        clientId = forceRef(tempInvalidRecord.value('client_id')) if tempInvalidRecord else None
        clientRecord = self.clientCache.get(clientId)
        if clientRecord:
            name  = formatName(clientRecord.value('lastName'),
                               clientRecord.value('firstName'),
                               clientRecord.value('patrName'))
            return QVariant(name)
        return CCol.invalid


    def invalidateRecordsCache(self):
        self.tempInvalidCache.invalidate()
        self.clientCache.invalidate()



class CReadyTempInvalidDocumentsModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent, [
            CTextCol(u'Номер',          ['number'], 20),
            CDateCol(u'Дата изменения', ['modifyDatetime'],    10),
#            CTextCol(u'Номер',   ['number'], 20),
            CDesignationCol(u'Врач',    ['master_id'],  [('TempInvalid', 'person_id'), ('vrbPersonWithSpeciality', 'name')], 20),
            CClientCol(u'Получатель', ['master_id'],  40)
            ], 'TempInvalidDocument' )



class CClient2Col(CCol):
    def __init__(self, title, fields, defaultWidth):
        CCol.__init__(self, title, fields, defaultWidth, 'l')
        db = QtGui.qApp.db
        self.tempInvalidDocumentCache = CTableRecordCache(db, 'TempInvalidDocument', 'master_id')
        self.tempInvalidCache = CTableRecordCache(db, 'TempInvalid', 'client_id')
        self.clientCache = CTableRecordCache(db, 'Client', 'lastName, firstName, patrName') #', birthDate, sex, SNILS')


    def format(self, values):
        tempInvalidDocumentId  = forceRef(values[0])
        tempInvalidDocumentRecord  = self.tempInvalidDocumentCache.get(tempInvalidDocumentId)
        tempInvalidId = forceRef(tempInvalidDocumentRecord.value('master_id'))
        tempInvalidRecord = self.tempInvalidCache.get(tempInvalidId)
        clientId = forceRef(tempInvalidRecord.value('client_id')) if tempInvalidRecord else None
        clientRecord = self.clientCache.get(clientId)
        if clientRecord:
            name  = formatName(clientRecord.value('lastName'),
                               clientRecord.value('firstName'),
                               clientRecord.value('patrName'))
            return QVariant(name)
        return CCol.invalid


    def invalidateRecordsCache(self):
        self.tempInvalidDocumentCache.invalidate()
        self.tempInvalidCache.invalidate()
        self.clientCache.invalidate()




class CTempInvalidDocumentExportsModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent, [
            CDateTimeCol(u'Дата передачи', ['dateTime'], 20),
            CTextCol(u'Номер',             ['externalId'], 20),
            CBoolCol(u'Успех',             ['success'], 20),
            CClient2Col(u'Получатель',     ['master_id'],  40),
            CDesignationCol(u'Врач',       ['respPerson_id'], [('vrbPersonWithSpeciality', 'name')], 20),
            CDesignationCol(u'Отправитель', ['person_id'], [('vrbPersonWithSpeciality', 'name')], 20),
            CTextCol(u'Сообщение',         ['note'], 100)
            ], 'TempInvalidDocument_Export' )


#    def data(self, index, role):
#        if role == Qt.TextAlignmentRole:
#            return QVariant(Qt.AlignLeft|Qt.AlignTop)
#        else:
#            return CTableModel.data(self, index, role)


class CExpiredTempInvalidDocumentsModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent, [
            CTextCol(u'Номер',          ['number'], 20),
            CDateCol(u'Дата изменения', ['modifyDatetime'],    10),
#            CTextCol(u'Номер',   ['number'], 20),
            CDesignationCol(u'Врач',    ['master_id'],  [('TempInvalid', 'person_id'), ('vrbPersonWithSpeciality', 'name')], 20),
            CClientCol(u'Получатель', ['master_id'],  40),
            CDesignationCol(u'Дата начала случая',  ['master_id'],  [('TempInvalid', 'begDate')], 20),
            CDesignationCol(u'Дата окончания случая',  ['master_id'],  [('TempInvalid', 'endDate')], 20),
            ], 'TempInvalidDocument' )


def selectTempInvalidDocumentExportIds(filter):
    db = QtGui.qApp.db
    tempInvalidDocTypeId = QtGui.qApp.getTempInvalidDocTypeId()
    fssSystemId          = QtGui.qApp.getFssSystemId()
    orgId                = QtGui.qApp.getCurrentOrgId()
    orgStructureId = filter.get('orgStructureId', None)
    personId       = filter.get('personId', None)
    number         = filter.get('number', None)
    begDate        = filter.get('begDate', None)
    endDate        = filter.get('endDate', None)

    tableTempInvalidDocumentExport = db.table('TempInvalidDocument_Export')
    tableTempInvalidDocument       = db.table('TempInvalidDocument')
    tableTempInvalid               = db.table('TempInvalid')
    tablePerson                    = db.table('Person')

    table = tableTempInvalidDocumentExport
    table = table.innerJoin( tableTempInvalidDocument,
                             tableTempInvalidDocument['id'].eq(tableTempInvalidDocumentExport['master_id'])
                           )

    table = table.innerJoin( tableTempInvalid,
                             tableTempInvalid['id'].eq(tableTempInvalidDocument['master_id'])
                           )
    table = table.innerJoin(tablePerson,
                            tablePerson['id'].eq(tableTempInvalid['person_id'])
                           )
    cond = [ tableTempInvalidDocument['deleted'].eq(0),
             tableTempInvalidDocument['electronic'].eq(1),
             tableTempInvalid['deleted'].eq(0),
             tableTempInvalid['doctype_id'].eq(tempInvalidDocTypeId),
             tableTempInvalidDocumentExport['system_id'].eq(fssSystemId)
           ]
    if personId:
        cond.append(tablePerson['id'].eq(personId))
    elif orgStructureId:
        orgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', orgStructureId)
        cond.append(tablePerson['orgStructure_id'].inlist(orgStructureIdList))
    else:
        cond.append(tablePerson['org_id'].eq(orgId))
    if number:
        cond.append(tableTempInvalidDocumentExport['externalId'].eq(number))
    if begDate:
        cond.append(tableTempInvalidDocumentExport['dateTime'].ge(begDate))
    if endDate:
        cond.append(tableTempInvalidDocumentExport['dateTime'].lt(endDate.addDays(1)))

    idList = db.getIdList(table,
                          idCol=tableTempInvalidDocumentExport['id'].name(),
                          where=cond,
                          order='TempInvalidDocument_Export.id'
                         )
    return idList
