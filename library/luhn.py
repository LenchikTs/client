# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Проверка кода по алгоритму Луна,
## применяется, например, для проверки идентификатора ЕКП
## https://ru.wikipedia.org/wiki/%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_%D0%9B%D1%83%D0%BD%D0%B0
## https://en.wikipedia.org/wiki/Luhn_algorithm
##
#############################################################################

__all__ = ( 'checkLuhn',
          )


oddLookupTable   = dict((('0', 0), ('1', 2), ('2', 4), ('3', 6), ('4', 8), ('5', 1), ('6', 3), ('7', 5), ('8', 7), ('9', 9)))
evenLookupTable  = dict((('0', 0), ('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9)))


def checkLuhn(identifier):
    if identifier == '':
        return False
    try:
        return (   sum(oddLookupTable[c]  for c in identifier[-2::-2])
                 + sum(evenLookupTable[c] for c in identifier[-1::-2])
               ) % 10 == 0
    except KeyError:
        return False


if __name__ == '__main__':

    tests = [ ( '', False),
              ( '0',  True),
              ( '1',  False),
              ( '2',  False),
              ( '3',  False),
              ( '4',  False),
              ( '5',  False),
              ( '6',  False),
              ( '7',  False),
              ( '8',  False),
              ( '9',  False),
              ( '18', True),
              ( '26', True),
              ( '34', True),
              ( '42', True),
              ( '125', True),
              ( '216', True),
              ( '752', True),
              ( '919', True),

              ( '49927398716', True),

              ( '7825108766852189', True),
              ( '7869607882141218', True),
              ( '7877182059217340', True),

              ( '1877182059217340', False),
              ( '7077182059217340', False),

              ( '7877182859217340', False),

              ( '96433078 36133920674622468 8'.replace(' ', ''), True), # номер транспортного приложения, в середине - mifare UID - 042C27029C5F80 -> 0x805F9C02272C04 -> 36133920674622468
            ]

    for (identifier, expectedResult) in tests:
        print( '%s: %s, %s' % ( identifier, expectedResult, ('failure', 'success')[ checkLuhn(identifier) == expectedResult ]))

