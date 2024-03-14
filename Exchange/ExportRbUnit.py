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
u"""Экспорт справочника 'Единицы измерения' в XML"""

from library.TableModel import CTextCol

from library.Utils import forceString
from Exchange.ExportRb import (CExportAbstractRbWizard, CExportAbstractRbPage1,
    CExportAbstractRbPage2, CRbXmlStreamWriter)

from Exchange.Ui_ExportRbUnit_Wizard_1 import Ui_ExportRbUnit_Wizard_1


def ExportRbUnit(parent):
    u"""Формирует мастер выгрузки справочника 'Единицы измерения'"""
    dlg = CExportRbUnit(parent)
    dlg.exec_()


rbUnitFields = ('code', 'name')

# ******************************************************************************

class CMyXmlStreamWriter(CRbXmlStreamWriter):
    u"""Класс для записи элементов справочника 'Единицы измерения' в XML"""
    def __init__(self, parent, idList):
        CRbXmlStreamWriter.__init__(self, parent, idList)


    def createQuery(self, idList):
        """ Запрос информации по справочнику. Если idList пуст,
            запрашиваются все элементы"""

        stmt = """SELECT %s
        FROM rbUnit""" % ' ,'.join([i for i in rbUnitFields])

        if idList:
            stmt += ' WHERE id in ('+', '.join([str(et) for et in idList])+ ')'

        query = self._db.query(stmt)
        return query


    def writeRecord(self, record):
        self.writeStartElement("Unit")

        # все свойства действия экспортируем как атрибуты
        for field in rbUnitFields:
            self.writeAttribute(field, forceString(record.value(field)))

        self.writeEndElement()


    def writeHeader(self):
        self.writeDTD("<!DOCTYPE xRbUnit>")
        self.writeStartElement("RbUnitExport")
        self.writeAttribute('version', "1.0")

# ******************************************************************************

class CExportRbUnitWizardPage1(CExportAbstractRbPage1,
                               Ui_ExportRbUnit_Wizard_1):
    u"""Первая страница мастера экспорта справочника 'Единицы измерения'"""
    def __init__(self, parent):
        CExportAbstractRbPage1.__init__(self, 'rbUnit', parent)
        self.cols = [
            CTextCol(u'Код', ['code'], 20),
            CTextCol(u'Наименование', ['name'], 30)
            ]
        self.order = ['code', 'name', 'id']

        self.preSetupUi()
        self.setupUi(self)
        self.postSetupUi()

# ******************************************************************************

class CExportRbUnit(CExportAbstractRbWizard):
    u"""Мастера экспорта справочника 'Единицы измерения'"""
    def __init__(self, parent=None):
        CExportAbstractRbWizard.__init__(self, 'rbUnit',
            u'Единицы измерения', parent)
        self.page1 = CExportRbUnitWizardPage1(self)
        self.page2 = CExportAbstractRbPage2(CMyXmlStreamWriter, self)
        self.addPage(self.page1)
        self.addPage(self.page2)
