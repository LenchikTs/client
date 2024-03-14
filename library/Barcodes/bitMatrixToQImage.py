#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui

def bitMatrixToQImage(bitMatrix, quietZone=4, scaleFactor=2):
    width =  (bitMatrix.width + 2*quietZone)*scaleFactor
    height = (bitMatrix.height + 2*quietZone)*scaleFactor
    image = QtGui.QImage(width, height, QtGui.QImage.Format_Mono)
    image.fill(1) # 1 - белый
    for row in xrange(bitMatrix.height):
        ybase = (quietZone+row)*scaleFactor
        for col in xrange(bitMatrix.width):
            xbase = (quietZone+col)*scaleFactor
            if bitMatrix.get(col, row): # рисуем чёрным
                for x in xrange(scaleFactor):
                    for y in xrange(scaleFactor):
                        image.setPixel(xbase+x, ybase+y, 0)
    return image

