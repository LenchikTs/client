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
u'Класс для записи журналов об ошибках и успехах импорта'

from PyQt4.QtCore import QXmlStreamWriter, QFile
from library.Utils import forceString

# ******************************************************************************

class CSuccessLogger(object):
    def __init__(self):
        self._xmlWriter = QXmlStreamWriter()
        self._errorString = u''
        self._file = None

    @property
    def fileName(self):
        return forceString(self._file.fileName()) if self._file else None


    def open(self, fileName):
        self._file = QFile(fileName)
        self._xmlWriter.setDevice(self._file)

        if not self._file.open(QFile.WriteOnly | QFile.Text):
            self._errorString = self._file.errorString()
            return False

        self._xmlWriter.writeStartDocument()
        self._xmlWriter.writeStartElement('LIST')


    def close(self):
        self._xmlWriter.writeEndDocument()
        self._file.close()


    def writeRecord(self, docId):
        self._xmlWriter.writeStartElement('DOC')
        self._xmlWriter.writeTextElement('ID', docId)
        self._xmlWriter.writeEndElement()


    def errorString(self):
        return self._errorString

# ******************************************************************************

class CErrorLogger(CSuccessLogger):
    def __init__(self):
        CSuccessLogger.__init__(self)


    def writeRecord(self, docId, fieldName=None, baseFieldName=None,
                    itemId=None, comment=None):
        self._xmlWriter.writeStartElement('OSHIB')

        for val, tagName in ((fieldName, 'IM_POL'), (baseFieldName, 'BAS_EL'),
                             (docId, 'DOC_ID'),  (itemId, 'ITEM_ID'),
                             (comment, 'COMMENT')):
            if val:
                self._xmlWriter.writeTextElement(tagName, forceString(val))

        self._xmlWriter.writeEndElement()

# ******************************************************************************
