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

from PyQt4               import QtGui
from PyQt4.QtCore        import Qt, pyqtSignature

from library.crbcombobox import CRBComboBox
from library.Utils       import exceptionToUnicode, forceRef, toVariant

from Registry.Ui_StatusObservationClientEditor import Ui_StatusObservationClientEditor


class CStatusObservationClientEditor(QtGui.QDialog, Ui_StatusObservationClientEditor):
    def __init__(self,  parent, clientIdList):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.clientIdList = clientIdList
        self.recordList = []
        self.cmbStatusObservationType.setTable('rbStatusObservationClientType', True)
        self.cmbStatusObservationType.setShowFields(CRBComboBox.showCodeAndName)
        self.setRecord()


    def setRecord(self):
        if len(self.clientIdList) == 1:
            clientId = self.clientIdList[0]
            if clientId:
                db = QtGui.qApp.db
                table = db.table('Client_StatusObservation')
                rbTable = db.table('rbStatusObservationClientType')
                record = db.getRecordEx(table.leftJoin(rbTable, table['statusObservationType_id'].eq(rbTable['id'])), 'Client_StatusObservation.*', [table['deleted'].eq(0), table['master_id'].eq(clientId)], 'Client_StatusObservation.id DESC')
                if record:
                    self.cmbStatusObservationType.setValue(forceRef(record.value('statusObservationType_id')))


    def getRecord(self):
        db = QtGui.qApp.db
        for clientId in self.clientIdList:
            if clientId:
                record = db.record('Client_StatusObservation')
                record.setValue('master_id', toVariant(clientId))
                record.setValue('statusObservationType_id', toVariant(forceRef(self.cmbStatusObservationType.value())))
                self.recordList.append(record)
        return self.recordList


    def save(self):
        try:
            db = QtGui.qApp.db
            db.transaction()
            idlist = []
            try:
                if self.clientIdList:
                    recordList = self.getRecord()
                    for record in recordList:
                        idlist.append(db.insertOrUpdate('Client_StatusObservation', record))
                db.commit()
            except:
                db.rollback()
                raise
            return idlist
        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical( self,
                                        u'',
                                        exceptionToUnicode(e),
                                        QtGui.QMessageBox.Close)
            return None


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.save()
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.close()
