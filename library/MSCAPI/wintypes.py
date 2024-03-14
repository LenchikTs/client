# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2017-2018 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Описчание типов данных, применияемых в CAPI
##
#############################################################################

import os
import sys

from ctypes   import (
                      CFUNCTYPE,
                      POINTER,
                      c_byte,
                      c_char,
                      c_char_p,
                      c_int,
                      c_long,
                      c_uint16,
                      c_uint32,
                      c_ulong,
                      c_void_p,
                      c_wchar_p,
                      Structure,
                     )
from datetime import datetime
from time     import mktime

__all__ = (
            'BOOL',
            'PBOOL',
            'BYTE',
            'PBYTE',
            'CHAR',
            'DWORD',
            'PDWORD',
            'HANDLE',
            'LONG',
            'ULONG',
            'ULONG_PTR',
            'LPCSTR',
            'LPCWSTR',
            'WORD',
            'FILETIME',
            'LPFILETIME',
            'CAPIFUNCTYPE',
          )

# "общие" типы данных

BOOL      = c_int
BYTE      = c_byte
CHAR      = c_char
DWORD     = c_uint32
#PWSTR     = c_wchar_p
ULONG     = c_ulong
LONG      = c_long
WORD      = c_uint16

LPCWSTR   = LPWSTR = c_wchar_p
LPCSTR    = LPSTR  = c_char_p

PBOOL     = POINTER(BOOL)
PDWORD    = POINTER(DWORD)
PBYTE     = c_void_p # оказалось, что так удобнее

HANDLE    = c_void_p

ULONG_PTR = c_void_p  # по описанию - это целое число, размером в указатель.


# Contains a 64-bit value representing the number of 100-nanosecond intervals since January 1, 1601 (UTC).

class FILETIME(Structure):
    _fields_ = (
                 ('dwLowDateTime',  DWORD),
                 ('dwHighDateTime', DWORD),
               )

    __scale  = 10**7
    __offset = 11644473600*10**7

    def _getDatetime(self):
        sec, part = divmod((self.dwHighDateTime << 32) + self.dwLowDateTime - self.__offset, self.__scale)
        timestamp = sec + float(part)/self.__scale
        return datetime.fromtimestamp(timestamp)

    def _setDatetime(self, dt):
        timestamp = mktime(dt.timetuple())
        number = long(timestamp*self.__scale) + self.__offset
        self.dwHighDateTime, self.dwLowDateTime = divmod(number, 2**32)

    datetime =  property(_getDatetime, _setDatetime)


LPFILETIME = POINTER(FILETIME)

if os.name == 'nt' or sys.platform == 'cygwin':
    from ctypes import WINFUNCTYPE
    CAPIFUNCTYPE = WINFUNCTYPE
elif os.name == 'posix':
    CAPIFUNCTYPE = CFUNCTYPE
else:
    raise NotImplementedError('Microsoft CryptoAPI for this platfom is not implemented')

