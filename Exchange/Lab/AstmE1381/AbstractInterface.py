# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Базовый класс интерфейса приёма/отравки сообщений согласно протокола
## ASTM E1381 (через последовательный порт или сокет)
##
#############################################################################


class CAbstractInterface(object):
    # базовый класс для разных интерфейсов, сейчас предполагаются
    # отладочный pipe,
    # tcp/ip - клиент,
    # tcp/ip - сервер,
    # последовательный порт

    def __init__(self):
        pass

    def prepareForWork(self):
        # if interface already open: return True
        # else try to open and return True on success or False on failure
        return False

    def read(self, timeout):
        # read single byte
        raise NotImplementedError


    def write(self, buff, timeout=60):
        # write bytes
        raise NotImplementedError


    def open(self):
        raise NotImplementedError


    def close(self):
        raise NotImplementedError
