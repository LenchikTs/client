# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2016-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Пункт меню, скрывающий под собой список прикреплённых файлов
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, QPoint

from .AttachedFile         import CAttachedFilesLoader, CAttachedFilesModel
from .AttachFilesPopup     import CAttachFilesPopup
from .AttachFilesTableFlag import CAttachFilesTableFlag


class CAttachAction(QtGui.QAction):
    u'Пункт меню, скрывающий под собой список прикреплённых файлов'

    def __init__(self,  text, parent):
        QtGui.QAction.__init__(self, text, parent)
        self.tableName  = None
        self.masterId   = None
#        self.modelFiles = None
        self._isEnabled = True

        self.__setEnabled()
        self.connect(self, SIGNAL('triggered()'), self.onTriggered)


    def setTable(self, tableName):
        self.tableName = tableName
        self.__setEnabled()


    def setMasterId(self, masterId):
        self.masterId = masterId
        self.__setEnabled()


    def setEnabled(self, val):
        self._isEnabled = val
        self.__setEnabled()


    def attachedFilesPresent(self):
        return bool(    self.tableName
                    and self.masterId
                    and CAttachedFilesLoader.itemsPresent(QtGui.qApp.webDAVInterface, self.tableName, self.masterId)>0
                   )


    def __setEnabled(self):
        val = self._isEnabled and self.attachedFilesPresent()
        if val != QtGui.QAction.isEnabled(self):
            QtGui.QAction.setEnabled(self, val)


    def onTriggered(self):
        modelFiles = CAttachedFilesModel(self)
        modelFiles.setInterface(QtGui.qApp.webDAVInterface)
        modelFiles.setTable(self.tableName)
        modelFiles.loadItems(self.masterId)

        screenPos = QtGui.QCursor.pos()
        widget = QtGui.qApp.focusWidget()
        if widget is None:
            widget = self.parentWidget()
        if widget:
            pos = widget.mapFromGlobal(screenPos)
            if 0<=pos.x()<=widget.width() and 0<=pos.y()<=widget.height():
                pass
            else:
                screenPos = widget.mapToGlobal(QPoint(8, 8))
        popup = CAttachFilesPopup(None)
        popup.setFlags(CAttachFilesTableFlag.canOpen | CAttachFilesTableFlag.canSave)
        popup.setModel(modelFiles)
        popup.move(screenPos)
        popup.exec_()
#        modelFiles.saveItems(self.masterId)


def getAttachAction(tableName, parent):
    result = CAttachAction(u'Прикреплённые файлы...', parent)
    result.setTable(tableName)
    return result
