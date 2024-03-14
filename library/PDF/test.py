#!/usr/bin/env python2
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
## Тестовая программа для преобрезования pdf
##
#############################################################################

import os.path
from locale import getpreferredencoding
from optparse import OptionParser

from fixPdf import fixPdf


encoding = getpreferredencoding(True)

parser = OptionParser(usage= 'usage: %prog [options] soure.pdf ...')
parser.add_option('-t', '--title',    dest='title',    help='set pdf title',    metavar='TITLE')
parser.add_option('-a', '--author',   dest='author',   help='set pdf author',   metavar='AUTHOR')
parser.add_option('-s', '--subject',  dest='subject',  help='set pdf subject',  metavar='SUBJECT')
parser.add_option('-k', '--keywords', dest='keywords', help='set pdf keywords', metavar='KEYWORDS')
parser.add_option('-c', '--creator',  dest='creator',  help='set pdf creator',  metavar='CREATOR')
parser.add_option('-p', '--producer', dest='producer', help='set pdf producer', metavar='PRODUCER')

(options, args) = parser.parse_args()


d = options.__dict__
for key, value in d.items():
    if value is not None:
        d[key] = value.decode(encoding)

for arg in args:
    sourceFileName = arg.decode(encoding)
    base, ext = os.path.splitext(sourceFileName)
    destinationFileName = '%s_fixed%s' % (base, ext)

    with open(sourceFileName, 'rb') as sourceStream:
        with open(destinationFileName, 'wb') as destinationStream:
            fixPdf(sourceStream, destinationStream, **d)
