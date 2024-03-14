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

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QRegExp, QString


from library.exception  import CException
from library.TableModel import CTextCol
from library.Utils      import exceptionToUnicode, forceString, forceStringEx, toVariant, trim


### МодификаторКодаУслуги: пусто - нет изменения, "-" - удаляет сервис, "+XXX"-меняет севис на XXХ, x - меняет первую букву в коде сервиса

def parseModifier(modifier):
    m = forceString(modifier)
    if not m:
        return (0, m)
    elif m.startswith('-'):
        return (1, u'')
    elif m.startswith('+'):
        return (2, trim(m[1:]))
    elif m.startswith('~'):
        return (4, m[1:])
    else:
        return (3, trim(m))


def createModifier(action, text):
    if action == 1:
        return u'-'
    elif action == 2:
        return u'+'+text
    elif action == 3:
        return text
    elif action == 4:
        return '~'+text
    else:
        return u''


def applyRegExp(complexModifierText, serviceCode):
    for modifierText in complexModifierText.split('\n'):
        if trim(modifierText):
            parts = modifierText.split(modifierText[0])
            if len(parts) != 4:
                raise CException(u'invalid service regexp modifier (%s)' % (modifierText))
            if parts[3].upper().find('I')>=0:
                cs = Qt.CaseInsensitive
            else:
                cs = Qt.CaseSensitive
            r = QRegExp(parts[1], cs, QRegExp.RegExp2)
            if not r.isValid():
                raise CException(u'invalid service regexp (%s)' % (parts[1]))
            if r.indexIn(serviceCode)>=0:
                return unicode(QString(serviceCode).replace(r, parts[2]))
    return serviceCode


def applyModifier(serviceCode, (modifierAction, modifierText)):
    if modifierAction == 0:
        return serviceCode
    elif modifierAction == 1:
        return ''
    elif modifierAction == 2:
        return modifierText
    elif modifierAction == 3:
        return modifierText + serviceCode[1:]
    elif modifierAction == 4:
        return applyRegExp(modifierText, serviceCode)
    else:
        raise CException(u'unknown service modifier (%s,%s)' % (modifierAction, modifierText))



class CServiceModifierCol(CTextCol):
    titles = [ u'не меняет услугу',
               u'удаляет услугу',
               u'заменяет код услуги на "%(text)s"',
               u'изменяет префикс кода услуги на "%(text)s"',
               u'изменяет код услуги по регулярному выражению "%(text)s"',
               u'неизвестный модификатор "%(text)s"',
            ]

    def format(self, values):
        action, text = parseModifier(values[0])
        return toVariant(CServiceModifierCol.titles[action if 0<=action<=4 else -1] % {'text':text})


def testRegExpServiceModifier(widget, regexp, regExpTestStr):
    title = u'Испытание регулярного выражения'
    str, ok = QtGui.QInputDialog.getText(widget,
                                         title,
                                         u'Исходный код',
                                         QtGui.QLineEdit.Normal,
                                         regExpTestStr)
    if ok:
        regExpTestStr = forceStringEx(str)
        try:
            result = applyRegExp(unicode(regexp), regExpTestStr)
            QtGui.QMessageBox.information(widget,
                                          title,
                                          u'В результате получилось "%s"'%result,
                                          QtGui.QMessageBox.Ok,
                                          QtGui.QMessageBox.Ok )
        except Exception, e:
            QtGui.QMessageBox.information(widget,
                                          title,
                                          u'Произошла ошибка:\n%s'% exceptionToUnicode(e),
                                          QtGui.QMessageBox.Ok,
                                          QtGui.QMessageBox.Ok )
    return regExpTestStr


def parseServiceFilter(filter, code):
    parts = filter.split(',')
    pos = int(parts[0])
    length = int(parts[1]) if len(parts) > 1 and bool(parts[1]) else None
    return code[pos-1:pos+length-1] if length else code[pos-1:]


def testServiceFilter(widget, filter, prevSrcStr):
    title = u'Испытания фильтра списка услуг'
    srcStr, ok = QtGui.QInputDialog.getText(widget,
                                            title,
                                            u'Исходный код',
                                            QtGui.QLineEdit.Normal,
                                           prevSrcStr)
    if ok:
        srcStr = forceStringEx(srcStr)
        result = parseServiceFilter(filter, srcStr)
        QtGui.QMessageBox.information(widget,
                                      title,
                                      u'В результате получилось "%s"'%result,
                                      QtGui.QMessageBox.Ok,
                                      QtGui.QMessageBox.Ok)
        return srcStr
    else:
        return prevSrcStr
