#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Это вектор битов.
##
## Вариант плотной упаковки битов рассматривался, но
## был отвергнут в пользу решения «Один байт для хранения одного бита»
## поскольку упаковка/распаковка на python обходится довольно дорого :(
##
#############################################################################


class BitVector(object):

    def __init__(self, size=0):
        self._size = size
        self._buff = bytearray([0]*size)


    def __copy__(self):
        result = BitVector()
        result._size = self._size
        result._buff.extend(self._buff)
        return result


    def __deepcopy__(self, memo):
        result = BitVector()
        result._size = self._size
        result._buff.extend(self._buff)
        return result


    def resize(self, size):
        if size<0:
            raise IndexError()

        if size > self._size:
            self._buff.extend([0]*(size > self._size))
            self._size = size
        elif size < self._size:
            self._buff = self.__buff[:size]
            self._size = size


    def append(self, v):
        s = self._size
        self.resize(s+1)
        self.__setitem__(s, v)


    def __getitem__(self, key):
        return bool(self._buff[key])


    def __setitem__(self, key, value):
        self._buff[key] = value


if __name__ == '__main__':
    # TODO: написать образцы
    pass
