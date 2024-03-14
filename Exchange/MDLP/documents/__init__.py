# -*- coding: UTF-8 -*-

# в пакете python-module-pyxb-1.2.4
# в модуле /usr/lib/python2.7/site-packages/pyxb/binding/saxer.py
# в функции PyXBSAXHandler.startElementNS
# в строке 342
# есть код "if self.__XSITypeTuple in attrs:"
# у меня установлен python-module-PyXML-0.8.4-alt5.1.1
# который реализует xml.sax.xmlreader.AttributesImpl ( /usr/lib64/python2.7/site-packages/_xmlplus/sax/xmlreader.py )
# который, в отличии /usr/lib64/python2.7/xml/sax/xmlreader.py
# не реализует метод __contain__
# и это приводит к ошибке.
#
# подобный код в pyxb встречается несколько раз,
# и согласно документации AttributesImpl не обязан реализовать __contain__
# и удалить python-module-PyXML я не готов.
# я могу пропатчить python-module-PyXML,
# но не готов распространять пропатченный модуль.
#
# monkey patch нам поможет...

try:
    from xml.sax.xmlreader import AttributesImpl
    if not hasattr(AttributesImpl, '__contains__'):
        AttributesImpl.__contains__ = AttributesImpl.has_key
except:
    pass
