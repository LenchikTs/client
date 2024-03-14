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
## Transliterations. Thanks to wikipedia!
##
#############################################################################

# Таблица по ГОСТ Р 52535.1-2006 
# применяется, в частности, для загран. паспортов
# если окажется неподходящей, прошу добавлять другие (подходящие) таблицы,
# и добавлять параметр в функцию transliterate

tabGOST_R_52535_1_2006 = { 
    0x0410: u'A',     #  CYRILLIC CAPITAL LETTER A
    0x0411: u'B',     #  CYRILLIC CAPITAL LETTER BE
    0x0412: u'V',     #  CYRILLIC CAPITAL LETTER VE
    0x0413: u'G',     #  CYRILLIC CAPITAL LETTER GHE
    0x0414: u'D',     #  CYRILLIC CAPITAL LETTER DE
    0x0415: u'E',     #  CYRILLIC CAPITAL LETTER IE
    0x0401: u'E',     #  CYRILLIC CAPITAL LETTER IO
    0x0416: u'ZH',    #  CYRILLIC CAPITAL LETTER ZHE
    0x0417: u'Z',     #  CYRILLIC CAPITAL LETTER ZE
    0x0418: u'I',     #  CYRILLIC CAPITAL LETTER I
    0x0419: u'I',     #  CYRILLIC CAPITAL LETTER SHORT I
    0x041a: u'K',     #  CYRILLIC CAPITAL LETTER KA
    0x041b: u'L',     #  CYRILLIC CAPITAL LETTER EL
    0x041c: u'M',     #  CYRILLIC CAPITAL LETTER EM
    0x041d: u'N',     #  CYRILLIC CAPITAL LETTER EN
    0x041e: u'O',     #  CYRILLIC CAPITAL LETTER O
    0x041f: u'P',     #  CYRILLIC CAPITAL LETTER PE
    0x0420: u'R',     #  CYRILLIC CAPITAL LETTER ER
    0x0421: u'S',     #  CYRILLIC CAPITAL LETTER ES
    0x0422: u'T',     #  CYRILLIC CAPITAL LETTER TE
    0x0423: u'U',     #  CYRILLIC CAPITAL LETTER U
    0x0424: u'F',     #  CYRILLIC CAPITAL LETTER EF
    0x0425: u'KH',    #  CYRILLIC CAPITAL LETTER HA
    0x0426: u'TC',    #  CYRILLIC CAPITAL LETTER TSE
    0x0427: u'CH',    #  CYRILLIC CAPITAL LETTER CHE
    0x0428: u'SH',    #  CYRILLIC CAPITAL LETTER SHA
    0x0429: u'SHCH',  #  CYRILLIC CAPITAL LETTER SHCHA
    0x042a: None,     #  CYRILLIC CAPITAL LETTER HARD SIGN
    0x042b: u'Y',     #  CYRILLIC CAPITAL LETTER YERU
    0x042c: None,     #  CYRILLIC CAPITAL LETTER SOFT SIGN
    0x042d: u'E',     #  CYRILLIC CAPITAL LETTER E
    0x042e: u'IU',    #  CYRILLIC CAPITAL LETTER YU
    0x042f: u'IA',    #  CYRILLIC CAPITAL LETTER YA

    0x0430: u'a',     #  CYRILLIC SMALL LETTER A
    0x0431: u'b',     #  CYRILLIC SMALL LETTER BE
    0x0432: u'v',     #  CYRILLIC SMALL LETTER VE
    0x0433: u'g',     #  CYRILLIC SMALL LETTER GHE
    0x0434: u'd',     #  CYRILLIC SMALL LETTER DE
    0x0435: u'e',     #  CYRILLIC SMALL LETTER IE
    0x0451: u'e',     #  CYRILLIC SMALL LETTER IO
    0x0436: u'zh',    #  CYRILLIC SMALL LETTER ZHE
    0x0437: u'z',     #  CYRILLIC SMALL LETTER ZE
    0x0438: u'i',     #  CYRILLIC SMALL LETTER I
    0x0439: u'i',     #  CYRILLIC SMALL LETTER SHORT I
    0x043a: u'k',     #  CYRILLIC SMALL LETTER KA
    0x043b: u'l',     #  CYRILLIC SMALL LETTER EL
    0x043c: u'm',     #  CYRILLIC SMALL LETTER EM
    0x043d: u'n',     #  CYRILLIC SMALL LETTER EN
    0x043e: u'o',     #  CYRILLIC SMALL LETTER O
    0x043f: u'p',     #  CYRILLIC SMALL LETTER PE
    0x0440: u'r',     #  CYRILLIC SMALL LETTER ER
    0x0441: u's',     #  CYRILLIC SMALL LETTER ES
    0x0442: u't',     #  CYRILLIC SMALL LETTER TE
    0x0443: u'u',     #  CYRILLIC SMALL LETTER U
    0x0444: u'f',     #  CYRILLIC SMALL LETTER EF
    0x0445: u'kh',    #  CYRILLIC SMALL LETTER HA
    0x0446: u'tc',    #  CYRILLIC SMALL LETTER TSE
    0x0447: u'ch',    #  CYRILLIC SMALL LETTER CHE
    0x0448: u'sh',    #  CYRILLIC SMALL LETTER SHA
    0x0449: u'shch',  #  CYRILLIC SMALL LETTER SHCHA
    0x044a: None,     #  CYRILLIC SMALL LETTER HARD SIGN
    0x044b: u'y',     #  CYRILLIC SMALL LETTER YERU
    0x044c: None,     #  CYRILLIC SMALL LETTER SOFT SIGN
    0x044d: u'e',     #  CYRILLIC SMALL LETTER E
    0x044e: u'iu',    #  CYRILLIC SMALL LETTER YU
    0x044f: u'ia',    #  CYRILLIC SMALL LETTER YA
}


def transliterate(s):
    return s.upper().translate(tabGOST_R_52535_1_2006)


if __name__ == '__main__':
    def test(s):
        print 'source\t\t\t\t:', s
        print 'default (ГОСТ Р 52535.1-2006)\t:', transliterate(s)

    test(u'Привет, мир!')
    test(u'Широкая электрификация южных губерний даст мощный толчок подъёму сельского хозяйства.')
    test(u'В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!')
    test(u'Съешь ещё этих мягких французских булок, да выпей же чаю.')
