# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################


from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, QDate, QLocale, QVariant

from library.Utils      import forceDate, forceDouble, forceRef, forceString, formatName, getMKB

from Orgs.Utils         import getOrgStructureDescendants
from Reports.ReportBase import CReportBase, createTable
from Reports.Report     import CReport
from library.DialogBase import CDialogBase

from Reports.Ui_SpendingToClients import Ui_SpendingToClientsSetup


class CSpendingToClients(CReport):
    def __init__(self, parent = None):
        CReport.__init__(self, parent)
        self.setTitle(u'Реестр списания ЛСиИМН на пациентов')


    def getSetupDialog(self, parent):
        result = CSpendingToClientsSetup(parent)
        return result


    def selectData(self, params):
        begDate = params.get('begDate')
        endDate = params.get('endDate')
        orgStructureId = params.get('orgStructureId')
        classId = params.get('classId')
        kindId = params.get('kindId')
        typeId = params.get('typeId')
        nomenclatureId = params.get('nomenclatureId')
        reason = params.get('reason')
        reasonDate = params.get('reasonDate')
        financeId = params.get('financeId')
        clientId = params.get('clientId')

        db = QtGui.qApp.db
        tableStockMotion = db.table('StockMotion')
        tableStockMotionItem = db.table('StockMotion_Item')
        tableNomenclature = db.table('rbNomenclature')
        tableClass = db.table('rbNomenclatureClass')
        tableKind  = db.table('rbNomenclatureKind')
        tableType  = db.table('rbNomenclatureType')
        tableClient= db.table('Client')
        tableActionMotion = db.table('vActionWithMotionAndDirection')
        tableAction = db.table('Action')
        tablePerson = db.table('Person')
        tableEvent = db.table('Event')
        tableSpeciality = db.table('rbSpeciality')

        table = tableStockMotionItem.innerJoin(tableStockMotion,  tableStockMotion['id'].eq(tableStockMotionItem['master_id']))
        table = table.innerJoin(tableNomenclature, tableNomenclature['id'].eq(tableStockMotionItem['nomenclature_id']))
        table = table.innerJoin(tableType, tableType['id'].eq(tableNomenclature['type_id']))
        table = table.innerJoin(tableKind, tableKind['id'].eq(tableType['kind_id']))
        table = table.innerJoin(tableClass,tableClass['id'].eq(tableKind['class_id']))
        table = table.innerJoin(tableClient, tableClient['id'].eq(tableStockMotion['client_id']))
        table = table.leftJoin(tableActionMotion, tableActionMotion['stockMotion_id'].eq(tableStockMotion['id']))
        table = table.leftJoin(tableAction, tableActionMotion['id'].eq(tableAction['id']))
        table = table.leftJoin(tablePerson, db.joinAnd([ tableAction['setPerson_id'].eq(tablePerson['id']), tablePerson['deleted'].eq(0) ]))
        table = table.leftJoin(tableEvent, db.joinAnd([ tableAction['event_id'].eq(tableEvent['id']), tableEvent['deleted'].eq(0) ]))
        table = table.leftJoin(tableSpeciality, tablePerson['speciality_id'].eq(tableSpeciality['id']))

        cond = [ tableStockMotion['deleted'].eq(0),
                 tableStockMotion['type'].eq(4), # списание на пациента
               ]
        if begDate:
            cond.append( tableStockMotion['date'].ge(begDate))
        if endDate:
            cond.append( tableStockMotion['date'].lt(endDate.addDays(1)))
        if orgStructureId:
            cond.append( tableStockMotion['supplier_id'].inlist(getOrgStructureDescendants(orgStructureId)))
        if nomenclatureId:
            cond.append(tableNomenclature['id'].eq(nomenclatureId))
        else:
            if classId:
                cond.append(tableClass['id'].eq(classId))
            if kindId:
                cond.append(tableKind['id'].eq(kindId))
            if typeId:
                cond.append(tableType['id'].eq(typeId))
        if reason:
            cond.append(tableStockMotion['reason'].like(reason))
        if reasonDate:
            cond.append(tableStockMotion['reasonDate'].eq(reasonDate))
        if financeId:
            cond.append(tableStockMotionItem['finance_id'].eq(financeId))
        if clientId:
            cond.append(tableStockMotion['client_id'].eq(clientId))

        fields =[ tableStockMotion['client_id'],
                  tableClient['lastName'],
                  tableClient['firstName'],
                  tableClient['patrName'],
                  tableActionMotion['direction'],
                  tableActionMotion['directionDate'],
                  tableStockMotion['date'],
                  tableStockMotion['number'],
                  tableNomenclature['name'],
                  tableNomenclature['code'],
                  tableStockMotionItem['qnt'],
                  tableStockMotionItem['sum'],
                  tableStockMotionItem['finance_id'],
                  tableStockMotionItem['batch'],
                  tableStockMotion['reason'],
                  tableStockMotion['reasonDate'],
                  tableStockMotion['supplier_id'],
                  tableClass['name'].alias('className'),
                  tableKind['name'].alias('kindName'),
                  tableType['name'].alias('typeName'),
                  tablePerson['lastName'].alias('personLastName'),
                  tablePerson['firstName'].alias('personFirstName'),
                  tablePerson['patrName'].alias('personPatrName'),
                  tableSpeciality['name'].alias('personSpeciality'),
                  getMKB(),
                ]
        order = [ tableStockMotion['reason'].name(),
                  tableStockMotion['reasonDate'].name(),
                  tableClass['name'].name(),
                  tableKind['name'].name(),
                  tableType['name'].name(),
                  tableStockMotion['date'].name(),
                  tableStockMotion['number'].name()
                ]
        stmt = db.selectStmt(table, fields, cond, order)
        return db.query(stmt)


    def build(self, params):
        locale = QLocale()
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
#        cursor.insertText(self.title())
        cursor.insertBlock()
#        self.dumpParams(cursor, params)
#        cursor.insertBlock()
#        cursor.insertText(u'(3000)')
#        cursor.insertBlock()

        title = u'Реестр списания ЛСиИМН на пациентов за период с %s по %s' % (
                    forceString(params.get('begDate')),
                    forceString(params.get('endDate')),
                )
        cursor.insertText(title)
        cursor.insertBlock()

        tableColumns = [
            ('5%', [u'№'], CReportBase.AlignRight),
            ('10%',[u'ФИО'], CReportBase.AlignLeft),
            ('5%', [u'Код пациента'], CReportBase.AlignLeft),
            ('5%', [u'Код МКБ'], CReportBase.AlignLeft),
            ('5%', [u'ФИО назначившего'], CReportBase.AlignLeft),
            ('5%', [u'Должность назначившего'], CReportBase.AlignLeft),
            ('5%', [u'№ Направления'], CReportBase.AlignLeft),
            ('5%', [u'Дата\nнаправления'], CReportBase.AlignLeft),
            ('5%', [u'Дата\nназначения'], CReportBase.AlignLeft),
            ('5%', [u'Дата\nвыдачи'], CReportBase.AlignLeft),
            ('5%', [u'Подразделение'], CReportBase.AlignLeft),
            ('5%', [u'№ документа'], CReportBase.AlignLeft),
            ('5%', [u'Серия'], CReportBase.AlignLeft),
            ('5%', [u'Название'], CReportBase.AlignLeft),
            ('5%', [u'Шифр'], CReportBase.AlignLeft),
            ('5%', [u'Коли-\nчество'], CReportBase.AlignRight),
            ('5%', [u'Тип финансирования'], CReportBase.AlignRight),
            ('5%', [u'Цена'], CReportBase.AlignRight),
            ('5%', [u'Сумма'], CReportBase.AlignRight),
            ]

        query = self.selectData(params)
        prevReason = prevReasonDate = table = idx = None
        while query.next():
            record = query.record()
            reason = forceString(record.value('reason'))
            reasonDate = forceString(record.value('reasonDate'))
            if prevReason != reason or prevReasonDate != reasonDate:
                subtitle = u'По основанию № %s от %s' % (reason, forceString(reasonDate))
                cursor.movePosition(QtGui.QTextCursor.End)
                if table is not None:
                    cursor.insertBlock()
                    cursor.insertBlock()
                cursor.setCharFormat(CReportBase.ReportSubTitle)
                cursor.insertText(subtitle)
                cursor.insertBlock()

                prevReason = reason
                prevReasonDate = reasonDate
                table = None

            if table is None:
                table = createTable(cursor, tableColumns)
                idx = 0

            idx += 1
            clientName = formatName(record.value('lastName'),
                                    record.value('firstName'),
                                    record.value('patrName'))
            clientId = forceRef(record.value('client_id'))
            personName = formatName(record.value('personLastName'),
                                    record.value('personFirstName'),
                                    record.value('personPatrName'))
            personSpeciality = forceString(record.value('personSpeciality'))
            MKB = forceString(record.value('MKB'))
            direction = forceString(record.value('direction'))
            directionDate = forceString(forceDate(record.value('directionDate')))
            financeId = forceRef(record.value('finance_id'))
            supplierId = forceRef(record.value('supplier_id'))
            date = forceString(forceDate(record.value('date')))
            batch = forceString(record.value('batch'))
            number = forceString(record.value('number'))
            name = forceString(record.value('name'))
            code = forceString(record.value('code'))
            qnt  = forceDouble(record.value('qnt'))
            sum  = forceDouble(record.value('sum'))
            price = sum/qnt if abs(qnt) >0.001 else None

            i = table.addRow()
            table.setText(i, 0, idx)
            table.setText(i, 1, clientName)
            table.setText(i, 2, clientId)
            table.setText(i, 3, MKB)
            table.setText(i, 4, personName)
            table.setText(i, 5, personSpeciality)
            table.setText(i, 6, direction)
            table.setText(i, 7, directionDate)
            table.setText(i, 8, directionDate)
            table.setText(i, 9, date)
            table.setText(i,10, forceString(QtGui.qApp.db.translate('OrgStructure', 'id', supplierId, 'name')))
            table.setText(i,11, number)
            table.setText(i,12, batch)
            table.setText(i,13, name)
            table.setText(i,14, code)
            table.setText(i,15, locale.toString(int(qnt)) if int(qnt) == qnt else locale.toString(qnt, 'f', 3) )
            table.setText(i,16, forceString(QtGui.qApp.db.translate('rbFinance', 'id', financeId, 'name')))
            table.setText(i,17, locale.toString(price, 'f', 2) if price is not None else '-')
            table.setText(i,18, locale.toString(sum, 'f', 2))
        return doc


class CSpendingToClientsSetup(CDialogBase, Ui_SpendingToClientsSetup):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.cmbClass.setTable('rbNomenclatureClass', True)
        self.cmbKind.setTable('rbNomenclatureKind', True)
        self.cmbType.setTable('rbNomenclatureType', True)
        self.edtReasonDate.canBeEmpty()
        self.cmbFinance.setTable('rbFinance', True)


    def setParams(self, params):
        currentDate = QDate.currentDate()
        self.edtBegDate.setDate(params.get('begDate', currentDate))
        self.edtEndDate.setDate(params.get('endDate', currentDate))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', QtGui.qApp.currentOrgId()))
        self.cmbClass.setValue(params.get('classId', None))
        self.cmbKind.setValue(params.get('kindId', None))
        self.cmbType.setValue(params.get('typeId', None))
        self.cmbNomenclature.setValue(params.get('nomenclatureId', None))
        self.edtReason.setText(params.get('reason', ''))
        self.edtReasonDate.setDate(params.get('reasonDate', QDate()))
        self.cmbFinance.setValue(params.get('financeId', None))
        self.chkAdjustRefund.setChecked(bool(params.get('adjustRefund', True)))
        self.edtClientId.setText(str(params.get('clientId') or ''))


    def params(self):
        return dict(begDate             = self.edtBegDate.date(),
                    endDate             = self.edtEndDate.date(),
                    orgStructureId      = self.cmbOrgStructure.value(),
                    classId             = self.cmbClass.value(),
                    kindId              = self.cmbKind.value(),
                    typeId              = self.cmbType.value(),
                    nomenclatureId      = self.cmbNomenclature.value(),
                    reason              = forceString(self.edtReason.text()),
                    reasonDate          = self.edtReasonDate.date(),
                    financeId           = self.cmbFinance.value(),
                    adjustRefund        = self.chkAdjustRefund.isChecked(),
                    clientId            = forceRef(QVariant(self.edtClientId.text()))
                   )


    @pyqtSignature('int')
    def on_cmbClass_currentIndexChanged(self, index):
        classId = self.cmbClass.value()
        if classId:
            self.cmbKind.setFilter('class_id=%d'%classId)
        else:
            self.cmbKind.setFilter('')
        self.cmbNomenclature.setDefaultClassId(classId)


    @pyqtSignature('int')
    def on_cmbKind_currentIndexChanged(self, index):
        kindId = self.cmbKind.value()
        if kindId:
            self.cmbType.setFilter('kind_id=%d'%kindId) #'rbNomenclatureType'
        else:
            self.cmbType.setFilter('')
        self.cmbNomenclature.setDefaultKindId(kindId)


    @pyqtSignature('int')
    def on_cmbType_currentIndexChanged(self, index):
        typeId = self.cmbType.value()
        self.cmbNomenclature.setDefaultTypeId(typeId)
