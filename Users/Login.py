# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import hashlib

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature

from library.DialogBase import CDialogBase
from library.database import CTableRecordCache
from library.TableModel import CTableModel, CTextCol, CRefBookCol
from library.Utils import exceptionToUnicode, forceString, forceStringEx, forceRef

from Users.Tables import demoUserName, usrId, usrLogin, usrPassword, tblLogin

from Users.Ui_Login import Ui_LoginDialog
from Users.Ui_SelectPersonDialog import Ui_SelectPersonDialog


class CLoginDialog(QtGui.QDialog, Ui_LoginDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self._loginId = None
        self._personId = None
        self._demoMode = False


    def accept(self):
        try:
            login    = forceStringEx(self.edtLogin.text())
            password = forceString(self.edtPassword.text())

            if login != '':
                db = QtGui.qApp.db

                if db is None:
                    return

                tableLogin = QtGui.qApp.db.table(tblLogin)

                # фантазия на тему challenge-response
                # с одним усложнением - в базе храним
                # пароли хешированные md5
                # таким образом мы нигде не передаём пароль в открытом виде.
                if db.name == 'mysql':
                    db.query('SET @USTS = CONCAT(NOW(), RAND())')
                    ustsQuery = db.query('SELECT @USTS')
                    ustsQuery.first()
                    ustsRecord = ustsQuery.record()
                    usts = forceString(ustsRecord.value(0))
                    encodedPassword = unicode(password).encode('utf8')
                    hashedPassword = hashlib.md5(encodedPassword).hexdigest()
                    cond = [tableLogin[usrLogin].eq(login),
                            tableLogin['deleted'].eq(0),
                            ('MD5(CONCAT(@USTS,' + usrPassword +'))=\'%s\'') % hashlib.md5(usts+hashedPassword).hexdigest(),
                            ]
                else:
                    #TODO: придумать что то для посгри
                    encodedPassword = unicode(password).encode('utf8')
                    hashedPassword = hashlib.md5(encodedPassword).hexdigest()
                    cond = [tableLogin[usrLogin].eq(login),
                            tableLogin['deleted'].eq(0),
                            ('MD5(' + usrPassword +')=\'%s\'') % hashlib.md5(hashedPassword).hexdigest()
                            ]
                recordList = db.getRecordList(tableLogin, [usrId], cond, [usrId])
                if len(recordList) == 1:
                    record = recordList[0]
                    loginId = forceRef(record.value(usrId))
                    personList = getLoginPersonList(loginId)
                    if len(personList) == 1:
                        personId = personList[0]
                        self._loginId = loginId
                        self._personId = personId
                        self._demoMode = False
                        QtGui.QDialog.accept(self)
                        return
                    elif len(personList) > 1:
                        dialogSelectPerson = CPersonSelectDialog(self, personList=personList)
                        if dialogSelectPerson.exec_():
                            personId = dialogSelectPerson.getPersonId()
                            self._loginId = loginId
                            self._personId = personId
                            self._demoMode = False
                            QtGui.QDialog.accept(self)
                            return
                        QtGui.QDialog.reject(self)
                        return
                if login == demoUserName and password == '' and QtGui.qApp.demoModePosible():
                    self._loginId = None
                    self._personId = None
                    self._demoMode = True
                    QtGui.QDialog.accept(self)
                    return
            QtGui.QMessageBox.critical(self,
                                       u'Внимание',
                                       u'Имя пользователя или пароль неверны',
                                       QtGui.QMessageBox.Close)
        except Exception, e:
            QtGui.QMessageBox.critical(self,
                                       u'',
                                       exceptionToUnicode(e),
                                       QtGui.QMessageBox.Close)


    def loginId(self):
        return self._loginId


    def personId(self):
        return self._personId


    def userId(self):
        return self._personId


    def demoMode(self):
        return self._demoMode


    def setLoginName(self, loginName):
        self.edtLogin.setText(loginName)


    def loginName(self):
        return unicode(self.edtLogin.text())


class CPersonSelectDialog(CDialogBase, Ui_SelectPersonDialog):
    def __init__(self, parent, personList):
        CDialogBase.__init__(self, parent)
        self.tableModel = CPersonTableModel(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.tblPerson.setModel(self.tableModel)
        self.tblPerson.setSelectionModel(self.tableSelectionModel)
        self.tblPerson.installEventFilter(self)
        self._parent = parent
        self.tblPerson.model().setIdList(personList)


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.personId = self.tblPerson.selectedItemIdList()[-1]
            QtGui.QDialog.accept(self)
            self.close()
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.close()


    @pyqtSignature('QModelIndex')
    def on_tblPerson_doubleClicked(self, index):
        self.personId = self.tblPerson.selectedItemIdList()[-1]
        QtGui.QDialog.accept(self)
        self.close()


    def getPersonId(self):
        return self.personId


class CPersonTableModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent)
        self._parent = parent
        self.addColumn(CTextCol(u'Код', ['code'], 5))
        self.addColumn(CTextCol(u'ФИО', ['name'], 15))
        self.addColumn(CRefBookCol(u'Должность', ['post_id'], 'rbPost', 15))
        self.addColumn(CRefBookCol(u'Специальность', ['speciality_id'], 'rbSpeciality', 10))
        self.addColumn(CRefBookCol(u'Подразделение', ['orgStructure_id'], 'OrgStructure', 10))
        self.addColumn(CTextCol(u'Профиль прав', ['userProfileName'], 20))
        self._fieldNames = [
            'vrbPerson.code',
            'vrbPerson.name',
            'Person.post_id',
            'vrbPerson.speciality_id',
            'vrbPerson.orgStructure_id',
            'rbUserProfile.name as userProfileName',
        ]
        self._tableName = u''
        self.setTable('vrbPerson')


    def setTable(self, tableName='vrbPerson', recordCacheCapacity=300):
        self._tableName = tableName
        db = QtGui.qApp.db
        tableVRBPerson = db.table(tableName)
        tablePerson = db.table('Person')
        tableUserProfile = db.table('rbUserProfile')
        loadFields = []
        loadFields.append(u'DISTINCT ' + u', '.join(self._fieldNames))
        table = tableVRBPerson.innerJoin(tablePerson, tablePerson['id'].eq(tableVRBPerson['id']))
        table = table.leftJoin(tableUserProfile, tableUserProfile['id'].eq(tablePerson['userProfile_id']))
        self._table = table
        self._recordsCache = CTableRecordCache(db, self._table, loadFields)


def getLoginPersonList(loginId):
    db = QtGui.qApp.db
    tableLoginPerson = db.table('Login_Person')
    tablePerson = db.table('Person')
    table = tableLoginPerson.leftJoin(tablePerson, tablePerson['id'].eq(tableLoginPerson['person_id']))
    cond = [tableLoginPerson['master_id'].eq(loginId),
            tablePerson['retireDate'].isNull(),
            tablePerson['userProfile_id'].isNotNull(),
            tablePerson['retired'].eq(0)
            ]
    return db.getIdList(table, idCol='person_id', where=cond)
