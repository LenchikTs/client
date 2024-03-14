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

from QRCodeWriter import QRCodeWriter
from bitMatrixToQImage import bitMatrixToQImage

def qrcodeImage(data, version=None, correctionLevel=None, minVersion=1, maxVersion=40, eci=None, scaleFactor=2):
    writer = QRCodeWriter(data,
                          version=version,
                          correctionLevel=correctionLevel,
                          minVersion=minVersion,
                          maxVersion=maxVersion,
                          eci=eci
                         )
    return bitMatrixToQImage(writer.matrix, quietZone=4, scaleFactor=scaleFactor)
