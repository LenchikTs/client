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
u"""Экспорт справочника 'Результаты События' в XML"""

from library.crbcombobox import CRBComboBox
from library.TableModel import CTextCol, CRefBookCol
from library.Utils import forceString

from Exchange.ExportRb import (CExportAbstractRbWizard, CExportAbstractRbPage1,
    CExportAbstractRbPage2, CRbXmlStreamWriter)

from Exchange.Ui_ExportRbResult_Wizard_1 import Ui_ExportRbResult_Wizard_1

# ******************************************************************************

rbResultFields = ('code', 'name', 'continued', 'regionalCode', 'federalCode')

def ExportRbResult(parent):
    u"""Формирует мастер выгрузки справочника 'Результаты События'"""
    dlg = CExportRbResult(parent)
    dlg.exec_()

# ******************************************************************************

class CMyXmlStreamWriter(CRbXmlStreamWriter):
    u"""Класс для записи элементов справочника 'Результаты События' в XML"""
    def __init__(self, parent, idList):
        CRbXmlStreamWriter.__init__(self, parent, idList)


    def createQuery(self, idList):
        stmt = """SELECT  %s,
                    E.code AS `purpose_code`
        FROM rbResult r
        LEFT JOIN rbEventTypePurpose E ON r.eventPurpose_id = E.id
        """ % ', '.join(['r.%s' % i for i in rbResultFields])

        if idList:
            stmt += 'WHERE r.id in ('+', '.join([str(et) for et in idList])+ ')'

        query = self._db.query(stmt)
        return query


    def writeRecord(self, record):
        self.writeStartElement("Result")

        # все свойства действия экспортируем как атрибуты
        for i in rbResultFields:
            self.writeAttribute(i, forceString(record.value(i)))

        # все, что определяется ссылками на другие таблицы - как элементы

        # Услуга (профиль ЕИС) экспортируемого элемента:
        if forceString(record.value("purpose_code")) != '':
            self.writeStartElement("EventTypePurpose")
            self.writeAttribute("code",
                                forceString(record.value("purpose_code")))
            self.writeEndElement()

        self.writeEndElement()


    def writeHeader(self):
        self.writeDTD("<!DOCTYPE xRbResult>")
        self.writeStartElement("RbResultExport")
        self.writeAttribute('version', "1.0")

# ******************************************************************************

class CExportRbResultWizardPage1(CExportAbstractRbPage1,
                                 Ui_ExportRbResult_Wizard_1):
    u"""Первая страница мастера экспорта справочника 'Результаты События'"""
    def __init__(self, parent):
        CExportAbstractRbPage1.__init__(self, 'rbResult', parent)
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

class CExportRbResult(CExportAbstractRbWizard):
    u"""Мастера экспорта справочника 'Результаты События'"""
    def __init__(self, parent=None):
        CExportAbstractRbWizard.__init__(self, 'rbResult',
            u'Результаты События', parent)
        self.page1 = CExportRbResultWizardPage1(self)
        self.page2 = CExportAbstractRbPage2(CMyXmlStreamWriter, self)
        self.addPage(self.page1)
        self.addPage(self.page2)
