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
##
## генерация QImage с QRCode
##
#############################################################################

from DataMatrixWriter import DataMatrixWriter
from bitMatrixToQImage import bitMatrixToQImage

def datamatrixImage(data, size=None, minSize=None, maxSize=None, shape=0, eci=None, encoding=None, scaleFactor=2):
    writer = DataMatrixWriter(data,
                              size=size,
                              minSize=minSize,
                              maxSize=maxSize,
                              shape=shape,
                              eci=eci,
                              encoding=encoding
                             )
    return bitMatrixToQImage(writer.matrix, quietZone=4, scaleFactor=scaleFactor)
