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
## Это матрица битов.
##
## Вариант с хранением данных в одном векторе с пересчётом
## vector[ row*width + column ] рассматривался, но был отвергнут из-за
## потерь при проверке правильности column и row.
##
#############################################################################


from BitVector import BitVector

class BitMatrix(object):
    def __init__(self, width=0, height=0):
        self.vov = [ BitVector(size=width) for row in range(height) ]
        self.width   = width
        self.height  = height


    def __copy__(self):
        return self.copy()


    def __deepcopy__(self, memo):
        return self.copy()


    def copy(self):
        result = type(self)()
        result.width  = self.width
        result.height = self.height
        result.vov = [ v.__copy__() for v in self.vov ]
        return result


    def get(self, x, y):
        return self.vov[y][x]


    def put(self, x, y, v):
        self.vov[y][x] = v


    def __unicode__(self):
        c = u' ▀▄█'
        q = 4

        background = True
        result = []
        result.append(u'▒'* (self.width+2+2*q))
        for y in xrange(-q, self.height+q, 2):
            line = []
            for x in xrange(-q, self.width+q):
                top    = background ^ ( self.vov[y][x]   if 0<=y<self.height   and 0<=x<self.width else False )
                bottom = background ^ ( self.vov[y+1][x] if 0<=y+1<self.height and 0<=x<self.width else False )
                idx    = top+bottom*2
                line.append(c[idx])
            result.append( ''.join(line) )
        result.append(u'▒'* (self.width+2+2*q))
        return u'▒▒\n▒▒'.join(result)


class SquareBitMatrix(BitMatrix):
    def __init__(self, size=0):
        BitMatrix.__init__(self, size, size)



if __name__ == '__main__':
    m = SquareBitMatrix(10)
    print unicode(m)

    m.put(1, 1, True)
    print unicode(m)

