#!/usr/bin/env python
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
## Собственно биндинг к hunspell средствами ctypes
##
## HunspellInterface:         экземпляр словаря
## HunspellInterfaceMultiton: механиз, мозволяющий иметь один
##                            экземпляр словаря для одной пары файлов
##
#############################################################################

import os
import os.path

from ctypes import ( CDLL,
                     POINTER,
                     byref,
                     c_char_p,
                     c_int,
                     c_void_p,
                   )

from ctypes.util import find_library

from weakref import WeakValueDictionary


class HunspellInterface:
    if os.name == 'nt':
#        libHandle = None
#        try:
#            libHandle = CDLL('libhunspell')
#        except WindowsError as e:
#            if e.winerror != 126:
#                raise e
#        if libHandle is None:
        libHandle = CDLL('hunspell')
    else:
        libHandle = CDLL(find_library('hunspell') or find_library('libhunspell'))


    #typedef struct Hunhandle Hunhandle;
    #
    #LIBHUNSPELL_DLL_EXPORTED Hunhandle* Hunspell_create(const char* affpath,
    #                                                    const char* dpath);

    _create = libHandle.Hunspell_create
    _create.restype      = c_void_p
    _create.argtypes     = (c_char_p, # affpath (which encoding?)
                            c_char_p, # dpath (which encoding?)
                           )

#    #LIBHUNSPELL_DLL_EXPORTED Hunhandle* Hunspell_create_key(const char* affpath,
#    #                                                        const char* dpath,
#    #                                                        const char* key);
#
#    _create_key = libHandle.Hunspell_create_key
#    _create_key.restype  = c_void_p
#    _create_key.argtypes = (c_char_p, # affpath (which encoding?)
#                            c_char_p, # dpath (which encoding?)
#                            c_char_p, # key
#                           )

    # LIBHUNSPELL_DLL_EXPORTED void Hunspell_destroy(Hunhandle* pHunspell);
    _destroy = libHandle.Hunspell_destroy
    _destroy.restype     = None
    _destroy.argtypes    = (c_void_p, # pHunspell
                           )


#    #/* load extra dictionaries (only dic files)
#    # * output: 0 = additional dictionary slots available, 1 = slots are now full*/
#    #LIBHUNSPELL_DLL_EXPORTED int Hunspell_add_dic(Hunhandle* pHunspell,
#    #                                              const char* dpath);
#
#    _add_dic = libHandle.Hunspell_add_dic
#    _add_dic.restype     = c_int
#    _add_dic.argtypes    = (c_void_p, # pHunspell
#                            c_char_p,   # dpath (which encoding?)
#                           )

    #LIBHUNSPELL_DLL_EXPORTED char* Hunspell_get_dic_encoding(Hunhandle* pHunspell);

    _get_dic_encoding = libHandle.Hunspell_get_dic_encoding
    _get_dic_encoding.restype  = c_char_p
    _get_dic_encoding.argtypes = (c_void_p,      # pHunspell
                                 )

    #/* spell(word) - spellcheck word
    # * output: 0 = bad word, not 0 = good word
    # */
    #LIBHUNSPELL_DLL_EXPORTED int Hunspell_spell(Hunhandle* pHunspell, const char*);

    _spell = libHandle.Hunspell_spell
    _spell.restype       = c_int
    _spell.argtypes      = (c_void_p,  # pHunspell
                            c_char_p,    # word (in dic encoding)
                          )

    #/* suggest(suggestions, word) - search suggestions
    # * input: pointer to an array of strings pointer and the (bad) word
    # *   array of strings pointer (here *slst) may not be initialized
    # * output: number of suggestions in string array, and suggestions in
    # *   a newly allocated array of strings (*slts will be NULL when number
    # *   of suggestion equals 0.)
    # */
    #LIBHUNSPELL_DLL_EXPORTED int Hunspell_suggest(Hunhandle* pHunspell,
    #                                              char*** slst,
    #                                              const char* word);

    _suggest = libHandle.Hunspell_suggest
    _suggest.restype = c_int
    _suggest.argtypes = (c_void_p,                   # pHunspell
                         POINTER(POINTER(c_char_p)), # slst
                         c_char_p, # word
                        )

    #
    #LIBHUNSPELL_DLL_EXPORTED int Hunspell_add(Hunhandle* pHunspell,
    #                                          const char* word);
    #
    _add = libHandle.Hunspell_add
    _add.restype = c_int
    _add.argtypes = (c_void_p,    # pHunspell
                     c_char_p,    # word
                    )

#    #/* add word to the run-time dictionary with affix flags of
#    # * the example (a dictionary word): Hunspell will recognize
#    # * affixed forms of the new word, too.
#    # */
#    #
#    #LIBHUNSPELL_DLL_EXPORTED int Hunspell_add_with_affix(Hunhandle* pHunspell,
#    #                                                     const char* word,
#    #                                                     const char* example);
#    #
#    _add_with_affix = libHandle.Hunspell_add_with_affix
#    _add_with_affix.restype = c_int
#    _add_with_affix.argtypes = (c_void_p,    # pHunspell
#                                c_char_p,    # word
#                                c_char_p,    # example
#                               )

    #/* remove word from the run-time dictionary */
    #
    #LIBHUNSPELL_DLL_EXPORTED int Hunspell_remove(Hunhandle* pHunspell,
    #                                             const char* word);
    _remove = libHandle.Hunspell_remove
    _remove.restype = c_int
    _remove.argtypes = (c_void_p,    # pHunspell
                        c_char_p,    # word
                       )

    #/* free suggestion lists */
    #
    #LIBHUNSPELL_DLL_EXPORTED void Hunspell_free_list(Hunhandle* pHunspell,
    #                                                 char*** slst,
    #                                                 int n);

    _free_list = libHandle.Hunspell_free_list
    _free_list.restype = None
    _free_list.argtypes = (c_void_p,                   # pHunspell
                           POINTER(POINTER(c_char_p)), # slst
                           c_int,                      # n
                          )

    def __init__(self, affpath, dpath):
        self.handle = self._create(affpath, dpath)
        self.encoding = self._get_dic_encoding(self.handle)


    def __del__(self):
        if self.handle:
            self._destroy(self.handle)
            self.handle = None


#    def addDict(self, dpath):
#        x = self._add_dic(self.handle, dpath.encode('utf-8'))
#        print 'add_dic', x


    def add(self, word):
        self._add(self.handle, word.encode(self.encoding))


    def remove(self, word):
        self._remove(self.handle, word.encode(self.encoding))


    def spell(self, word):
        return bool(self._spell(self.handle, word.encode(self.encoding)))


    def suggest(self, word):
        slots = POINTER(c_char_p)()
        n = self._suggest(self.handle, byref(slots), word.encode(self.encoding))
        if n>0:
            suggested = [ slots[i].decode(self.encoding) for i in xrange(n) ]
            self._free_list(self.handle, byref(slots), n)
            return suggested
        else:
            return []


class HunspellInterfaceMultiton:
    registry = WeakValueDictionary()

    @classmethod
    def getHunspellInterface(cls, affpath, dpath):
        realAffPath = os.path.realpath(affpath)
        realDPath   = os.path.realpath(dpath)
        key = (realAffPath, realDPath)
        result = cls.registry.get(key)
        if result is None:
            cls.registry[key] = result = HunspellInterface(realAffPath, realDPath)
        return result
