# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import QFile, SIGNAL


from library.interchange     import getLabelImageValue, getLineEditValue, getSpinBoxValue, setLabelImageValue, setLineEditValue, setSpinBoxValue
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CTextCol

from RefBooks.Tables         import rbCode, rbName

from .Ui_RBImageMapEditor import Ui_ItemEditorDialog


class CRBImageMapList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], 'rbImageMap', [rbCode, rbName])
        self.setWindowTitleEx(u'Отметки проблемных зон')

    def getItemEditor(self):
        return CRBImageMapEditor(self)

#
# ##########################################################################
#

class CRBImageMapEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self, parent):
        self.tableName = 'rbImageMap'
        CItemEditorBaseDialog.__init__(self, parent, self.tableName)
        self.setupUi(self)
        self.setWindowTitleEx(u'Отметка проблемной зоны')
        self.connect(self.btnOpen, SIGNAL('clicked()'), self.btnOpenClicked)
        self.homeDir = QtGui.qApp.getHomeDir()
        self.loadedImage = None
        self.loadedFile = None


    def btnOpenClicked(self):
        fileDialog = QtGui.QFileDialog()
        fileName = fileDialog.getOpenFileNames(self,
                                               "Select image",
                                               self.homeDir,
                                               u'Файлы изображений (*.bmp *.jpg *.jpeg *.png *.ppm *.tiff *.xpm);;Все файлы (* *.*)')
        if fileName:
            self.loadedImage = QtGui.QPixmap(fileName[0])
            self.loadedFile = QFile(fileName[0])
            self.edtImage.setText(fileName[0])
            self.addImageOnWidget()


    def addImageOnWidget(self):
        self.lblPixmap.setGeometry(0, 0,
                      self.loadedImage.size().width(),
                      self.loadedImage.size().height())
        self.lblPixmap.setPixmap(self.loadedImage)


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode,   record, 'code' )
        setLineEditValue(self.edtName,   record, 'name' )
        setLabelImageValue(self.lblPixmap, record, 'image')
        setSpinBoxValue(self.edtMarkSize, record, 'markSize')


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode,  record, 'code' )
        getLineEditValue(self.edtName,  record, 'name' )
        getLabelImageValue(self.loadedFile, record, 'image')
        getSpinBoxValue(self.edtMarkSize, record, 'markSize')
        return record
