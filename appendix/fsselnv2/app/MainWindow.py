# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2018-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

#import shutil
#import tempfile

from PyQt4                  import QtGui
from PyQt4.QtCore           import Qt, pyqtSignature, SIGNAL, QVariant

from library                import database
from library.Utils          import getPref, setPref, forceString, forceStringEx


from preferences.connection import CConnectionDialog
from preferences.decor      import CDecorDialog
from localPreferences.appPreferencesDialog import CAppPreferencesDialog

from Users.Login            import CLoginDialog
from Users.tryKerberosAuth  import tryKerberosAuth


from WorkSpace              import CWorkSpaceWindow
from Ui_MainWindow          import Ui_CMainWindow



class CMainWindow(QtGui.QMainWindow, Ui_CMainWindow):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setCentralWidget(self.centralwidget)
        self.loadPreferences()
        self.status = QtGui.QLabel(self)
        self.statusbar.addPermanentWidget(self.status)
        self.cashRegisterWindow = None
        self.actLogout.setEnabled(False)
        self.actAppPreferences.setEnabled(False)

#    def show(self):
#        QtGui.QMainWindow.show(self)
#        self.workSpaceWindow = CWorkSpaceWindow(self)
#        self.centralWidget().addSubWindow(self.workSpaceWindow, Qt.Window)
#        self.workSpaceWindow.setWindowState(Qt.WindowMaximized)


    def loadPreferences(self):
        preferences = getPref(QtGui.qApp.preferences.windowPrefs, self.objectName(), {})
        geometry = getPref(preferences, 'geometry', None)
        if type(geometry) == QVariant and geometry.type() == QVariant.ByteArray and not geometry.isNull():
            self.restoreGeometry(geometry.toByteArray())
        state = getPref(preferences, 'state', None)
        if type(state) == QVariant and state.type() == QVariant.ByteArray and not geometry.isNull():
            self.restoreState(state.toByteArray())


    def savePreferences(self):
        preferences = {}
        setPref(preferences,'geometry',QVariant(self.saveGeometry()))
        setPref(preferences,'state', QVariant(self.saveState()))
        setPref(QtGui.qApp.preferences.windowPrefs, self.objectName(), preferences)


    def setUserName(self, userName):
        app = QtGui.qApp
        if userName:
            orgStructureName = ''
            orgStructureId = QtGui.qApp.getCurrentOrgStructureId()
            if orgStructureId:
                db = QtGui.qApp.db
                orgStructureName = forceStringEx(db.translate('OrgStructure', 'id', orgStructureId, 'name'))
            self.setWindowTitle(u'%s: %s%s' % (app.title, userName, (u': %s'%(orgStructureName)) if orgStructureName else u''))
        else:
            self.setWindowTitle(app.title)


    @pyqtSignature('')
    def on_actLogin_triggered(self):
        ok = False
        try:
            QtGui.qApp.openDatabase()
            if QtGui.qApp.kerberosAuthEnabled():
                userId = tryKerberosAuth()
                if userId:
                    ok = True
                    login = forceString(QtGui.qApp.db.translate('Person', 'id', userId, 'login'))
            if not ok and QtGui.qApp.passwordAuthEnabled():
                dialog = CLoginDialog(self)
                dialog.setLoginName(QtGui.qApp.preferences.appUserName)
                if dialog.exec_():
                    ok, userId, login = True, dialog.userId(), dialog.loginName()
                else:
                    ok, userId, login = False, None, ''
                ok = ok and userId is not None
            if ok:
                QtGui.qApp.setUserId(userId)
                QtGui.qApp.preferences.appUserName = login
                self.setUserName(QtGui.qApp.userName())
#                self.updateActionsState()
                self.actLogin.setEnabled(False)
                self.actLogout.setEnabled(True)
                self.actAppPreferences.setEnabled(True)
        except database.CDatabaseException, e:
            QtGui.QMessageBox.critical(self,
                                       u'Ошибка открытия базы данных',
                                       unicode(e),
                                       QtGui.QMessageBox.Close)
        except Exception, e:
            QtGui.QMessageBox.critical(self,
                                       u'Ошибка открытия базы данных',
                                       u'Невозможно установить соедиенение с базой данных\n' + unicode(e),
                                       QtGui.QMessageBox.Close)
            QtGui.qApp.logCurrentException()
        finally:
            if ok:
                pass
            else:
                QtGui.qApp.closeDatabase()

        if ok:
            self.workSpaceWindow = CWorkSpaceWindow(self)
            self.centralWidget().addSubWindow(self.workSpaceWindow, Qt.Window)
            self.workSpaceWindow.setWindowState(Qt.WindowMaximized)


    @pyqtSignature('')
    def on_actLogout_triggered(self):
        if QtGui.qApp.db:
            if self.workSpaceWindow:
                self.workSpaceWindow.close()
            QtGui.qApp.clearUserId(True)
            self.setUserName(QtGui.qApp.userName())
            QtGui.qApp.closeDatabase()
            self.actLogin.setEnabled(True)
            self.actLogout.setEnabled(False)
            self.actAppPreferences.setEnabled(False)


    @pyqtSignature('')
    def on_actQuit_triggered(self):
        self.close()


    @pyqtSignature('')
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
    def on_actAppPreferences_triggered(self):
#        print " QtGui.qApp.db=%r" % (QtGui.qApp.db,)

        qApp = QtGui.qApp
        prevOrgId = qApp.getCurrentOrgId()
        prevOrgStructureId = qApp.getCurrentOrgStructureId()
        dialog = CAppPreferencesDialog(self)
        dialog.setProps(qApp.preferences.appPrefs)
        if dialog.exec_():
            qApp.preferences.appPrefs.update(dialog.props())
            qApp.preferences.save()
            orgId = qApp.getCurrentOrgId()
            self.setUserName(qApp.userName())
            if orgId != prevOrgId:
                qApp.emit(SIGNAL('currentOrgIdChanged()'))
            if QtGui.qApp.getCurrentOrgStructureId() != prevOrgStructureId:
                qApp.emit(SIGNAL('currentOrgStructureIdChanged()'))


    @pyqtSignature('')
    def on_actDecor_triggered(self):
        dlg = CDecorDialog(self)
        preferences = QtGui.qApp.preferences
        dlg.setStyle(preferences.decorStyle)
        dlg.setStandardPalette(preferences.decorStandardPalette)
        dlg.setMaximizeMainWindow(preferences.decorMaximizeMainWindow)
        dlg.setFullScreenMainWindow(preferences.decorFullScreenMainWindow)
        dlg.setUseCustomFont(preferences.useCustomFont)
        dlg.setFont(preferences.font)
        if dlg.exec_():
            preferences.decorStyle = dlg.style()
            preferences.decorStandardPalette = dlg.standardPalette()
            preferences.decorMaximizeMainWindow = dlg.maximizeMainWindow()
            preferences.decorFullScreenMainWindow = dlg.fullScreenMainWindow()
            preferences.useCustomFont = dlg.useCustomFont()
            preferences.font = dlg.font()
            preferences.save()
            QtGui.qApp.applyDecorPreferences()


    @pyqtSignature('')
    def on_actAbout_triggered(self):
        QtGui.QMessageBox.about(self, u'О программе', QtGui.qApp.getAbout() )


    @pyqtSignature('')
    def on_actAboutQt_triggered(self):
        QtGui.QMessageBox.aboutQt(self, u'О Qt')

