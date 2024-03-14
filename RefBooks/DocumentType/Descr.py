# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2016-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
#from PyQt4.QtCore import QRegExp


from library.DbEntityCache               import CDbEntityCache
from library.LineEditWithRegExpValidator import prepareRegExp, romanRegExp
from library.Utils                       import forceBool, forceRef, forceString

__all__ = [ 'getDocumentTypeDescr',
            'CDocumentTypeDescr',
          ]


def getDocumentTypeDescr(documentTypeId):
    return CDocumentTypeDescr.getDescr(documentTypeId)


class CDocumentTypeDescr(CDbEntityCache):
    mapIdToDescription = {}

    @classmethod
    def purge(cls):
        cls.mapIdToDescription.clear()


    @classmethod
    def register(cls, record):
        result = cls(record)
        cls.mapIdToDescription[result.id] = result
        return result


    @classmethod
    def getDescr(cls, id):
        if id in cls.mapIdToDescription:
            return cls.mapIdToDescription[id]
        else:
            cls.connect()
            db = QtGui.qApp.db
            table = db.table('rbDocumentType')
            result = cls.register(db.getRecord(table, '*', id))
            return result


    def __init__(self, record):
        if record:
            self.id = forceRef(record.value('id'))
            self.code = forceString(record.value('code'))
            self.regionalCode = forceString(record.value('regionalCode'))
            self.name = forceString(record.value('name'))
            self.isCitizenship = forceBool(record.value('isCitizenship'))
            self.title = forceString(record.value('title'))
            self.leftPartRegExp = forceString(record.value('leftPartRegExp')) or '\\S*'
            self.hasRightPart = forceBool(record.value('hasRightPart'))
            self.rightPartRegExp = forceString(record.value('rightPartRegExp')) or '\\S*'
            self.partSeparator = forceString(record.value('partSeparator'))[:1] or ' '
            self.numberRegExp = forceString(record.value('numberRegExp')) or '\\S*'
            if self.leftPartRegExp == u'R':
                self.leftPartRegExp = romanRegExp
            if self.rightPartRegExp == u'R':
                self.rightPartRegExp = romanRegExp
        else:
            self.id = None
            self.code = None
            self.regionalCode = None
            self.name = None
            self.isCitizenship = False
            self.title = None
            self.leftPartRegExp  = '\\S*'
            self.hasRightPart    = False
            self.rightPartRegExp = None
            self.partSeparator   = None
            self.numberRegExp    = '\\S*'


    def splitDocSerial(self, serial):
        if self.hasRightPart:
            for regExp in ( '(%s)\s*%s\s*(%s)' % (self.leftPartRegExp, self.partSeparator, self.rightPartRegExp),
                            '(%s)\s*%s\s*(.*)' % (self.leftPartRegExp, self.partSeparator),
                            '(%s)\s*(%s)' % (self.leftPartRegExp, self.rightPartRegExp),
                            '(%s)\s*(.*)' % (self.leftPartRegExp, )
                          ):
                rx = prepareRegExp(regExp)
                if rx.exactMatch(serial):
                    capturedTexts = rx.capturedTexts()
                    return unicode(capturedTexts[1]), unicode(capturedTexts[2])
        return serial, ''


    def compoundDocSerial(self, leftPart, rightPart):
        if self.hasRightPart:
            return leftPart + self.partSeparator + rightPart
        else:
            return leftPart


    def matchLeftPart(self, part):
        rx = prepareRegExp(self.leftPartRegExp)
        return rx.exactMatch(part)


    def matchRightPart(self, part):
        if self.hasRightPart:
            rx = prepareRegExp(self.rightPartRegExp)
            return rx.exactMatch(part)
        else:
            return not part


    def matchNumber(self, number):
        rx = prepareRegExp(self.numberRegExp)
        return rx.exactMatch(number)
