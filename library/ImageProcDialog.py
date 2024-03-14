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

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignature, QFileInfo, QString

from library.DialogBase import CDialogBase
from library.Utils import forceString

from library.Ui_ImageProcDialog import Ui_ImageProcDialog


class CImageProcDialog(CDialogBase, Ui_ImageProcDialog):
    imageDir = ''

    def __init__(self, parent, image):
        CDialogBase.__init__(self, parent)
        self.addObject('btnLoad',  QtGui.QPushButton(u'Загрузить', self))
        self.addObject('btnSave',  QtGui.QPushButton(u'Сохранить', self))
        self.addObject('btnClear', QtGui.QPushButton(u'Очистить',  self))
        self.addObject('scene',    QtGui.QGraphicsScene(self))

        self.setupUi(self)
#        self.setWindowFlags(Qt.Popup)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitleEx(u'Просмотр изображения')
        self.buttonBox.addButton(self.btnLoad,  QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.btnSave,  QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.btnClear, QtGui.QDialogButtonBox.ActionRole)
        self.grpView.setScene(self.scene)
        self._pixmapItem = None
        self._image = None
        self.setImage(image)
        if parent.locked:
            self.btnLoad.setEnabled(False)
            self.btnClear.setEnabled(False)


    def setImage(self, image):
        scene = self.grpView.scene()
        if self._pixmapItem:
            scene.removeItem(self._pixmapItem)
            self._pixmapItem = None
        if image:
            pixmap = QtGui.QPixmap.fromImage(image)
            self._pixmapItem = scene.addPixmap(pixmap)
        self._image = image
        self.btnSave.setEnabled(bool(self._image))


    def image(self):
        return self._image


    @pyqtSignature('int')
    def on_scrSize_valueChanged(self, value):
        s = 2.0**(value*0.25)
        self.grpView.resetMatrix()
        self.grpView.scale(s, s)


    @pyqtSignature('')
    def on_btnLoad_clicked(self):
        if not CImageProcDialog.imageDir:
            CImageProcDialog.imageDir = QtGui.qApp.getSaveDir()
        fileName = forceString(QtGui.QFileDialog.getOpenFileName(
                                self,
                                u'Укажите файл с изображением',
                                CImageProcDialog.imageDir,
                                u'Файлы изображений (*.bmp *.jpg *.jpeg *.png *.ppm *.tiff *.xpm);;Все файлы (* *.*)'))
        if fileName != '':
            CImageProcDialog.imageDir = fileName
            image = QtGui.QImage()
            if image.load(fileName):
                self.setImage(image)
            else:
                pass


    @pyqtSignature('')
    def on_btnSave_clicked(self):
        if self._image:
            saveFormats = [u'Windows Bitmap (*.bmp)',
                           u'Joint Photographic Experts Group (*.jpg, *.jpeg)',
                           u'Portable Network Graphics (*.png)',
                           u'Portable Pixmap (*.ppm)',
                           u'Tagged Image File Format (*.tiff)',
                           u'X11 Pixmap (*.xpm)',
                          ]
            selectedFilter = QString('')

            if not CImageProcDialog.imageDir:
                CImageProcDialog.imageDir = QtGui.qApp.getSaveDir()

            fileName = QtGui.QFileDialog.getSaveFileName(
                self,
                u'Выберите имя файла',
                CImageProcDialog.imageDir,
                ';;'.join(saveFormats),
                selectedFilter)
            if not fileName.isEmpty():
                exts = selectedFilter.section('(*.',1,1).section(')',0,0).split(';*.')
                ext = QFileInfo(fileName).suffix()
                if exts and not exts.contains(ext, Qt.CaseInsensitive):
                    ext = exts[0]
                    fileName.append('.'+ext)
                fileName = unicode(fileName)
                self._image.save(fileName)


    @pyqtSignature('')
    def on_btnClear_clicked(self):
        self.setImage(None)
