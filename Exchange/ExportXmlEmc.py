# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import QDate, QDir, QFile, QIODevice, pyqtSignature
#from PyQt4.QtXml import *

from library.Utils  import forceDate, forceString, forceStringEx, formatSNILS, toVariant

from Events.Utils import getEventName, getWorkEventTypeFilter
from Exchange.AbstractExportXmlStreamWriter import CAbstractExportXmlStreamWriter
from Exchange.Utils import tbl, compressFileInRar
from Registry.Utils import getClientInfoEx, getInfisForStreetKLADRCode, getInfisForKLADRCode

from Exchange.Ui_ExportXmlEmc import Ui_Dialog


nameFields = ('last', 'first', 'middle')
basicFields = ('id', 'date', 'result')
otherFields = ('date', 'name', 'result')

basicSubGroup = {
    'record' : {'fields': basicFields}
}

otherSubGroup = {
    'record' : {'fields': otherFields}
}

issledSubGroup = {
    'basic': { 'subGroup': basicSubGroup },
    'other': { 'subGroup': otherSubGroup }
}

osmotriFields = ('id',  'date')

osmotriSubGroup = {
    'record' : {'fields': osmotriFields}
}

privivkiFields = ('state', )


cardSubGroup = {
    'issled': { 'subGroup': issledSubGroup},
    'zakluchVrachName': {'fields': nameFields},
    'osmotri' : {'subGroup': osmotriSubGroup},
    'privivki': {'fields': privivkiFields},
}

cardFields = ('idInternal',  'dateOfObsled', 'height', 'weight',
    'healthGroupBefore', 'healthGroup', 'zakluchDate', 'idType',
    'healthyMKB', 'oms', 'recommendZOZH', )

cardsGroup = {
    'card': {'fields': cardFields,  'subGroup': cardSubGroup},
}

childDateFields = ('dateOfBirth', )
childFields = ('idInternal', 'idSex', 'idDocument', 'documentSer',
    'documentNum', 'snils', 'polisSer', 'polisNum',
    'idType','idCategory', 'idInsuranceCompany', 'medSanName',
    'medSanAddress', 'idEducationOrg', 'idOrphHabitation',
    'dateOrphHabitation', 'idStacOrg'
    ) + childDateFields

addressFields = ('kladrNP', 'kladrStreet', 'house', 'building', 'appartment')

childGroup = {
    'name': {'fields': nameFields},
    'address': {'fields': addressFields},
    'cards': {'subGroup': cardsGroup},
}

def ExportXmlEmc(parent):
    QtGui.qApp.setWaitCursor()
    dlg = CExportXmlEmc(parent)
    dlg.edtFileName.setText(forceString(QtGui.qApp.preferences.appPrefs.get('ExportXmlEmcFileName', '')))
    dlg.edtBegDate.setDate(forceDate(QtGui.qApp.preferences.appPrefs.get('ExportXmlEmcFileNameBegDate', QDate.currentDate())))
    dlg.edtEndDate.setDate(forceDate(QtGui.qApp.preferences.appPrefs.get('ExportXmlEmcFileNameEndDate', QDate.currentDate())))
    QtGui.qApp.restoreOverrideCursor()
    dlg.exec_()
    QtGui.qApp.preferences.appPrefs['ExportXmlEmcFileName'] = toVariant(dlg.edtFileName.text())
    QtGui.qApp.preferences.appPrefs['ExportXmlEmcFileNameBegDate'] = toVariant(dlg.edtBegDate.date())
    QtGui.qApp.preferences.appPrefs['ExportXmlEmcFileNameEndDate'] = toVariant(dlg.edtEndDate.date())


class CEmcXmlStreamWriter(CAbstractExportXmlStreamWriter):
    idTypeMap = {
        u'467': '1',
        u'05 дет.':  '2',
        u'50-1дет':  '3',
        u'50-2дет':  '4'
    }

    defaultValue = {
        'snils' : '000-000-000-00',
        'idInternal': '0',
        'idSex': '0',
        'idDocument': '0',
        'documentSer': '0',
        'documentNum': '0',
        'polisSer': '0',
        'polisNum': '0',
        'idType': '1',
        'idCategory': '0',
        'idInsuranceCompany': '0',
        'medSanName': '0',
        'medSanAddress': '0',
        'idEducationOrg': '0',
        'idOrphHabitation': '0',
        'dateOrphHabitation': '1917-10-07',
        'idStacOrg': '0',
        'dateOfBirth': '1917-10-07',
        'dateOfObsled': '1917-10-07',
        'height': '0',
        'weight': '0',
        'healthGroupBefore': '1',
        'healthGroup': '1',
        'zakluchDate': '1917-10-07',
        'last': '0',
        'first': '0',
        'middle': '0',
        'last': '0',
        'first': '0',
        'middle': '0',
        'kladrNP': '0',
        'kladrStreet': '0',
        'house': '0',
        'building': '0',
        'appartment': '0',
        'name': '0',
        'result': '0',
        'id': '1',
        'date': '1917-10-07',
        'diagnosisBefore': '0',
        'healthyMKB': 'Z00',
        'diagnosisAfter': '0',
        'osmotri': '0',
        'privivki': '0',
        'oms': '0',
        'recommendZOZH': '-',
        'state' : '1',
    }

    def __init__(self, parent):
        CAbstractExportXmlStreamWriter.__init__(self, parent)
        currentOrgId = QtGui.qApp.currentOrgId()
        self.currentOrgFullName = forceString(QtGui.qApp.db.translate('Organisation', 'id', currentOrgId, 'fullName'))
        self.currentOrgAddress = forceString(QtGui.qApp.db.translate('Organisation', 'id', currentOrgId, 'address'))


    def writeElement(self, elementName, value=None):
            self.writeTextElement(elementName, value if value else self.defaultValue.get(elementName, ''))


    def writeHeader(self, _):
        self.writeStartElement('children')


    def writeRecord(self, record, _):
        if forceString(record.value('child_snils')):
            record.setValue('child_snils', toVariant(formatSNILS(record.value('child_snils'))))

        if not forceString(record.value('child_medSanName')):
            record.setValue('child_medSanName', toVariant(self.currentOrgFullName))
            record.setValue('child_medSanAddress', toVariant(self.currentOrgAddress))

        eventTypeCode = forceString(record.value('child_idType'))
        record.setValue('child_idType', toVariant(self.idTypeMap.get(eventTypeCode, '1')))

        self.writeGroup('child', childFields, record, childGroup,
            dateFields=childDateFields)


    def writeFooter(self, _):
        self.writeEndElement()


class CExportXmlEmc(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.checkRun = False
        self.abort = False
        self.setWindowTitle(u'Экспорт XML для РосМинЗдрава')

        self.cmbSpeciality.setTable('rbSpeciality', True)
        self.cmbEventPurpose.setTable('rbEventTypePurpose', False, filter='code != \'0\'')
        self.cmbEventType.setTable('EventType', False, filter=getWorkEventTypeFilter())
        self.cmbEventProfile.setTable('rbEventProfile', True)

        self.progressBar.setFormat('%v')
        self.progressBar.setValue(0)

        self.tableEvent = tbl('Event')
        self.tableEventType = tbl('EventType')
        self.tableAction = tbl('Action')
        self.tableActionType = tbl('ActionType')
        self.tableClient = tbl('Client')
        self.tableVisit = tbl('Visit')
        self.tablePerson = tbl('vrbPersonWithSpeciality').alias('ExecPerson')
        self.tableTempInvalidPeriod = tbl('TempInvalid_Period')
        self.tempInvalidCond =  []
        self.defaultSpecialityCodeFieldName = 'OKSOCode'

        self.db = QtGui.qApp.db
        self.xmlWriter = None


    def createQuery(self, params):
        dateFrom = params.get('dateFrom')
        dateTo   = params.get('dateTo')
        specialityId = params.get('specialityId')
        doctorPersonId = params.get('doctorPersonId')
        ageBegin = params.get('ageBegin')
        ageEnd = params.get('ageEnd')
        sex = params.get('sex')
#        onlyMes = params.get('onlyMes')

        cond = []
        cond.append(self.tableEvent['execDate'].le(dateTo))
        cond.append(self.tableEvent['execDate'].ge(dateFrom))
        cond.append(self.tableEvent['deleted'].eq(0))

        if specialityId:
            cond.append(self.tablePerson['speciality_id'].eq(specialityId))

        if doctorPersonId:
            cond.append(self.tablePerson['id'].eq(doctorPersonId))

        if sex:
            cond.append(self.tableClient['sex'].eq(sex))

        if ageBegin:
            cond.append(self.tableClient['birthDate'].le(QDate.currentDate().addYears(-ageBegin)))
            cond.append(self.tableClient['birthDate'].ge(QDate.currentDate().addYears(-ageEnd)))

        purposeId      = params.get('purposeId')
        eventTypeId    = params.get('eventTypeId')
        eventProfileId = params.get('eventProfileId')
        mesId          = params.get('mesId')

        if purposeId:
            cond.append(self.tableEventType['purpose_id'].eq(purposeId))

        if eventTypeId:
            cond.append(self.tableEventType['id'].eq(eventTypeId))

        if eventProfileId:
            cond.append(self.tableEventType['eventProfile_id'].eq(eventProfileId))

        if mesId:
            cond.append(self.tableEvent['MES_id'].eq(mesId))

        if params.get('isPolicy'):
            insurerId = params.get('insurerId')
            policyType = params.get('policyType')

            if policyType:
                if policyType == u'ОМС':
                    if insurerId:
                        cond.append('ClientPolicyCompulsory.`insurer_id`=%d'%insurerId)
                    else:
                        cond.append('ClientPolicyCompulsory.`insurer_id` IS NULL')
                else:
                    if insurerId:
                        cond.append('ClientPolicyVoluntary.`insurer_id`=%d'%insurerId)
                    else:
                        cond.append('ClientPolicyVoluntary.`insurer_id` IS NULL')
            else:
                if insurerId:
                    cond.append(self.db.joinOr(['ClientPolicyCompulsory.`insurer_id`=%d'%insurerId, 'ClientPolicyVoluntary.`insurer_id`=%d'%insurerId]))
                else:
                    cond.append(self.db.joinAnd(['ClientPolicyCompulsory.`insurer_id` IS NULL', 'ClientPolicyVoluntary.`insurer_id` IS NULL']))

        specialityCodeFieldName = params.get('specialityCodeFieldName', '')

        if not specialityCodeFieldName:
            specialityCodeFieldName = self.defaultSpecialityCodeFieldName

        stmt = '''SELECT
    CONCAT(Client.`id`, '.', Event.`id`) AS child_idInternal,
    Client.lastName AS name_last,
    Client.firstName AS name_first,
    Client.patrName AS name_middle,
    Client.SNILS AS child_snils,
    Client.sex AS child_idSex,
    Client.birthDate AS child_dateOfBirth,
    ClientPolicy.serial AS child_polisSer,
    ClientPolicy.number AS child_polisNum,
    ClientDocument.serial AS child_documentSer,
    ClientDocument.number AS child_documentNum,
    AttachOrg.fullName AS child_medSanName,
    AttachOrg.address AS child_medSanAddress,
    rbDocumentType.regionalCode AS child_idDocument,
    Insurer.smoCode AS child_idInsuranceCompany,
    '4' AS child_idCategory,
    EventType.code AS child_idType,
    Address.flat AS address_appartment,
    AddressHouse.number AS address_house,
    AddressHouse.corpus AS address_building,
    AddressHouse.KLADRCode AS address_kladrNP,
    AddressHouse.KLADRStreetCode AS address_kladrStreet
FROM Event
    LEFT OUTER JOIN Contract ON Event.`contract_id` = Contract.`id`
    INNER JOIN Client ON Client.`id` = Event.`client_id`
    LEFT OUTER JOIN ClientPolicy ON
        ClientPolicy.`id` = getClientPolicyIdForDate(Client.`id`, 1, Event.execDate, Event.id)
    LEFT JOIN Organisation AS Insurer ON Insurer.`id` = ClientPolicy.insurer_id
    LEFT JOIN ClientDocument ON
        ClientDocument.`id` = getClientDocumentId(Client.`id`)
    LEFT JOIN rbDocumentType ON
        ClientDocument.`documentType_id` = rbDocumentType.`id`
    LEFT JOIN ClientAddress ON
        ClientAddress.`id` = getClientLocAddressId(Client.`id`)
    LEFT JOIN Address ON ClientAddress.address_id = Address.`id`
    LEFT JOIN AddressHouse ON Address.house_id = AddressHouse.`id`
    LEFT JOIN Person AS ExecPerson ON Event.execPerson_id = ExecPerson.`id`
    LEFT JOIN EventType ON Event.eventType_id = EventType.`id`
    LEFT JOIN ClientAttach ON ClientAttach.id = getClientAttachIdForDate(Client.`id`, 0, Event.execDate)
    LEFT JOIN Organisation AS AttachOrg ON AttachOrg.id = ClientAttach.LPU_id
WHERE %s
        ''' % self.db.joinAnd(cond)

        return self.db.query(stmt)


    def process(self, query, params):
        if query.size():
            self.xmlWriter = CEmcXmlStreamWriter(self)
            fileName = forceStringEx(self.edtFileName.text())

            outFile = QFile(fileName)
            if not outFile.open(QIODevice.WriteOnly | QIODevice.Text):
                QtGui.QMessageBox.warning(self, self.windowTitle(),
                    self.tr(u'Не могу открыть файл для записи %1:\n%2.')
                        .arg(fileName)
                        .arg(outFile.errorString()))
                return
            else:
                self.xmlWriter.setDevice(outFile)

            if self.xmlWriter.writeFile(outFile, query, self.progressBar):
                self.progressBar.setText(u'Готово')

                if params.get('makeRar', None):
                    compressFileInRar(fileName, fileName + '.rar')
            else:
                self.progressBar.setText(u'Прервано')

            self.xmlWriter = None
        else:
            self.progressBar.setText(u'Нечего выгружать')

        self.btnClose.setText(u'Закрыть')


    @pyqtSignature('')
    def on_btnOpenFilePath_clicked(self):
        fileName = QtGui.QFileDialog.getSaveFileName(
            self, u'Укажите каталог и название файла', self.edtFileName.text(), u'Файлы XML (*.xml)')
        if fileName:
            self.edtFileName.setText(QDir.toNativeSeparators(fileName))


    @pyqtSignature('')
    def on_btnStart_clicked(self):
        if not forceStringEx(self.edtFileName.text()):
            QtGui.QMessageBox.critical(self,
                                   u'Внимание!',
                                   u'Укажите каталог и название файла!',
                                   QtGui.QMessageBox.Close)
            return

        params = {}
        params['dateFrom'] = self.edtBegDate.date()
        params['dateTo']   = self.edtEndDate.date()
        params['isPolicy'] = self.chkInsurer.isChecked()

        if params['isPolicy']:
            params['insurerId'] = self.cmbInsurer.value()
            policyType = self.cmbPolicyType.currentIndex()

            if policyType:
                params['policyType'] = self.cmbPolicyType.currentText()
            else:
                params['policyType'] = None

        if self.chkSpeciality.isChecked():
            params['specialityId'] = self.cmbSpeciality.value()

        if self.chkDoctor.isChecked():
            params['doctorPersonId'] = self.cmbDoctor.value()

        if self.chkAge.isChecked():
            params['ageBegin'] = self.edtBegAge.value()
            params['ageEnd'] = self.edtEndAge.value()

        if self.chkSex.isChecked():
            params['sex'] = self.cmbSex.currentIndex()

        params['purposeId'] = self.cmbEventPurpose.value()
        params['eventTypeId'] = self.cmbEventType.value()
        params['eventProfileId'] = self.cmbEventProfile.value()
        params['mesId'] = self.cmbMes.value()
        params['makeRar'] = self.chkMakeRar.isChecked()

        self.btnClose.setText(u'Прервать')
        self.progressBar.setText(u'Запрос в БД...')
        QtGui.qApp.processEvents()
        QtGui.qApp.setWaitCursor()
        query = self.createQuery(params)
        QtGui.qApp.restoreOverrideCursor()
        QtGui.qApp.processEvents()
        self.process(query, params)
        self.btnClose.setText(u'Закрыть')


    @pyqtSignature('int')
    def on_cmbSpeciality_currentIndexChanged(self, index):
        specialityId = self.cmbSpeciality.value()
        self.cmbDoctor.setSpecialityId(specialityId)


    @pyqtSignature('')
    def on_btnClose_clicked(self):
        if self.xmlWriter:
            self.xmlWriter.abort()
            self.btnClose.setText(u'Закрыть')
        else:
            self.close()


    @pyqtSignature('int')
    def on_cmbEventProfile_currentIndexChanged(self, index):
        self.cmbMes.setEventProfile(self.cmbEventProfile.value())
