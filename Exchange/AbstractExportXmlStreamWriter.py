# -*- coding: utf-8 -*-
#pylint: disable=R0921
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
u"""Абстрактный класс экспорта в XML."""


from PyQt4 import QtGui
from PyQt4.QtCore import Qt,QXmlStreamWriter, QVariant

from library.Utils import (anyToUnicode, exceptionToUnicode, forceDate,
                           forceString)
from Exchange.ExtendedRecord import CExtendedRecord

# ******************************************************************************

class CAbstractExportXmlStreamWriter(QXmlStreamWriter):
    u"""Абстрактный класс для экспорта в формате XML"""
    def __init__(self, parent):
        QXmlStreamWriter.__init__(self)
        self._parent = parent
        self.setAutoFormatting(True)
        self.aborted = False


    def abort(self):
        self.aborted = True


    def writeHeader(self, params):
        u"""Запись заголовка xml файла, абстрактный метод"""
        raise NotImplementedError


    def writeRecord(self, record, params):
        u"""Пишет sql запись в файл, абстрактный метод"""
        raise NotImplementedError


    def writeFooter(self, params):
        raise NotImplementedError


    def writeElement(self, elementName, value=None):
        self.writeTextElement(elementName, '' if not value else value)


    def handleEmptyRequiredField(self, field, prefix):
        pass

    def writerFuncEx(self, prefix, rec, field, dateFields=None,
                     requiredFields=None):
        val = rec.value('%s_%s' % (prefix, field))

        if requiredFields and field in requiredFields and not forceString(val):
            self.handleEmptyRequiredField(field, prefix)

        if isinstance(val, (tuple, list, set)):
            for i in val:
                self.writeElement(field, i)
        elif dateFields and field in dateFields:
            self.writeElement(field, forceDate(val).toString(Qt.ISODate))
        else:
            self.writeElement(field, forceString(val))


    def writeGroup(self, groupName, fieldList, record, subGroup=None,
                closeGroup=True, namePrefix=None, dateFields=tuple(),
                openGroup=True, requiredFields=None):

        def checkSubGroup(subGroup):
            flag = False

            for subGroupName, subGroupData in subGroup.iteritems():
                for field in subGroupData.get('fields', []):
                    fieldName = '%s_%s' % (subGroupName, field)
                    if namePrefix:
                        fieldName = '{0}_{1}'.format(namePrefix, fieldName)

                    if not record.isNull(fieldName):
                        flag = True
                        break

                if not flag and subGroupData.has_key('subGroup'):
                    flag, fieldName = checkSubGroup(subGroupData['subGroup'])

                if flag:
                    break

            return flag, fieldName

        for field in fieldList:
            fieldName = '%s_%s' % (groupName, field)
            if namePrefix:
                fieldName = '{0}_{1}'.format(namePrefix, fieldName)

            if not record.isNull(fieldName):
                break
        else:
            flag = False

            if subGroup:
                flag, fieldName = checkSubGroup(subGroup)

            if not flag:
                return

        if isinstance(record.value(fieldName), (tuple, list)):
            items = []
            keys = []
            flag = True

            for f in fieldList:
                name = '%s_%s' % (groupName, f)
                if namePrefix:
                    name = '{0}_{1}'.format(namePrefix, name)

                if record.isNull(name):
                    continue

                if not isinstance(record.value(name), (tuple, list)):
                    flag = False
                    break

                items.append(record.value(name))
                keys.append(name)

            if subGroup and flag:
                for subGroupName, subGroupData in subGroup.iteritems():
                    for field in subGroupData['fields']:
                        name = '%s_%s' % (subGroupName, field)
                        if subGroupData.get('prefix'):
                            name = '{0}_{1}'.format(
                                subGroupData['prefix'], name)
                        if not record.isNull(name):
                            items.append(record.value(name))
                            keys.append(name)

            if flag:
                for group in zip(*items):
                    r = CExtendedRecord(params=dict(zip(keys, group)))
                    self.writeGroup(groupName, fieldList, r, subGroup, True,
                        namePrefix, dateFields, True, requiredFields)

                return
        elif isinstance(record.value(fieldName), QVariant) and record.value(fieldName).type() == 0:
            return

        if openGroup:
            self.writeStartElement(groupName)

        if namePrefix:
            groupName = '%s_%s' % (namePrefix, groupName)

        exportedSubgroups = set()

        # если поле совпадает с именем подгруппы, выгружаем ее
        for field in fieldList:
            if subGroup and field in subGroup.keys():
                val = subGroup[field]
                self.writeGroup(field, val.get('fields', tuple()), record,
                    val.get('subGroup'), True, val.get('prefix'),
                    val.get('dateFields'),
                    requiredFields=val.get('requiredFields'))
                exportedSubgroups.add(field)
            else:
                self.writerFuncEx(groupName, record, field, dateFields,
                                  requiredFields)

        # выгружаем оставшиемя подгруппы
        if subGroup:
            for (name, val) in subGroup.iteritems():
                if name not in exportedSubgroups:
                    self.writeGroup(name, val.get('fields', tuple()), record,
                        val.get('subGroup'), True, val.get('prefix'),
                        val.get('dateFields'),
                        requiredFields=val.get('requiredFields'))

        if closeGroup:
            self.writeEndElement()


    def writeFile(self, device, query, progressBar=None, params=None):
        try:
            self.setDevice(device)

            if progressBar:
                progressBar.setMaximum(max(query.size(), 1))
                progressBar.reset()
                progressBar.setValue(0)

            self.writeStartDocument()
            self.writeHeader(params)
            self.aborted = False

            while query.next():
                self.writeRecord(query.record(), params)

                if progressBar:
                    progressBar.step()

                if self.aborted:
                    return False

                QtGui.qApp.processEvents()

            self.writeFooter(params)
            self.writeEndDocument()

        except IOError, e:
            QtGui.qApp.logCurrentException()
            msg = ''

            if hasattr(e, 'filename'):
                msg = u'%s:\n[Errno %s] %s' % (
                   e.filename, e.errno,
                   anyToUnicode(e.strerror))
            else:
                msg = u'[Errno %s] %s' % (e.errno,
                                          anyToUnicode(e.strerror))

            QtGui.QMessageBox.critical(self._parent,
                u'Произошла ошибка ввода-вывода', msg,
                QtGui.QMessageBox.Close)
            return False

        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical(self._parent,
                u'Произошла ошибка', exceptionToUnicode(e),
                QtGui.QMessageBox.Close)
            return False

        return True


    def close(self):
        u'Закрывает устройство при его наличии'
        if self.device():
            self.device().close()
