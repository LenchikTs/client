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

from PyQt4              import QtGui
from PyQt4.QtCore       import Qt, pyqtSignature

from library.DialogBase import CConstructHelperMixin
from library.InDocTable import CInDocTableModel
from Orgs.PersonComboBoxEx import CPersonFindInDocTableCol

from Ui_OperatingAssistents import Ui_OperatingAssistents


class COperatingAssistents(QtGui.QDialog, CConstructHelperMixin, Ui_OperatingAssistents):
    def __init__(self,  parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.addModels('Person', COperatingAssistentsModel(self))
        self.tblPerson.setModel(self.modelPerson)
        self.items = []


    def loadAssistentIdList(self, items):
        self.modelPerson.setItems(items)


    def setAssistentList(self, records):
        self.items = records


    def getAssistentList(self):
        return self.items


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.setAssistentList(self.modelPerson.items())
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.close()


class COperatingAssistentsModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'Person_ActionProperty', 'id', 'actionProperty_id', parent)
        self.addCol(CPersonFindInDocTableCol(u'Ассистент', 'person_id', 20, 'vrbPersonWithSpecialityAndOrgStr', parent=parent))

