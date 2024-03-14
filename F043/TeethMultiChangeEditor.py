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
##
## Форма 043: стоматология и другие зубные дела
##
#############################################################################


from PyQt4 import QtGui
from PyQt4.QtCore import Qt, SIGNAL

# WFT, хаскеры?

class CTeethMultiChangeEditor(QtGui.QDialog):
    def __init__(self, parent, editorTypeList={}):
        QtGui.QDialog.__init__(self, parent)
        self._resultCache = {}
        self.vLayout = QtGui.QVBoxLayout(self)
        editorTypeKeyList = editorTypeList.keys()
        editorTypeKeyList.sort(key=lambda item: item[1])
        for editorTypeKey in editorTypeKeyList:
            editor = editorTypeKey[0](*editorTypeList[editorTypeKey])
            if parent.selectionModel().selectedIndexes()[0].row() in [0, 7]:
                if editor and hasattr(editor, 'setRBComboBoxMark'):
                    editor.setRBComboBoxMark(True)
            editor.setParent(self)
            self.vLayout.addWidget(editor)
            self._resultCache[editorTypeKey] = editor.value
        self.vLayout.addStretch()

        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok,
                                          Qt.Horizontal,
                                          self)
        self.vLayout.addWidget(self.buttonBox)

        self.setLayout(self.vLayout)

        self.connect(self.buttonBox, SIGNAL('accepted()'), self.accept)
        self.connect(self.buttonBox, SIGNAL('rejected()'), self.reject)

        self.setWindowTitle(u'Изменение значений зуба')

    def values(self):
        return self._resultCache

