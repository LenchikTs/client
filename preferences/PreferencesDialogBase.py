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
## Базовый класс диалога настроек
##
#############################################################################

from PyQt4.QtCore import Qt, pyqtSignature

from library.DialogBase import CDialogBase

from Ui_Preferences import Ui_preferencesDialog


class CPreferencesDialogBase(Ui_preferencesDialog, CDialogBase):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.pages = []


    def exec_(self):
        self.pagesList.setCurrentRow(0)
        return CDialogBase.exec_(self)


    def addPage(self, page):
        self.pages.append(page)


    def setupUi(self, holder):
        Ui_preferencesDialog.setupUi(self, holder)
        for page in self.pages:
            pageName = unicode(page.objectName())
            self.__setattr__(pageName, page)
            self.pagesHolder.addWidget(page)
            idx = self.pagesList.count()
            self.pagesList.addItem(page.windowTitle())
            item = self.pagesList.item(idx)
            item.setData(Qt.UserRole, pageName)
            item.setData(Qt.ToolTipRole, page.toolTip())

#        page.setProperty('list_index', idx)
#        print page.property('list_index').toString()


    def enablePage(self, page, enable):
        pageName = unicode(page.objectName())
        for idx in xrange(self.pagesList.count()):
            item = self.pagesList.item(idx)
            if item.data(Qt.UserRole).toString() == pageName:
                if enable:
                    item.setFlags((item.flags() & ~Qt.ItemIsEnabled) | Qt.ItemIsEnabled)
                else:
                    item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                page.setEnabled(enable)

#        self.pagesList.item()

    def setProps(self, props):
        for i in xrange(self.pagesHolder.count()):
            page = self.pagesHolder.widget(i)
            if page.isEnabled():
                page.setProps(props)


    def getProps(self):
        props = {}
        for i in xrange(self.pagesHolder.count()):
            page = self.pagesHolder.widget(i)
            if page.isEnabled():
                page.getProps(props)
        return props


    @pyqtSignature('int')
    def on_pagesList_currentRowChanged(self, currentRow):
        self.pagesHolder.setCurrentIndex(currentRow)
