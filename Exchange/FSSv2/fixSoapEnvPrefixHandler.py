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
## "Handler" изменяющий префикс пространства имён 'SOAP-ENV' -> 'soapenv'
## для обхода ошибки в сервисе СФР.
##
#############################################################################

class CFixSoapEnvPrefixHandler(object):

    def sign(self, sw):
        envelope = sw.dom
        self._fixPrefix(envelope.node, 'SOAP-ENV', 'soapenv')
#        self._fixPrefix(envelope.node, 'SOAP-ENC', 'soapenc')


    def verify(self, ps):
        return


    ### implementation ##########################3

    def _fixPrefix(self, node, oldPrefix, newPrefix):
        oldPrefixWithColon = oldPrefix + ':'
        xmlnsOldPrefix = 'xmlns:' + oldPrefix
        xmlnsNewPrefix = 'xmlns:' + newPrefix

        def iterate(node):
            if node.prefix == oldPrefix:
                node.prefix = newPrefix
                if node.tagName.startswith(oldPrefixWithColon):
                    node.tagName = node.tagName.replace(oldPrefix, newPrefix)
                if node.nodeName.startswith(oldPrefixWithColon):
                    node.nodeName = node.nodeName.replace(oldPrefix, newPrefix, 1)

            attributes = node.attributes
            for i in xrange(attributes.length):
                attribute = attributes.item(i)
#                print attribute, attribute.prefix, attribute.nodeName
                if attribute.prefix == oldPrefix:
                    attribute.prefix = newPrefix
                if attribute.nodeName.startswith(oldPrefixWithColon):
                    attribute.nodeName = attribute.nodeName.replace(oldPrefix, newPrefix, 1)
                elif attribute.nodeName == xmlnsOldPrefix:
                    attribute.nodeName = xmlnsNewPrefix

            for childNode in node.childNodes:
                if childNode.nodeType == childNode.ELEMENT_NODE:
                    iterate(childNode)

        iterate(node)
