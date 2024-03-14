# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import QDate

from library.DialogBase import CDialogBase
from library.TreeModel  import CDBTreeModel
from library.Utils      import forceDate, forceRef, forceString, formatDate, formatSex, formatSNILS

from Registry.Utils     import getClientInfo, getClientPhonesEx

from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.StatReport1NPUtil import havePermanentAttach

from Reports.Ui_SocStatusSetup import Ui_SocStatusSetupDialog


def selectData(begDate, endDate, statusInPeriod, statusStart, statusFinish, sex, ageFrom, ageTo, groupId, onlyPermanentAttach, groupBySocStatus, grbOrgStructure = False, orgStructureIdList = None, areaAddressType = None):
    stmt="""
SELECT
    Client.id as client_id,
    ClientSocStatus.begDate, ClientSocStatus.endDate, ClientSocStatus.document_id, ClientSocStatus.socStatusType_id,
    rbSocStatusType.name as socStatusTypeName, rbSocStatusClass.name as socStatusClassName
FROM
    Client
    join ClientSocStatus on ClientSocStatus.client_id=Client.id
    left join rbSocStatusType on rbSocStatusType.id=ClientSocStatus.socStatusType_id
    left join rbSocStatusClassTypeAssoc on rbSocStatusClassTypeAssoc.type_id=rbSocStatusType.id
    left join rbSocStatusClass on rbSocStatusClass.id=rbSocStatusClassTypeAssoc.class_id
WHERE Client.deleted=0 AND ClientSocStatus.deleted=0 AND %s
ORDER BY %s Client.lastName, Client.firstName, Client.patrName
    """
    db = QtGui.qApp.db
    tableClient = db.table('Client')
    tableClientSocStatus = db.table('ClientSocStatus')
    tableSocStatusClass = db.table('rbSocStatusClass')
    tableOrgStructureAddress = db.table('OrgStructure_Address')
    tableClientAddress = db.table('ClientAddress')
    tableAddress = db.table('Address')
    cond = []

    if grbOrgStructure and orgStructureIdList:
        houseIdList = db.getDistinctIdList(tableOrgStructureAddress, tableOrgStructureAddress['house_id'], [tableOrgStructureAddress['master_id'].inlist(orgStructureIdList)])
        clientIdList = []
        if houseIdList and areaAddressType is not None:
            clientIdList = db.getDistinctIdList(tableAddress.innerJoin(tableClientAddress, tableClientAddress['address_id'].eq(tableAddress['id'])), tableClientAddress['client_id'], [tableAddress['house_id'].inlist(houseIdList), tableAddress['deleted'].eq(0), tableClientAddress['type'].eq(areaAddressType)])
        if clientIdList:
            cond.append(tableClient['id'].inlist(clientIdList))

    if statusInPeriod:
        if begDate:
            cond.append('(ClientSocStatus.endDate is null or (%s))'%tableClientSocStatus['endDate'].ge(begDate))
        if endDate:
            cond.append('(ClientSocStatus.endDate is null or (%s))'%tableClientSocStatus['endDate'].le(endDate))
    if statusStart:
        if begDate:
            cond.append(tableClientSocStatus['begDate'].ge(begDate))
        if endDate:
            cond.append(tableClientSocStatus['begDate'].le(endDate))
    if statusFinish:
        if begDate:
            cond.append(tableClientSocStatus['endDate'].ge(begDate))
        if endDate:
            cond.append(tableClientSocStatus['endDate'].le(endDate))
    if sex:
        cond.append(tableClient['sex'].eq(sex))
    if ageFrom <= ageTo:
        if begDate:
            cond.append('(%s >= ADDDATE(Client.birthDate, INTERVAL %d YEAR))'%(db.formatDate(begDate), ageFrom))
        if endDate:
            cond.append('(%s < SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1))'%(db.formatDate(endDate), ageTo+1))
    if onlyPermanentAttach:
        cond.append(havePermanentAttach(endDate))
    if groupId:
        groupIdList=[groupId]
        groupIdList+=db.getIdList('rbSocStatusClass', where='group_id=%d'%groupId)
        cond.append(tableSocStatusClass['id'].inlist(groupIdList))
#        rbSocStatusTypeIdList=[]
#        for groupId in groupIdList:
#            rbSocStatusTypeIdList+=db.getIdList(
#                'rbSocStatusClassTypeAssoc', idCol='type_id', where='class_id=%d'%groupId)
#        cond.append(tableClientSocStatus['id'].inlist(rbSocStatusTypeIdList))
    if groupBySocStatus:
        order = 'rbSocStatusClass.name, rbSocStatusType.name, '
    else:
        order = ''
    return db.query(stmt % (db.joinAnd(cond), order))


def getMKB(clientId):
    strMKB = u''
    if clientId:
        db = QtGui.qApp.db
        tableDiagnosis = db.table('Diagnosis')
        dtidBase = forceRef(db.translate('rbDiagnosisType', 'code', '2', 'id'))
        dtidAcomp = forceRef(db.translate('rbDiagnosisType', 'code', '9', 'id'))
        cols = [tableDiagnosis['MKB'],
                tableDiagnosis['MKBEx']
                ]
        cond = [tableDiagnosis['client_id'].eq(clientId)]
        dtIdList = [dtidBase, dtidAcomp]
        cond.append(tableDiagnosis['diagnosisType_id'].inlist(dtIdList))
        cond.append(tableDiagnosis['mod_id'].isNull())
        records = db.getRecordList(tableDiagnosis, cols, cond, tableDiagnosis['endDate'].name()+' DESC')
        for record in records:
            MKB = forceString(record.value('MKB'))
            MKBEx = forceString(record.value('MKBEx'))
            if MKB or MKBEx:
                strMKB += ((MKB + u'+' + MKBEx) if MKBEx else MKB) + u'; '
    return strMKB


class CSocStatus(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Социальный статус')
        self.socStatusSetupDialog = None

    def getSetupDialog(self, parent):
        result = CSocStatusSetupDialog(parent)
        result.setTitle(self.title())
        self.socStatusSetupDialog = result
        return result


    def getOrgStructureIdList(self, treeIndex):
        treeItem = treeIndex.internalPointer() if treeIndex.isValid() else None
        return treeItem.getItemIdList() if treeItem else []


    def build(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        statusInPeriod = params.get('statusInPeriod', 0)
        statusStart = params.get('statusStart', 0)
        statusFinish = params.get('statusFinish', 0)
        sex = params.get('sex', 0)
        ageFrom = params.get('ageFrom', 0)
        ageTo = params.get('ageTo', 150)
        groupId = params.get('groupId', 0)
        onlyPermanentAttach = params.get('onlyPermanentAttach', False)
        addMKB = params.get('addMKB', False)
        groupBySocStatus = params.get('groupBySocStatus', True)
        areaAddressType = params.get('areaAddressType', 0)
        grbOrgStructure = params.get('grbOrgStructure', False)
        orgStructureIdList = []
        if grbOrgStructure:
            orgStructureIndex = self.socStatusSetupDialog.cmbOrgStructure._model.index(self.socStatusSetupDialog.cmbOrgStructure.currentIndex(), 0, self.socStatusSetupDialog.cmbOrgStructure.rootModelIndex()) #WTF?
            orgStructureIdList = self.getOrgStructureIdList(orgStructureIndex)

        db = QtGui.qApp.db

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Социальный статус')
        cursor.insertBlock()
        if groupId:
            statusType=forceString(db.translate('rbSocStatusClass', 'id', groupId, 'name '))
            cursor.insertText(u'тип социального статуса: %s\n' % statusType)
        self.dumpParams(cursor, params)
        if statusInPeriod:
            cursor.insertText(u'статус присутствует в периоде\n')
        if statusStart:
            cursor.insertText(u'статус начал действовать в периоде\n')
        if statusFinish:
            cursor.insertText(u'статус прекратил действовать в периоде\n')
        cursor.insertBlock()

        if groupBySocStatus:
            tableColumns = [
                ('2%', [u'№'],   CReportBase.AlignRight),
                ('10%',[u'ФИО'], CReportBase.AlignLeft),
                ('2%', [u'пол'], CReportBase.AlignLeft),
                ('8%', [u'д/р'], CReportBase.AlignLeft),
                ('8%', [u'СНИЛС'], CReportBase.AlignLeft),
                ('20%',[u'полис'], CReportBase.AlignLeft),
                ('10%',[u'документ'], CReportBase.AlignLeft),
                ('20%',[u'Адрес'], CReportBase.AlignLeft),
                ('10%',[u'телефон'], CReportBase.AlignLeft),
                ]
        else:
            tableColumns = [
                ('2%', [u'№'],   CReportBase.AlignRight),
                ('8%', [u'ФИО'], CReportBase.AlignLeft),
                ('1%', [u'пол'], CReportBase.AlignLeft),
                ('6%', [u'д/р'], CReportBase.AlignLeft),
                ('7%', [u'СНИЛС'], CReportBase.AlignLeft),
                ('20%',[u'полис'], CReportBase.AlignLeft),
                ('9%', [u'документ'], CReportBase.AlignLeft),
                ('20%',[u'Адрес'], CReportBase.AlignLeft),
                ('10%',[u'телефон'], CReportBase.AlignLeft),
                ('20%',[u'класс\nсоц.статуса'], CReportBase.AlignLeft),
                ('20%',[u'тип\nсоц.статуса'], CReportBase.AlignLeft),
                ]
        if addMKB:
            tableColumns.append(('10%',[u'Заболевания'], CReportBase.AlignLeft))

        table = createTable(cursor, tableColumns)
        n = 0
        query = selectData(begDate, endDate, statusInPeriod, statusStart, statusFinish, sex, ageFrom, ageTo, groupId, onlyPermanentAttach, groupBySocStatus, grbOrgStructure, orgStructureIdList, areaAddressType)
        prevSocStatusTypeId = False
        while query.next():
            n += 1
            record = query.record()
            clientId = forceRef(record.value('client_id'))
            begDate = forceDate(record.value('begDate'))
            endDate = forceDate(record.value('endDate'))
            info = getClientInfo(clientId)
            name = '\n'.join([info['lastName'], info['firstName'], info['patrName']])
            sex = formatSex(info['sexCode'])
            birthDate = formatDate(info['birthDate'])
            regAddress = info.get('regAddress', u'не указан')
            phones = getClientPhonesEx(clientId)
            SNILS=formatSNILS(info['SNILS'])
            policy=info.get('policy', u'нет')
            socStatusTypeId = forceRef(record.value('socStatusType_id'))
            socStatusClassName = forceString(record.value('socStatusClassName'))
            socStatusTypeName = forceString(record.value('socStatusTypeName'))
            document=info.get('document', u'нет')

            if groupBySocStatus:
                if socStatusTypeId != prevSocStatusTypeId:
                    i = table.addRow()
                    table.mergeCells(i, 0, 1, 9)
                    table.setText(i, 0, socStatusClassName+': '+socStatusTypeName, CReportBase.ReportSubTitle, CReportBase.AlignLeft)
                    prevSocStatusTypeId = socStatusTypeId
                    n = 1

            i = table.addRow()
            table.setText(i, 0, n)
            table.setText(i, 1, name)
            table.setText(i, 2, sex)
            table.setText(i, 3, birthDate)
            table.setText(i, 4, SNILS)
            table.setText(i, 5, policy)
            table.setText(i, 6, document)
            table.setText(i, 7, regAddress)
            table.setText(i, 8, phones)
            if not groupBySocStatus:
                table.setText(i, 9,  socStatusClassName)
                table.setText(i, 10, socStatusTypeName)
            if addMKB:
                strMKB = getMKB(clientId)
                table.setText(i, len(tableColumns) - 1, strMKB)
        return doc


class CSocStatusSetupDialog(CDialogBase, Ui_SocStatusSetupDialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.addModels('Tree', CDBTreeModel(self, 'rbSocStatusClass', 'id', 'group_id', 'name', ['code', 'name', 'id']))
        self.modelTree.setLeavesVisible(True)
        self.modelTree.setOrder('code')
        self.setupUi(self)
        self.setModels(self.treeItems,  self.modelTree,  self.selectionModelTree)
        self.treeItems.header().hide()
        self.setTitle(u'Социальный статус')
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())


    def currentGroupId(self):
        return self.modelTree.itemId(self.treeItems.currentIndex())


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.btnStatusInPeriod.setChecked(params.get('statusInPeriod', False))
        self.btnStatusStart.setChecked(params.get('statusStart', False))
        self.btnStatusFinish.setChecked(params.get('statusFinish', False))
        self.chkOnlyPermanentAttach.setChecked(params.get('onlyPermanentAttach', False))
        self.cmbSex.setCurrentIndex(params.get('sex', 0))
        self.edtAgeFrom.setValue(params.get('ageFrom', 0))
        self.edtAgeTo.setValue(params.get('ageTo', 999))
        self.chkAddMKB.setChecked(params.get('addMKB', False))
        self.chkGroupBySocStatus.setChecked(params.get('groupBySocStatus', True))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbAreaAddressType.setCurrentIndex(params.get('areaAddressType', 0))
        self.grbOrgStructure.setChecked(params.get('grbOrgStructure', False))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['statusInPeriod'] = self.btnStatusInPeriod.isChecked()
        result['statusStart'] = self.btnStatusStart.isChecked()
        result['statusFinish'] = self.btnStatusFinish.isChecked()
        result['onlyPermanentAttach'] = self.chkOnlyPermanentAttach.isChecked()
        result['sex'] = self.cmbSex.currentIndex()
        result['ageFrom'] = self.edtAgeFrom.value()
        result['ageTo'] = self.edtAgeTo.value()
        result['groupId'] = self.currentGroupId()
        result['addMKB'] = self.chkAddMKB.isChecked()
        result['groupBySocStatus'] = self.chkGroupBySocStatus.isChecked()
        grbOrgStructure = self.grbOrgStructure.isChecked()
        result['grbOrgStructure'] = grbOrgStructure
        if grbOrgStructure:
            result['orgStructureId'] = self.cmbOrgStructure.value()
            result['areaAddressType'] = self.cmbAreaAddressType.currentIndex()
        return result
