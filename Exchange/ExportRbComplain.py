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
u"""Экспорт справочника 'Жалобы' в XML"""

from PyQt4 import QtGui

from library.TableModel import CTextCol
from library.Utils import forceString, forceInt

from Exchange.ExportRb import (CExportAbstractRbWizard,
    CExportAbstractRbPage1WithTree, CExportAbstractRbPage2WithTree,
    CRbXmlStreamWriter)

# ******************************************************************************

rbComplainFields = ('code', 'name')


def ExportRbComplain(parent):
    u"""Формирует мастер выгрузки справочника 'Жалобы'"""
    dlg = CExportRbComplain(parent)
    dlg.exec_()

# ******************************************************************************

class CMyXmlStreamWriter(CRbXmlStreamWriter):
    u"""Класс для записи элементов справочника 'Жалобы' в XML"""
    def __init__(self, parent, idList):
        CRbXmlStreamWriter.__init__(self, parent, idList)
        self.nestedGroups = []


    def createQuery(self, idList):
        stmt = """SELECT  id, %s, group_id
        FROM rbComplain
        """ % ' ,'.join([i for i in rbComplainFields])

        if idList:
            stmt += ' WHERE id in ('+', '.join([str(et) for et in idList])+')'

        query = self._db.query(stmt)
        return query


    def writeRecord(self, record):
        self.writeStartElement('ComplainElement')

        # все свойства действия экспортируем как атрибуты
        for i in rbComplainFields:
            self.writeAttribute(i, forceString(record.value(i)))

        # все, что определяется ссылками на другие таблицы - как элементы
        # группа экспортируемого элемента:
        group_id = forceInt(record.value("group_id"))
        _id = forceInt(record.value("id"))

        if _id == group_id:
            QtGui.QMessageBox.critical(self._parent,
                u'Ошибка в логической структуре данных',
                (u'Элемент id=%d: (%s) "%s", group_id=%d'
                u' является сам себе группой' %
                (id, forceString(record.value("code")),
                      forceString(record.value("name")), group_id)),
                QtGui.QMessageBox.Close)
        elif group_id in self.nestedGroups:
            QtGui.QMessageBox.critical(self._parent,
                u'Ошибка в логической структуре данных',
                (u'Элемент id=%d: group_id=%d обнаружен'
                u' в списке родительских групп "%s"' %
                (_id, group_id,
                u'(' + '-> '.join([str(et) for et in self.nestedGroups])+ ')')),
                QtGui.QMessageBox.Close)
        elif group_id != 0: # все в порядке
            self.writeStartElement('group')
            query = self.createQuery([group_id])

            while query.next():
                self.nestedGroups.append(group_id)
                self.writeRecord(query.record()) # рекурсия
                self.nestedGroups.remove(group_id)

            self.writeEndElement() # group

        self.writeEndElement() # ThesaurusElement

    def writeHeader(self):
        self.writeDTD("<!DOCTYPE xRbThesaurus>")
        self.writeStartElement('RbComplainExport')
        self.writeAttribute('version', '1.00')

# ******************************************************************************

class CExportRbComplainWizardPage1(CExportAbstractRbPage1WithTree):
    u"""Первая страница мастера экспорта справочника 'Жалобы'"""
    def __init__(self, parent):
        self.cols = [
            CTextCol(u'Код', ['code'], 20),
            CTextCol(u'Наименование', ['name'], 40)
            ]
        self.order = ['code', 'name', 'id']

        CExportAbstractRbPage1WithTree.__init__(self, 'rbComplain', parent)

# ******************************************************************************

class CExportRbComplain(CExportAbstractRbWizard):
    u"""Мастера экспорта справочника 'Жалобы'"""
    def __init__(self, parent=None):
        CExportAbstractRbWizard.__init__(self, 'rbComplain', u'Жалобы', parent)
        self.selectedItems = {}
        self.page1 = CExportRbComplainWizardPage1(self)
        self.page2 = CExportAbstractRbPage2WithTree(CMyXmlStreamWriter, self)
        self.addPage(self.page1)
        self.addPage(self.page2)
