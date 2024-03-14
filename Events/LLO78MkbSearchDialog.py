# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4                   import QtGui, QtCore
from PyQt4.QtCore            import pyqtSignature, SIGNAL, QObject

from library.DialogBase      import CDialogBase
from library.Utils           import exceptionToUnicode
from Ui_LLO78MkbSearch       import Ui_LLO78MkbSearchDialog

import requests
import xml.etree.ElementTree as ET


class CLLO78MkbSearchDialog(CDialogBase, Ui_LLO78MkbSearchDialog):
    idFieldName = 'id'
    def __init__(self, parent, ckatl, login, password, servCode):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.ckatl = ckatl
        self.login = login
        self.password = password
        self.servCode = servCode
        self.currentMkbCode = None
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinMaxButtonsHint)
    
    
    @pyqtSignature('')
    def on_btnGetMkb_clicked(self):
        try:
            nameds = self.edtDiagnosisSearch.text()
            xmlGetMkb = """<?xml version="1.0" encoding="utf-8"?>
                             <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                             xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                             xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                              <soap:Body>
                               <GetMkb xmlns="http://tempuri.org/">
                                <nameds>%s</nameds>
                                <ckatl>%s</ckatl>
                                <user>%s</user>
                                <pass>%s</pass>
                                <serv>%s</serv>
                               </GetMkb>
                              </soap:Body>
                             </soap:Envelope>
                          """ % (nameds, self.ckatl, self.login, self.password, self.servCode)
            body = xmlGetMkb.encode('utf-8')
            #print(body.decode('utf-8'))
            headers = {'Content-Type': 'text/xml; charset=utf-8', 'Content-Length': str(len(body))}
            serviceUrl = QtGui.qApp.lloServiceUrl()
            response = requests.post(serviceUrl, data=body, headers=headers)
            content = response.content
            status = response.status_code
            #print(content.decode('utf-8'))
            QtGui.qApp.log('================================================================================\nLLO78Service', 'ResponseStatus ' + str(status) + ' ResponseContent:\n' + content.decode('utf-8'))
            diagnosisData = []
            root = ET.fromstring(content)
            hasTagsWithData = False
            for NewDataSet in root.getiterator('NewDataSet'):
                for tableTag in NewDataSet.getiterator('Table'):
                    hasTagsWithData = True
                    diagnosisData.append([])
                    diagnosisData[-1].append(tableTag.find('ds').text)
                    diagnosisData[-1].append(tableTag.find('name_Ds').text)
            if not hasTagsWithData:
                QtGui.QMessageBox.critical( self, u'', u'Диагнозы в сервисе ЛЛО не найдены', QtGui.QMessageBox.Close)
            self.tblRecievedDiagnosises.setRowCount(len(diagnosisData))
            self.tblRecievedDiagnosises.setColumnCount(2)
            self.tblRecievedDiagnosises.setHorizontalHeaderLabels([u'Код МКБ', u'Наименование'])
            for i, lp in enumerate(diagnosisData):
                for j, item in enumerate(lp):
                    self.tblRecievedDiagnosises.setItem(i, j, QtGui.QTableWidgetItem(item))
            self.tblRecievedDiagnosises.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            self.tblRecievedDiagnosises.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
            self.tblRecievedDiagnosises.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
            QObject.connect(self.tblRecievedDiagnosises, SIGNAL('clicked(QModelIndex)'), self.on_tblRecievedDiagnosises_clicked)
        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical( self,
                                        u'',
                                        exceptionToUnicode(e),
                                        QtGui.QMessageBox.Close)


    @pyqtSignature('')
    def on_tblRecievedDiagnosises_clicked(self):
        index = self.tblRecievedDiagnosises.currentIndex()
        if index.isValid():
            row = index.row()
        self.tblRecievedDiagnosises.setCurrentCell(row, 0)
        itemCode = self.tblRecievedDiagnosises.currentItem()
        self.currentMkbCode = itemCode.data(0).toString()


    def accept(self):
        if self.currentMkbCode:
            QtGui.QDialog.accept(self)
            return
        else:
            QtGui.QMessageBox.critical( self, u'', u'Диагноз не определен', QtGui.QMessageBox.Close)
