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
## Это генерация Data Matrix ЕСС 200
##
## использованы источники:
##   ГОСТ Р ИСО/МЭК 16022-2008 ( http://docs.cntd.ru/document/1200071931 )
##   https://en.wikipedia.org/wiki/Data_Matrix
##   http://grandzebu.net/informatique/codbar-en/datamatrix.htm
##
#############################################################################


import re
from math import ceil

from ReedSolomonCode import RSCode
from BitMatrix import BitMatrix


class DataMatrixWriter:
    #         (h,   w): ключ: размер символа
    #                   (hic, wic, ((dbc, ndcw, neccw), (dbc, ndcw, neccw)...))
    #                    hic: высота в клетках, количество областей данных по вертикали
    #                    wic: ширина в клетках, количество областей данных по горизонтали
    #                    dbc:  количество блоков данных
    #                    ndcw: количество кодовых слов данных в блоке
    #                    neccw:количество кодовых слов исправления ошибок в блоке
    #                    тройка (dbc, ndcw, neccw) может быть поторена несколько раз.
    defs = {
            ( 10,  10): ( 1, 1, ((1,   3,  5),               )),
            ( 12,  12): ( 1, 1, ((1,   5,  7),               )),
            ( 14,  14): ( 1, 1, ((1,   8, 10),               )),
            ( 16,  16): ( 1, 1, ((1,  12, 12),               )),
            ( 18,  18): ( 1, 1, ((1,  18, 14),               )),
            ( 20,  20): ( 1, 1, ((1,  22, 18),               )),
            ( 22,  22): ( 1, 1, ((1,  30, 20),               )),
            ( 24,  24): ( 1, 1, ((1,  36, 24),               )),
            ( 26,  26): ( 1, 1, ((1,  44, 28),               )),
            ( 32,  32): ( 2, 2, ((1,  62, 36),               )),
            ( 36,  36): ( 2, 2, ((1,  86, 42),               )),
            ( 40,  40): ( 2, 2, ((1, 114, 48),               )),
            ( 44,  44): ( 2, 2, ((1, 144, 56),               )),
            ( 48,  48): ( 2, 2, ((1, 174, 68),               )),
            ( 52,  52): ( 2, 2, ((2, 102, 42),               )),
            ( 64,  64): ( 4, 4, ((2, 140, 56),               )),
            ( 72,  72): ( 4, 4, ((4,  92, 36),               )),
            ( 80,  80): ( 4, 4, ((4, 114, 48),               )),
            ( 88,  88): ( 4, 4, ((4, 144, 56),               )),
            ( 96,  96): ( 4, 4, ((4, 174, 68),               )),
            (104, 104): ( 4, 4, ((6, 136, 56),               )),
            (120, 120): ( 6, 6, ((6, 175, 68),               )),
            (132, 132): ( 6, 6, ((8, 163, 62),               )),
            (144, 144): ( 6, 6, ((8, 156, 62), (2, 155, 62), )),
            (  8,  18): ( 1, 1, ((1,   5,  7),               )),
            (  8,  32): ( 1, 2, ((1,  10, 11),               )),
            ( 12,  26): ( 1, 1, ((1,  16, 14),               )),
            ( 12,  36): ( 1, 2, ((1,  22, 18),               )),
            ( 16,  36): ( 1, 2, ((1,  32, 24),               )),
            ( 16,  48): ( 1, 2, ((1,  49, 28),               )),
           }

    def __init__(self, data, size=None, minSize=10, maxSize=None, shape=0, eci=None, encoding=None):
        cws = self.encode(data, eci, encoding)
        if size is None:
            h,w = self.chooseSize(len(cws), minSize, maxSize, shape)
        else:
            h,w = self.parseSize(size)
            if self.getMaxDataSize(h, w) < len(cws):
                raise Exception('Too big')

        self.height = h
        self.width = w
        self.heightInCells, self.widthInCells, self.blockDefs = self.defs[(h,w)]
        assert( self.height % self.heightInCells == 0 )
        self.cellHeight = self.height // self.heightInCells
        assert( self.width % self.widthInCells == 0 )
        self.cellWidth = self.width // self.widthInCells
        self.logicalHeight = (self.cellHeight-2) * self.heightInCells
        self.logicalWidth = (self.cellWidth-2) * self.widthInCells
        self.matrix = BitMatrix(width=self.width, height=self.height)
        self.used = BitMatrix(width=self.logicalWidth, height=self.logicalHeight)
        self.drawFinderPatterns()

        self.fillPadding(cws, self.getMaxDataSize(h, w))
        outCws = self.prepareBits(cws)

        self.placeBits(outCws)


    @classmethod
    def encode(cls, data, eci, encoding):
        if isinstance(data, unicode):
            src = bytearray(data.encode('utf8'))
        elif isinstance(data, bytearray):
            src = data
        elif not isinstance(data, bytes):
            src = bytearray(bytes(data))
        else:
            src = bytearray(data)

        result = bytearray()
        if eci is not None:
            cls._encodeEci(result, eci)

        if src:
            if isinstance(encoding, (str, unicode)):
                encoding = encoding.lower()
            else:
                encoding = ''
            if encoding.startswith('a'):
                cls._encodeASCII(result, src)
            elif encoding.startswith('c'):
                cls._encodeC40(result, src)
            elif encoding.startswith('t'):
                cls._encodeTEXT(result, src)
            elif encoding.startswith('b'):
                cls._encodeBASE256(result, src)
            else:
                cls._encodeANY(result, src)
        return result



        d, m = divmod(len(data), 250)
        if d != 0:
            result = bytearray([ 231, d+249, m ])
        else:
            result = bytearray([ 231, m ])
        for ch in data:
            result.append( ord(ch) )
        for p in xrange(1, len(result)):
            r = 149*(p+1) % 255 + 1
            result[p] = (result[p] + r) % 256
        return result


    @classmethod
    def _encodeEci(cls, result, eci):
        if 0<=eci<=126:
            result.append(241)
            result.append(eci+1)
            return
        if 127<=eci<=16382:
            c1, c2 = divmod(eci-127, 254)
            result.append(241)
            result.append(c1+128)
            result.append(c2+1)
            return
        if 16383<=eci<=999999:
            c1, c23 = divmod(eci-16383, 64516)
            c2, c3 = divmod(c23, 254)
            result.append(241)
            result.append(c1+192)
            result.append(c2+1)
            result.append(c3+1)
            return
        raise Exception('bad ECI')


    @classmethod
    def parseSize(cls, size):
        if (size, size) in cls.defs:
            return (size, size)
        if isinstance(size, tuple):
           if size in cls.defs:
               return size
        if isinstance(size, (str, unicode)):
           m = re.match(r'\s*(\d+)\D+(\d+)\s*', size)
           if m:
               h = int(m.groups()[0])
               w = int(m.groups()[1])
               if (h, w) in cls.defs:
                   return (h, w)
           m = re.match(r'\s*(\d+)\s*', size)
           if m:
               h = w = int(m.groups()[0])
               if (h, w) in cls.defs:
                   return (h, w)
        raise Exception('Size undefined')


    @classmethod
    def chooseSize(cls, cwCount, minSize, maxSize, shape):
        sizes = cls.defs.keys()
        sizes.sort(key=lambda (h, w): (h != w, cls.getMaxDataSize(h, w)))
        for (h, w) in sizes:
            if (    (not minSize or h>=minSize)
                and (not maxSize or h<=maxSize)
                and (shape==0 or h==w)
               ):
               if cwCount<=cls.getMaxDataSize(h, w):
                   return (h, w)
        raise Exception('Too big')


    @classmethod
    def getMaxDataSize(cls, h, w):
        hic, wic, blockDefs = cls.defs[(h,w)]
        maxDataSize = sum( dbc*ndcw for (dbc, ndcw, neccw) in blockDefs )
        return maxDataSize



    def drawFinderPatterns(self):
        for y in xrange(0, self.height, self.cellHeight):
            for x in xrange(0, self.width, self.cellWidth):
                self.drawFinderPattern(y, x)


    def drawFinderPattern(self, basey, basex):
        for x in xrange(self.cellWidth):
            if x % 2 == 0:
                self.matrix.put(basex + x, basey, True)
            self.matrix.put(basex + x, basey+self.cellHeight-1, True)

        for y in xrange(self.cellHeight):
            if y % 2:
                self.matrix.put(basex+self.cellWidth-1, basey+y, True)
            self.matrix.put(basex, basey+y, True)


    def fillPadding(self, csw, size):
        if len(csw)<size:
            csw.append(129)
        for pos in xrange(len(csw), size):
            csw.append(((pos+1)*149 % 253 + 1 + 129) % 254 )


    def prepareBits(self, cws):
        dataBlocks = []
        eccBlocks = []

        numBlocks = sum(dbc for (dbc, ndcw, neccw) in self.blockDefs)
        if numBlocks == 1:
            dataBlocks = [ cws ]
        else:
            dataBlocks = [ bytearray() for i in xrange(numBlocks) ]
            for i, cw in enumerate(cws):
                dataBlocks[i%numBlocks].append(cw)

        iBlock = 0
        for (dbc, ndcw, neccw) in self.blockDefs:
            assert( ndcw == len(dataBlocks[iBlock]) )
            rsc = RSCode(256, 301, n=ndcw + neccw, k=ndcw, basePower=1)
            for i in xrange(dbc):
                ecc = rsc.encode(list(dataBlocks[iBlock]))
                eccBlocks.append(ecc)
                iBlock += 1

        result = bytearray()
        result.extend(cws)
        for i in xrange(max(len(ecc) for ecc in eccBlocks)):
            for ecc in eccBlocks:
                result.append(ecc[i])
        return result


    def placeBits(self, cws):
        cwi = iter(cws)
        logicalRow = 4
        logicalCol = 0

        while logicalRow < self.logicalHeight or logicalCol < self.logicalWidth:
            # repeatedly first check for one of the special corner cases, then... 
            if logicalRow == self.logicalHeight and logicalCol == 0:
                self.placeCorner1(cwi.next())
            if logicalRow == self.logicalHeight-2 and logicalCol == 0 and self.logicalWidth%4:
                self.placeCorner2(cwi.next())
            if logicalRow == self.logicalHeight-2 and logicalCol == 0 and self.logicalWidth%8 == 4:
                self.placeCorner3(cwi.next())
            if logicalRow == self.logicalHeight+4 and logicalCol == 2 and not self.logicalWidth%8:
                self.placeCorner4(cwi.next())

            # /* sweep upward diagonally, inserting successive characters,... */
            while True:
                if logicalRow < self.logicalHeight and (logicalCol >= 0) and not self.used.get(logicalCol, logicalRow):
                    self.placeUtah(logicalRow, logicalCol, cwi.next())
                logicalRow -= 2
                logicalCol += 2
                if logicalRow<0 or logicalCol >= self.logicalWidth:
                    break
            logicalRow += 1
            logicalCol += 3
            # & then sweep downward diagonally, inserting successive haracters,... 
            while True:
                if logicalRow >= 0 and logicalCol < self.logicalWidth and not self.used.get(logicalCol, logicalRow):
                    self.placeUtah(logicalRow, logicalCol, cwi.next())
                logicalRow += 2
                logicalCol -= 2
                if logicalRow >= self.logicalHeight or logicalCol < 0:
                    break
            logicalRow += 3
            logicalCol += 1
        # until the entire array is scanned
        # Lastly, if the lower righthand corner is untouched, fill in fixed pattern 
        if not  self.used.get(self.logicalWidth-1, self.logicalHeight-1):
            self.placeModule(self.logicalHeight-1, self.logicalWidth-1, 255, 1)
            self.placeModule(self.logicalHeight-2, self.logicalWidth-2, 255, 1)



    # "utah" places the 8 bits of a utah-shaped symbol character in ECC200
    def placeUtah(self, logicalRow, logicalCol, cw):
        self.placeModule(logicalRow-2, logicalCol-2, cw, 1);
        self.placeModule(logicalRow-2, logicalCol-1, cw, 2);
        self.placeModule(logicalRow-1, logicalCol-2, cw, 3);
        self.placeModule(logicalRow-1, logicalCol-1, cw, 4);
        self.placeModule(logicalRow-1, logicalCol,   cw, 5);
        self.placeModule(logicalRow,   logicalCol-2, cw, 6);
        self.placeModule(logicalRow,   logicalCol-1, cw, 7);
        self.placeModule(logicalRow,   logicalCol,   cw, 8);


    # "cornerN" places 8 bits of the four special corner cases in ECC200
    def placeCorner1(self, cw):
        self.placeModule(self.logicalHeight-1, 0,                   cw, 1);
        self.placeModule(self.logicalHeight-1, 1,                   cw, 2);
        self.placeModule(self.logicalHeight-1, 2,                   cw, 3);
        self.placeModule(0,                    self.logicalWidth-2, cw, 4);
        self.placeModule(0,                    self.logicalWidth-1, cw, 5);
        self.placeModule(1,                    self.logicalWidth-1, cw, 6);
        self.placeModule(2,                    self.logicalWidth-1, cw, 7);
        self.placeModule(3,                    self.logicalWidth-1, cw, 8);


    def placeCorner2(self, cw):
        self.placeModule(self.logicalHeight-3, 0,                   cw, 1);
        self.placeModule(self.logicalHeight-2, 0,                   cw, 2);
        self.placeModule(self.logicalHeight-1, 0,                   cw, 3);
        self.placeModule(0,                    self.logicalWidth-4, cw, 4);
        self.placeModule(0,                    self.logicalWidth-3, cw, 5);
        self.placeModule(0,                    self.logicalWidth-2, cw, 6);
        self.placeModule(0,                    self.logicalWidth-1, cw, 7);
        self.placeModule(1,                    self.logicalWidth-1, cw, 8);


    def placeCorner3(self, cw):
        self.placeModule(self.logicalHeight-3, 0,                   cw, 1);
        self.placeModule(self.logicalHeight-2, 0,                   cw, 2);
        self.placeModule(self.logicalHeight-1, 0,                   cw, 3);
        self.placeModule(0,                    self.logicalWidth-2, cw, 4);
        self.placeModule(0,                    self.logicalWidth-1, cw, 5);
        self.placeModule(1,                    self.logicalWidth-1, cw, 6);
        self.placeModule(2,                    self.logicalWidth-1, cw, 7);
        self.placeModule(3,                    self.logicalWidth-1, cw, 8);


    def placeCorner4(self, cw):
        self.placeModule(self.logicalHeight-1, 0,                   cw, 1);
        self.placeModule(self.logicalHeight-1, self.logicalWidth-1, cw, 2);
        self.placeModule(0,                    self.logicalWidth-3, cw, 3);
        self.placeModule(0,                    self.logicalWidth-2, cw, 4);
        self.placeModule(0,                    self.logicalWidth-1, cw, 5);
        self.placeModule(1,                    self.logicalWidth-3, cw, 6);
        self.placeModule(1,                    self.logicalWidth-2, cw, 7);
        self.placeModule(1,                    self.logicalWidth-1, cw, 8);


    def placeModule(self, logicalRow, logicalCol, cw, bit):
        if logicalRow < 0:
            logicalRow += self.logicalHeight
            logicalCol += 4 - ((self.logicalHeight+4)%8)
        if logicalCol < 0:
            logicalCol += self.logicalWidth
            logicalRow += 4 - ((self.logicalWidth+4)%8)

        cell, offset = divmod(logicalRow, self.cellHeight-2)
        row = cell*self.cellHeight + offset + 1

        cell, offset = divmod(logicalCol, self.cellWidth-2)
        col = cell*self.cellWidth + offset + 1

        self.matrix.put(col, row, cw & (1<<(8-bit)) )
        self.used.put(logicalCol, logicalRow, True)

    #
    # кодирование данных
    #

    ASCII   = 'a'
    C40     = 'c'
    TEXT    = 't'
    BASE256 = 'b'

    @classmethod
    def _encodeASCII(cls, result, src):
        cls._produceASCII(result, src, 0)

    @classmethod
    def _encodeC40(cls, result, src):
        tmpBuff = bytearray()
        rollbackTmpBuffLen = 0
        rollbackPos = 0
        for pos, byte in enumerate(src):
            if len(tmpBuff) % 3 == 0:
                rollbackTmpBuffLen = len(tmpBuff)
                rollbackPos = pos
            tmpBuff.extend( cls._convertC40(byte) )
        if len(tmpBuff)%3:
            if rollbackTmpBuffLen:
                cls._produceC40(result, tmpBuff[:rollbackTmpBuffLen])
            cls._produceASCII(result, src, rollbackPos)
        elif tmpBuff:
            cls._produceC40(result, tmpBuff)


    @classmethod
    def _encodeTEXT(cls, result, src):
        tmpBuff = bytearray()
        rollbackTmpBuffLen = 0
        rollbackPos = 0
        for pos, byte in enumerate(src):
            if len(tmpBuff) % 3 == 0:
                rollbackTmpBuffLen = len(tmpBuff)
                rollbackPos = pos
            tmpBuff.extend( cls._convertTEXT(byte) )
        if len(tmpBuff)%3:
            if rollbackTmpBuffLen:
                cls._produceTEXT(result, tmpBuff[:rollbackTmpBuffLen])
            cls._produceASCII(result, src, rollbackPos)
        elif tmpBuff:
            cls._produceTEXT(result, tmpBuff)


    @classmethod
    def _encodeBASE256(cls, result, src):
        cls._produceBASE256(result, src)


    @classmethod
    def _encodeANY(cls, result, src):
        encodingMode = cls.ASCII
        pos = 0
        tmpBuff = bytearray()
#        rollbackTmpBuffLen = None
#        rollbackPos = None

        while pos<len(src):
            if encodingMode == cls.ASCII:
                if (     pos<len(src)-1
                     and 48<=src[pos]<=57
                     and 48<=src[pos+1]<=57
                   ):
                    result.append( 130 + (src[pos]-48)*10 + (src[pos+1]-48) )
                    pos += 2
                    continue

                nextEncodingMode = cls._adviseEncodingMode(src, pos, encodingMode)
                if encodingMode != nextEncodingMode:
                    encodingMode = nextEncodingMode
                    continue
                if src[pos]>=128:
                    result.append(235)
                    result.append(src[pos]-128)
                else:
                    result.append(src[pos]+1)
                pos += 1
            elif encodingMode == cls.C40:
                if tmpBuff and len(tmpBuff)%3 == 0:
                    nextEncodingMode = cls._adviseEncodingMode(src, pos, encodingMode)
                    if encodingMode != nextEncodingMode:
                        cls._produceC40(result, tmpBuff)
                        del tmpBuff[:]
                        encodingMode = nextEncodingMode
                        continue
                if len(tmpBuff) % 3 == 0:
                    rollbackTmpBuffLen = len(tmpBuff)
                    rollbackPos = pos
                tmpBuff.extend( cls._convertC40(src[pos]) )
                pos += 1
            elif encodingMode == cls.TEXT:
                if tmpBuff and len(tmpBuff)%3 == 0:
                    nextEncodingMode = cls._adviseEncodingMode(src, pos, encodingMode)
                    if encodingMode != nextEncodingMode:
                        cls._produceTEXT(result, tmpBuff)
                        del tmpBuff[:]
                        encodingMode = nextEncodingMode
                        continue
                if len(tmpBuff) % 3 == 0:
                    rollbackTmpBuffLen = len(tmpBuff)
                    rollbackPos = pos
                tmpBuff.extend( cls._convertTEXT(src[pos]) )
                pos += 1
            elif encodingMode == cls.BASE256:
                if tmpBuff:
                    nextEncodingMode = cls._adviseEncodingMode(src, pos, encodingMode)
                    if encodingMode != nextEncodingMode:
                        cls._produceBASE256(result, tmpBuff)
                        del tmpBuff[:]
                        encodingMode = nextEncodingMode
                        continue
                tmpBuff.append(src[pos])
                pos += 1
            else:
                assert False

        if encodingMode == cls.C40:
            if len(tmpBuff)%3:
                if rollbackTmpBuffLen:
                    cls._produceC40(result, tmpBuff[:rollbackTmpBuffLen])
                cls._produceASCII(result, src, rollbackPos)
            elif tmpBuff:
                cls._produceC40(result, tmpBuff)
        elif encodingMode == cls.TEXT:
            if len(tmpBuff)%3:
                if rollbackTmpBuffLen:
                    cls._produceTEXT(result, tmpBuff[:rollbackTmpBuffLen])
                cls._produceASCII(result, src, rollbackPos)
            elif tmpBuff:
                cls._produceTEXT(result, tmpBuff)
        elif encodingMode == cls.BASE256:
            if tmpBuff:
                cls._produceBASE256(result, tmpBuff)

    @classmethod
    def _adviseEncodingMode(cls, src, pos, encodingMode):
        avgShiftBASE256 = 1 if len(src)-pos<250 else 1.25
        if encodingMode == cls.ASCII:
            shiftASCII, shiftC40, shiftTEXT, shiftBASE256 = 0, 1, 1, avgShiftBASE256
        elif encodingMode == cls.C40:
            shiftASCII, shiftC40, shiftTEXT, shiftBASE256 = 1, 0, 1, avgShiftBASE256
        elif encodingMode == cls.TEXT:
            shiftASCII, shiftC40, shiftTEXT, shiftBASE256 = 1, 1, 0, avgShiftBASE256
        elif encodingMode == cls.BASE256:
            shiftASCII, shiftC40, shiftTEXT, shiftBASE256 = 0, 1, 1, 0
        else:
            assert False
        cntASCII = cntC40 = cntTEXT = cntBASE256 = 0
        rollbackCntC40,  rollbackPosC40  = 0, pos
        rollbackCntTEXT, rollbackPosTEXT = 0, pos

        for i in xrange(pos, len(src)):
            d = src[i]
            c = chr(d)

            if '0'<=c<='9':
                cntASCII += 0.5
            elif d>=128:
                cntASCII = ceil(cntASCII)+2
            else:
                cntASCII = ceil(cntASCII)+1

            if cntC40%3 == 0:
                rollbackCntC40, rollbackPosC40  = cntC40, i
            cntC40 += cls._lenC40(d)

            if cntTEXT%3 == 0:
                rollbackCntTEXT, rollbackPosTEXT  = cntTEXT, i
            cntTEXT += cls._lenTEXT(d)
            cntBASE256 += 1

            if i-pos>=3:
                scores  = [ (shiftASCII + cntASCII,     cls.ASCII),
                            (shiftC40 + cntC40*2/3.,    cls.C40),
                            (shiftTEXT + cntTEXT*2/3.,  cls.TEXT),
                            (shiftBASE256 + cntBASE256, cls.BASE256)
                          ]
                scores.sort()
                firstScore,  firstEncodingMode = scores[0]
                secondScore, secondEncodingMode = scores[1]
                if firstScore+1<=secondScore:
                    return firstEncodingMode

        if cntC40%3 == 0:
            scoreC40 = shiftC40 + cntC40*2//3
        else:
            scoreC40 = shiftC40 + rollbackCntC40*2//3 + 1 + cls._lenASCII(src, rollbackPosC40)
        if cntTEXT%3 == 0:
            scoreTEXT = shiftTEXT + cntTEXT*2//3
        else:
            scoreTEXT = shiftTEXT + rollbackCntTEXT*2//3 + 1 + cls._lenASCII(src, rollbackPosTEXT)

        scores = [ (shiftASCII+ceil(cntASCII),     0, cls.ASCII),
                   (scoreC40,                      2, cls.C40),
                   (scoreTEXT,                     2, cls.TEXT),
                   (ceil(shiftBASE256)+cntBASE256, 1, cls.BASE256)
                 ]
        firstScore, firstPrty, firstEncodingMode = min(scores)
        return firstEncodingMode


    @classmethod
    def _lenASCII(cls, src, pos):
        cntASCII = 0
        for i in xrange(pos, len(src)):
            d = src[i]
            c = chr(d)

            if '0'<=c<='9':
                cntASCII += 0.5
            elif d>=128:
                cntASCII = ceil(cntASCII)+2
            else:
                cntASCII = ceil(cntASCII)+1
        return ceil(cntASCII)


    @classmethod
    def _produceASCII(cls, result, src, pos):
        while pos<len(src):
            if (     pos<len(src)-1
                 and 48<=src[pos]<=57
                 and 48<=src[pos+1]<=57
               ):
                result.append( 130 + (src[pos]-48)*10 + (src[pos+1]-48) )
                pos += 2
            else:
                if src[pos]>=128:
                    result.append(235)
                    result.append(src[pos]-128)
                else:
                    result.append(src[pos]+1)
                pos += 1


    # код символа -> табица*40 + код_по_таблице
    # табица = 0 для обсновной таблицы, 1 для 
    tabC40  = bytearray([ 40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54,  55,
                          56,  57,  58,  59,  60,  61,  62,  63,  64,  65,  66,  67,  68,  69,  70,  71,
                           3,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,
                           4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  95,  96,  97,  98,  99, 100,
                         101,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,
                          29,  30,  31,  32,  33,  34,  35,  36,  37,  38,  39, 102, 103, 104, 105, 106,
                         120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135,
                         136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151])

    tabTEXT = bytearray([ 40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54,  55,
                          56,  57,  58,  59,  60,  61,  62,  63,  64,  65,  66,  67,  68,  69,  70,  71,
                           3,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,
                           4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  95,  96,  97,  98,  99, 100,
                         101, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135,
                         136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 102, 103, 104, 105, 106,
                         120,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,
                          29,  30,  31,  32,  33,  34,  35,  36,  37,  38,  39, 147, 148, 149, 150, 151])

    @classmethod
    def _lenC40orTEXT(cls, tab, d):
        if d<=127:
            shift, code = divmod(tab[d], 40)
            if shift == 0:
                return 1
            else:
                return 2
        else:
            shift, code = divmod(tab[d-128], 40)
            if shift == 0:
                return 3
            else:
                return 4


    @classmethod
    def _convertC40orTEXT(cls, tab, d):
        if d<=127:
            shift, code = divmod(tab[d], 40)
            if shift == 0:
                return [ code ]
            else:
                return [ shift-1, code ]
        else:
            shift, code = divmod(tab[d-128], 40)
            if shift == 0:
                return [ 1, 30, code ]
            else:
                return [ 1, 30, shift-1, code ]


    @classmethod
    def _produceC40orTEXT(cls, result, tmpBuff):
        for p in xrange(0, len(tmpBuff), 3):
            c1 = tmpBuff[p]
            c2 = tmpBuff[p+1]
            c3 = tmpBuff[p+2]
            a, b = divmod((c1*40 + c2)*40 + c3 + 1, 256)
            result.append(a)
            result.append(b)
        result.append(254) # UNLATCH


    @classmethod
    def _lenC40(cls, d):
        return cls._lenC40orTEXT(cls.tabC40, d)


    @classmethod
    def _convertC40(cls, d):
        return cls._convertC40orTEXT(cls.tabC40, d)


    @classmethod
    def _produceC40(cls, result, tmpBuff):
        result.append(230) # LATCH_C40
        cls._produceC40orTEXT(result, tmpBuff)


    @classmethod
    def _lenTEXT(cls, d):
        return cls._lenC40orTEXT(cls.tabTEXT, d)


    @classmethod
    def _convertTEXT(cls, d):
        return cls._convertC40orTEXT(cls.tabTEXT, d)



    @classmethod
    def _produceTEXT(cls, result, tmpBuff):
        result.append(239) # LATCH_TEXT
        cls._produceC40orTEXT(result, tmpBuff)


    @classmethod
    def _produceBASE256(cls, result, tmpBuff):
        def addv(d):
            pos = len(result)+1
            r = 149*pos%255 + 1
            result.append((d+r)%256)

        result.append(231) # LATCH_BASE256
        d,m = divmod(len(tmpBuff), 250)
        if d:
            addv(d+249)
        addv(m)
        for d in tmpBuff:
            addv(d)



if __name__ == '__main__':
#    w = DataMatrixWriter('Ab', size=14)
#    w = DataMatrixWriter('Ab', size=14, eci=22)
#    w = DataMatrixWriter(u'Привет'.encode('cp1251'), size=16, eci=22)
#    w = DataMatrixWriter(u'Привет'.encode('cp1251'), eci=22)
#    w = DataMatrixWriter(u'Привет'.encode('cp1251'), size="12x36",  eci=22)
#    w = DataMatrixWriter(u'Привет'.encode('utf-8'), size="132x132",  eci=26)
#    w = DataMatrixWriter(u'Привет'.encode('utf-8'), size=144)
#    w = DataMatrixWriter(u'Привет'.encode('utf-8'),  eci=26)
#    w = DataMatrixWriter(u'Привет'.encode('utf-8'))
#    w = DataMatrixWriter('Ab', size=14, eci=1022)
#    w = DataMatrixWriter('Ab', size=14, eci=100022)
#    w = DataMatrixWriter('Hello world!', size=44)
#    w = DataMatrixWriter('Hello world!', size=44)
#    w = DataMatrixWriter(u'!!8!!!01!001234567891!!1!0!2011-01-01!Городская больница №1!г.Москва, ул.Бутырская, д.88!123456789012345!Иванов!Иван!Иванович!1980-01-01!0!ОАО Предприятие!1!01!!!!0!!!!!!!!!!!!!!!!!!!!!!2011-05-01!2011-05-10!Терапевт!Петрова В.В.!!!!!!!!!!!2011-05-11!!'.encode('cp1251'),  eci=22, encoding='base256')
#    w = DataMatrixWriter(u'!!8!!!01!001234567891!!1!0!2011-01-01!Городская больница №1!г.Москва, ул.Бутырская, д.88!123456789012345!Иванов!Иван!Иванович!1980-01-01!0!ОАО Предприятие!1!01!!!!0!!!!!!!!!!!!!!!!!!!!!!2011-05-01!2011-05-10!Терапевт!Петрова В.В.!!!!!!!!!!!2011-05-11!!'.encode('cp1251'),  eci=22)
#    w = DataMatrixWriter(u'!!8!!!01!001234567891!!1!0!2011-01-01!Городская больница №1!г.Москва, ул.Бутырская, д.88!123456789012345!Иванов!Иван!Иванович!1980-01-01!0!ОАО Предприятие!1!01!!!!0!!!!!!!!!!!!!!!!!!!!!!2011-05-01!2011-05-10!Терапевт!Петрова В.В.!!!!!!!!!!!2011-05-11!!'.encode('cp1251'))
#    w = DataMatrixWriter(u'Привет'.encode('utf-8'),  eci=26, size=48)
    w = DataMatrixWriter(u'Привет'.encode('utf-8'),  eci=26, size=52)

    print w.width, w.height
    print unicode(w.matrix)
    print
