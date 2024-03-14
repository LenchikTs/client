# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2017-2018 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## "Handler" дописывающий XML в заголовок SOAP
##
#############################################################################

import xml.dom.minidom

class CAppendXmlToHeader(object):

    def __init__(self, app=[]):
        if isinstance(app, basestring):
            self.appendices = [ app ]
        elif isinstance(app, (list,tuple) ):
            self.appendices = app
        else:
            assert False


    def append(self, app):
        if isinstance(app, basestring):
            self.appendices.append(app)
        elif isinstance(app, (list,tuple) ):
            self.appendices.extend(app)
        else:
            assert False


    def sign(self, sw):
        header = sw._header
        for appendix in self.appendices:
            self._append(header.node, appendix)


    def verify(self, ps):
        return


    ### implementation ##########################3

    def _append(self, headerNode, appendixXml):
        appendixDoc = xml.dom.minidom.parseString(appendixXml)
        headerNode.appendChild(appendixDoc.documentElement)
