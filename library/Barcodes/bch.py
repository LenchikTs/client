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
## Это Код Боуза — Чоудхури — Хоквингема в применении к QR-коду.
##
#############################################################################


def _encodeData(data, dataBitLen, divisor):
    addLen = len(divisor)-1
    dataBits = [int(bit) for bit in list(format(data, 'b'))]
    bits     = dataBits + [0]*addLen
    for i in xrange(len(bits) - len(divisor)+1):
        if bits[i]:
            for j in xrange(len(divisor)):
                bits[i+j] ^= divisor[j]
    bits = [0]*(dataBitLen-len(dataBits)) + dataBits + bits[-addLen:]
    return bits


def encodeFormat(mode):
    # С.1 Вычисление битов исправления ошибок
    #          10  9  8  7  6  5  4  3  2  1  0
    divisor = [ 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1 ]
    mask    = [ 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0 ]
    bits    = _encodeData(mode, len(mask)-len(divisor)+1, divisor)
    assert len(bits) == len(mask)
    return [ bits[i] ^ mask[i] for i in xrange(len(mask)) ]


def encodeVersion(version):
    # D.2 Вычисление битов исправления ошибок
    #          12, 11, 10  9  8  7  6  5  4  3  2  1  0
    divisor = [ 1,  1,  1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1 ]
    return _encodeData(version, 6, divisor)


if __name__ == '__main__':

    print 'C1:'
    # 7.9 Информация о формате
    # Рисунок 25 - Позиция информации о формате

    for m, r in ( ('00000', '101010000010010'),
                  ('00101', '100000011001110'),
                  ('01010', '111110110101010'),
                  ('10101', '000001001010101'),
                  ('11111', '010101111101101'),
                ):
        bits = ''.join(str(bit) for bit in encodeFormat(int(m, 2)))
        print m, r, bits, r == bits

    print 'test1:', ''.join(str(bit) for bit in encodeFormat(int('10000', 2)))
    print 'test1:', ''.join(str(bit) for bit in encodeFormat(int('00001', 2)))

    print 'D1:'
    # 7.10 Информация о версии
    # версия размещается в порядке, определённом в Рисунок 28 - Размещение модулей в информации о версии
    # но вопрос нумерации бит не очень ясен. в наших индексах -
    # в нижнем-левом углу -
    # 17 14 11  8  5  2
    # 16 13 10  7  4  1
    # 15 12  9  6  3  0
    # в правом-верхнем углу -
    # 17 16 15
    # 14 13 12
    # 11 10  9
    #  8  7  6
    #  5  4  3
    #  2  1  0

    for v, r in ( ( 7, '000111110010010100'), 
                  (21, '010101011010000011'),
                  (31, '011111001001010000'),
                  (32, '100000100111010101'),
                  (40, '101000110001101001'),
                ):
        bits = ''.join(str(bit) for bit in encodeVersion(v))
        print '%2d %s %s %r' % (v, r, bits, r == bits)
