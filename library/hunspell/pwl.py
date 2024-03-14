# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Pwl: список слов
## PwlMultiton: механизм, позволяющий использовать один единственный
##              экземпляр pwl для одного пути.
##
#############################################################################

import codecs
import os
import os.path

from weakref import WeakKeyDictionary, WeakValueDictionary


class Pwl:
    def __init__(self, fileName):
        self.fileName = os.path.expanduser(fileName)
        self.words = set()
        self.interfaces = WeakKeyDictionary() # Здесь лучше бы WeakSet, но d 2.6 его нет.
        self.load()


    def addInterface(self, interface):
        self.interfaces[interface] = None
        for word in self.words:
            interface.add(word)


    def load(self):
        try:
            if os.path.exists(self.fileName):
                f = codecs.open(self.fileName, 'r', encoding='utf-8')
                self.words = set(word.strip() for word in f)
        except EnvironmentError as e:
            pass # я не знаю что делать с этой ошибкой


    def store(self):
        f = None
        try:
            dir = os.path.dirname(self.fileName)
            if not os.path.exists(dir):
                os.makedirs(dir)
            f = codecs.open(self.fileName, 'w', encoding='utf-8')
            for word in self.words:
                f.write(word)
                f.write('\n')
        except EnvironmentError as e:
            pass # я не знаю что делать с этой ошибкой


    def add(self, word):
        for interface in self.interfaces.iterkeys():
            interface.add(word)
        self.words.add(word)
        self.store()


    def remove(self, word):
        for interface in self.interfaces.iterkeys():
            interface.remove(word)
        self.words.discard(word)
        self.store()


class PwlMultiton:
    registry = WeakValueDictionary()

    @classmethod
    def getPwl(cls, fileName):
        realFileName = os.path.realpath(fileName)
        result = cls.registry.get(realFileName)
        if result is None:
            cls.registry[realFileName] = result = Pwl(realFileName)
        return result
