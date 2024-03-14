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
## Страница настройки - отчёты
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, QDir

from library.Utils            import (
                                         forceString,
                                         toVariant,
                                     )

from Ui_ReportPage import Ui_reportPage


class CReportPage(Ui_reportPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


    def setProps(self, props):
        self.edtDocumentEditor.setText(forceString(props.get('documentEditor',  '')))
        self.edtExtGenRep.setText(forceString(props.get('extGenRep',  '')))
        self.edtExaroEditor.setText(forceString(props.get('exaroEditor', '')))


    def getProps(self, props):
        props['documentEditor']         = toVariant(self.edtDocumentEditor.text())
        props['extGenRep']              = toVariant(self.edtExtGenRep.text())
        props['exaroEditor']            = toVariant(self.edtExaroEditor.text())


    @pyqtSignature('')
    def on_btnSelectDocumentEditor_clicked(self):
        fileName = forceString(QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите исполняемый файл редактора документов',
            self.edtDocumentEditor.text(), u'Исполняемые файлы (*)'))
        if fileName:
            self.edtDocumentEditor.setText(QDir.toNativeSeparators(fileName))


    @pyqtSignature('')
    def on_btnSelectExtGenRep_clicked(self):
        fileName = forceString(QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите исполняемый файл генератора отчетов',
            self.edtExtGenRep.text(), u'Исполняемые файлы (*)'))

        if fileName:
            self.edtExtGenRep.setText(QDir.toNativeSeparators(fileName))


    @pyqtSignature('')
    def on_btnSelectExaroEditor_clicked(self):
        fileName = forceString(QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите исполняемый файл редактора отчетов Exaro',
            self.edtExaroEditor.text(), u'Исполняемые файлы (*)'))

        if fileName:
            self.edtExaroEditor.setText(QDir.toNativeSeparators(fileName))

