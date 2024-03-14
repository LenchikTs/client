from .base import BaseImage
from PyQt4 import QtGui
from PyQt4.QtCore import Qt

class QRImage(BaseImage):
    def new_image(self, **kwargs):
        image = QtGui.QImage(self.pixel_size, self.pixel_size, QtGui.QImage.Format_RGB16)
        image.fill(Qt.white)
        self._painter = QtGui.QPainter(image)
        return image

    def drawrect(self, row, col):
        self._painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size,
            Qt.black)