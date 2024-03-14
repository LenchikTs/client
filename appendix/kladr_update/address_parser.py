#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from sys import *

#from library.DialogBase  import CDialogBase
from library.database    import CDatabase
from library.Utils       import *


def parseAddress(db, freeInput, defaultRegion): # db - любая БД, из которой можно вызывать kladr
    u'''status:
0 - адрес восстановлен полностью.
1 - адрес восстановлен неточно
2 - адрес восстановлен частично, и восстановление продолжается
3 - адрес восстановлен частично и неточно, и восстановление продолжается
4 - адрес восстановлен частично, и больше не восстановить
5 - адрес восстановлен частично и неточно, и больше не восстановить
6 - где-то ошибка
    '''
    freeInput = freeInput.replace(',', ' ')
    addressParts = freeInput.split(" ")
    addressParts = [p for p in addressParts if len(p)]
    [status, addressParts, region] = extractRegion(db, addressParts, defaultRegion)
    if status in (2, 3):
        [status, addressParts, street] = extractStreet(db, addressParts, region)
    else:
        return [status, region, '', '', '', '', " ".join(addressParts)]
    if status in (2, 3):
        [status, addressParts, house, corpus, flat] = extractHouseCorpusFlat(db, addressParts)
    else:
        return [status, region, street, '', '', '', " ".join(addressParts)]
    return [status,  region, street, house, corpus, flat, " ".join(addressParts)]
    
    
def extractSocr(addressParts, add, pointAdd, map_):
    if not len(addressParts):
        return [addressParts, '']
    addressParts[0] = addressParts[0].lower()
    if addressParts[0] == u'иногородний':
        addressParts = addressParts[1:]  
        if not len(addressParts):
            return [addressParts, '']
        addressParts[0] = addressParts[0].lower()    
    socr = ''
    for pa in pointAdd:
        if addressParts[0].startswith(pa):
            addressParts[0] = addressParts[0][len(pa):]
            socr = map_[pa]
    if addressParts[0] in add:
        socr = map_[addressParts[0]]
    if not len(addressParts[0]) or addressParts[0] in add:
        addressParts = addressParts[1:]
    return [addressParts, socr]
    
    
def rightTrim(code):
    length = 11
    if code[8:11] == '000':
        length = 8
        if code[5:8] == '000':
            length = 5
            if code[2:5] == '000':
                length = 2
    return code[:length]
    
def queryRegion(db, regionName, regionSocr, parent, checkParent=False):
    result = db.query(u"""
    SELECT CODE 
    FROM kladr.KLADR
    WHERE NAME = '%s'
    AND SOCR IN %s
    """%(regionName, regionSocr))
    if result.size() > 0:
        if result.size() == 1 and not checkParent:
            result.next()
            return str(result.record().value('CODE').toString())
        else: # если регион определился неоднозначно, для уточнения используем родителя, обрезав у него лишние нули
            parent = rightTrim(parent)
            result = db.query(u"""
        SELECT CODE 
        FROM kladr.KLADR
        WHERE NAME = '%s'
        AND CODE LIKE '%s%%'
        AND SOCR IN %s		
        """%(regionName, parent, regionSocr))		            
            if result.next():
                return str(result.record().value('CODE').toString())
    return ''


def extractRegionLevel(db, addressParts, regionAdd, pointRegionAdd, regionMap, regionList, parent='7800000000000', checkParent = True):    
    [addressParts, regionSocr] = extractSocr(addressParts, regionAdd, pointRegionAdd, regionMap) 
    if not len(addressParts):
        return [4, addressParts, '']
    addressParts[0] = addressParts[0][0].upper() + addressParts[0][1:].lower()
    region = queryRegion(db, addressParts[0], regionSocr if len(regionSocr) else regionList, parent, checkParent)
    if len(region):
        addressParts = addressParts[1:]
    elif len(addressParts) >= 2:
        addressParts[1] = addressParts[1][0].upper() + addressParts[1][1:].lower()
        region = queryRegion(db, addressParts[0] + ' ' + addressParts[1], regionSocr if len(regionSocr) else regionList, parent, checkParent)
        if len(region):
            addressParts = addressParts[2:]
        elif len(addressParts) >= 3:
            addressParts[2] = addressParts[2][0].upper() + addressParts[2][1:].lower()
            region = queryRegion(db, addressParts[0] + ' ' + addressParts[1] + ' ' + addressParts[2], regionSocr if len(regionSocr) else regionList, parent, checkParent)
            if len(region):
                addressParts = addressParts[3:]
    [addressParts, regionSocr] = extractSocr(addressParts, regionAdd, pointRegionAdd, regionMap) 
    return [2, addressParts, region]


def extractRegion(db, addressParts, defaultRegion):
    if not len(addressParts):
        return [5, addressParts, '']
    regionAdd1 = [u"г.", u"г", u"гор.", u"гор", u"город", u"обл.", u"обл", u"область", u"респ.", u"респ", u"республика", u"ао", u"авт. обл.", u"автономная область", u"авт. округ", u"автономный округ", u"край"]
    pointRegionAdd1 = [u"г.", u"гор.", u"обл.", u"респ.", u"авт. обл."]
    regionMap1 = {u"г.": u"('г')", u"г": u"('г')", u"гор.": u"('г')", u"гор": u"('г')", u"город": u"('г')", 
        u"обл.": u"('обл')", u"обл": u"('обл')", u"область": u"('обл')", 
        u"респ.": u"('Респ')", u"респ": u"('Респ')", u"республика": u"('Респ')",
        u"ао": u"('Аобл', 'АО')", u"авт. обл.": u"('Аобл')", u"автономная область": u"('Аобл')",
        u"авт. округ": u"('АО')", u"автономный округ": u"('АО')",
        u"край": u"('край')"}   
    regionList1 = u"('г', 'обл', 'Респ', 'Аобл', 'АО', 'край')"
    [addressParts, regionSocr] = extractSocr(addressParts, regionAdd1, pointRegionAdd1, regionMap1) 
    region = ''
    if not len(addressParts):
        return [4, addressParts, region]
    checkParent = True
    addressParts[0] = addressParts[0][0].upper() + addressParts[0][1:].lower()
    if addressParts[0] in (u"Санкт-петербург", u"Спб", u"С-пб", u'С-петербург', u"С-петерб", u"С-петерб."):
        region = '7800000000000'
        addressParts = addressParts[1:]
        status = 2
    elif addressParts[0] in (u"Ленинградская", u"Ленобласть", u"Лен.область", u"Лен.обл.", u"Ло", u"Лен."):
        region = '4700000000000'
        addressParts = addressParts[1:]
        status = 2
    elif addressParts[0] in (u"Москва", u"М.", u"М"):
        region = '7700000000000'
        addressParts = addressParts[1:]
        status = 2
    else:
        [status, addressParts, region] = extractRegionLevel(db, addressParts, regionAdd1, pointRegionAdd1, regionMap1, regionList1, defaultRegion, checkParent=False)
    [addressParts, regionSocr] = extractSocr(addressParts, regionAdd1, pointRegionAdd1, regionMap1)
    if not len(region):
        region = defaultRegion
        checkParent = True#False
        status = 3
    regionAdd2 = [u"г.", u"г", u"гор.", u"гор", u"город", u"обл.", u"обл", u"область", u"респ.", u"респ", u"республика", u"ао", u"авт. обл.", u"автономная область", u"авт. округ", u"автономный округ", u"край", u"район", u"р-н", u"р.-н", u"р-он", u"р/он", u"п", u"п.", u"пос.", u"пос", u"поселок", u"посёлок", u"рп", u"пгт", u"пгт.", u"дп", u"кп", u"д", u"д.", u"дер", u"дер.", u"деревня", u"с.", u"с", u"село"]
    pointRegionAdd2 = [u"г.",  u"гор.", u"обл.", u"респ.", u"авт. обл.", u"п.", u"пос.", u"пгт.", u"д.", u"дер.", u"с."]
    regionMap2 = {u"г.": u"('г')", u"г": u"('г')", u"гор.": u"('г')", u"гор": u"('г')", u"город": u"('г')", 
        u"обл.": u"('обл')", u"обл": u"('обл')", u"область": u"('обл')", 
        u"респ.": u"('Респ')", u"респ": u"('Респ')", u"республика": u"('Респ')",
        u"ао": u"('Аобл', 'АО')", u"авт. обл.": u"('Аобл')", u"автономная область": u"('Аобл')",
        u"авт. округ": u"('АО')", u"автономный округ": u"('АО')",
        u"край": u"('край')",
        u"район": u"('р-н')", u"р-н": u"('р-н')", u"р.-н": u"('р-н')", u"р-он": u"('р-н')", u"р/он": u"('р-н')",
        u"п": u"('п', 'рп', 'пгт', 'дп', 'кп')", u"п.": u"('п', 'рп', 'пгт', 'дп', 'кп')", u"пос.": u"('п', 'рп', 'пгт', 'дп', 'кп')", u"пос": u"('п', 'рп', 'пгт', 'дп', 'кп')", u"поселок": u"('п', 'рп', 'пгт', 'дп', 'кп')", u"посёлок": u"('п', 'рп', 'пгт', 'дп', 'кп')", u"рп": u"('рп')", u"пгт": u"('пгт')", u"пгт.": u"('пгт')", u"дп": u"('дп')", u"кп": u"('кп')",
        u"д": u"('д')", u"д.": u"('д')", u"дер": u"('д')", u"дер.": u"('д')", u"деревня": u"('д')",
        u"с.": u"('с')", u"с": u"('с')", u"село": u"('с')"
        }   
    regionList2 = u"('г', 'обл', 'Респ', 'Аобл', 'АО', 'край', 'р-н', 'п', 'рп', 'пгт', 'дп', 'кп', 'д', 'с')"
    [status, addressParts, region2] = extractRegionLevel(db, addressParts, regionAdd2, pointRegionAdd2, regionMap2, regionList2, region, checkParent)
    if len(region2):
        region = region2
        regionAdd3 = [u"г.", u"г", u"гор.", u"гор", u"город", u"район", u"р-н", u"р.-н", u"р-он", u"р/он", u"волость", u"вол.", u"вол", u"микрорайон", u"мкр", u"мкр.", u"территория", u"терр.", u"терр", u"тер.", u"тер", u"п", u"п.", u"пос.", u"пос", u"поселок", u"посёлок", u"рп", u"пгт", u"пгт.", u"дп", u"кп", u"д", u"д.", u"дер", u"дер.", u"деревня", u"с.", u"с", u"село"]
        pointRegionAdd3 = [u"вол.", u"мкр.", u"терр.", u"тер.", u"г.", u"гор.", u"п.", u"пос.", u"пгт.", u"д.", u"дер.", u"с."]
        regionMap3 = {u"г.": u"('г')", u"г": u"('г')", u"гор.": u"('г')", u"гор": u"('г')", u"город": u"('г')", 
        u"район": u"('р-н')", u"р-н": u"('р-н')", u"р.-н": u"('р-н')", u"р-он": u"('р-н')", u"р/он": u"('р-н')",
        u"волость": u"('волость')", u"вол.": u"('волость')", u"вол": u"('волость')",
        u"микрорайон": u"('мкр')", u"мкр": u"('мкр')", u"мкр.": u"('мкр')",
        u"территория": u"('тер')", u"терр.": u"('тер')", u"терр": u"('тер')", u"тер.": u"('тер')", u"тер": u"('тер')",
        u"п": u"('п', 'рп', 'пгт', 'дп', 'кп')", u"п.": u"('п', 'рп', 'пгт', 'дп', 'кп')", u"пос.": u"('п', 'рп', 'пгт', 'дп', 'кп')", u"пос": u"('п', 'рп', 'пгт', 'дп', 'кп')", u"поселок": u"('п', 'рп', 'пгт', 'дп', 'кп')", u"посёлок": u"('п', 'рп', 'пгт', 'дп', 'кп')", u"рп": u"('рп')", u"пгт": u"('пгт')", u"пгт.": u"('пгт')", u"дп": u"('дп')", u"кп": u"('кп')",
        u"д": u"('д')", u"д.": u"('д')", u"дер": u"('д')", u"дер.": u"('д')", u"деревня": u"('д')",
        u"с.": u"('с')", u"с": u"('с')", u"село": u"('с')"
        }   
        regionList3 = u"('г', 'р-н', 'волость', 'мкр', 'тер', 'п', 'рп', 'пгт', 'дп', 'кп', 'д', 'с')"
        [status, addressParts, region3] = extractRegionLevel(db, addressParts, regionAdd3, pointRegionAdd3, regionMap3, regionList3, region, checkParent = True)
        if len(region3):
            region = region3
            regionAdd4 = [u"микрорайон", u"мкр", u"мкр.", u"территория", u"терр.", u"терр", u"тер.", u"тер", u"п", u"п.", u"пос.", u"пос", u"поселок", u"посёлок", u"рп", u"пгт", u"пгт.", u"дп", u"кп", u"д", u"д.", u"дер", u"дер.", u"деревня", u"с.", u"с", u"село"]
            pointRegionAdd4 = [u"мкр.", u"терр.", u"тер.", u"п.", u"пос.", u"пгт.", u"д.", u"дер.", u"с."]
            regionMap4 = {u"микрорайон": u"('мкр')", u"мкр": u"('мкр')", u"мкр.": u"('мкр')",
        u"территория": u"('тер')", u"терр.": u"('тер')", u"терр": u"('тер')", u"тер.": u"('тер')", u"тер": u"('тер')",
        u"п": u"('п', 'рп', 'пгт', 'дп', 'кп')", u"п.": u"('п', 'рп', 'пгт', 'дп', 'кп')", u"пос.": u"('п', 'рп', 'пгт', 'дп', 'кп')", u"пос": u"('п', 'рп', 'пгт', 'дп', 'кп')", u"поселок": u"('п', 'рп', 'пгт', 'дп', 'кп')", u"посёлок": u"('п', 'рп', 'пгт', 'дп', 'кп')", u"рп": u"('рп')", u"пгт": u"('пгт')", u"пгт.": u"('пгт')", u"дп": u"('дп')", u"кп": u"('кп')",
        u"д": u"('д')", u"д.": u"('д')", u"дер": u"('д')", u"дер.": u"('д')", u"деревня": u"('д')",
        u"с.": u"('с')", u"с": u"('с')", u"село": u"('с')"
        }  
            regionList4 = u"('мкр', 'тер', 'п', 'рп', 'пгт', 'дп', 'кп', 'д', 'с')"
            [status, addressParts, region4] = extractRegionLevel(db, addressParts, regionAdd4, pointRegionAdd4, regionMap4, regionList4, region, checkParent = True)
            if len(region4):
                region = region4
    return [status, addressParts, region]
    
    
def queryStreet(db, streetName, streetSocr, parent):
    parent = parent[:11]
    result = db.query(u"""
    SELECT CODE 
    FROM kladr.STREET
    WHERE NAME = '%s'
    AND SOCR IN %s
    """%(streetName, streetSocr))
    if result.size() > 0:
        if result.size() == 1:
            result.next()
            code = str(result.record().value('CODE').toString())
            if code.startswith(parent):
                return code
        else: # если улица определилась неоднозначно, для уточнения используем родителя
            result = db.query(u"""
        SELECT CODE 
        FROM kladr.STREET
        WHERE NAME = '%s'
        AND CODE LIKE '%s%%'
        AND SOCR IN %s		
        """%(streetName, parent, streetSocr))		            
            if result.next():
                return str(result.record().value('CODE').toString())
    return ''

    
def extractStreet(db, addressParts, region):
    if not len(addressParts):
        return [4, addressParts, '']
    streetAdd = [u"у.", u"ул.", u"ул", u"улица", u"тупик", u"туп.", u"туп", u"станция", u"ст.", u"ст", u"ст-ция", u"проулок", u"проезд", u"площадь", u"пл.", u"пл", u"п.", u"п", u"пр.", u"пр", u"пр-кт", u"проспект", u"переулок", u"пер.", u"пер", u"шоссе", u"ш.", u"ш", u"набережная", u"наб.", u"наб", u"линия", u"л.", u"л", u"квартал", u"кв.", u"кв", u"кв.-л", u"кв-л", u"дорога", u"дор.", u"дор", u"бульвар", u"бул.", u"бул", u"б.-р", u"б-р", u"аллея", u"ал.", u"ал"]
    pointStreetAdd = [u"у.", u"ул.", u"туп.", u"ст.", u"пл.", u"п.", u"пр.", u"пер.", u"ш.", u"наб.", u"л.", u"кв.", u"дор.", u"бул.", u"ал."]
    streetMap = {u"у.": u"('ул')", u"ул.": u"('ул')", u"ул": u"('ул')", u"улица": u"('ул')",
    u"тупик": u"('туп')", u"туп.": u"('туп')", u"туп": u"('туп')",
    u"станция": u"('ст')", u"ст.": u"('ст')", u"ст": u"('ст')", u"ст-ция": u"('ст')",
    u"проулок": u"('проулок')",
    u"проезд": u"('проезд')",
    u"площадь": u"('пл')", u"пл.": u"('пл')", u"пл": u"('пл')",
    u"п.": u"('пр-кт')", u"п": u"('пр-кт', 'пер', 'пл')", u"пр.": u"('пр-кт')", u"пр": u"('пр-кт')", u"пр-кт": u"('пр-кт')", u"проспект": u"('пр-кт')",
    u"переулок": u"('пер')", u"пер.": u"('пер')", u"пер": u"('пер')",
    u"шоссе": u"('ш')", u"ш.": u"('ш')", u"ш": u"('ш')",
    u"набережная": u"('наб')", u"наб.": u"('наб')", u"наб": u"('наб')",
    u"линия": u"('линия')", u"л.": u"('линия')", u"л": u"('линия')",
    u"квартал": u"('кв-л')", u"кв.": u"('кв-л')", u"кв": u"('кв-л')", u"кв.-л": u"('кв-л')", u"кв-л": u"('кв-л')",
    u"дорога": u"('дор')", u"дор.": u"('дор')", u"дор": u"('дор')",
    u"бульвар": u"('б-р')", u"бул.": u"('б-р')", u"бул": u"('б-р')", u"б.-р": u"('б-р')", u"б-р": u"('б-р')",
    u"аллея": u"('аллея')", u"ал.": u"('аллея')", u"ал": u"('аллея')"}
    streetList = u"('ул', 'туп', 'ст', 'проулок', 'проезд', 'пл', 'пр-кт', 'пер', 'ш', 'наб', 'линия', 'кв-л', 'дор', 'б-р', 'аллея')"
    [addressParts, streetSocr] = extractSocr(addressParts, streetAdd, pointStreetAdd, streetMap) 
    if not len(addressParts):
        return [4, addressParts, '']
    addressParts[0] = addressParts[0][0].upper() + addressParts[0][1:].lower()
    street = queryStreet(db, addressParts[0], streetSocr if len(streetSocr) else streetList, region)
    if len(street):
        addressParts = addressParts[1:]
    elif len(addressParts) >= 2:
        addressParts[1] = addressParts[1][0].upper() + addressParts[1][1:].lower()
        street = queryRegion(db, addressParts[0] + ' ' + addressParts[1], streetSocr if len(streetSocr) else streetList, region)
        if len(street):
            addressParts = addressParts[2:]
        elif len(addressParts) >= 3:
            addressParts[2] = addressParts[2][0].upper() + addressParts[2][1:].lower()
            street = queryStreet(db, addressParts[0] + ' ' + addressParts[1] + ' ' + addressParts[2], streetSocr if len(streetSocr) else streetList, region)
            if len(street):
                addressParts = addressParts[3:]
    [addressParts, streetSocr] = extractSocr(addressParts, streetAdd, pointStreetAdd, streetMap) 
    return [2, addressParts, street]
    

def extractHouseCorpusFlat(db, addressParts):
    [status, addressParts, house] = extractHouse(db, addressParts)
    if status in (2, 3):
        [status, addressParts, corpus, flat] = extractCorpusFlat(db, addressParts)     
    else:
        return [status, addressParts, house, '', '']
    return [status, addressParts, house, corpus, flat]


def extractCorpusFlat(db, addressParts):
    [status, addressParts, corpus] = extractCorpus(db, addressParts)     
    if status in (2, 3):
        [status, addressParts, flat] = extractFlat(db, addressParts)     
    else:
        return [status, addressParts, corpus, '']
    return [status, addressParts, corpus, flat]


def extractHouse(db, addressParts):
    if not len(addressParts):
        return [4, addressParts, '']
    houseAdd = [u"д.", u"д", u"дом"]
    pointHouseAdd = [u"д.",]
    houseMap = {u"д.": u"('ДОМ')", u"дом": u"('ДОМ')", u"д": u"('ДОМ')"}
    [addressParts, houseSocr] = extractSocr(addressParts, houseAdd, pointHouseAdd, houseMap) 
    if len(houseSocr) and len(addressParts):
        house = addressParts[0]
        addressParts = addressParts[1:]       
    else:
        house = ''
        while (not len(house)) and len(addressParts):
            try:
                # TODO: делать разбор начала с помощью чего-то вроде scanf
                house = str(int(addressParts[0:]))
            except Exception, ex: 
                addressParts = addressParts[1:]       
    return [2, addressParts, house]


def extractCorpus(db, addressParts):
    if not len(addressParts):
        return [4, addressParts, '']
    corpusAdd = [u"к.", u"к", u"кор", u"кор.", u"корпус"]
    flatAdd = [u"кв.", u"кв", u"к.", u"к", u"квартира"]
    pointCorpusAdd = [u"к.", u"кор."]
    corpusMap = {u"к.": u"('корпус','кв')", u"к": u"('корпус','кв')", u"кор.": u"('корпус')", u"кор": u"('корпус')", u"корпус": u"('корпус')"}
    [addressParts, corpusSocr] = extractSocr(addressParts, corpusAdd, pointCorpusAdd, corpusMap) 
    if len(addressParts):
        if corpusSocr == u"('корпус')":
            corpus = addressParts[0]
            addressParts = addressParts[1:]       
        elif corpusSocr == u"('корпус','кв')": # непонятно, корпус это или квартира
            hasFlat = False # если дальше есть квартира, значит, это корпус, иначе - квартира
            for socr in flatAdd:
                if " ".join(addressParts).find(socr) != -1:
                    hasFlat = True
            if hasFlat: # это был корпус
                corpus = addressParts[0]
                addressParts = addressParts[1:]       
            else: # это была квартира, значит, корпус не указан
                corpus = ''
        else:
            return [4, addressParts, '']
    else:
       return [4, addressParts, '']
    return [2, addressParts, corpus]


    
def extractFlat(db, addressParts):
    if not len(addressParts):
        return [4, addressParts, '']
    flatAdd = [u"кв.", u"кв", u"к.", u"к", u"квартира"]
    pointFlatAdd = [u"кв.", u"к."]
    flatMap = {u"кв.": u"('кв')", u"кв": u"('кв')", u"к.": u"('кв')", u"к": u"('кв')", u"квартира": u"('кв')"}
    [addressParts, flatSocr] = extractSocr(addressParts, flatAdd, pointFlatAdd, flatMap) 
    if len(flatSocr) and len(addressParts):
        flat = addressParts[0]
        addressParts = addressParts[1:]       
    else:
        flat = ''
        while (not len(flat)) and len(addressParts):
            try:
                # TODO: делать разбор начала с помощью чего-то вроде scanf
                flat = str(int(addressParts[0:]))
            except Exception, ex: 
                addressParts = addressParts[1:] 
    if len(flat):
        return [0, addressParts, flat]
    else:
        return [4, addressParts, flat]
    
