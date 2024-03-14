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

import struct
from PyQt4 import QtGui
from PyQt4.QtCore import QDate

from IdentCard               import CIdentCard, CIdentCardPolicy
from library.Utils           import nameCase

__all__ = ( 'policyBarCodeAsIdentCard',
          )



chars = u' .-‘0123456789АБ'\
        u'ВГДЕЁЖЗИЙКЛМНОПР'\
        u'СТУФХЦЧШЩЬЪЫЭЮЯ?'\
        u'???????????????|'


#def encodeName(lastName, firstName, patrName):
#    result = ''
#    s = (lastName+'|'+firstName+'|'+patrName).upper().ljust(56)
#    bits = ''.join( format(chars.index(c), '>06b') for c in s )
#    result = ''.join( chr(int(bits[i:i+8],2)) for i in range(0, len(bits), 8) )
#    return result


def decodeName(binStr):
    bits = ''.join( format(ord(bc),'>08b') for bc in binStr )
    if len(bits) % 6:
        bits += '0'*(6 - len(bits)%6)
    charStr = ''.join( chars[int(bits[i:i+6],2)]  for i in range(0, len(bits), 6) )
    parts = [part.strip() for part in charStr.split('|', 3)]
    if len(parts)<3:
        parts.extend(['']*(3-len(parts)))
    return parts


def policyBarCodeAsIdentCard(widget, data):
    result = None
    try:
        if data[0] == '\x01' and len(data)>=130:
            policyNumberAsInt, encodedName, encodedSex, daysToBirthDate, daysToPolicyExpired = struct.unpack('>xQ42sBHH', data[:56])
            revPatrName, revLastName, revFirstName = decodeName(encodedName[::-1])

            result = CIdentCard()
            result.lastName  = nameCase(revLastName[::-1])
            result.firstName = nameCase(revFirstName[::-1])
            result.patrName  = nameCase(revPatrName[::-1])
            result.sex = encodedSex if encodedSex in (1,2) else 0
            result.birthDate = QDate(1900, 1, 1).addDays(daysToBirthDate)
            result.policy = CIdentCardPolicy()
            result.policy.serial = ''
            result.policy.number = str(policyNumberAsInt)

        elif data[0] == '\x02' and len(data)>=130:
            policyNumberAsInt, encodedName, encodedSex, daysToBirthDate, daysToPolicyExpired = struct.unpack('>xQ51sBHH', data[:65])
            lastName, firstName, patrName = decodeName(encodedName)

            result = CIdentCard()
            result.lastName  = nameCase(lastName)
            result.firstName = nameCase(firstName)
            result.patrName  = nameCase(patrName)
            result.sex = encodedSex if encodedSex in (1,2) else 0
            result.birthDate = QDate(1900, 1, 1).addDays(daysToBirthDate)
            result.policy = CIdentCardPolicy()
            result.policy.serial = ''
            result.policy.number = str(policyNumberAsInt)

        elif data.count(';') == 15 and data[0:1] == 'A':
            # В Архангельской области
            parts = data.decode('cp1251').split(';')

            result = CIdentCard()
            result.lastName  = nameCase(parts[10])
            result.firstName = nameCase(parts[11])
            result.patrName  = nameCase(parts[12])
            result.sex       = 1 if parts[14].upper() == u'М' else 2
            result.birthDate = QDate.fromString(parts[13], 'yyyyMMdd')
            result.policy = CIdentCardPolicy()
            result.policy.serial = parts[1]
            result.policy.number = parts[2]
    except:
        QtGui.qApp.logCurrentException()

    if not result and QtGui.qApp.scannerParseReport():
        message = ( u'Это может быть связано с неподходящими настройками соединения со сканером\n'
                    u'или с незнанием разработчиками программы принципов кодирования данного шрих-кода.\n'
                    u'\n'
                    u'Если Вы уверены что настройки соединения со сканером правильны,\n'
                    u'и Вам требуется обеспечить распознование штрих-кода этого типа,\n'
                    u'то свяжитесь с разработчиками и передайте образец штрих-кода и\n'
                    u'спецификацию кодирования информации.' )

        QtGui.QMessageBox.information(widget, u'Не удалось распознать штрих-код',  message, QtGui.QMessageBox.Close, QtGui.QMessageBox.Close)
    return result

