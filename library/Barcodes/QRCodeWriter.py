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
## Это генерация QR-кода
##
## использованы источники:
##   ГОСТ Р ИСО/МЭК 18004-2015 ( http://docs.cntd.ru/document/1200121043 )
##   https://ru.wikipedia.org/wiki/QR-%D0%BA%D0%BE%D0%B4
##   http://grandzebu.net/informatique/codbar-en/qrcode.htm
##   https://ppt-online.org/365464 p21
##   https://www.thonky.com/qr-code-tutorial/error-correction-coding
##   https://www.nayuki.io/page/optimal-text-segmentation-for-qr-codes
##   https://zxing.org/w/decode.jspx
##
## ещё может быть полезно -
##
##   https://pypi.org/project/qrcode/
##   https://pypi.org/project/PyQRCode/
##   https://www.geeksforgeeks.org/reading-generating-qr-codes-python-using-qrtools/
##   https://segno.readthedocs.io/en/stable/comparison-qrcode-libs.html
##
#############################################################################


import copy

from ReedSolomonCode import RSCode
from bch import encodeFormat, encodeVersion
from BitMatrix import SquareBitMatrix


class QRCodeDataSegment:
    codeableCharacters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:'

    etNumeric      = '0001'
    etAlphanumeric = '0010'
    etBytes        = '0100'

    ciLenV1to9     = { etNumeric: 10, etAlphanumeric:  9, etBytes:  8}
    ciLenV10to26   = { etNumeric: 12, etAlphanumeric: 11, etBytes: 16}
    ciLenV27to40   = { etNumeric: 14, etAlphanumeric: 13, etBytes: 16}


    def __init__(self, encodingType, data):
        self.encodingType = encodingType
        self.data         = data


    def append(self, byte):
        self.data += byte


    def __add__(self, other):
        return QRCodeDataSegment( max(self.encodingType, other.encodingType),
                                  self.data + other.data
                                )


    @classmethod
    def detectEncodingType(cls, s):
        assert isinstance(s, bytes)

        if s.isdigit():
            return cls.etNumeric
        elif all(c in cls.codeableCharacters for c in s):
            return cls.etAlphanumeric
        else:
            return cls.etBytes


    def _getCountIndicatorBitLength(self, version):
        assert 1 <= version <= 40
        if version<=9:
            return self.ciLenV1to9[self.encodingType]
        if version<=26:
            return self.ciLenV10to26[self.encodingType]
        return self.ciLenV27to40[self.encodingType]


    def bitLength(self, version):
        countIndicatorBitLength = self._getCountIndicatorBitLength(version)
        if self.encodingType == self.etNumeric:
            w, p = divmod(len(self.data), 3)
            return 4 + countIndicatorBitLength + w*10 + (7 if p == 2 else 4 if p == 1 else 0)
        elif self.encodingType == self.etAlphanumeric:
            w, p = divmod(len(self.data), 2)
            return 4 + countIndicatorBitLength + w*11 + (6 if p else 0)
        elif self.encodingType == self.etBytes:
            return 4 + countIndicatorBitLength + len(self.data)*8
        else:
            assert False


    def bits(self, version):
        countIndicatorBitLength = self._getCountIndicatorBitLength(version)
        parts = [ self.encodingType, '{0:0{width}b}'.format(len(self.data), width=countIndicatorBitLength) ]
        if self.encodingType == self.etNumeric:
            m = { 3: 10, 2: 7, 1: 4 }
            for i in xrange(0, len(self.data), 3):
                part = self.data[i:i+3]
                parts.append( '{0:0{width}b}'.format(int(part), width=m.get(len(part))) )
        elif self.encodingType == self.etAlphanumeric:
            for i in xrange(0, len(self.data), 2):
                part = self.data[i:i+2]
                if len(part) == 2:
                    code = self.codeableCharacters.index(part[0])*45 + self.codeableCharacters.index(part[1])
                    parts.append( '{0:0{width}b}'.format(code, width=11) )
                else:
                    code = self.codeableCharacters.index(part[0])
                    parts.append( '{0:0{width}b}'.format(code, width=6))
        elif self.encodingType == self.etBytes:
            for c in self.data:
                parts.append( '{0:08b}'.format(ord(c)) )
        else:
            assert False
        return ''.join(parts)


class QRCodeWriter:
    alignmentPatterns = (
                            None,                              # 1
                            (6, 18),                           # 2
                            (6, 22),                           # 3
                            (6, 26),                           # 4
                            (6, 30),                           # 5
                            (6, 34),                           # 6
                            (6, 22, 38),                       # 7
                            (6, 24, 42),                       # 8
                            (6, 26, 46),                       # 9
                            (6, 28, 50),                       # 10
                            (6, 30, 54),                       # 11
                            (6, 32, 58),                       # 12
                            (6, 34, 62),                       # 13
                            (6, 26, 46, 66),                   # 14
                            (6, 26, 48, 70),                   # 15
                            (6, 26, 50, 74),                   # 16
                            (6, 30, 54, 78),                   # 17
                            (6, 30, 56, 82),                   # 18
                            (6, 30, 58, 86),                   # 19
                            (6, 34, 62, 90),                   # 20
                            (6, 28, 50, 72, 94),               # 21
                            (6, 26, 50, 74, 98),               # 22
                            (6, 30, 54, 78, 102),              # 23
                            (6, 28, 54, 80, 106),              # 24
                            (6, 32, 58, 84, 110),              # 25
                            (6, 30, 58, 86, 114),              # 26
                            (6, 34, 62, 90, 118),              # 27
                            (6, 26, 50, 74, 98, 122),          # 28
                            (6, 30, 54, 78, 102, 126),         # 29
                            (6, 26, 52, 78, 104, 130),         # 30
                            (6, 30, 56, 82, 108, 134),         # 31
                            (6, 34, 60, 86, 112, 138),         # 32
                            (6, 30, 58, 86, 114, 142),         # 33
                            (6, 34, 62, 90, 118, 146),         # 34
                            (6, 30, 54, 78, 102, 126, 150),    # 35
                            (6, 24, 50, 76, 102, 128, 154),    # 36
                            (6, 28, 54, 80, 106, 132, 158),    # 37
                            (6, 32, 58, 84, 110, 136, 162),    # 38
                            (6, 26, 54, 82, 110, 138, 166),    # 39
                            (6, 30, 58, 86, 114, 142, 170),    # 40
                        )


    # перепев таблицы 7 из ГОСТа - количество слов (байт) данных в зависимости от версии и
    # таблица взята из википедии.
    # в моём экземпляре ГОСТа есть два недочёта:
    # - в версии 22 потеряна строка для уровня исправления ошибок L.
    # - для версии 26 уроветь исправления ошибок M  искажено значение "число кодовых слов данных"
    codeCapacity = { #      1   2   3   4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19   20   21    22    23    24    25    26    27    28    29    30    31    32    33   34     35    36    37    38    39    40
                     'L': (19, 34, 55, 80, 108, 136, 156, 194, 232, 274, 324, 370, 428, 461, 523, 589, 647, 721, 795, 861, 932, 1006, 1094, 1174, 1276, 1370, 1468, 1531, 1631, 1735, 1843, 1955, 2071, 2191, 2306, 2434, 2566, 2702, 2812, 2956),
                     'M': (16, 28, 44, 64,  86, 108, 124, 154, 182, 216, 254, 290, 334, 365, 415, 453, 507, 563, 627, 669, 714,  782,  860,  914, 1000, 1062, 1128, 1193, 1267, 1373, 1455, 1541, 1631, 1725, 1812, 1914, 1992, 2102, 2216, 2334),
                     'Q': (13, 22, 34, 48,  62,  76,  88, 110, 132, 154, 180, 206, 244, 261, 295, 325, 367, 397, 445, 485, 512,  568,  614,  664,  718,  754,  808,  871,  911,  985, 1033, 1115, 1171, 1231, 1286, 1354, 1426, 1502, 1582, 1666),
                     'H': ( 9, 16, 26, 36,  46,  60,  66,  86, 100, 122, 140, 158, 180, 197, 223, 253, 283, 313, 341, 385, 406,  442,  464,  514,  538,  596,  628,  661,  701,  745,  793,  845,  901,  961,  986, 1054, 1096, 1142, 1222, 1276),
                   }

    # часть таблицы 9 - (Характеристики исправления ошибок для QR Code) количество блоков
    blocksCount =  { #       1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39  40
                      'L':(  1,  1,  1,  1,  1,  2,  2,  2,  2,  4,  4,  4,  4,  4,  6,  6,  6,  6,  7,  8,  8,  9,  9, 10, 12, 12, 12, 13, 14, 15, 16, 17, 18, 19, 19, 20, 21, 22, 24, 25),
                      'M':(  1,  1,  1,  2,  2,  4,  4,  4,  5,  5,  5,  8,  9,  9, 10, 10, 11, 13, 14, 16, 17, 17, 18, 20, 21, 23, 25, 26, 28, 29, 31, 33, 35, 37, 38, 40, 43, 45, 47, 49),
                      'Q':(  1,  1,  2,  2,  4,  4,  6,  6,  8,  8,  8, 10, 12, 16, 12, 17, 16, 18, 21, 20, 23, 23, 25, 27, 29, 34, 34, 35, 38, 40, 43, 45, 48, 51, 53, 56, 59, 62, 65, 68),
                      'H':(  1,  1,  2,  4,  4,  4,  5,  6,  8,  8, 11, 11, 16, 16, 18, 16, 19, 21, 25, 25, 25, 34, 30, 32, 35, 37, 40, 42, 45, 48, 51, 54, 57, 60, 63, 66, 70, 74, 77, 81)
                   }

    # часть таблицы 9 - (Характеристики исправления ошибок для QR Code) Число  кодовых слов исправления ошибок
    rsPerBlock = { #         1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39  40
                     'L': (  7, 10, 15, 20, 26, 18, 20, 24, 30, 18, 20, 24, 26, 30, 22, 24, 28, 30, 28, 28, 28, 28, 30, 30, 26, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30),
                     'M': ( 10, 16, 26, 18, 24, 16, 18, 22, 22, 26, 30, 22, 22, 24, 24, 28, 28, 26, 26, 26, 26, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28),
                     'Q': ( 13, 22, 18, 26, 18, 24, 18, 22, 20, 24, 28, 26, 24, 20, 30, 24, 28, 28, 26, 30, 28, 30, 30, 30, 30, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30),
                     'H': ( 17, 28, 22, 16, 22, 28, 26, 26, 24, 28, 24, 28, 22, 24, 24, 30, 28, 28, 26, 28, 30, 24, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30),
                 }


    def __init__(self, data, version=None, correctionLevel=None, minVersion=1, maxVersion=40, eci=None):
        if version is None:
            eciBits = self.encodeEci(eci)
            bitsV1  = eciBits + self.encode(1, data)
            bitsV10 = eciBits + self.encode(10, data)
            bitsV27 = eciBits + self.encode(27, data)
            bitses  = [bitsV1]*(10-1) + [bitsV10]*(27-10) + [bitsV27]*(41-27)
            bits = None
            for cl in ('H', 'Q', 'M', 'L') if correctionLevel is None else (correctionLevel,):
                for v in xrange(minVersion, maxVersion+1):
                    if len(bitses[v-1]) <= self.codeCapacity[cl][v-1]*8:
                        version = v
                        correctionLevel = cl
                        bits = bitses[v-1]
                        break
                if version is not None:
                    break
        else:
            bits = self.encodeEci(eci) + self.encode(version, data)
            if correctionLevel is None:
                for cl in ('H', 'Q', 'M', 'L'):
#                    print 'len(bits) =', len(bits), 'version =', version, 'correctionLevel =', cl, 'cap =', self.codeCapacity[cl][version]*8
                    if len(bits) <= self.codeCapacity[cl][version-1]*8:
                        correctionLevel = cl
                        break
        if (    version is None
             or correctionLevel is None
             or bits is None
             or len(bits) > self.codeCapacity[correctionLevel][version-1]*8
           ):
            raise Exception('too much data for this code')

        self.version = version
        self.correctionLevel = correctionLevel
        self.size = self.__getSize(version)

        self.matrix = SquareBitMatrix(self.size)
        self.used = SquareBitMatrix(self.size)

        self.drawFinderPatterns()
        self.drawTimingPatterns()
        self.drawAlignmentPatterns()

        self.maskFormatInfo()
        self.maskVersionInfo()

        self.drawVersionInfo()
        self.setBits(bits)
        self.applyBestMask()


    @classmethod
    def encodeEci(cls, eci):
        if eci is None:
            return ''
        elif 0<=eci<128:
            return '0111' + format(eci, '08b')
        elif 0<=eci<=16383:
            return '0111' + '10' + format(eci, '014b')
        elif 0<=eci<=999999:
            return '0111' + '110' + format(eci, '021b')
        raise ValueError('Wrong eci %r' % eci)


    @classmethod
    def encode(cls, version, data):
        if isinstance(data, unicode):
            data = data.encode('utf8')
        elif not isinstance(data, bytes):
            data = bytes(data)
        segments = cls.splitToSegments(version, data)
        return ''.join(segment.bits(version) for segment in segments)


    @classmethod
    def splitToSegments(cls, version, data):
        segments = []
        segment = None
        for c in data:
            encodingType = QRCodeDataSegment.detectEncodingType(c)
            if segment is not None and encodingType == segment.encodingType:
                segment.append(c)
            else:
                segment = QRCodeDataSegment(encodingType, c)
                segments.append(segment)
        # жадное слияние сегментов
        if len(segments) >= 2:
            bitLen = [ s.bitLength(version) for s in segments ]
            bonus  = [ bitLen[i]+bitLen[i+1]-(segments[i]+segments[i+1]).bitLength(version)
                       for i in xrange(len(segments)-1)
                     ]

            while len(bonus):
                maxBonus = max(bonus)
                if maxBonus<=0:
                    break
                i = bonus.index(maxBonus)
                # сливаем i и i+1
                segment = segments[i] = segments[i] + segments[i+1]
                bitLen[i] = bitLen[i]+bitLen[i+1]-bonus[i]
                # assert bitLen[i] == segment.bitLength(version)
                del segments[i+1]
                del bitLen[i+1]
                del bonus[i]
                if i>0:
                    # пересчитываем бонус для слияния i-1 и i
                    prevSegment = segments[i-1]
                    bonus[i-1] = bitLen[i-1]+bitLen[i]-(prevSegment+segment).bitLength(version)
                if i<len(segments)-1:
                    # пересчитываем бонус для слияния i и i+1
                    nextSegment = segments[i+1]
                    bonus[i] = bitLen[i]+bitLen[i+1]-(segment+nextSegment).bitLength(version)
        return segments




###############################################################################

    def setBits(self, bits):
        codeCapacityInBytes = self.codeCapacity[self.correctionLevel][self.version-1]
        codeCapacity = codeCapacityInBytes*8
        assert len(bits) <= codeCapacity

        if len(bits)+4 <= codeCapacity: # терминатор помещается
            bits += '0000'

        bits += '0' * (-len(bits) % 8) # заполнение слова нулями

        filler = '1110110000010001'
        numFillers, fillerPart = divmod(codeCapacity-len(bits), len(filler))
        bits += filler*numFillers + filler[:fillerPart]

        assert len(bits) == codeCapacity

        words = [bits[i:i+8] for i in xrange(0, len(bits), 8)]

        blocks = self.__splitIntoBlocks(words)
#        print blocks
#        print [ len(b) for b in blocks ]
        rsc = None
        corrBlocks = []
        for block in blocks:
            if not rsc or rsc.k != len(block):
                rsPerBlock = self.rsPerBlock[self.correctionLevel][self.version-1]
                n = rsPerBlock + len(block)
#                print 'n =', n, 'k =', len(block)
                rsc = RSCode(256, 285, n=n, k=len(block), basePower=0)
#            print block, '==',[int(word, 2) for word in  block]
#            print '->'
            ex = rsc.encode([int(word, 2) for word in  block])
#            print ex, len(ex)
            corrBlocks.append([format(b, '08b') for b in ex])
#        print corrBlocks

        outWords = []
        for i in xrange(len(blocks[-1])):
            for block in blocks:
                if i<len(block):
                    outWords.append(block[i])
        for i in xrange(self.rsPerBlock[self.correctionLevel][self.version-1]):
            for corrBlock in corrBlocks:
                outWords.append(corrBlock[i])
        self.drawBits( ''.join(outWords) )



    @staticmethod
    def __getSize(version):
        assert 1<=version<=40
        return 21+(version-1)*4


    def drawFinderPatterns(self):
        for baseX, baseY in ( ( 0,                 0 ),
                              ( 0 + self.size - 7, 0 ),
                              ( 0,                 self.size - 7 )
                            ):
            self.drawFinderPattern(baseX, baseY)


    def drawFinderPattern(self, baseX, baseY):
        for x in xrange(7):
            for y in xrange(7):
                b = (abs(x-3) == 2 and abs(y-3) <= 2) or (abs(x-3) <= 2 and abs(y-3) == 2)
                self.matrix.put( baseX+x, baseY+y, not b)
        if baseX>0:
           baseX -= 1
        if baseY>0:
           baseY -= 1
        for x in xrange(8):
            for y in xrange(8):
                self.used.put( baseX+x, baseY+y, True )


    def drawTimingPatterns(self):
        flip = False
        for p in xrange(7, self.size-7):
            self.matrix.put(6, p, flip)
            self.matrix.put(p, 6, flip)
            flip = not flip
            self.used.put(6, p, True)
            self.used.put(p, 6, True)


    def drawAlignmentPatterns(self):
        coords = self.alignmentPatterns[self.version-1]
        if coords:
            cmin = coords[0]
            cmax = coords[-1]
            for x in coords:
                for y in coords:
                    if (x != cmin or (y != cmin and y != cmax)) and (x != cmax or y != cmin):
                        self.drawAlignmentPattern(x,y)


    def drawAlignmentPattern(self, baseX, baseY):
        for x in xrange(-2,3):
            for y in xrange(-2,3):
                f = not(abs(x) == 1 and -1<=y<=1 or -1<=x<=1 and abs(y) == 1)
                self.matrix.put( baseX+x, baseY+y, f)
                self.used.put(baseX+x, baseY+y, True)


    def maskFormatInfo(self):
        for k in xrange(8):
            pass
            self.used.put( k, 8, True)
            self.used.put( 8, k, True)
            self.used.put( 8, self.size-1-k, True)
            self.used.put( self.size-1-k, 8, True)
        self.used.put( 8, 8, True)


    def drawBits(self, bits):
        def enumPoints():
            up = True
            x = self.size-1
            y = self.size-1
            while x>=0:
                if not self.used.get(x,y):
                    yield((x,y))
                if not self.used.get(x-1,y):
                    yield((x-1,y))
                if up:
                    y -= 1
                    if y < 0:
                        x -= 2
                        if x == 6:
                            x -= 1
                        y = 0
                        up = False
                else:
                    y += 1
                    if y >= self.size:
                        x -= 2
                        if x == 6:
                            x -= 1
                        y = self.size-1
                        up = True

#        points = enumPoints()
#        lp = list(points)
#        print len(lp)
        points = enumPoints()

        for bit in bits:
            x,y = points.next()
#            print x,y, self.used.get(x,y), self.matrix.get(x,y)
            self.matrix.put(x, y, int(bit))
#            self.used.put(x,y,True)



    def drawFormatInfo(self, maskId):
        self.__drawFormatInfo(self.matrix, maskId)
        return
##        bits = encodeFormat(format)
##        bits = [1]*len(bits)
##        bits = [0]*len(bits)
#        k = 0
#        for k in xrange(8):
#            self.matrix.put( k+(1 if k>5 else 0), 8, bits[k])
##            self.used.put(   k+(1 if k>5 else 0), 8, True)
#
#            self.matrix.put( 8, self.size-1-k, bits[k] or k == 7)
##            self.used.put(   8, self.size-1-k, True)
#
#        for k in xrange(8):
#            self.matrix.put( 8, 8-k-(1 if k > 1 else 0),  bits[k+7])
##            self.used.put( 8, 8-k-(1 if k > 1 else 0),  True)
#            self.matrix.put( self.size-8+k, 8, bits[k+7])
##            self.used.put(   self.size-8+k, 8, True)

    def __drawFormatInfo(self, matrix, maskId):
        formatBits = {'L': '01', 'M': '00', 'Q': '11', 'H' : '10'}.get(self.correctionLevel) + maskId
        bits = encodeFormat(int(formatBits, 2))
        k = 0
        for k in xrange(8):
            matrix.put( k+(1 if k>5 else 0), 8, bits[k])
            matrix.put( 8, self.size-1-k, bits[k] or k == 7)
#            self.used.put(   8, self.size-1-k, True)

        for k in xrange(8):
            matrix.put( 8, 8-k-(1 if k > 1 else 0),  bits[k+7])
            matrix.put( self.size-8+k, 8, bits[k+7])



    def maskVersionInfo(self):
        if self.version >= 7:
            for k in xrange(18):
                a, b = divmod(k, 3)
                self.used.put(   a, self.size-11+b, True)
                self.used.put(   self.size-11+b, a, True)


    def drawVersionInfo(self):
        if self.version >= 7:
            bits = encodeVersion(self.version)[::-1]
            for k in xrange(18):
                a, b = divmod(k, 3)
                self.matrix.put( a, self.size-11+b, bits[k])
                self.matrix.put( self.size-11+b, a, bits[k])

    # см. табл.3

    def __splitIntoBlocks(self, words):
        wordCount = len(words)
        blocksCount = self.blocksCount[self.correctionLevel][self.version-1]
        smallBlockSize, overs = divmod(wordCount, blocksCount)
        smallBlockCount = blocksCount-overs
        start = 0
        result = []
        for iBlock in xrange(blocksCount):
            blockSize = smallBlockSize if iBlock < smallBlockCount else smallBlockSize+1
            result.append(words[start:start+blockSize])
            start += blockSize
        return result

    masks = { '000' : lambda row, column: (row + column) % 2 == 0,
              '001' : lambda row, column: row % 2 == 0,
              '010' : lambda row, column: (column) % 3 == 0,
              '011' : lambda row, column: (row + column) % 3 == 0,
              '100' : lambda row, column: (row//2 + column//3) % 2 == 0,
              '101' : lambda row, column: (row*column)%6 == 0, # ((row * column) % 2) + ((row * column) % 3) == 0,
              '110' : lambda row, column: (row*column)%6 < 3,  # ( ((row * column) % 2) + ((row * column) % 3) ) % 2 == 0
              '111' : lambda row, column: (row + column + row*column% 3) % 2 == 0, # ( ((row + column) %2) + ((row * column) % 3) ) % 2 == 0
            }

    def __applyMask(self, matrix, maskId):
        mask = self.masks[maskId]
        for y in xrange(self.size):
            for x in xrange(self.size):
                m = mask(y,x)
                if m and not self.used.get(x,y):
                    matrix.put(x,y, not matrix.get(x,y))


    def applyBestMask(self):
        minScore = minMaskId = None
        for maskId in self.masks:
            matrix = copy.deepcopy(self.matrix)
            self.__drawFormatInfo(matrix, maskId)
            self.__applyMask(matrix, maskId)
            score = self.calcPenalty(matrix)
#            print 'maskId:', maskId, 'score:', score
#            print unicode(matrix)
#            print
            if minMaskId is None or minScore>score:
                minMaskId = maskId
                minScore  = score
#        print 'best maskId:', minMaskId, 'best score:', minScore
        self.__drawFormatInfo(self.matrix, minMaskId)
        self.__applyMask(self.matrix, minMaskId)


    def calcPenalty(self, matrix):
        return (   self.calcPenalty1H(matrix)
                 + self.calcPenalty1V(matrix)
                 + self.calcPenalty2(matrix)
                 + self.calcPenalty3H(matrix)
                 + self.calcPenalty3V(matrix)
                 + self.calcPenalty4(matrix)
               )


    def calcPenalty1H(self, matrix):
        score = 0
        for y in xrange(self.size):
            currValue = None
            currCount = 0
            for x in xrange(self.size):
                value = matrix.get(x,y)
                if currValue == value:
                    currCount += 1
                else:
                    if currCount >= 5:
                        score += currCount-2
                    currValue = value
                    currCount = 1
            if currCount >= 5:
                score += currCount-2
        return score


    def calcPenalty1V(self, matrix):
        score = 0
        for x in xrange(self.size):
            currValue = None
            currCount = 0
            for y in xrange(self.size):
                value = matrix.get(x,y)
                if currValue == value:
                    currCount += 1
                else:
                    if currCount >= 5:
                        score += currCount-2
                    currValue = value
                    currCount = 1
            if currCount >= 5:
                score += currCount-2
        return score


    def calcPenalty2_(self, matrix):
        cnt = 0
        for y in xrange(self.size-1):
            for x in xrange(self.size-1):
                if matrix.get(x,y) == matrix.get(x,y+1) == matrix.get(x+1,y) == matrix.get(x+1,y+1):
                    cnt += 1
        return cnt*3

    def calcPenalty2(self, matrix):
        cnt = 0
        v = [ matrix.get(x,0) for x in xrange(self.size)]
        for y in xrange(1, self.size):
            vn = [ matrix.get(x,y) for x in xrange(self.size)]
            for x in xrange(1, self.size):
                if v[x-1] == v[x] == vn[x-1] == vn[x]:
                    cnt += 1
            v = vn
        return cnt*3



    def calcPenalty3H(self, matrix):
        cnt = 0
        for y in xrange(self.size):
            s = ''
            for x in xrange(self.size):
                s += '1' if matrix.get(x,y) else '0'
            cnt += s.count('10111010000') + s.count('00001011101')
        return cnt*40


    def calcPenalty3V(self, matrix):
        cnt = 0
        for x in xrange(self.size):
            s = ''
            for y in xrange(self.size):
                s += '1' if matrix.get(x,y) else '0'
            cnt += s.count('10111010000') + s.count('00001011101')
        return cnt*40


    def calcPenalty4(self, matrix):
        cnt = 0
        for y in xrange(self.size):
            for x in xrange(self.size):
                if matrix.get(x,y):
                    cnt += 1
        total = self.size**2
        return (abs(20*cnt-10*total)//total)*10


if __name__ == '__main__':
#    w = QRCodeWriter('HELLO WORLD')
#    w = QRCodeWriter('HELLO WORLD', version=1, correctionLevel='Q')
#    w = QRCodeWriter('HELLO WORLD', version=1)
#    w = QRCodeWriter('http://samson-rus.com', version=30)
#    w = QRCodeWriter('http://samson-rus.com/SAMSON/12345', version=40)
    w = QRCodeWriter('http://samson-rus.com', eci=26)
#    w = QRCodeWriter(u'*\u0410\u043d\u0442\u043c\u0430\u043d\u0430/\u0422\u0435\u0441\u0442\u0430//30.09.2000/\u0416/030-303-030 60/13 21/234213/\u041e\u041c\u0421 \u0422\u0435\u0440\u0440\u0438\u0442\u043e\u0440\u0438\u0430\u043b\u044c\u043d\u044b\u0439 \u0417\u0410\u041e "\u0421\u041c\u041a \u0410\u0421\u041a-\u041c\u0435\u0434" 134 1234212312321/12.0/\u0423\u0434\u043e\u0432\u043b\u0435\u0442\u0432\u043e\u0440\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0435/\u0412\u0435\u0437\u0438\u043a\u0443\u043b\u044f\u0440\u043d\u043e\u0435/\u0421\u0443\u0445\u0438\u0435 \u0440\u0430\u0441\u0441\u0435\u044f\u043d\u043d\u044b\u0435/23.0/14444.0/\u042f\u0441\u043d\u044b\u0435/134.0/1234.0/True/True/True/2 \u0413\u0440\u0438\u043f\u043f\u043e\u043b \u043f\u043b\u044e\u0441/\u0443\u043a\u0443\u043a\u0443\u043a\u0443\u043a\u0443\u043a\u0443\u043a\u0443\u043a\u0443\u043a/True/\u0445\u0445\u0445\u0445\u0445\u0445\u0445\u0445\u0445\u0445\u0445/True/True/True/True/True/True/True/True/True/\u0439\u0439\u0439\u0439\u0439\u0439\u0439\u0439\u0439\u0439\u0439\u0439\u0439\u0439\u0439\u0439\u0439\u0439\u0439\u0439/True/\u0446\u0446\u0446\u0446\u0446\u0446\u0446\u0446\u0446\u0446\u0446\u0446\u0446\u0446/True/\u0443\u0443\u0443\u0443\u0443\u0443\u0443\u0443\u0443\u0443\u0443/True/7 \u0422\u044f\u0436\u0435\u043b\u044b\u0435 \u0430\u043b\u043b\u0435\u0440\u0433\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0440\u0435\u0430\u043a\u0446\u0438\u0438 \u0432 \u0430\u043d\u0430\u043c\u043d\u0435\u0437\u0435/True/3 \u041e\u0441\u0442\u0430\u043b\u044c\u043d\u044b\u0435/27.03.2021/\u041e\u041c\u0421 \u0422\u0435\u0440\u0440\u0438\u0442\u043e\u0440\u0438\u0430\u043b\u044c\u043d\u044b\u0439/\u0417\u0410\u041e "\u0421\u041c\u041a \u0410\u0421\u041a-\u041c\u0435\u0434"/\u0418\u0432\u0430\u043d\u043e\u043e\u0432/\u0418\u0432\u0430\u043d/\u041f\u0435\u0442\u0440\u043e\u0432\u0438\u0447/024-678-902 00'.encode('utf-8'))

    print w.size, w.version, w.correctionLevel
    print unicode(w.matrix)
    print
#    print unicode(w.used)
