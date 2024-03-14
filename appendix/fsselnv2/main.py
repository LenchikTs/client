#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2017-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import codecs
import locale
import sys
import os
import platform
if platform.system() != 'Windows':
    pathtail = '/appendix/fsselnv2/main.py'
    sys.path.insert(0, os.path.realpath(__file__).replace(pathtail, ''))
from optparse import OptionParser

from PyQt4 import QtGui
from PyQt4.QtCore import QTranslator, Qt

import library.patches
assert library.patches # silence pyflakes

from appendix.fsselnv2.app.WorkSpace import CWorkSpaceWindow
from app.App        import CApp
from app.MainWindow import CMainWindow


def main():
    parser = OptionParser(usage = 'usage: %prog [options]')
    parser.add_option('-c', '--config',
                      dest='iniFile',
                      help='custom .ini file name',
                      metavar='iniFile',
                      default=CApp.iniFileName
                     )

    parser.add_option('--SQL',
                      dest='logSql',
                      help='log sql queries',
                      action='store_true',
                      default=False
                     )

    parser.add_option('-l', '--nolock',
                      dest='nolock',
                      help='Disable record lock',
                      action='store_true',
                      default=False
                     )

#    parser.add_option('--logFile',
#                      dest='logFile',
#                      help='custom .log file name',
#                      action='store_true',
#                      metavar='logFile',
#                      default=None)
#
#    parser.add_option('--logLevel',
#                      dest='logLevel',
#                      help='log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)',
#                      action='store_true',
#                      metavar='logFile',
#                      default=None)

    parser.add_option('--version',
                      dest='version',
                      help='print version and exit',
                      action='store_true',
                      default=False)

    parser.add_option('-t', '--transfer',
                      dest='transfer',
                      help='transfer documents from MIS',
                      action='append',
                      default=None)

    parser.add_option('-u', '--user',
                      dest='user',
                      help='person id from MIS',
                      action='store',
                      default=None)

    #    parser.add_option("-q", "--quiet",   action="store_false", dest="verbose", default=True,  help="don't print status messages to stdout")
    (options, args) = parser.parse_args()

    if options.version:
        print '%s - %s' % (sys.argv[0] if sys.argv else '', CApp.getLatVersion())
    elif options.transfer:
        locale.setlocale(locale.LC_ALL, '')
        app = CApp(sys.argv, options.iniFile, options.nolock, options.logSql)
        stdTtranslator = QTranslator()
        stdTtranslator.load('i18n/std_ru.qm')
        app.installTranslator(stdTtranslator)
        QtGui.qApp = app
        app.applyDecorPreferences()
        mainWindow = CMainWindow()
        app.mainWindow = mainWindow
        QtGui.qApp.openDatabase()
        user_id = options.user
        if app.checkPersonInSession(user_id):
            app.mainWindow.workSpaceWindow = CWorkSpaceWindow(app.mainWindow)
            QtGui.qApp.setUserId(user_id)
            idList = [int(id) for id in options.transfer]
            idList.sort()
            for id in idList:
                # Здесь я m.letunenko очень сильно надеюсь что метод честно работает и ok всегда передает правильный
                ok, number, message = QtGui.qApp.sendDocument(id)
                messageBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, u'Внимание!',
                                               u'ЭЛН %s'
                                               u'%s' % (number, message),
                                               QtGui.QMessageBox.Ok)
                messageBox.exec_()
                if not ok:
                    break
        else:
            messageBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, u'Внимание!',
                                           u'У пользователя id = %s отсутствует активная сессия' % user_id,
                                           QtGui.QMessageBox.Ok)
            messageBox.exec_()

        del mainWindow
        app.preferences.save()
        app.closeDatabase()
        app.doneTrace()
        del app
        QtGui.qApp = None
    else:
        locale.setlocale(locale.LC_ALL, '')
        app = CApp(sys.argv, options.iniFile, options.nolock, options.logSql)
        stdTtranslator = QTranslator()
        stdTtranslator.load('i18n/std_ru.qm')
        app.installTranslator(stdTtranslator)

        QtGui.qApp = app
        app.applyDecorPreferences()
        mainWindow = CMainWindow()
        app.mainWindow = mainWindow
        app.applyDecorPreferences() # применение максимизации/полноэкранного режима к главному окну

        mainWindow.show()
        if app.preferences.dbAutoLogin:
            mainWindow.actLogin.activate(QtGui.QAction.Trigger)
        res = app.exec_()
        mainWindow.savePreferences()
        del mainWindow
        app.preferences.save()
        app.closeDatabase()
        app.doneTrace()
        del app
        QtGui.qApp = None
        return res

#    sys.exit(res)

class CWriter:
    def __init__(self, baseStream):
        self._writer = codecs.getwriter(locale.getpreferredencoding())(baseStream)


    def write(self, data):
        if isinstance(data, unicode):
            self._writer.write(data)
        elif isinstance(data, str):
            try:
                self._writer.write(data.decode('utf8'))
            except:
                self._writer.write(data)
        else:
            self._writer.write(unicode(data))


    def writelines(self, list):
        for s in list:
            self.write(s)


if __name__ == '__main__':
#    sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
#    sys.stderr = codecs.getwriter(locale.getpreferredencoding())(sys.stderr)
    sys.stdout = CWriter(sys.stdout)
    sys.stderr = CWriter(sys.stderr)

    main()
