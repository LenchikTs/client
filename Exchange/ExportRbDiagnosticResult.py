#!/usr/bin/env python
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
u"""Экспорт справочника 'Результаты Осмотра' в XML"""

from library.crbcombobox import CRBComboBox
from library.TableModel import CTextCol, CRefBookCol

from library.Utils import forceString
from Exchange.ExportRb import (CExportAbstractRbWizard, CExportAbstractRbPage1,
    CExportAbstractRbPage2, CRbXmlStreamWriter)

from Exchange.Ui_ExportRbDiagnosticResult_Wizard_1 import (
    Ui_ExportRbDiagnosticResult_Wizard_1)

# ******************************************************************************

def ExportRbDiagnosticResult(parent):
    u"""Формирует мастер выгрузки справочника 'Результаты Осмотра'"""
    dlg = CExportRbDiagnosticResult(parent)
    dlg.exec_()

rbDiagnosticResultFields = ('code', 'name', 'continued', 'regionalCode',
    'federalCode')

# ******************************************************************************

class CMyXmlStreamWriter(CRbXmlStreamWriter):
    u"""Класс для записи элементов справочника 'Результаты Осмотра' в XML"""
    def __init__(self, parent, idList):
        CRbXmlStreamWriter.__init__(self, parent, idList)


    def createQuery(self, idList):
        stmt = """SELECT %s,
                    E.code AS `purposeCode`,
                    rbResult.code AS `resultCode`,
                    RP.code AS `resultPurposeCode`
        FROM rbDiagnosticResult r
        LEFT JOIN rbEventTypePurpose E ON r.eventPurpose_id = E.id
        LEFT JOIN rbResult ON r.result_id = rbResult.id
        LEFT JOIN rbEventTypePurpose RP ON rbResult.eventPurpose_id = RP.id
        """ % ', '.join(['r.%s' % i for i in rbDiagnosticResultFields])

        if idList:
            stmt += 'WHERE r.id in ('+', '.join([str(et) for et in idList])+ ')'

        query = self._db.query(stmt)
        return query


    def writeRecord(self, record):
        self.writeStartElement('DiagnosticResult')

        # все свойства действия экспортируем как атрибуты
        for i in rbDiagnosticResultFields:
            self.writeAttribute(i, forceString(record.value(i)))

        # все, что определяется ссылками на другие таблицы - как элементы

        # Услуга (профиль ЕИС) экспортируемого элемента:
        if forceString(record.value('purposeCode')) != '':
            self.writeStartElement('EventTypePurpose')
            self.writeAttribute('code',
                                forceString(record.value('purposeCode')))
            self.writeEndElement()

        if forceString(record.value('resultCode')) != '':
            self.writeStartElement('Result')
            self.writeAttribute('code', forceString(record.value('resultCode')))
            self.writeAttribute('purposeCode',
                                forceString(record.value('resultPurposeCode')))
            self.writeEndElement()

        self.writeEndElement()

    def writeHeader(self):
        self.writeDTD('<!DOCTYPE xRbDiagnosticResult>')
        self.writeStartElement('RbDiagnosticResultExport')
        self.writeAttribute('version', '1.0')

# ******************************************************************************

class CExportRbDiagnosticResultWizardPage1(CExportAbstractRbPage1,
   Ui_ExportRbDiagnosticResult_Wizard_1):
    u"""Первая страница мастера экспорта справочника 'Результаты Осмотра'"""
    def __init__(self, parent):
        CExportAbstractRbPage1.__init__(self, 'rbDiagnosticResult', parent)

        self.cols = [
            CRefBookCol(u'Назначение', ['eventPurpose_id'],
                'rbEventTypePurpose', 50, CRBComboBox.showCodeAndName),
            CTextCol(u'Код', ['code'], 20),
            CTextCol(u'Наименование', ['name'], 30)
            ]
        self.order = ['eventPurpose_id', 'code', 'name', 'id']

        self.preSetupUi()
        self.setupUi(self)
        self.postSetupUi()

# ******************************************************************************

class CExportRbDiagnosticResult(CExportAbstractRbWizard):
    u"""Мастера экспорта справочника 'Результаты Осмотра'"""
    def __init__(self, parent=None):
        CExportAbstractRbWizard.__init__(self, 'rbDiagnosticResult',
            u'Результаты Осмотра', parent)
        self.page1 = CExportRbDiagnosticResultWizardPage1(self)
        self.page2 = CExportAbstractRbPage2(CMyXmlStreamWriter, self)
        self.addPage(self.page1)
        self.addPage(self.page2)
