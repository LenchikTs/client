#!/usr/bin/env python
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

import library.patches
assert library.patches # затыкаем pyflakes

import codecs
import gc
import locale
import os
import os.path
import shutil
import sys
import tempfile
import traceback
from optparse import OptionParser

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import (pyqtSignature, QDir, qInstallMsgHandler, QVariant, Qt,
    QDateTime, QTimer, SIGNAL)

from Users.Login         import CLoginDialog
from Users.UserInfo      import CUserInfo, CDemoUserInfo
from Users.Tables        import (tblUser, usrLogin, usrPassword, usrRetired,
    demoUserName)
from library             import database
from library.BaseApp import CBaseApp
from library.DialogBase import CConstructHelperMixin
from library.Utils       import (getPref, getPrefString, forceInt, setPref,
                                 forceString, anyToUnicode, forceBool, forceRef,
                                 exceptionToUnicode)

from preferences.connection import CConnectionDialog

from ExportDialog import CExportDialog
from Progress             import CProgressDialog
from appPreferencesDialog import CAppPreferencesDialog
from Ui_importNomenclature     import Ui_MainWindow

gTitle = u'САМСОН'
gTitleLat = 'SAMSON'
gVersion = '2.5'
gAbout = u'Комплекс Программных Средств \n' \
        u'"Система Автоматизации Медико-Страхового Обслуживания Населения"\n' \
        u'КПС «%s»\n'   \
        u'Версия %s (ревизия %s от %s)\n' \
        u'Copyright © 2015 ООО "САМСОН Групп"\n' \
        u'распространяется под лицензией GNU GPL v.3 или выше\n' \
        u'Основано на КПС «САМСОН-ВИСТА» версии 2.0\n' \
        u'телефон тех.поддержки: (812) 418-39-70'


class CMyApp(CBaseApp):
    __pyqtSignals__ = ('dbConnectionChanged(bool)',
                       'currentUserIdChanged()',
                      )

    def __init__(self, args, demoModeRequest, service):
        CBaseApp.__init__(self, args, 'importNomenclature.ini')
        self.logDir = os.path.join(unicode(QDir.toNativeSeparators(QDir.homePath())), '.samson-vista')
        self.oldMsgHandler = qInstallMsgHandler(self.msgHandler)
        self.oldEexceptHook = sys.excepthook
        sys.excepthook = self.logException
        self.traceActive = True
        self.homeDir= None
        self.saveDir= None
        self.userId = None
        self.userSpecialityId = None
        self.userOrgStructureId = None
        self.db     = None
        self.mainWindow = None
        self.registerDocumentTables()
        self._currentClientId = None
        self.userInfo = None
        self.demoModeRequested = True
        self.serviceName = 'SamsonImportNomenclature'

        self._highlightRedDate = None


    def currentOrgId(self):
        return forceRef(QtGui.qApp.preferences.appPrefs.get('orgId', QVariant()))


    def doneTrace(self):
        self.traceActive = False
        qInstallMsgHandler(self.oldMsgHandler)
        sys.excepthook = self.oldEexceptHook


    def applyDecorPreferences(self):
        self.setStyle(self.preferences.decorStyle)
        if self.preferences.decorStandardPalette:
            self.setPalette(self.style().standardPalette())
        if self.mainWindow:
            state = Qt.WindowNoState
            if self.preferences.decorMaximizeMainWindow:
                state |= Qt.WindowMaximized
            if self.preferences.decorFullScreenMainWindow:
                state |= Qt.WindowFullScreen
            self.mainWindow.setWindowState(state)


    def registerDocumentTables(self):
        database.registerDocumentTable('Organisation')
        database.registerDocumentTable('OrgStructure')
        database.registerDocumentTable('Person')
        database.registerDocumentTable('StockMotion')


    def getHomeDir(self):
        if not self.homeDir:
            homeDir = os.path.expanduser('~')
            if homeDir == '~':
                homeDir = unicode(QDir.homePath())
            if isinstance(homeDir, str):
                homeDir = unicode(homeDir, locale.getpreferredencoding())
            self.homeDir = homeDir
        return self.homeDir


    def getSaveDir(self):
        self.saveDir = forceString(self.preferences.appPrefs.get('saveDir', QVariant()))
        if not self.saveDir:
            self.saveDir = self.getHomeDir()
        return self.saveDir


    def setSaveDir(self, path):
#        mode = os.stat(path)[ST_MODE]
#        if if S_ISDIR(mode):
        saveDir = os.path.dirname(unicode(path))
        if saveDir and self.saveDir != saveDir:
            self.preferences.appPrefs['saveDir'] = QVariant(saveDir)


    def getTemplateDir(self):
        result = forceString(self.preferences.appPrefs.get('templateDir', None))
        if not result:
            result = os.path.join(self.logDir, 'templates')
        return result


    def getTmpDir(self, suffix=''):
        return unicode(tempfile.mkdtemp('','samson_%s_'%suffix), locale.getpreferredencoding())


    def removeTmpDir(self, dir):
        try:
            shutil.rmtree(dir, False)
        except:
            self.logCurrentException()


    def log(self, title, message, stack=None):
        try:
            if not os.path.exists(self.logDir):
                os.makedirs(self.logDir)
            logFile = os.path.join(self.logDir, 'error.log')
            timeString = unicode(QDateTime.currentDateTime().toString(Qt.SystemLocaleDate))
            logString = u'%s\n%s: %s(%s)\n' % ('='*72, timeString, title, message)
            if stack:
                try:
                    logString += ''.join(traceback.format_list(stack)).decode('utf-8') + '\n'
                except:
                    logString += 'stack lost\n'
            file = codecs.open(logFile, mode='a', encoding=locale.getpreferredencoding())
            file.write(logString)
            file.close()
        except:
            pass


    def logException(self, exceptionType, exceptionValue, exceptionTraceback):
        title = repr(exceptionType)
        message = exceptionToUnicode(exceptionValue)
        self.log(title, message, traceback.extract_tb(exceptionTraceback))
        sys.__excepthook__(exceptionType, exceptionValue, exceptionTraceback)


    def logCurrentException(self):
        self.logException(*sys.exc_info())


    def msgHandler(self, type, msg):
        if type == 0: # QtMsgType.QtDebugMsg:
            typeName = 'QtDebugMsg'
        elif type == 1: # QtMsgType.QtWarningMsg:
            typeName = 'QtWarningMsg'
        elif type == 2: # QtMsgType.QtCriticalMsg:
            typeName = 'QtCriticalMsg'
        elif type == 3: # QtFatalMsg
            typeName = 'QtFatalMsg'
        else:
            typeName = 'QtUnknownMsg'

        self.log( typeName, msg, traceback.extract_stack()[:-1])
#        print typeName, msg


    def openDatabase(self):
        self.db = None
        self.db = database.connectDataBase(self.preferences.dbDriverName,
                                     self.preferences.dbServerName,
                                     self.preferences.dbServerPort,
                                     self.preferences.dbDatabaseName,
                                     self.preferences.dbUserName,
                                     self.preferences.dbPassword)
        self.emit(QtCore.SIGNAL('dbConnectionChanged(bool)'), True)


    def closeDatabase(self):
        if self.db:
            self.db.close()
            self.db = None
            self.emit(QtCore.SIGNAL('dbConnectionChanged(bool)'), False)


    def notify(self, receiver, event):
        try:
#            report = ["notify:: receiver.type=",unicode(type(receiver))," receiver.name=", unicode(receiver.objectName())," event.type=",unicode(type(event)), "event.type()=", unicode(event.type())]
#            print >>sys.stderr, ("".join(report)).encode('cp866')
            return QtGui.QApplication.notify(self, receiver, event)
        except Exception, e:
            if self.traceActive:
                self.logCurrentException()
                widget = self.activeModalWidget()
                if widget is None:
                    widget = self.mainWindow
                QtGui.QMessageBox.critical( widget,
                                            u'Произошла ошибка',
                                            unicode(e),
                                            QtGui.QMessageBox.Close)
            return False
        except:
            return False


    def call(self, widget, func, params = ()):
        try:
            return True, func(*params)
        except IOError, e:
            msg=''
            if hasattr(e, 'filename'):
                msg = u'%s:\n[Errno %s] %s' % (e.filename, e.errno, anyToUnicode(e.strerror))
            else:
                msg = u'[Errno %s] %s' % (e.errno, anyToUnicode(e.strerror))
            QtGui.QMessageBox.critical(widget,
                u'Произошла ошибка ввода-вывода', msg, QtGui.QMessageBox.Close)
        except Exception, e:
            self.logCurrentException()
            widget = widget or self.activeModalWidget() or self.mainWindow
            QtGui.QMessageBox.critical( widget,
                                        u'Произошла ошибка',
                                        unicode(e),
                                        QtGui.QMessageBox.Close)
        return False, None


    def callWithWaitCursor(self, widget, func, *params, **kwparams):
        self.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))
        try:
            return func(*params, **kwparams)
        finally:
            self.restoreOverrideCursor()


    def demoModePosible(self):
        try:
            tableUser = self.db.table(tblUser)
            record = self.db.getRecordEx(tableUser, [usrPassword, usrRetired], tableUser[usrLogin].eq(demoUserName))
            return not record or (not forceString(record.value(usrPassword)) and not forceBool(record.value(usrRetired)))
        except:
            pass
        return False


    def setUserId(self, userId, demoMode = False):
        self.userId = userId
        record = self.db.getRecord('Person', ['speciality_id', 'orgStructure_id'], userId) if userId else None
        if record:
            self.userSpecialityId = forceRef(record.value('speciality_id'))
            self.userOrgStructureId = forceRef(record.value('orgStructure_id'))
        else:
            self.userSpecialityId = None
            self.userOrgStructureId = None
        self.demoMode = demoMode
        if demoMode:
            self.userInfo = CDemoUserInfo(userId)
        else:
            if userId:
                self.userInfo = CUserInfo(userId)
            else:
                self.userInfo = None
        self.emit(QtCore.SIGNAL('currentUserIdChanged()'))


    def userName(self):
        if self.userInfo:
#            orgId = self.currentOrgId()
#            orgInfo = getOrganisationInfo(orgId)
#            if not orgInfo:
#                QtGui.qApp.preferences.appPrefs['orgId'] = QVariant()
#            shortName = orgInfo.get('shortName', u'ЛПУ в настройках не указано!')
            return u'%s (%s)' % (self.userInfo.name(), self.userInfo.login())
        else:
            return ''


    def userHasRight(self, right):
        return self.userInfo is not None and self.userInfo.hasRight(right)


    def userHasAnyRight(self, rights):
        return self.userInfo is not None and self.userInfo.hasAnyRight(rights)


    def defaultKLADR(self):
        # возвращает код по умолчанию
        result = forceString(self.preferences.appPrefs.get('defaultKLADR', ''))
        if not result:
            result = '7800000000000'
        return result


    def highlightRedDate(self):
        if self._highlightRedDate is None:
            self._highlightRedDate = forceBool(QtGui.qApp.preferences.appPrefs.get('highlightRedDate', False))
        return self._highlightRedDate

# #############################################################

class CMainWindow(QtGui.QMainWindow, Ui_MainWindow, CConstructHelperMixin):

    maskCsv = u'Файлы CSV (*.csv)'

    def __init__(self, parent=None, service=False):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.loadPreferences()
        self.scanTimer = None

        if service:
            self.prepareService()


    def loadPreferences(self):
        preferences = getPref(QtGui.qApp.preferences.windowPrefs, self.objectName(), {})
        geometry = getPref(preferences, 'geometry', None)
        if type(geometry) == QVariant and geometry.type() == QVariant.ByteArray and not geometry.isNull():
            self.restoreGeometry(geometry.toByteArray())
        state = getPref(preferences, 'state', None)
        if type(state) == QVariant and state.type() == QVariant.ByteArray and not geometry.isNull():
            self.restoreState(state.toByteArray())

        appPreferences = QtGui.qApp.preferences.appPrefs
        self.edtFileName.setText(
                getPrefString(appPreferences, 'fileName', ''))
        self.edtExportFileName.setText(
                getPrefString(appPreferences, 'exportFileName', ''))
        self.checkFileNames()


    def savePreferences(self):
        preferences = {}
        setPref(preferences,'geometry',QVariant(self.saveGeometry()))
        setPref(preferences,'state', QVariant(self.saveState()))
        setPref(QtGui.qApp.preferences.windowPrefs, self.objectName(), preferences)

        appPreferences = QtGui.qApp.preferences.appPrefs
        setPref(appPreferences, 'fileName',
            QVariant(self.edtFileName.text()))
        setPref(appPreferences, 'exportFileName',
            QVariant(self.edtExportFileName.text()))


    def setUserName(self, userName):
        title = u'Импорт номенклатуры'
        if userName:
            self.setWindowTitle(title + u': '+ userName)
        else:
            self.setWindowTitle(title)


    def updateStatus(self):
        pass


    @pyqtSignature('')
    def on_btnImport_clicked(self):
        fileName = forceString(self.edtFileName.text())
        self.processFile(fileName)


    @pyqtSignature('')
    def on_btnExport_clicked(self):
        fileName = forceString(self.edtExportFileName.text())

        dialog = CExportDialog(self)
        dialog.fileName = fileName
        dialog.exec_()


    def checkFileNames(self):
        self.btnImport.setEnabled(self.isLoggedIn() and
            not self.edtFileName.text().isEmpty())
        self.btnExport.setEnabled(self.isLoggedIn() and
            not self.edtExportFileName.text().isEmpty())


    def getOpenFileName(self, editor, mask):
        fileName = QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите файл с данными', editor.text(), mask)
        if fileName != '':
            editor.setText(QDir.toNativeSeparators(fileName))
            self.checkFileNames()


    def getSaveFileName(self, editor, mask):
        fileName = QtGui.QFileDialog.getSaveFileName(
            self, u'Укажите файл с данными', editor.text(), mask)
        if fileName != '':
            editor.setText(QDir.toNativeSeparators(fileName))
            self.checkFileNames()


    def isLoggedIn(self):
        app = QtGui.qApp
        return bool(app.db) and (app.demoMode or app.userId is not None)


    def updateActionsState(self):
        loggedIn = self.isLoggedIn()

        # Меню Сессия
        self.actLogin.setEnabled(not loggedIn)
        self.actLogout.setEnabled(loggedIn)
        self.actQuit.setEnabled(True)

        self.checkFileNames()


    @pyqtSignature('QString')
    def on_edtFileName_textChanged(self, text):
        self.checkFileNames()


    @pyqtSignature('')
    def on_btnSelectFileName_clicked(self):
        self.getOpenFileName(self.edtFileName, u'Файлы XML (*.xml)')


    @pyqtSignature('')
    def on_btnSelectExportFileName_clicked(self):
        self.getSaveFileName(self.edtExportFileName, u'Файлы XML (*.xml)')


    @pyqtSignature('')
    def on_actLogin_triggered(self):
        try:
            QtGui.qApp.openDatabase()
            prefs = QtGui.qApp.preferences.appPrefs
            isServiceMode = prefs.get('autoImport', False)
            if ((QtGui.qApp.demoModePosible() and QtGui.qApp.demoModeRequested)
                    or isServiceMode):
                QtGui.qApp.setUserId(None, True)
                self.setUserName('service' if isServiceMode else QtGui.qApp.userName())
                self.updateActionsState()
            else:
                dialog = CLoginDialog(self)
                dialog.setLoginName(QtGui.qApp.preferences.appUserName)
                if dialog.exec_():
                    QtGui.qApp.setUserId(dialog.userId(), dialog.demoMode())
                    QtGui.qApp.preferences.appUserName = dialog.loginName()
                    self.setUserName(QtGui.qApp.preferences.appUserName)
                    self.updateActionsState()
            return
        except database.CDatabaseException, e:
            QtGui.QMessageBox.critical(
                self,
                u'Ошибка открытия базы данных',
                unicode(e),
                QtGui.QMessageBox.Close)
        except Exception, e:
            QtGui.QMessageBox.critical(
                self,
                u'Ошибка открытия базы данных',
                u'Невозможно установить соедиенение с базой данных\n' + unicode(e),
                QtGui.QMessageBox.Close)
            QtGui.qApp.logCurrentException()
        QtGui.qApp.closeDatabase()


    @pyqtSignature('')
    def on_actLogout_triggered(self):
        QtGui.qApp.setUserId(None, False)
        QtGui.qApp.closeDatabase()
        self.setUserName('')
        self.updateActionsState()


    @QtCore.pyqtSignature('')
    def on_actConnection_triggered(self):
        dlg   = CConnectionDialog(self)
        preferences = QtGui.qApp.preferences
        dlg.setDriverName(preferences.dbDriverName)
        dlg.setServerName(preferences.dbServerName)
        dlg.setServerPort(preferences.dbServerPort)
        dlg.setDatabaseName(preferences.dbDatabaseName)
        dlg.setUserName(preferences.dbUserName)
        dlg.setPassword(preferences.dbPassword)
        if dlg.exec_():
            preferences.dbDriverName = dlg.driverName()
            preferences.dbServerName = dlg.serverName()
            preferences.dbServerPort = dlg.serverPort()
            preferences.dbDatabaseName = dlg.databaseName()
            preferences.dbUserName = dlg.userName()
            preferences.dbPassword = dlg.password()
            preferences.save()


    @pyqtSignature('')
    def on_actQuit_triggered(self):
        self.close()


    @QtCore.pyqtSignature('')
    def on_actAbout_triggered(self):
        global lastChangedRev
        global lastChangedDate
        try:
            from buildInfo import lastChangedRev, lastChangedDate
        except:
            lastChangedRev  = 'unknown'
            lastChangedDate = 'unknown'

        QtGui.QMessageBox.about(
            self, u'О программе', gAbout % ( gTitle, gVersion, lastChangedRev,
                                            lastChangedDate))


    @QtCore.pyqtSignature('')
    def on_actAboutQt_triggered(self):
        QtGui.QMessageBox.aboutQt(self, u'О Qt')


    @QtCore.pyqtSignature('')
    def on_actDefaults_triggered(self):
        qApp = QtGui.qApp
        dialog = CAppPreferencesDialog(self)
        prefs = qApp.preferences.appPrefs
        dialog.setProps(prefs)

        if dialog.exec_():
            isServiceEnabled = prefs.get('autoImport', False)
            prefs.update(dialog.props())

            if not isServiceEnabled and prefs.get('autoImport', False):
                pass # FIXME: service enable
            elif isServiceEnabled and not prefs.get('autoImport', False):
                pass # FIXME: service disable

            qApp.preferences.save()


    def processFile(self, fileName, auto=False):
        prefs = QtGui.qApp.preferences.appPrefs
        process = CProgressDialog(self, fileName, auto)
        process.setLogError(forceBool(prefs.get('logErrors', False)))
        process.setLogSuccess(forceBool(prefs.get('logSuccess', False)))
        process.setCreateNomenclature(forceBool(prefs.get(
            'createNomenclatureDuringImport', False)))
        QtGui.qApp.call(self, process.exec_)


    def prepareService(self):
        prefs = QtGui.qApp.preferences.appPrefs
        period = forceInt(prefs.get('autoImportScanPeriod', 1))
        self.scanTimer = QTimer()
        self.connect(self.scanTimer, SIGNAL('timeout()'), self.checkDir);
        self.scanTimer.start(period*10)


    def checkDir(self):
        self.scanTimer.stop()
        prefs = QtGui.qApp.preferences.appPrefs
        dirName = forceString(prefs.get('autoImportScanDir', ''))
        scanDir = QDir(dirName)

        for entry in scanDir.entryList(['*.ok']):
            entry = forceString(entry)
            fileName = u'{0}xml'.format(entry[:-2])
            self.processFile(os.path.join(dirName, fileName), auto=True)
            os.remove(os.path.join(dirName, entry))

        self.scanTimer.start()


def parseGCDebug(val):
    result = 0
    for char in val.upper():
        if char == 'S':
            result |= gc.DEBUG_STATS
        elif char == 'C':
            result |= gc.DEBUG_COLLECTABLE
        elif char == 'U':
            result |= gc.DEBUG_UNCOLLECTABLE
        elif char == 'I':
            result |= gc.DEBUG_INSTANCES
        elif char == 'O':
            result |= gc.DEBUG_OBJECTS
    return result

def parseGCThreshold(val):
    result = []
    if val:
        for s in val.split(','):
            try:
                v = int(s)
            except:
                v = 0
            result.append(v)
        l = len(result)
        if l > 3:
            result = result[0:3]
    return result


if __name__ == '__main__':
##    gc.set_threshold(*[10*k for k in gc.get_threshold()])
    parser = OptionParser(usage = "usage: %prog [options]")
    parser.add_option('-d', '--demo',
                      dest='demo',
                      help='Login as demo',
                      action='store_true',
                      default=False)
    parser.add_option('--gc-debug',
                      dest='gcDebug',
                      help='gc debug flags, chars S(stat), C(collectable), U(uncollectable), I(instances), O(objects), for details see gc.set_debug',
                      metavar='[S][C][U][I][O]',
                      default=''
                      )
    parser.add_option('--gc-threshold',
                      dest='gcThreshold',
                      help='gc thresholds list, see gc.set_threshold ',
                      metavar='threshold0[,threshold1[,threshold2]]',
                      default=''
                     )
    parser.add_option('--version',
                      dest='version',
                      help='print version and exit',
                      action='store_true',
                      default=False)
    parser.add_option('--service', dest='service',  help='Run as service',
                      action='store_true', default=False)
    (options, args) = parser.parse_args()

    if options.version:
        print '%s v.0.1' % (sys.argv[0] if sys.argv else '')
    else:
        gcDebug = parseGCDebug(options.gcDebug)
        gcThreshold = parseGCThreshold(options.gcThreshold)
        if gcDebug:
            gc.set_debug(gcDebug)
            print 'debug set to ', gcDebug
        if gcThreshold:
            gc.set_threshold(*gcThreshold)
            print 'threshold set to ', gcThreshold

        app = CMyApp(sys.argv, options.demo, options.service)
        stdTtranslator = QtCore.QTranslator()
        stdTtranslator.load('i18n/std_ru.qm')
        app.installTranslator(stdTtranslator)

        QtGui.qApp = app
        app.applyDecorPreferences() # надеюсь, что это поможет немного сэкономить при создании гл.окна
        mainWindow = CMainWindow(service=options.service)
        app.mainWindow = mainWindow
        app.applyDecorPreferences() # применение максимизации/полноэкранного режима к главному окну

        if app.preferences.dbAutoLogin:
            mainWindow.actLogin.activate(QtGui.QAction.Trigger)

        mainWindow.show()
        res = app.exec_()
        mainWindow.savePreferences()
        app.preferences.save()
        app.doneTrace()
        QtGui.qApp = None

#    sys.exit(res)
