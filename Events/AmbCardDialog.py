# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2015-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignature

from library.DialogBase    import CDialogBase

from Registry.Utils        import CClientInfo, getClientBanner, getClientSexAge

from Events.Ui_AmbCardDialog   import Ui_AmbCardDialog
from library.PrintInfo import CInfoContext
from library.PrintTemplates import applyTemplate


class CAmbCardDialog(CDialogBase, Ui_AmbCardDialog):
    def __init__(self, parent=None, clientId=None):
        CDialogBase.__init__(self, parent)

        self.addObject('actPortal_Doctor', QtGui.QAction(u'Перейти на портал врача', self))
        self.setupUi(self)

        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setClientId(clientId)
        self.ambCardPageWidget.resetWidgets()
        self.txtClientInfoBrowser.actions.append(self.actPortal_Doctor)


    def setClientId(self, clientId):
        self._clientId = clientId
        self._clientSex, self._clientAge = getClientSexAge(self._clientId)
        if clientId:
            self.txtClientInfoBrowser.setHtml(getClientBanner(clientId))
        else:
            self.txtClientInfoBrowser.setText('')
        self.ambCardPageWidget.setClientId(clientId, self._clientSex, self._clientAge)

    @pyqtSignature('')
    def on_actPortal_Doctor_triggered(self):
        templateId = None
        result = QtGui.qApp.db.getRecordEx('rbPrintTemplate', 'id',
                                           '`default` LIKE "%s" AND deleted = 0' % ('%/EMK_V3/indexV2.php%'))
        context = CInfoContext()
        clientInfo = context.getInstance(CClientInfo, self._clientId)
        data = {'client': clientInfo}

        if result:
            templateId = result.value('id').toString()
            if templateId:
                QtGui.qApp.call(self, applyTemplate, (self, templateId, data))
            else:
                QtGui.QMessageBox.information(self, u'Ошибка', u'Шаблон для перехода на портал врача не найден',
                                              QtGui.QMessageBox.Close, QtGui.QMessageBox.Close)
        else:
            QtGui.QMessageBox.information(self, u'Ошибка', u'Шаблон для перехода на портал врача не найден',
                                          QtGui.QMessageBox.Close, QtGui.QMessageBox.Close)