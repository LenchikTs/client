# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, Qt

from library.DialogBase import CDialogBase
from library.PrintTemplates import getPrintButton
from library.Utils import calcAge, formatDate, formatName, formatSex

from Registry.Utils import getClientInfo

from Reports.ReportView import CReportViewDialog

from Ui_AmbulatoryCardDialog import Ui_AmbulatoryCardDialog


class CAmbulatoryCardDialog(CDialogBase, Ui_AmbulatoryCardDialog):
    def __init__(self, parent=None, clientId=None):
        CDialogBase.__init__(self, parent)
        self.addObject('btnPrint', getPrintButton(self, '', u'Печать'))
        self.setupUi(self)
        self.buttonBox.addButton(self.btnPrint, QtGui.QDialogButtonBox.ActionRole)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)

        self.btnPrint.setEnabled(True)
        if clientId:
            self.setClientId(clientId)

    def exec_(self):
        self.loadDialogPreferences()
        result = QtGui.QDialog.exec_(self)
        return result

    @pyqtSignature('')
    def on_btnPrint_clicked(self):
        html = self.ambulatoryCardPage.txtAmbulatoryCardReport.toHtml()
        view = CReportViewDialog(self)
        view.setText(html)
        view.exec_()

    def setClientId(self, clientId):
        self.ambulatoryCardPage.setClientId(clientId)
        self.setWindowTitle(u'Пациент: %s' % (getClientString(clientId) if clientId else u'не известен'))


def getClientString(clientId, atDate=None):
    info = getClientInfo(clientId)
    return formatClientString(info, atDate)


def formatClientString(info, atDate=None):
    clientId = info.id
    name = formatName(info.lastName, info.firstName, info.patrName)
    birthDate = formatDate(info.birthDate)
    age = calcAge(info.birthDate, atDate)
    sex = formatSex(info.sexCode)
    bannerHTML = u'''%s, дата рождения: %s (%s)  пол: %s  код: %s''' % (name, birthDate, age, sex, clientId)
    clientBanner = u'%s' % bannerHTML
    return clientBanner
