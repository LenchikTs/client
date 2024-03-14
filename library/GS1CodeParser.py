#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#############################################################################
##
## Copyright (C) 2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Разбор данных штрих-кода GS1
## см. GS1 General Specifications
## 7.8 Processing of data from a GS1 symbology using GS1 Application
## Identifiers
##
## Это базовый парсер:
## - Данные штрих-кода разбираются по AI
## - Делается минимальная проверка допустимости данных,
##   - символы должны быть в ASCII (7bit), Не должно быть управляющих символов
##   - допустимость символов в зависимости от AI не проверяется
##     (цифры, character set 39, character set 82)
##   - длины элементов данных контролируются только по Figure 7.8.4-2
##   - в случаях, когда AI кодирует положение десятичной точки, любое значение
##     от 0 до 9 считается годным.
## - Повторы AI не анализируются
## - Данные не преобразуются:
##   - даты не разбираются
##   - десятичная точка не вставляется
##   - если AI предполагает кортеж данных, кортеж не разбирается.
##
#############################################################################


class EGS1Exception(Exception):
    pass


class CGS1CodeParser:
    GS = '\x1d'

    # Таблица длин AI+данных по первым двум символам
    # Figure 7.8.4-2. Element strings with predefined length using GS1 Application Identifiers
    mapPrefixToPredefinedLength = { '00': 20,
                                    '01': 16,
                                    '02': 16,
                                    '03': 16,
                                    '04': 18,
                                    '11': 8,
                                    '12': 8,
                                    '13': 8,
                                    '14': 8,
                                    '15': 8,
                                    '16': 8,
                                    '17': 8,
                                    '18': 8,
                                    '19': 8,
                                    '20': 4,
                                    '31': 10,
                                    '32': 10,
                                    '33': 10,
                                    '34': 10,
                                    '35': 10,
                                    '36': 10,
                                    '41': 16,
                                  }

    # GS1 определяет довольно много AI, и у этих AI длина может быть от 2 до 4 цифр.
    # длины распределены довольно прихотливо, поэтому для определения
    # длины AI сделан конечный автомат, принимающий на входе символы AI
    # и предсказывающий длину AI.
    # Работать это должно так:
    # - устанавливаем в таблице позицию p=0
    # - идём по символам:
    #   - смотрим значение в позиции p + int(char)
    #     - Положительные числа - переход на позицию с этим значением и след.символ
    #     - Отрицательные числа - меняем знак и возвращаем длину
    #     - None - нет такого AI, остановка.
    #       десятичный 0 тоже в принципе годен. но None - выразительней
    # построено автоматически по 3.2 GS1 Application Identifiers in numerical order
    aipat = (#     0     1     2     3     4     5     6     7     8     9
                  10,   20,   30,   70,  110, None, None,  130,  200,   -2,  #   0
                  -2,   -2,   -2, None, None, None, None, None, None, None,  #  10
                  -2,   -2,   -2,   -2, None,   -2,   -2,   -2, None, None,  #  20
                  -2,   -2,   -2,   40,   50,   60, None, None, None, None,  #  30
                None, None, None, None, None,   -3, None, None, None, None,  #  40
                  -3,   -3,   -3,   -3, None, None, None, None, None, None,  #  50
                  -3,   -3, None,   -3,   -3,   -3, None, None, None, None,  #  60
                  -2,   80,   -4,   90,   -4,   90,   -4,   -2, None,  100,  #  70
                  -4,   -4,   -4,   -4,   -4,   -4,   -4, None, None, None,  #  80
                  -4,   -4,   -4,   -4,   -4,   -4,   -4,   -4, None, None,  #  90
                  -4,   -4,   -4,   -4,   -4, None, None, None, None, None,  # 100
                  50,  120,  120, None, None, None, None, None, None, None,  # 110
                  -3,   -3,   -3,   -3,   -3,   -3,   -3,   -3, None, None,  # 120
                 140,  180,  190, None, None, None, None, None, None, None,  # 130
                 150,  160,  170,   -4,  160, None, None, None, None, None,  # 140
                None,   -4,   -4,   -4,   -4,   -4,   -4,   -4,   -4,   -4,  # 150
                  -4, None, None, None, None, None, None, None, None, None,  # 160
                  -4,   -4,   -4,   -4, None, None, None, None, None, None,  # 170
                  -3,   -3,   -3,   -3,   -3, None, None, None, None, None,  # 180
                None, None, None,   -4,  160, None, None, None, None, None,  # 190
                 210,  240,  260, None, None, None, None, None, None, None,  # 200
                 150,  220,  230, None, None, None, None, None, None, None,  # 210
                  -4,   -4,   -4,   -4, None, None, None,   -4,   -4,   -4,  # 220
                  -4, None, None, None, None, None,   -4, None, None, None,  # 230
                None,  250, None, None, None, None, None, None, None, None,  # 240
                  -4,   -4,   -4, None, None, None, None, None, None, None,  # 250
                 160, None, None, None, None, None, None, None, None, None,  # 260
            )


    @classmethod
    def parseCode(cls, chars, start=0):
        result = []

        p = start
        while p<len(chars):
            elementStart = p
            prefix = chars[p:p+2]
            predefinedlength = cls.mapPrefixToPredefinedLength.get(prefix)
            if predefinedlength:
                aiWithData = chars[p:p+predefinedlength]
                p += predefinedlength
                if p<len(chars) and chars[p] == cls.GS:
                    p += 1
            else:
                gsPos = chars.find(cls.GS, p)
                if gsPos >= 0:
                    aiWithData = chars[p:gsPos]
                    p = gsPos+1
                else:
                    aiWithData = chars[p:]
                    p = len(chars)+1
            for i, c in enumerate(aiWithData):
                 if not(' '<=c<='\x7F'):
                    print elementStart, i, elementStart+i, repr(c), ord(c), repr(aiWithData)
                    raise EGS1Exception('wrong character in %r at pos %d' % (chars, elementStart+i))
            aiLen = cls.determineAi(aiWithData)
            if aiLen is None:
               raise EGS1Exception('broken data or unknown AI in %r at pos %d' % (chars, elementStart))
            ai, data = aiWithData[:aiLen], aiWithData[aiLen:]
            result.append((ai, data))
        return result


    @classmethod
    def determineAi(cls, aiWithData):
        aipat = cls.aipat
        p = 0
        for c in aiWithData:
            if not c.isdigit():
                return None
            n = aipat[p+int(c)]
            if n is None:
                return None
            if n < 0:
                return -n
            p = n
        return None

#if __name__ == '__main__':
#    for code, expect in (
#                         ('010599532711203921oFE2UWc5peGoo\x1d91EE05\x1d92OYsISxUTdIlrogkwxsG5265b0r6tETjLhYhofu02TR4=', [('01', '05995327112039'), ('21', 'oFE2UWc5peGoo'), ('91', 'EE05'), ('92', 'OYsISxUTdIlrogkwxsG5265b0r6tETjLhYhofu02TR4=')]),
#                         ('00006141411234567890',                                                                        [('00', '006141411234567890')]),
#                         ('01095011015300031721011910AB-123',                                                            [('01', '09501101530003'), ('17', '210119'), ('10', 'AB-123')]),
#                         ('42045458',                                                                                    [('420', '45458')]),
#                         ('401931234518430GR',                                                                           [('401', '931234518430GR')]),
#                         ('02006141410004181521022810451214\x1d3720',                                                    [('02', '00614141000418'), ('15', '210228'), ('10', '451214'), ('37', '20')]),
#                         ('000931234500000000124210362770401931234518430GR403MEL',                                       [('00', '093123450000000012'), ('421', '0362770401931234518430GR403MEL')]),
#                         ('01950123456789033102000400',                                                                  [('01', '95012345678903'), ('3102', '000400')]),
#                         ('120104258020ABC123',                                                                          [('12', '010425'), ('8020', 'ABC123')]),
#                         ('2530123456789012ABCDEFGHIJKLMNOPQ',                                                           [('253', '0123456789012ABCDEFGHIJKLMNOPQ')]),
#                         ('01095040000591012112345678901\x1d101234567\x1d171411208200http://www.yandex.ru',              [('01', '09504000059101'), ('21', '12345678901'), ('10', '1234567'), ('17', '141120'), ('8200', 'http://www.yandex.ru')]),
#                        ):
#        value = CGS1CodeParser.parseCode(code)
#        print value == expect, repr(code), value
