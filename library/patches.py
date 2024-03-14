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

import sys
import os
import locale

from PyQt4.QtCore import QDateTime

builtinListDir = os.listdir

def myListDir(path):
    if isinstance(path, unicode):
        encoding = sys.getfilesystemencoding()
        return [ f if isinstance(f, unicode) else unicode(f, encoding) for f in builtinListDir(path)]
    else:
        return builtinListDir(path)

os.listdir = myListDir

# =================================================

builtinUnlink = os.unlink

def myUnlink(path):
    if isinstance(path, unicode):
        try:
            builtinUnlink(path)
        except UnicodeError:
            encoding = sys.getfilesystemencoding()
            builtinUnlink(path.encode(encoding))
    else:
        builtinUnlink(path)

os.unlink = myUnlink
os.remove = myUnlink

# =================================================
# обнаружено, что в python2 locale.strcoll работает неверно,
# а locale.strxfrm ломается на юникодных строках

builtinStrxfrm = locale.strxfrm
builtinStrcoll = locale.strcoll
_strEncoding = None # мелкая жуля - предположим, что когда дело дойдёт до
                    # strxfrm или strcoll setlocale() уже будет выполнено
                    # и не будет меняться.

def myStrxfrm(s):
    global _strEncoding

    if isinstance(s, unicode):
        if _strEncoding is None:
           _strEncoding  = (    locale.getlocale(locale.LC_COLLATE)[1]
                             or locale.getpreferredencoding()
                             or 'utf8'
                           )
        return builtinStrxfrm(s.encode(_strEncoding))
    else:
        return builtinStrxfrm(s)


def myStrcol(a, b):
    return cmp(myStrxfrm(a), myStrxfrm(b))

locale.strxfrm = myStrxfrm
locale.strcoll = myStrcol

# =================================================

if os.name == 'nt':
    builtinExpanduser = os.path.expanduser
    builtinExpandvars = os.path.expandvars

    def myExpanduser(path):
        if isinstance(path, unicode):
            try:
                return builtinExpanduser(path)
            except UnicodeError:
                encoding='cp1251'
                return builtinExpanduser(path.encode(encoding)).decode(encoding)
        else:
            return builtinExpanduser(path)

    def myExpandvars(path):
        if isinstance(path, unicode):
            try:
                return builtinExpandvars(path)
            except UnicodeError:
                encoding='cp1251'
                return builtinExpandvars(path.encode(encoding)).decode(encoding)
        else:
            return builtinExpandvars(path)

    os.path.expanduser = myExpanduser
    os.path.expandvars = myExpandvars

# =================================================

if os.name == 'nt':
    import ctypes
    builtinFormatError = ctypes.FormatError

    def myFormatError(code=None):
        result = builtinFormatError(code)
        result = result if isinstance(result, unicode) else result.decode(sys.getfilesystemencoding())
        return result

    ctypes.FormatError = myFormatError

# =================================================
# Обнаружено, что bool(QDateTime(QDate(), QTime(0,0)) == True,
# а на наш взгяд должно быть False
# альтернатива: написать функцию в замен QDateTime
# типа def qDateTime(d,t): return QDateTime(d,t) if d else QDateTime()


def qdt__nonzero__(self):
    return bool(self.date())

QDateTime.__nonzero__ = qdt__nonzero__

# =================================================
# Обнаружено, что в некоторых установках windows
# кодировка усрановлена как cp65001 (имеется в виду utf-8)
# а в некоторых - cp28595 (имеется в виду iso8859-5)
# так что я до кучи добавлю что я ещё знаю :(
# см. https://docs.microsoft.com/en-us/windows/desktop/intl/code-page-identifiers
if os.name == 'nt':
    import codecs
    remapCodecs = {
                    'cp10007' : 'mac-cyrillic', # Cyrillic (Mac)
                    'cp20866' : 'koi8-r',       # Russian (KOI8-R)
                    'cp20936' : 'gb2312',       # Что-то китайское, но русские буквы там тоже есть
                    'cp21866' : 'koi8-u',       # united Russian & Ukrainian (KOI8-U)
                    'cp28595' : 'iso8859-5',    # ISO 8859-5 Cyrillic
                    'cp65001' : 'utf-8',        # Unicode (UTF-8)
                  }
    codecs.register(lambda name: codecs.lookup(remapCodecs[name]) if name in remapCodecs else None)

