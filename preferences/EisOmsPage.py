# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Страница настройки соединения с ЕИС ОМС (СПб)
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature

from library.database         import connectDataBase
from library.Utils            import (
                                         forceInt,
                                         forceString,
                                         forceStringEx,
                                         toVariant,
                                     )

from Ui_EisOmsPage import Ui_eisOmsPage


class CEisOmsPage(Ui_eisOmsPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


    def setProps(self, props):
        self.cmbDriverName.setEditText(forceString(props.get('EIS_driverName', '')))
        self.edtServerName.setText(forceString(props.get('EIS_serverName', '')))
        self.edtServerPort.setValue(forceInt(props.get('EIS_serverPort', 0)))
        self.edtDatabaseName.setText(forceString(props.get('EIS_databaseName', '')))
        self.edtUserName.setText(forceString(props.get('EIS_userName', '')))
        self.edtPassword.setText(forceString(props.get('EIS_password', '')))


    def getProps(self, props):
        props['EIS_driverName']   = toVariant(self.cmbDriverName.currentText())
        props['EIS_serverName']   = toVariant(self.edtServerName.text())
        props['EIS_serverPort']   = toVariant(self.edtServerPort.value())
        props['EIS_databaseName'] = toVariant(self.edtDatabaseName.text())
        props['EIS_userName']     = toVariant(self.edtUserName.text())
        props['EIS_password']     = toVariant(self.edtPassword.text())


    @pyqtSignature('')
    def on_btnEisTest_clicked(self):
        try:
            EIS_db=QtGui.qApp.EIS_db
            if not EIS_db:
                EIS_dbDriverName=forceStringEx(self.cmbDriverName.currentText())
                EIS_dbServerName=forceStringEx(self.edtServerName.text())
                EIS_dbServerPort=forceInt(self.edtServerPort.value())
                EIS_dbDatabaseName=forceStringEx(self.edtDatabaseName.text())
                EIS_dbUserName=forceStringEx(self.edtUserName.text())
                EIS_dbPassword=forceStringEx(self.edtPassword.text())
                EIS_db = connectDataBase(
                    EIS_dbDriverName, EIS_dbServerName, EIS_dbServerPort,
                    EIS_dbDatabaseName, EIS_dbUserName, EIS_dbPassword, 'EIS')
                QtGui.qApp.EIS_db=EIS_db
            TARIFF_MONTH=EIS_db.getRecordEx('TARIFF_MONTH', '*', '')
            ID_TARIFF_MONTH=forceString(TARIFF_MONTH.value('ID_TARIFF_MONTH'))
            TARIFF_MONTH_BEG=forceString(TARIFF_MONTH.value('TARIFF_MONTH_BEG').toDate())
            TARIFF_MONTH_END=forceString(TARIFF_MONTH.value('TARIFF_MONTH_END').toDate())
            MU_IDENT = EIS_db.getRecordEx('MU_IDENT', 'ID_LPU')
            ID_LPU = forceInt(MU_IDENT.value('ID_LPU')) if MU_IDENT else None
            message=u'Соединение успешно!\nтарифный месяц: %s (%s-%s)\nИдентификатор ЛПУ в ЕИС ОМС: %s' % (ID_TARIFF_MONTH, TARIFF_MONTH_BEG, TARIFF_MONTH_END, ID_LPU)
            QtGui.qApp.EIS_db.close()
            QtGui.qApp.EIS_db=None
        except:
            QtGui.qApp.logCurrentException()
            if QtGui.qApp.EIS_db:
                QtGui.qApp.EIS_db.close()
                QtGui.qApp.EIS_db=None
            message=u'Установить соединение не удалось'
        QtGui.QMessageBox.information(self, u'Проверка обращения к серверу ЕИС',
            message, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

