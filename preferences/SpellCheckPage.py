# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Страница настроек проверки орфографии
##
#############################################################################

from PyQt4              import QtGui
from PyQt4.QtCore       import pyqtSignature, QUrl, QDir

from library.Utils      import forceBool, toVariant, forceString
from library.SpellCheck import gSpellCheckAvailable
from Ui_SpellCheckPage  import Ui_spellCheckPage
from os.path            import isfile


class CSpellCheckPage (Ui_spellCheckPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


    def setProps(self, props):
        if gSpellCheckAvailable:
            self.chkSpellCheckHighlight.setChecked(forceBool(props.get('showingSpellCheckHighlight', True)))
            pathToDict = forceString(props.get('edtPathToPersonalDict', ''))
            if not isfile(unicode(pathToDict)):
                pathToDict = QtGui.qApp.getDefaultPathToDictionary()
            self.edtPathToPersonalDict.setText(pathToDict)
        else:
            self.chkSpellCheckHighlight.setChecked(False)
            self.chkSpellCheckHighlight.setEnabled(False)
            self.edtPathToPersonalDict.setEnabled(False)


    def getProps(self, props):
        props['showingSpellCheckHighlight'] = toVariant(self.chkSpellCheckHighlight.isChecked())
        props['edtPathToPersonalDict']      = toVariant(self.edtPathToPersonalDict.text())


    @pyqtSignature('')
    def on_btnEditPersonalDict_clicked(self):
        #pathToDict = QtGui.qApp.getPathToDictionary()
        pathToDict = self.edtPathToPersonalDict.text()

        if not isfile(unicode(pathToDict)):
            errorDictMessage = u'Словарь не настроен'
            QtGui.QMessageBox.information(self, u'Произошла ошибка', errorDictMessage, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            return

        QtGui.QDesktopServices.openUrl(QUrl.fromLocalFile(pathToDict))


    @pyqtSignature('')
    def on_btnSelectPathToPersonalDict_clicked(self):
        if not self.edtPathToPersonalDict.text():
            self.edtPathToPersonalDict.setText(QtGui.qApp.getDefaultPathToDictionary())
        fileName = forceString(QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите путь к персональному словарю',
            self.edtPathToPersonalDict.text(), u'Текстовые файлы (*.txt)'))
        if fileName:
            self.edtPathToPersonalDict.setText(QDir.toNativeSeparators(fileName))
