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
## Код Рида-Соломона.
## Страшное дело...
##
#############################################################################

from GaloisField import GF


class RSCodeBase:
    def __init__(self, field, n, k, basePower=0):
        self.field = field

        self.n = n #  общее количество символов
        self.k = k #  «полезное» количество символов

        dist = n - k + 1
        # generator polynomial
        self.gpc = self._calcGpCoefficients(field, dist, basePower)


    def encode(self, data):
        assert len(data) == self.k
        extdata = data + [0] * (self.n-self.k)
        for i in xrange(self.k):
#            print i, extdata
            p = extdata[i]
            if p:
                for j, v in enumerate(self.gpc):
#                    print '[*]', j, v, p
                    extdata[i+j] = self.field.add( extdata[i+j], self.field.mult(v, p) )
#        print 'x', extdata
        return extdata[self.k:]


    @staticmethod
    def _calcGpCoefficients(field, dist, basePower):
#        print 'dist =', repr(dist)
        result = [0]*dist
        result[0] = 1
        t = field.exp[basePower]
        for i in xrange(1, dist):
#            t = self.mult(t,2)
#            print 'loop, i=', i, 't=',t, 'coefrs=', coefrs
            for j in xrange(i, 0, -1):
#                print 'i=',i, 'j=',j, 't=',t, 'coefrs[j-1]=', coefrs[j-1], 'coefrs[j]=', coefrs[j], 'self.mult(t, coefrs[j-1])=', self.mult(t, coefrs[j-1]), 'xor=', coefrs[j] ^ self.mult(t, coefrs[j-1])
                result[j] = field.add(result[j], field.mult(t, result[j-1]))
            t = field.mult(t, field.primitiveElement)
        return result



class RSCode(RSCodeBase):
    def __init__(self, size, modulo, n, k, basePower=0):
        RSCodeBase.__init__(self, GF(size, modulo), n, k, basePower)


if __name__ == '__main__':
    def testGenerator():
        # Тестируем заполнение порождающего многочлена
        class FakeField:
            def __init__(self):
                self.primitiveElement = 2
                self.exp = [ 2**k for k in xrange(16) ]

            def add(self, x, y):
                return x+y

            def mult(self, x, y):
                return x*y

        # просто строим полиномы (НЕ в полях Галуа!):
        # (x+2**0)                 = (x+1)                          -> [1, 1]
        # (x+2**0)(x+2**1)         = (x+1)(x+2) = x**2 + 3*x + 2    -> [1, 3, 2]
        # (x+2**0)(x+2**1)(x+2**2) = (x+1)(x+2)(x+4) = x**3 + 7*x**2 + 14*x + 8 -> [1, 7, 14, 8]
        ff = FakeField()
        print 'test1', '*'*40
        for dist, expected in [ (2, [1, 1]),
                                (3, [1, 3, 2]),
                                (4, [1, 7, 14, 8]),
                              ]:
            rsc = RSCodeBase(ff, dist, 1, basePower=0)
            print rsc.gpc, 'ok' if rsc.gpc == expected else 'fail'

        # ещё раз просто строим полиномы (опять НЕ в полях Галуа!):
        # (x+2**1)                 = (x+2)                          -> [1, 2]
        # (x+2**1)(x+2**2)         = (x+2)(x+4) = x**2 + 6*x + 8    -> [1, 6, 8]
        # (x+2**1)(x+2**2)(x+2**3) = (x+2)(x+4)(x+8) = x**3 + 14*x**2 + 50*x + 64 -> [1, 14, 56, 64]
        ff = FakeField()
        print 'test2', '*'*40
        for dist, expected in [ (2, [1, 2]),
                                (3, [1, 6, 8]),
                                (4, [1, 14, 56, 64]),
                              ]:
            rsc = RSCodeBase(ff, dist, 1, basePower=1)
            print rsc.gpc, 'ok' if rsc.gpc == expected else 'fail'

        print 'test from book', '*' * 40
        expected = [1, 7, 9, 3, 12, 10, 12]
        rsc = RSCode(16, 19, n=15, k=9, basePower=1)
        print rsc.gpc, 'ok' if rsc.gpc == expected else 'fail'

        print 'test from GOST', '*' * 40
        gf = GF(256, 285)
        for dist in xrange(2, 32):
            rsc = RSCodeBase(gf, dist, 1, basePower=0)
            print dist, [ gf.log[c] for c in rsc.gpc ]


    def testEncoding():
        # источник: "Коды Рида-Соломона с точки зрения обывателя"
        # https://lvk.cs.msu.su/~bahmurov/course_advanced_networks/2016/%D0%9A%D0%BE%D0%B4%D1%8B%20%D0%A0%D0%B8%D0%B4%D0%B0%20%D0%A1%D0%BE%D0%BB%D0%BE%D0%BC%D0%BE%D0%BD%D0%B0.pdf
        # некоторые подробности не совпадают с таковыми при вычислениях для QR-кода :(
        rsc = RSCode(16, 19, n=15, k=9, basePower=1)
        data = [9, 1, 1, 1, 9, 0, 10, 5, 7] # в источнике 7, 5, 10, 0, 9, 1, 1, 1, 9
        res = rsc.encode(data)
        expect = [13, 6, 14, 15, 15, 3] # в источнике 3, 15, 15, 14, 6, 13
        print data, '->', res, ':', 'ok' if res == expect else 'fail'


    def testEncoding2():
        # пример из https://www.thonky.com/qr-code-tutorial/error-correction-coding
        data = [32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17]
        rsc = RSCode(256, 285, n=len(data)+10, k=len(data), basePower=0)
        res = rsc.encode(data)
        expect = [196, 35, 39, 119, 235, 215, 231, 226, 93, 23]
        print data, '->', res, ':', 'ok' if res == expect else 'fail'


    def testEncoding3():
        # пример из Data Matrix (Приложение О (справочное). Пример кодирования символа версии ЕСС 200)
        data = [142, 164, 186]
        rsc = RSCode(256, 301, n=len(data)+5, k=len(data), basePower=1)
        res = rsc.encode(data)
        expect = [114, 25, 5, 88, 102]
        print data, '->', res, ':', 'ok' if res == expect else 'fail'

#    testGenerator()
#    testEncoding()
#    testEncoding2()
    testEncoding3()

