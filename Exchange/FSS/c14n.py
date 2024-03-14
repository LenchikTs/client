# -*- coding: UTF-8 -*-
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
## exclusive canonicalization 
## В ZSI в принципе есть каноникализация, но в ней есть ошибки :(
##
#############################################################################

import cStringIO as StringIO


def escapeAttrValue(value):
    charEscapeMap = {
                    '&':'&amp;',
                    '<':'&lt;',
                    '"':'&quot;',
                    '\r': '&#xD;',
                    '\n': '&#xA;',
                    '\t': '&#x9;',
                    }
    return ''.join( charEscapeMap.get(ch, ch) for ch in value )


def escapeText(value):
    charEscapeMap = {
                    '&':'&amp;',
                    '<':'&lt;',
                    '>':'&gt;',
                    '\r': '&#xD;',
                    }
    return ''.join( charEscapeMap.get(ch, ch) for ch in value )


def exclusiveC14N(e):
    def _exclusiveC14N(write, e, definedNameSpaces):
        usedNameSpaces = {}
        if e.namespaceURI is not None:
            usedNameSpaces[e.prefix or ''] = e.namespaceURI

        attributes = []
        for attribute in e.attributes.values():
            if attribute.prefix != 'xmlns' and attribute.nodeName != 'xmlns':
                attributes.append(attribute)
                if attribute.namespaceURI:
                    usedNameSpaces[attribute.prefix or ''] = attribute.namespaceURI

        # начало элемента - открываем тег
        write('<%s' % e.tagName)
        # пространства имён, в правильном порядке
        for prefix, uri in sorted(usedNameSpaces.iteritems()):
            if prefix not in definedNameSpaces:
                if prefix == '':
                    write(' xmlns="%s"' % uri)
                else:
                    write(' xmlns:%s="%s"' % (prefix, uri))

        # атрибуты, в правильном порядке
        attributeTexts = ['%s="%s"' % (attribute.nodeName, escapeAttrValue(attribute.value)) for attribute in attributes]
        attributeTexts.sort()
        for attributeText in attributeTexts:
            write(' %s' % attributeText)
        # закрываем открывающий тег
        write('>')

        newDefinedNameSpaces = definedNameSpaces.copy()
        newDefinedNameSpaces.update(usedNameSpaces)
        # дети - текст, комментарии и элементы
        for childNode in e.childNodes:
            if childNode.nodeType == childNode.TEXT_NODE:
                write( escapeText(childNode.data) )
            if childNode.nodeType == childNode.COMMENT_NODE:
                write( '<!--' +escapeText(childNode.data) +'-->' )
            if childNode.nodeType == childNode.ELEMENT_NODE:
                _exclusiveC14N(write, childNode, newDefinedNameSpaces)
        # закрывающий тег.
        write('</%s>' % e.tagName)

    output = StringIO.StringIO()

#    def w(t):
#        print type(t), repr(t)
#        output.write( t.encode('utf-8') if isinstance(t, unicode) else t )
#
#    _exclusiveC14N(w, e, {})
    _exclusiveC14N(lambda t: output.write(t.encode('utf-8') if isinstance(t, unicode) else t  ), e, {})

#    print '------------'
#    print output.getvalue()
#    print '------------'

    return output.getvalue()
