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
## Биндинг к hunspell средствами ctypes,
##
## ENoDictionaryFound: исключение "нет словаря для языка"
## DictWithPWL: похожий на такой же из encant
##
#############################################################################

import os.path


from _hunspell import HunspellInterfaceMultiton
from pwl       import PwlMultiton
from utils     import getDicts, isDictAvailable


class ENoDictionaryFound(Exception):
    def __init__(self, lang):
        Exception('No dictionary found for language "%s"' % lang)


class DictWithPWL:
    __dicts = None
    __lang = None

    def __init__(self, tag=None, pwl=None):
        affPath, dicPath = self._getPatches(tag)
        self.interface = HunspellInterfaceMultiton.getHunspellInterface(affPath, dicPath)
        self.pwl = PwlMultiton.getPwl(pwl or self._getDefaultPwl())
        self.pwl.addInterface(self.interface)


    def check(self, word):
        return self.interface.spell(word)


    def suggest(self, word):
        return self.interface.suggest(word)


    def add(self, word):
        self.pwl.add(word)


    def remove(self, word):
        self.pwl.remove(word)


    @classmethod
    def _getDicts(cls):
        if cls.__dicts is None:
            cls.__dicts = getDicts()
        return cls.__dicts


    @classmethod
    def _getDefaultLang(cls):
        if cls.__lang is None:
            cls.__lang = 'ru_RU'
        return cls.__lang


    @classmethod
    def _getPatches(cls, lang):
        key = lang or cls._getDefaultLang()
        dicts = cls._getDicts()
        if key in dicts:
            affPath, dicPath = dicts[key][0]
            if isDictAvailable(affPath, dicPath):
                return affPath, dicPath
        raise ENoDictionaryFound(key)


    @classmethod
    def _getDefaultPwl(cls):
        return os.path.join('~', '.mywords.txt')


class Dict(DictWithPWL):
    def __init__(self, tag=None):
        DictWithPWL.__init__(self, tag)


