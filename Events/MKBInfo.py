# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from library.PrintInfo import CInfo, CIdentificationInfoMixin
from library.ICDUtils import getMKBClassName, getMKBBlockName, getMKBName, getMKBC_Id


class CMKBInfo(CInfo, CIdentificationInfoMixin):
    def __init__(self, context, code):
        CInfo.__init__(self, context)
        CIdentificationInfoMixin.__init__(self)
        self.code = code
        self.tableName = 'MKB'
        self._descr = None
        self._class = None
        self._block = None
        if self.code:
            self.id = self.getId()
        self._ok = bool(self.code)
        self._loaded = True


    def getId(self):
        self._id = getMKBC_Id(self.code) if self.code else ''
        return self._id

    def getClass(self):
        if self._class is None:
            self._class = getMKBClassName(self.code) if self.code else ''
        return self._class


    def getBlock(self):
        if self._block is None:
            self._block = getMKBBlockName(self.code) if self.code else ''
        return self._block


    def getDescr(self):
        if self._descr is None:
            self._descr = getMKBName(self.code) if self.code else ''
        return self._descr


    class_ = property(getClass)
    block = property(getBlock)
    descr = property(getDescr)

    def __str__(self):
        return self.code


class CMorphologyMKBInfo(CInfo):
    def __init__(self, context, code):
        CInfo.__init__(self, context)
        self.code = code
        self._ok = bool(self.code)
        self._loaded = True

    def __str__(self):
        return self.code
