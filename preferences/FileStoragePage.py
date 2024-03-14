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
## Страница настройки - файловое хранилище
##
#############################################################################

from PyQt4 import QtGui

from library.Utils import (
    forceString,
    toVariant, forceBool,
)

from Ui_FileStoragePage import Ui_fileStoragePage


class CFileStoragePage(Ui_fileStoragePage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


    def setProps(self, props):
        self.edtWebDAVUrl.setText(forceString(props.get('WebDAVUrl', '')))
        self.chkSaveWithSignatures.setChecked(forceBool(props.get('saveWithSignatures', False)))


    def getProps(self, props):
        props['WebDAVUrl'] = toVariant(self.edtWebDAVUrl.text())
        props['saveWithSignatures'] = toVariant(self.chkSaveWithSignatures.isChecked())


