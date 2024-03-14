# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2016-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Всплывающее окно со списком прикреплённых файлов
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignature, QEvent, QMetaObject

from library.adjustPopup import adjustPopupToWidget, adjustPopupToScreen
from .AttachFilesTable import CAttachFilesTable


class CAttachFilesPopup(QtGui.QFrame):
    u'Всплывающее окно со списком прикреплённых файлов'

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
#        QtGui.QFrame.__init__(self, parent, Qt.Window)
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        # self.setAttribute(Qt.WA_DeleteOnClose)
#        self.setWindowModality(Qt.NonModal)
        self.layout = QtGui.QGridLayout(self)
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0,0,0,0)
        self.tblFiles = CAttachFilesTable(self)
        self.tblFiles.setObjectName('tblFiles')
        self.tblFiles.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.tblFiles.setFrameShape(QtGui.QFrame.NoFrame)

        self.layout.addWidget(self.tblFiles, 0, 0, 1, 1)
        self.setFocusProxy(self.tblFiles)

        self.sizeGrip = QtGui.QSizeGrip(self)
        self.layout.addWidget(self.sizeGrip, 1, 0, 1, 1, Qt.AlignBottom | Qt.AlignRight)

        QMetaObject.connectSlotsByName(self)


    def setFlags(self, flags):
        self.tblFiles.setFlags(flags)


    def setModel(self, modelFiles):
        self.tblFiles.setModel(modelFiles)


    def exec_(self):
        self.tblFiles.resizeColumnsToContents()
        self.tblFiles.resizeRowsToContents()
        self.resize(self.sizeHint())
        if self.parentWidget():
            adjustPopupToWidget(self.parentWidget(), self)
        else:
            adjustPopupToScreen(self)
        self.show()
        self.setFocus(Qt.OtherFocusReason)
        # eventLoop = QEventLoop()
        # self.connect(self, SIGNAL('destroyed()'), eventLoop.quit)
        # eventLoop.exec_()


    def event(self, event):
        if event.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonDblClick, QEvent.MouseButtonRelease):
            if not self.rect().contains(event.pos()):
                parentWidget = self.parentWidget()
                if ( parentWidget
                    and parentWidget.rect().contains(parentWidget.mapFromGlobal(event.globalPos()))
                   ):
#                    print self.parentWidget().rect().contains(self.mapToParent(event.pos()))
                    self.setAttribute(Qt.WA_NoMouseReplay, True)
        return QtGui.QFrame.event(self, event)

#    def mousePressEvent(self, event):
#        print 'mousePressEvent',  event, event.type()
#        QtGui.QFrame.mousePressEvent(self, event)
#
#
#    def closeEvent(self, event):
#        print 'closeEvent',  event, event.type()
#        QtGui.QFrame.closeEvent(self, event)


    @pyqtSignature('')
    def on_tblFiles_iteractionDone(self):
        self.close()
