# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QEvent, QString, pyqtSignature, SIGNAL


from library.Utils      import forceStringEx
from KLADR.KLADRModel   import CKLADRSearchModel, getKladrTreeModel

from KLADR.Ui_KLADRTree import Ui_KLADRTreePopup


class CKLADRTreePopup(QtGui.QFrame, Ui_KLADRTreePopup):
    __pyqtSignals__ = ('codeSelected(QString)',
                       'codeSelected(QModelIndex)',
                      )

    def __init__(self, parent = None):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setAttribute(Qt.WA_WindowPropagation)
        self.treeModel = getKladrTreeModel()
        self.tableModel = CKLADRSearchModel(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel,  self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.treeView.setModel(self.treeModel)
        self.treeView.setUniformRowHeights(True)
        self.treeView.setAllColumnsShowFocus(True)
#        self.treeView.setColumnWidth(0, self.treeView.indentation()*5+textWidth)
        self.tblSearchResult.horizontalHeader().hide()
        self.tblSearchResult.setModel(self.tableModel)
        self.tblSearchResult.setSelectionModel(self.tableSelectionModel)

        self.tabTree.setFocusProxy(self.treeView)
        self.tabSearch.setFocusProxy(self.edtWords)
        self.edtWords.installEventFilter(self)


    def mousePressEvent(self, event):
        parent = self.parentWidget()
        if parent!=None:
            opt=QtGui.QStyleOptionComboBox()
            opt.init(parent)
            arrowRect = parent.style().subControlRect(
                QtGui.QStyle.CC_ComboBox, opt, QtGui.QStyle.SC_ComboBoxArrow, parent)
            arrowRect.moveTo(parent.mapToGlobal(arrowRect.topLeft()))
            if (arrowRect.contains(event.globalPos()) or self.rect().contains(event.pos())):
                self.setAttribute(Qt.WA_NoMouseReplay)
        QtGui.QFrame.mousePressEvent(self, event)


    def eventFilter(self, watched, event):
        if watched == self.edtWords:
            if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Select):
                event.accept()
                self.btnSearch.animateClick()
#                self.btnSearch.emit(SIGNAL('click()'))
                return True
        return QtGui.QFrame.eventFilter(self, watched, event)
        
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.selectCode('')
            event.accept()
        else:
            QtGui.QFrame.keyPressEvent(self, event)


#    def mouseReleaseEvent(self, event):
##        self.emit(SIGNAL('resetButton()'))
#        self.parent().mouseReleaseEvent(event)
#        pass

    def beforeShow(self):
        self.tabWidget.setCurrentIndex(0)
        self.treeView.setFocus()
        self.edtWords.clear()
        self.treeView.setExpanded(self.treeView.currentIndex(), True)


    def setCurrentIndex(self, index):
        if self.treeView.currentIndex() != index:
            self.treeView.collapseAll()
            self.treeView.scrollTo(index)
            self.treeView.setCurrentIndex(index)
            self.treeView.setExpanded(index, True)


    def setCurrentCode(self, code):
        if code:
            index = self.treeModel.findCode(code)
            self.setCurrentIndex(index)


    def selectIndex(self, index):
        self.emit(SIGNAL('codeSelected(QModelIndex)'), index)
        self.close()


    def selectCode(self, code):
        self.emit(SIGNAL('codeSelected(QString)'), QString(code))
        self.close()


    def getCurrentCode(self):
        index = self.tblSearchResult.currentIndex()
        code = self.tableModel.code(index.row())
        return code


    @pyqtSignature('int')
    def on_tabWidget_currentChanged(self, index):
        if index == 0:
            code = self.getCurrentCode()
            self.setCurrentCode(code)


    @pyqtSignature('QModelIndex')
    def on_treeView_doubleClicked(self, index):
        flags = self.treeModel.flags(index)
        if flags & Qt.ItemIsSelectable:
            self.selectIndex(index)


    @pyqtSignature('')
    def on_btnSearch_clicked(self):
        prefix = ''
        keyboardModifiers = QtGui.qApp.keyboardModifiers()
        if not(keyboardModifiers & (Qt.AltModifier|Qt.ShiftModifier)):
            index = self.treeView.currentIndex()
            item = index.internalPointer()
            if item:
                prefix = item.prefix()
        searchString = forceStringEx(self.edtWords.text())
        self.tableModel.setFilter(prefix, searchString)


    @pyqtSignature('QModelIndex')
    def on_tblSearchResult_doubleClicked(self, index):
        code = self.tableModel.code(index.row())
        self.selectCode(code)
#        self.setCurrentCode(code)


