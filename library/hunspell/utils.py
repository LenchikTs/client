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
## поиск словарей,
##
#############################################################################

import glob
import os
import os.path
import sys
import locale


def getDefaultSearchDirectory():
    result = []
    result.append('.')

    mainScript = sys.argv[0] or '.'
    mainScriptDir = os.path.dirname(os.path.abspath(mainScript))
    result.append( os.path.join( mainScriptDir, 'hunspell'))

    dicPath = os.environ.get('DICPATH')
    if dicPath:
        result.append( dicPath.split(os.pathsep) )


    if os.name == 'posix':
        # подсмотрено в hunspell
        homePath = os.environ.get('HOME')
        prefixes = [ homePath + '/.local' if homePath else '/',
                     sys.prefix,
                     sys.prefix + '/local',
                   ]
        dirs = [ '/share/hunspell',
                 '/share/myspell',
                 '/share/myspell/dicts',
               ]
        result.extend( ( prefix + dir
                         for prefix in prefixes
                         for dir in dirs
                       )
                     )
    elif os.name == 'nt':
        # это наше правило
        prefixes = filter(None,
                          [ os.environ.get('APPDATA'),
                            os.environ.get('ALLUSERSPROFILE'),
                          ]
                         )
        dirs = [ 'hunspell',
               ]

        result.extend( ( os.path.join(prefix, dir)
                         for prefix in prefixes
                         for dir in dirs
                       )
                     )
    return result


def getDicts():
    result = {}
    dirs = getDefaultSearchDirectory()
    for dir in dirs:
        for affPath in glob.iglob(dir + os.path.sep + '*.aff'):
            absAffPath = os.path.abspath(affPath)
            if os.access(absAffPath, os.R_OK):
                root, ext = os.path.splitext(affPath)
                dicPath = root + '.dic'
                absDicPath = os.path.abspath(dicPath)
                if os.access(absDicPath, os.R_OK):
                    langCode = os.path.basename(root)
                    langDicts = result.setdefault(langCode, [])
                    langDicts.append((absAffPath, absDicPath))
    return result


def isDictAvailable(affPath, dicPath):
    return os.access(affPath, os.R_OK) and os.access(dicPath, os.R_OK)
