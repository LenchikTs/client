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

import requests

from PyQt4 import QtGui

from library.Utils  import exceptionToUnicode, forceString

from Events.Ui_LLO78Login import Ui_LLO78LoginDialog

import xml.etree.ElementTree as ET


class CLLO78LoginDialog(QtGui.QDialog, Ui_LLO78LoginDialog):
    def __init__(self, parent, clientInfo):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.clientInfo = clientInfo
        if not self.edtLogin.text() and QtGui.qApp.lloLogin():
            self.edtLogin.setText(QtGui.qApp.lloLogin())
        if not self.edtPassword.text() and QtGui.qApp.lloPassword():
            self.edtPassword.setText(QtGui.qApp.lloPassword())


    def accept(self):
        try:
            self.login = forceString(self.edtLogin.text())
            self.password = forceString(self.edtPassword.text())
            if not QtGui.qApp.lloLogin() or QtGui.qApp.lloLogin() != self.login:
                QtGui.qApp.preferences.appPrefs['edtlloLogin'] = self.login
            if not QtGui.qApp.lloPassword() or QtGui.qApp.lloPassword() != self.password:
                QtGui.qApp.preferences.appPrefs['edtlloPassword'] = self.password
            
            if self.login != '':
                url = QtGui.qApp.lloServiceUrl()
                fam, im, ot, ss, dr, policySeria, policyNumber, clientId, sex = self.clientInfo
                xml = """<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                        <soap:Body><GetCat xmlns="http://tempuri.org/">
                            <fam>%s</fam>
                            <im>%s</im>
                            <ot>%s</ot>
                            <ss>%s</ss>
                            <dr>%s</dr>
                            <user>%s</user>
                            <pass>%s</pass>
                        </GetCat></soap:Body>
                    </soap:Envelope>""" % (fam, im, ot, ss, dr, self.login, self.password)
                body = xml.encode('utf-8')
                #print(body.decode('utf-8'))
                headers = {'Content-Type': 'text/xml; charset=utf-8', 'Content-Length': str(len(body))}
                response = requests.post(url, data=body, headers=headers)
                content = response.content
                status = response.status_code
                #print(content.decode('utf-8'))
                QtGui.qApp.log('================================================================================\nLLO78Service', 'ResponseStatus ' + str(status) + ' ResponseContent:\n' + content.decode('utf-8'))
                self.ckatlList = []
                root = ET.fromstring(content)
                for DocumentElement in root.getiterator('DocumentElement'):
                    for queryTable in DocumentElement.getiterator('QueryTable'):
                        self.ckatlList.append(queryTable.find('c_katl').text)
                        self.servCode = queryTable.find('servCod').text
                        self.NPP = queryTable.find('NPP').text
                for answer in root.getiterator('answer'):
                    errorTag = answer.find('error')
                    if errorTag is not None:
                        errorMessage = errorTag.text
                    else:
                        errorMessage = answer.text
                    errorMessage = errorMessage + u'. Возможно на портале ЛЛО не зарегистрирован пациент' if errorMessage == u'Поиск не принес результата' else errorMessage
                    QtGui.QMessageBox.critical( self, u'', errorMessage, QtGui.QMessageBox.Close)
                    return
                QtGui.QDialog.accept(self)
                return
        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical( self,
                                        u'',
                                        exceptionToUnicode(e),
                                        QtGui.QMessageBox.Close)
