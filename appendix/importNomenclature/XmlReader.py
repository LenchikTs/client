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
u'Класс для чтения XML документов'

from PyQt4 import QtGui
from PyQt4.QtCore import QXmlStreamReader

from library.Utils import forceString

# ******************************************************************************

class CXmlStreamReader(QXmlStreamReader):
    u"""Разбирает XML документ и выдает его словарями поэлементно через yield.
        groupNames - словарь кортежей с именами подгрупп,
                     ключ - имя текущей группы.
    """

    def __init__(self, parent, groupNames, startElementName, logBrowser,
                 showLog=False):
        QXmlStreamReader.__init__(self)
        self._parent = parent
        self._logBrowser = logBrowser
        self._showLog = showLog
        self._groupNames = groupNames
        self._startElementName = startElementName

    def raiseError(self, msg):
        u'Вызывает обработчик ошибок'
        QXmlStreamReader.raiseError(self, u'[%d:%d] %s' % (
            self.lineNumber(), self.columnNumber(), msg))


    def errorString(self):
        u'Возвращает сообщение с текстом ошибки'
        return u'[%d:%d] %s' % (
            self.lineNumber(), self.columnNumber(),
            QXmlStreamReader.errorString(self))


    def log(self, msg, forceLog=False):
        u'Пишет сообщение в журнал'
        if self._logBrowser and (self._showLog or forceLog):
            self._logBrowser.append(msg)
            self._logBrowser.update()


    def readHeader(self):
        u''' Разбирает заголовок'''

        while not self.atEnd():
            self.readNext()

            if self.isStartElement():
                if self.name() == self._startElementName:
                    return True
                else:
                    self.raiseError(u'Неверный формат экспорта данных.')

        return False


    def readData(self):
        u'Разбирает данные, раскладывая их по словарю'
        currentGroup = forceString(self.name())
        assert self.isStartElement()

        while not self.atEnd():
            QtGui.qApp.processEvents()
            self.readNext()

            if self.isEndElement():
                break

            if self.isStartElement():
                if self.name() in self._groupNames[currentGroup]:
                    yield self.readRow()
                else:
                    self.readUnknownElement()

            if self.hasError() or self._parent.aborted:
                break


    def readValue(self):
        u'Читает значение тега'
        assert self.isStartElement()
        result = None

        if self._parent.aborted:
            return None

        while not self.atEnd():
            self.readNext()

            if self.isEndElement():
                break

            if self.isStartElement():
                name = forceString(self.name())
                if name == 'VALUE':
                    result = forceString(self.readElementText())
                else:
                    self.readUnknownElement()

        return result


    def readUnknownElement(self, report=True):
        """ Читает неизвестный элемент, и сообщает об этом,
            если report ==True """

        assert self.isStartElement()

        if report:
            self.log(u'Неизвестный элемент: '+self.name().toString())

        while not self.atEnd():
            self.readNext()

            if self.isEndElement():
                break

            if self.isStartElement():
                self.readUnknownElement(report)

            if self.hasError() or self._parent.aborted:
                break


    def readRow(self):
        u'Читает строку в словарь:'
        assert self.isStartElement()

        groupName = forceString(self.name())
        result = {}

        if self._parent.aborted:
            return None

        while not self.atEnd():
            self.readNext()

            if self.isEndElement():
                break

            if self.isStartElement():
                name = forceString(self.name())

                if name in self._groupNames.get(groupName, tuple()):
                    _, row = self.readRow()

                    if result.has_key(name):
                        if not isinstance(result[name], list):
                            result[name] = [result[name]]
                        result[name].append(row)
                    else:
                        result[name] = row
                else:
                    result[name] = forceString(self.readElementText())

        return groupName, result
