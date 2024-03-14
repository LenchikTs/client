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
import threading

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, Qt
from time import sleep

from Ui_DBReconnectProgressDialog import Ui_DialogDBReconnect

class ConnectBackgroundWorker (threading.Thread): #TODO переделать на QThread?
   def __init__(self, parent, runType):
       threading.Thread.__init__(self)
       self.parent = parent
       self.runType = runType

   def run(self):
       sleep(1)
       if self.runType == 1:
            self.tryConnect()
       elif self.runType == 2:
           self.progreeBarProcess()

   def progreeBarProcess(self):
       counterProgress = 0
       while (self.parent.tryConnection == 1):
           #print ('start progress')
           counterProgress = counterProgress + 1
           self.parent.progressBar.setValue(counterProgress)

           sleep(0.1)

           if self.parent.progressBar.value() >= self.parent.progressBar.maximum():
               counterProgress = 0
               self.parent.progressBar.setValue(counterProgress)

   def tryConnect(self):
        while (self.parent.tryConnection == 1):
            #print ('start conncet')
            try:
                self.parent.dbconnection.remoteConnect()
            except Exception:
                pass
            if (self.parent.dbconnection.execDBNotCheck("select 1 as id from dual") == 1):
                self.parent.tryConnection = 0
                self.parent.close()
            #print ('before sleep')
            sleep(1)

class CDBReconnectProgressDialog(Ui_DialogDBReconnect, QtGui.QDialog):

    def __init__(self, parent, parentg):

        QtGui.QDialog.__init__(self, parentg)
        self.dbconnection = parent
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.tryConnection = 1

    def exec_(self):
        backgroundWorker = ConnectBackgroundWorker(self, 1)
        backgroundWorker.start()
        #backgroundWorkerPr = ConnectBackgroundWorker(self, 2)
        #backgroundWorkerPr.start()
        return QtGui.QDialog.exec_(self)

    @pyqtSignature('')
    def on_abortBtn_clicked(self):
        self.tryConnection = 0
        self.dbconnection.isCloseApp = 1
        self.close()
        self.dbconnection.parentGl.close()
