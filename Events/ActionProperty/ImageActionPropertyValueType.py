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
from PyQt4.QtCore import Qt, QBuffer, QByteArray, QIODevice, QSize, QVariant, pyqtSignature, SIGNAL

from library.ImageProcDialog import CImageProcDialog
from ActionPropertyValueType import CActionPropertyValueType
from library.PrintInfo       import CImageInfo


class CImageActionPropertyValueType(CActionPropertyValueType):
    name                = 'Image'
    variantType         = QVariant.Map
    preferredHeight     = 64
    preferredHeightUnit = 0
    isHtml              = True
    isImage             = True


    class CPropEditor(QtGui.QPushButton):
        __pyqtSignals__ = ('commit()',
                          )


        def __init__(self, action, domain, parent, clientId, eventTypeId):
            QtGui.QPushButton.__init__(self, parent)
            self.setFocusPolicy(Qt.StrongFocus)
            self._value = None
            self.connect(self, SIGNAL('clicked()'), self.runViewer)
            self.locked = action.isLocked()


        def setValue(self, value):
            self._value = value if isinstance(value, QtGui.QImage) else QtGui.QImage(value)
            self.setIconByValue()


        def setIconByValue(self):
            iconMaxSize = self.size()
            style = self.style()
            iconMaxSize -= QSize( style.pixelMetric(QtGui.QStyle.PM_FocusFrameHMargin)*2
                                 +style.pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)*2,
                                  style.pixelMetric(QtGui.QStyle.PM_FocusFrameVMargin)*2
                                 +style.pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)*2,
                                )
            if self._value:
                if self._value.height() > iconMaxSize.height() or self._value.width() > iconMaxSize.width():
                    preview = self._value.scaled(iconMaxSize.width(), iconMaxSize.height(), Qt.KeepAspectRatio)
                else:
                    preview = self._value
            else:
                preview = QtGui.QImage()
            pixmap = QtGui.QPixmap.fromImage(preview)
            self.setIcon(QtGui.QIcon(pixmap))
            self.setIconSize(preview.size())


        @pyqtSignature('')
        def runViewer(self):
            dlg = CImageProcDialog(self, self._value)
            if dlg.exec_():
                self.setValue(dlg.image())
                self.emit(SIGNAL('commit'))
            dlg.deleteLater()


        def value(self):
            return self._value


    @classmethod
    def getTableName(cls):
        return cls.tableNamePrefix+'Image'


    @staticmethod
    def convertDBValueToPyValue(value):
        if value.type() == QVariant.ByteArray:
            byteArray = value.toByteArray()
            if byteArray:
                image = QtGui.QImage()
                if image.loadFromData(byteArray):
                    return image
                else:
                    return None
        elif value.type() == QVariant.Image:
            image = QtGui.QImage(value)
            return image
        return None


    @staticmethod
    def convertQVariantToPyValue(value):
        if value.type() == QVariant.Image:
            image = QtGui.QImage(value)
            return image
        return None


    @staticmethod
    def convertPyValueToDBValue(value):
        if value:
            byteArray = QByteArray()
            buffer = QBuffer(byteArray)
            buffer.open(QIODevice.WriteOnly)
            value.save(buffer, 'PNG')
            buffer.close()
            return QVariant(byteArray)
        return None


    def toText(self, v):
        return None


    def toImage(self, v):
        if isinstance(v, QtGui.QImage):
            return v
        elif isinstance(v, QVariant):
            if v.type() == QVariant.Image:
                image = QtGui.QImage(v)
                return image
#        if v:
#            if v.height() > self.preferredHeight:
#                return v.scaledToHeight(self.preferredHeight, Qt.FastTransformation)
        return v


    def toInfo(self, context, v):
        return CImageInfo(context, v)
