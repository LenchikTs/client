# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import *
from library.TableModel import *
from library.crbcombobox import CRBComboBox
from library.Utils import *

from RefBooks.Tables import *
from Ui_LocationCardEditor import Ui_LocationCardEditor


class CLocationCardTypeEditor(QtGui.QDialog, Ui_LocationCardEditor):
    def __init__(self,  parent, clientId):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.clientId = clientId
        self.record = None
        self.cmbLocationCardType.setTable('rbLocationCardType', True)
        self.cmbLocationCardType.setShowFields(CRBComboBox.showCodeAndName)
        self.setRecord()


    def setRecord(self):
        if self.clientId:
            db = QtGui.qApp.db
            table = db.table('Client_LocationCard')
            rbTable = db.table('rbLocationCardType')
            self.record = db.getRecordEx(table.innerJoin(rbTable, table['locationCardType_id'].eq(rbTable['id'])), 'Client_LocationCard.*', [table['deleted'].eq(0), table['master_id'].eq(self.clientId)], 'Client_LocationCard.id DESC')
            if self.record:
                self.cmbLocationCardType.setValue(forceRef(self.record.value('locationCardType_id')))
                self.cmbPerson.setValue(forceRef(self.record.value('person_id')))
                self.edtNotesPage.setPlainText(forceString(self.record.value('notesPage'))) 


    def getRecord(self):
        if self.clientId:
            db = QtGui.qApp.db
            if not self.record:
                self.record = db.record('Client_LocationCard')
                self.record.setValue('master_id', toVariant(self.clientId))
            self.record.setValue('locationCardType_id', toVariant(forceRef(self.cmbLocationCardType.value())))
            self.record.setValue('person_id', toVariant(forceRef(self.cmbPerson.value())))
            self.record.setValue('notesPage', toVariant(forceRef(self.edtNotesPage.toPlainText())))
        return self.record


    def save(self):
        try:
            db = QtGui.qApp.db
            db.transaction()
            try:
                record = self.getRecord()
                id = db.insertOrUpdate('Client_LocationCard', record)
                db.commit()
            except:
                db.rollback()
                raise
            return id
        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical( self,
                                        u'',
                                        unicode(e),
                                        QtGui.QMessageBox.Close)
            return None


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.save()
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.close()
