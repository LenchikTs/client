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
from PyQt4.QtCore import QVariant

from library.Utils import forceDouble, forceInt, forceRef, forceString

from Reports.ReportBase import CReportBase, createTable
from Reports.ReportView import CReportViewDialog
from library.MES.Model import parseModel


def showMesDescription(widget, mesId):
    view = CReportViewDialog(widget)
    view.setWindowTitle(u'МЭС')
    view.setText(getMesDescription(mesId))
    view.showMaximized()
    view.exec_()


def getMesDescription(mesId):
    doc = QtGui.QTextDocument()
    cursor = QtGui.QTextCursor(doc)

#    cursor.setCharFormat(format)

#    cursor.insertText(forceString(mesRecord.value('code')))
#    cursor.insertBlock()
#    cursor.insertText(forceString(mesRecord.value('name')))
#    cursor.insertBlock()
#    cursor.setCharFormat(QtGui.QTextCharFormat())

    insertMainSection(cursor, mesId)
    cursor.insertBlock()
    cursor.insertBlock()

    insertMKBSection(cursor, mesId)
    cursor.insertBlock()
    cursor.insertBlock()

    insertMKBExSection(cursor, mesId)
    cursor.insertBlock()
    cursor.insertBlock()

    insertPersonServicesSection(cursor, mesId)
    insertServiceSection(cursor, mesId, u'Услуги лечащего врача', u'в')
    insertServiceSection(cursor, mesId, u'Лабораторные диагностические услуги', u'к')
    insertServiceSection(cursor, mesId, u'Инструментальные диагностические услуги', u'д')
    insertServiceSection(cursor, mesId, u'Немедикаментозная терапия', u'л')
    insertServiceSection(cursor, mesId, u'Вспомогательные услуги', u'с')
    insertServiceSection(cursor, mesId, u'Услуги по экспертизе', u'э')
    insertServiceSection(cursor, mesId, u'Несгруппированные услуги', '55')
    insertServiceSection(cursor, mesId, u'Прочие услуги', None)
    insertMedicamentsSection(cursor, mesId)
    return doc



def insertMainSection(cursor, mesId):
    db = QtGui.qApp.db
    mesRecord = db.getRecord('mes.MES', '*', mesId)
    bigChars = QtGui.QTextCharFormat()
    bigChars.setProperty(QtGui.QTextFormat.FontSizeIncrement, QVariant(2))
    bigChars.setFontWeight(QtGui.QFont.Bold)
    boldChars = QtGui.QTextCharFormat()
    boldChars.setFontWeight(QtGui.QFont.Bold)

    columns = [
            ('30%',[], CReportBase.AlignLeft),
            ('60%',[], CReportBase.AlignLeft),
            ]

    table = createTable(cursor, columns, headerRowCount=0, border=0, cellPadding=2, cellSpacing=0)
    i = table.addRow()
    table.setText(i, 0, forceString(mesRecord.value('code')), charFormat=bigChars)
    table.setText(i, 1, forceString(mesRecord.value('name')), charFormat=bigChars)
    i = table.addRow()
    table.setText(i, 0, u'Описание')
    table.setText(i, 1, forceString(mesRecord.value('descr')))
    i = table.addRow()
    table.setText(i, 0, u'Минимальная длительность')
    table.setText(i, 1, forceInt(mesRecord.value('minDuration')))
    i = table.addRow()
    table.setText(i, 0, u'Максимальная длительность')
    table.setText(i, 1, forceInt(mesRecord.value('maxDuration')))
    i = table.addRow()
    table.setText(i, 0, u'Средняя длительность')
    table.setText(i, 1, forceDouble(mesRecord.value('avgDuration')))
    i = table.addRow()
    table.setText(i, 0, u'Норматив визитов')
    table.setText(i, 1, forceInt(mesRecord.value('KSGNorm')))
    i = table.addRow()
    i = table.addRow()
    table.setText(i, 0, u'Модель пациента')
    table.setText(i, 1, forceString(mesRecord.value('patientModel')), charFormat=boldChars)
    for title, value in parseModel(forceString(mesRecord.value('patientModel'))):
        i = table.addRow()
        table.setText(i, 0, title)
        table.setText(i, 1, value)
    cursor.movePosition(QtGui.QTextCursor.End)


def insertMKBSection(cursor, mesId):
    db = QtGui.qApp.db
    cursor.insertText(u'Заболевания, входящие в МЭС (в формулировках МКБ)')
    cursor.insertBlock()
    charFormat = QtGui.QTextCharFormat()
    cursor.setCharFormat(charFormat)

    tableColumns = [
            ('5%',[u'№' ], CReportBase.AlignRight),
            ('10%',[u'Код диагноза по МКБ' ], CReportBase.AlignLeft),
            ('75%',[u'Диагноз' ],             CReportBase.AlignLeft),
            ]

    table = createTable(cursor, tableColumns)
    tableMKB = db.table('mes.MES_mkb')
    for record in db.getRecordList(tableMKB, 'mkb', tableMKB['master_id'].eq(mesId), 'mkb'):
        i = table.addRow()
        table.setText(i, 0, i)
        mkb = record.value('mkb')
        table.setText(i, 1, forceString(mkb))
        table.setText(i, 2, forceString(db.translate('MKB', 'DiagID', mkb, 'DiagName')))

    cursor.movePosition(QtGui.QTextCursor.End)


def insertMKBExSection(cursor, mesId):
    db = QtGui.qApp.db
    cursor.insertText(u'Заболевания, входящие в МЭС (в формулировках доп.МКБ)')
    cursor.insertBlock()
    charFormat = QtGui.QTextCharFormat()
    cursor.setCharFormat(charFormat)

    tableColumns = [
            ('5%',[u'№' ], CReportBase.AlignRight),
            ('10%',[u'Код диагноза по доп.МКБ' ], CReportBase.AlignLeft),
            ('75%',[u'Диагноз' ],             CReportBase.AlignLeft),
            ]

    table = createTable(cursor, tableColumns)
    tableMKB = db.table('mes.MES_mkb')
    for record in db.getRecordList(tableMKB, 'mkbEx', tableMKB['master_id'].eq(mesId), 'mkbEx'):
        i = table.addRow()
        table.setText(i, 0, i)
        mkbEx = record.value('mkbEx')
        table.setText(i, 1, forceString(mkbEx))
        table.setText(i, 2, forceString(db.translate('MKB', 'DiagID', mkbEx, 'DiagName')))

    cursor.movePosition(QtGui.QTextCursor.End)


def insertPersonServicesSection(cursor, mesId):
    db = QtGui.qApp.db
    cursor.insertText(u'Услуги лечащего и консультирующего врача (ВИЗИТЫ)')
    cursor.insertBlock()

    tableColumns = [
            ('5%', [u'№ группы'],      CReportBase.AlignRight),
            ('5%', [u'Количество'],    CReportBase.AlignRight),
            ('10%',[u'Тип визита'],    CReportBase.AlignLeft),
            ('20%',[u'Специальность'], CReportBase.AlignLeft),
            ('15%',[u'Код услуги'],    CReportBase.AlignLeft),
            ('30%',[u'Название'],      CReportBase.AlignLeft),
            ('5%', [u'Доп.код'],       CReportBase.AlignLeft),
            ]

    table = createTable(cursor, tableColumns)
    tableVisit = db.table('mes.MES_visit')
    tableVisitType  = db.table('mes.mrbVisitType')
    tableSpeciality = db.table('mes.mrbSpeciality')
    tableService = db.table('mes.mrbService')
    tableQuery = tableVisit.leftJoin(tableVisitType,  tableVisitType['id'].eq(tableVisit['visitType_id']))
    tableQuery = tableQuery.leftJoin(tableSpeciality, tableSpeciality['id'].eq(tableVisit['speciality_id']))
    tableQuery = tableQuery.leftJoin(tableService,    tableService['code'].eq(tableVisit['serviceCode']))
    cols = [tableVisit['groupCode'],
            tableVisit['averageQnt'],
            tableVisitType['name'],
            tableSpeciality['name'],
            tableVisit['serviceCode'],
            tableService['name'],
            tableVisit['additionalServiceCode']
           ]
    prevGroupCode = False
    for record in db.getRecordList(tableQuery, cols, tableVisit['master_id'].eq(mesId), 'groupCode, '+tableSpeciality['name'].name()):
        i = table.addRow()
        groupCode  = forceString(record.value(0))
        averageQnt = forceInt(record.value(1))
        visitType  = forceString(record.value(2))
        speciality = forceString(record.value(3))
        serviceCode = forceString(record.value(4))
        serviceName = forceString(record.value(5))
        additionalServiceCode = forceString(record.value(6))

        if prevGroupCode != groupCode:
            table.setText(i, 0, groupCode)
            prevGroupCode = groupCode
        table.setText(i, 1, averageQnt)
        table.setText(i, 2, visitType)
        table.setText(i, 3, speciality)
        table.setText(i, 4, serviceCode)
        table.setText(i, 5, serviceName)
        table.setText(i, 6, additionalServiceCode)


def insertServiceSection(cursor, mesId, title, code):
    cursor.movePosition(QtGui.QTextCursor.End)
    cursor.insertBlock()
    cursor.insertBlock()
    groupId = forceRef(QtGui.qApp.db.translate('mes.mrbServiceGroup', 'code', code, 'id'))
    columns = [
                ('5%',[u'№'],      CReportBase.AlignRight),
                ('20%',[u'Код'],   CReportBase.AlignLeft),
                ('40%',[title],    CReportBase.AlignLeft),
                ('5%',[u'Группа'], CReportBase.AlignLeft),
                ('5%',[u'CK'],    CReportBase.AlignRight),
                ('5%',[u'Чп'],    CReportBase.AlignRight),
                ('5%',[u'УЕТвр'], CReportBase.AlignRight),
                ('5%',[u'УЕТср'], CReportBase.AlignRight),
                ]
    table = createTable(cursor, columns)
    stmt = '''
            SELECT mrbService.code, mrbService.name, MES_service.averageQnt, MES_service.necessity, mrbService.doctorWTU, mrbService.paramedicalWTU, MES_service.groupCode AS groupAlternative
            FROM mes.mrbService
            LEFT JOIN mes.MES_service ON MES_service.service_id = mrbService.id
            WHERE MES_service.master_id=%d AND mrbService.group_id = %d AND MES_service.deleted = 0 AND mrbService.deleted = 0
            GROUP BY mrbService.code
            ORDER BY groupAlternative, mrbService.code, mrbService.name, mrbService.id
            ''' % (mesId, groupId if groupId else 55)
    query = QtGui.qApp.db.query(stmt)
    while query.next():
        record = query.record()
        code  = forceString(record.value('code'))
        name  = forceString(record.value('name'))
        averageQnt = forceInt(record.value('averageQnt'))
        necessity = forceDouble(record.value('necessity'))
        doctorWTU = forceDouble(record.value('doctorWTU'))
        paramedicalWTU = forceDouble(record.value('paramedicalWTU'))
        groupAlternativeNew = forceString(record.value('groupAlternative'))
        i = table.addRow()
        table.setText(i, 0, i)
        table.setText(i, 1, code)
        table.setText(i, 2, name)
        table.setText(i, 3, groupAlternativeNew)
        table.setText(i, 4, averageQnt)
        table.setText(i, 5, '%.2f'%(round(necessity, 2)))
        table.setText(i, 6, '%.2f'%(round(doctorWTU, 2)))
        table.setText(i, 7, '%.2f'%(round(paramedicalWTU, 2)))


def insertMedicamentsSection(cursor, mesId):
    cursor.movePosition(QtGui.QTextCursor.End)
    cursor.insertBlock()
    cursor.insertBlock()
    cursor.insertText(u'Лекарственные средства (МНН) в официнальной дозировке')
    cursor.insertBlock()
    columns = [
            ('5%',[u'№'],             CReportBase.AlignRight),
            ('10%',[u'Код'],          CReportBase.AlignLeft),
            ('65%',[u'Наименование'], CReportBase.AlignLeft),
            ('5%',[u'СЧЕ'],           CReportBase.AlignRight),
            ('5%',[u'Чн'],            CReportBase.AlignRight),
            ]
    table = createTable(cursor, columns)
    stmt = '''
        SELECT MES_medicament.medicamentCode as code, MES_medicament.dosage, MES_medicament.averageQnt, MES_medicament.necessity,
               mrbMedicamentDosageForm.name AS formName,
               mrbMedicament.name AS name, mrbMedicament.form AS medicamentForm, mrbMedicament.dosage AS medicamentDosage,
               G1.name AS groupName,
               G2.name AS subgroupName
        FROM mes.MES_medicament
        LEFT JOIN mes.mrbMedicamentDosageForm ON mrbMedicamentDosageForm.id = MES_medicament.dosageForm_id
        LEFT JOIN mes.mrbMedicament ON mrbMedicament.code = MES_medicament.medicamentCode
        LEFT JOIN mes.mrbMedicamentGroup AS G1 ON G1.code = SUBSTRING_INDEX(MES_medicament.medicamentCode, '.', 1)
        LEFT JOIN mes.mrbMedicamentGroup AS G2 ON G2.code = SUBSTRING_INDEX(MES_medicament.medicamentCode, '.', 2)
        WHERE MES_medicament.master_id=%d
        ORDER BY MES_medicament.medicamentCode, mrbMedicament.name
        ''' % mesId
    query = QtGui.qApp.db.query(stmt)
    row = 0
    while query.next():
        row += 1
        record = query.record()
        groupName = forceString(record.value('groupName'))
        subgroupName = forceString(record.value('subgroupName'))
        code  = forceString(record.value('code'))
        name  = forceString(record.value('name'))
        averageQnt = forceInt(record.value('averageQnt'))
        necessity = forceDouble(record.value('necessity'))
        i = table.addRow()
        table.setText(i, 0, row)
        table.setText(i, 1, u'Группа')
        table.setText(i, 2, groupName)
        i = table.addRow()
        table.setText(i, 1, u'Подгруппа')
        table.setText(i, 2, subgroupName)
        i = table.addRow()
        table.setText(i, 1, code)
        table.setText(i, 2, name)
        table.setText(i, 3, averageQnt)
        table.setText(i, 4, necessity)
        table.mergeCells(i-2, 0, 3, 1)
        table.mergeCells(i-2, 2, 1, 3)
        table.mergeCells(i-1, 2, 1, 3)
