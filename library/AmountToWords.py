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


__all__ = [ 'currencyRUR',
            'currencyUSD',
            'amountToWords',
          ]


minus = u'минус'

zero = u'ноль'

masculine = (zero, u'один', u'два', u'три', u'четыре', u'пять', u'шесть', u'семь', u'восемь', u'девять')
feminine  = (zero, u'одна', u'две') + masculine[3:]
neuter    = (zero, u'одно') + masculine[2:]

units = { 'm': masculine,
          'f': feminine,
          'n': neuter,
        }

secondTen = ( u'десять', u'одиннадцать',  u'двенадцать', u'тринадцать', u'четырнадцать', u'пятнадцать', u'шестнадцать', u'семнадцать', u'восемнадцать', u'девятнадцать')
tens      = ('', '', u'двадцать', u'тридцать', u'сорок', u'пятьдесят', u'шестьдесят', u'семьдесят', u'восемьдесят', u'девяносто')
hundreds  = ('', u'сто', u'двести', u'триста', u'четыреста', u'пятьсот', u'шестьсот', u'семьсот', u'восемьсот', u'девятьсот')

#          один        два         много      грамматический род (mfn)
nRouble = (u'рубль',   u'рубля',   u'рублей', 'm')
nCop    = (u'копейка', u'копейки', u'копеек', 'f')
currencyRUR = (nRouble, nCop)

nDollar = (u'доллар',  u'доллара', u'долларов', 'm')
nCent   = (u'цент',    u'цента',   u'центов', 'm')
currencyUSD = (nDollar, nCent)

#nPeople = (u'человек', u'человека', u'человек', 'm')
#currencyPeople = (nPeople, None)

#nEvent = (u'случай',   u'случая',   u'случаев', 'm')
#currencyEvent = (nEvent,  None)

nThousand = (u'тысяча', u'тысячи',      u'тысяч', 'f')
nMillion  = (u'миллион', u'миллиона',   u'миллионов', 'm')
nBillion  = (u'миллиард', u'миллиарда', u'миллиардов', 'm')


def writeThousand(num, gender):
    if num:
        numTens, numUnits = divmod(num, 10)
        numHundreds, numTens = divmod(numTens, 10)

        res = []
        if numHundreds:
            res.append(hundreds[numHundreds])

        if numTens == 1:
            res.append(secondTen[numUnits])
        else:
            if numTens:
                res.append(tens[numTens])
            if numUnits:
                res.append(units[gender][numUnits])
        return ' '.join(res)
    else:
        return ''


def selectDeclension(descr, num):
    if (num//10)%10 != 1:
        if num%10 == 1:
            return descr[0]
        elif 1<num%10<5:
            return descr[1]
    return descr[2]


def formThousand(descr, num):
    return ('%s %s' % (writeThousand(num, descr[3]), selectDeclension(descr, num))) if num else ''


def writeNumber(descr, num):
    assert isinstance(num, (int, long))
    assert num<10**12
    if num:
        res = []
        res.append(formThousand(nBillion,  num//10**9 % 1000))
        res.append(formThousand(nMillion,  num//10**6 % 1000))
        res.append(formThousand(nThousand, num//1000  % 1000))
        res.append(writeThousand(num % 1000, descr[3]))
        return ' '.join(filter(None, res))
    else:
        return zero


def amountToWords(num, currency=currencyRUR):
    wholeDescr, centDescr = currency
    whole, cents = divmod(int(round(abs(num)*100)), 100)
    res = []
    if num<0:
        res.append(minus)
    res.append(writeNumber(wholeDescr, whole))
    res.append(selectDeclension(wholeDescr, whole))

    if centDescr:
        res.append(u'%02d %s' % (cents, selectDeclension(centDescr, cents)))

    result = u' '.join(res)
    return result.capitalize()


if __name__ == '__main__':
    print amountToWords(0)
    print amountToWords(0.20)
    print amountToWords(1.40)
    print amountToWords(4.99)
    print amountToWords(4.999)
    print amountToWords(12.12)
    print amountToWords(21.21)
    print amountToWords(111)
    print amountToWords(1000)
    print amountToWords(10000)
    print amountToWords(100000)
    print amountToWords(1000000)
    print amountToWords(10000000)
    print amountToWords(100000000)
    print amountToWords(1000000000)
    print amountToWords(1234567890)
    print amountToWords(-123.456)
    for n in 0, 1, 2, 3, 111:
        print amountToWords(n, ((u'ясень', u'ясеня',   u'ясеней',   'm'), None))
        print amountToWords(n, ((u'сосна', u'сосны',   u'сосен',    'f'), None))
        print amountToWords(n, ((u'дерево', u'дерева', u'деревьев', 'n'), None))