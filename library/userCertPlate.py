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
## Вывод данных сертификата пользователя как изображения в духе 
## приказа минсвязи №186 от 27 мая 2015 г.
##
#############################################################################

from base64 import b64encode

from PyQt4 import QtGui
from PyQt4.QtGui  import (
                            QBrush, 
                            QFont, 
                            QImage, 
                            QPainter,
                            QPen, 
                            QTextBlockFormat, 
                            QTextCharFormat, 
                            QTextCursor, 
                            QTextDocument
                         )

from PyQt4.QtCore import (  Qt, 
                            QBuffer, 
                            QDateTime, 
                            QRectF,
                            QSizeF
                         )

from library.MSCAPI import MSCApi
from library.Utils import forceBool

class CCertInfoPlate:
    def __init__(self, ownerName, serialNumber, begDate, endDate, orgName=u'', scale=1.0):
        self.ownerName = ownerName
        self.serialNumber = serialNumber
        self.begDate = begDate
        self.endDate = endDate
        self.orgName = orgName
        self.scale = scale
        self.originalSize = QSizeF()
        self.scaledSize = QSizeF()
        self._draw()
    
    @classmethod
    def fromCert(cls, cert, **kwargs):
        commonName      = cert.commonName()
        surName         = cert.surName()
        givenName       = cert.givenName()
        if surName and givenName:
            name = u'%s %s' % (surName, givenName)
        else:
            name = commonName or ''
        serialNumber    = cert.serialNumber()
        notBefore       = QDateTime(cert.notBefore())
        notAfter        = QDateTime(cert.notAfter())
        return cls(name, serialNumber, notBefore, notAfter, **kwargs)
    
    def _draw(self):
        text = QFont('Times New Roman', 8, QFont.Normal)
        font = QFont('Times New Roman', 8, QFont.Normal)
        orgNameFont = QFont('Times New Roman', 6, QFont.Normal)
        titleSigner = QFont('Times New Roman', 5, QFont.Normal)

        titleBlockFormat = QTextBlockFormat()
        titleBlockFormat.setAlignment(Qt.AlignHCenter)
        bodyBlockFormat = QTextBlockFormat()
        bodyBlockFormat.setAlignment(Qt.AlignLeft)

        normalFormat = QTextCharFormat()
        normalFormat.setFont(text)
        normalFormat.setForeground(Qt.black)

        boldFormat = QTextCharFormat(normalFormat)
        boldFormat.setFontWeight(QFont.Bold)

        elSigner = QTextCharFormat()
        elSigner.setFont(titleSigner)

        orgNameFormat = QTextCharFormat()
        orgNameFormat.setFont(orgNameFont)
        document = QTextDocument()
        document.setDocumentMargin(0)
        document.setDefaultFont(font)
        document.setUseDesignMetrics(True)
        cursor = QTextCursor(document)
        cursor.setBlockFormat(titleBlockFormat)
        cursor.insertText(u'ДОКУМЕНТ ПОДПИСАН\nЭЛЕКТРОННОЙ ПОДПИСЬЮ', elSigner)

        cursor.insertBlock()
        cursor.setBlockFormat(bodyBlockFormat)
        cursor.insertText(u'Сертификат ', normalFormat)
        cursor.insertText(self.serialNumber, boldFormat)

        cursor.insertBlock()
        cursor.setBlockFormat(bodyBlockFormat)
        cursor.insertText(u'Владелец ', normalFormat)
        if len(self.ownerName.split(u" ")) >= 4:
            splitownerName= self.ownerName.split(u' ')
            ownerName = u''
            index = 1
            for word in splitownerName:
                ownerName += u'{0} '.format(word)
                if index % 3 == 0 and self.ownerName.split(" ")[::-1][0] != word:
                    ownerName += u'\n'
                index += 1
            cursor.insertText(ownerName, boldFormat)
        else:
            cursor.insertText(self.ownerName, boldFormat)

        cursor.insertBlock()
        cursor.setBlockFormat(bodyBlockFormat)
        cursor.insertText(u'Действителен с ', normalFormat)
        cursor.insertText(self.begDate.toString('dd.MM.yyyy'), boldFormat)
        cursor.insertText(u' по ', normalFormat)
        cursor.insertText(self.endDate.toString('dd.MM.yyyy'), boldFormat)

        if forceBool(self.orgName):
            cursor.insertBlock()
            cursor.setBlockFormat(bodyBlockFormat)
            cursor.insertText(u'Наименование МО ', normalFormat)
            splitOrgName = self.orgName.split(u' ')
            orgString = u''
            index = 1
            for word in splitOrgName:
                orgString += u'{0} '.format(word)
                if index % 3 == 0:
                    orgString += u'\n'
                index += 1
            cursor.insertText(orgString, orgNameFormat)

        document.setTextWidth(document.idealWidth())

        documentSize = document.size()

        padding = 6

        areaWidth  = documentSize.width() + padding * 2
        areaHeight = documentSize.height() + padding * 2
        self.originalSize = QSizeF(areaWidth, areaHeight)
        self.scaledSize = QSizeF(areaWidth * self.scale, areaHeight * self.scale)

        self.image = QImage(areaWidth * self.scale, areaHeight * self.scale, QImage.Format_RGB888) # Inherits: QPaintDevice.

        self.image.setDotsPerMeterX(self.image.dotsPerMeterX() * self.scale)
        self.image.setDotsPerMeterY(self.image.dotsPerMeterY() * self.scale)

        painter = QPainter()
        painter.begin(self.image)
        painter.scale(self.scale, self.scale)

        painter.fillRect(0, 0, areaWidth, areaHeight, Qt.white)

        painter.save()
        painter.translate(padding, padding)
        document.drawContents(painter, QRectF(0, 0, documentSize.width(), documentSize.height()))
        painter.restore()

        transparentBrush = QBrush(Qt.NoBrush)
        painter.setBrush(transparentBrush)
        thickBlackPen = QPen(Qt.black)
        thickBlackPen.setWidth(3)
        thickBlackPen.setCapStyle(Qt.RoundCap)
        thickBlackPen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(thickBlackPen)
        painter.drawRoundedRect(1, 1, areaWidth-3, areaHeight-3, padding*2, padding*2)

        painter.end()

        buffer = QBuffer()
        self.image.save(buffer, 'PNG')
        byteArray = buffer.data()
        self.bytes = bytes(byteArray)


def certInfoPlateBytes(ownerName, serialNumber, begDate, endDate, orgName=u'', scale=1.0):
    certInfoPlate = CCertInfoPlate(ownerName, serialNumber, begDate, endDate, orgName, scale)
    return certInfoPlate.bytes


def userCertPlate():
    qApp = QtGui.qApp
    try:
        api = MSCApi(qApp.getCsp())
        cert = qApp.getUserCert(api)
    except:
        cert = None

    if cert is None:
        return '&nbsp;'

    certInfoPlate = CCertInfoPlate.fromCert(cert)
    imageBytes = certInfoPlate.bytes

    return '<img src="data:image/png;base64,%s">' % b64encode(imageBytes)

if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    certInfoPlate = CCertInfoPlate(u"Кошка", u"Лижет", QDateTime.currentDateTime(), QDateTime.currentDateTime().addDays(1), scale=4.0)
    print(certInfoPlate.originalSize)
    print(certInfoPlate.scaledSize)
    with open("D:\\temp\\test.png", "wb") as file:
        file.write(certInfoPlate.bytes)