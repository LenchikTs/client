# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## временные ряды.
##

from bisect import bisect_right


# базовый класс серии - отображение чего-нибудь на что-нибуть
class CBaseSeries:
    def __init__(self, default=None):
        self.keys = []
        self.values = []
        self.default = default


    def __len__(self):
        return len(self.keys)


    def __getitem__(self, key):
        idx = bisect_right(self.keys, key)-1
        if 0<=idx<len(self.keys):
            return self.values[idx]
        else:
            return self.default


    def __setitem__(self, key, value):
        idx = bisect_right(self.keys, key)-1

        if 0<=idx<len(self.keys) and self.keys[idx] == key:
            self.values[idx] = value
        else:
            self.keys.insert(idx+1, key)
            self.values.insert(idx+1, value)


    def __delitem__(self, key):
        idx = bisect_right(self.keys, key)-1
        if 0<=idx<len(self.keys) and self.keys[idx] == key:
            del self.keys[idx]
            del self.values[idx]


    def __contains__(self, key):
        return self.keys.__contains__(key)


    def __iter__(self):
        return self.keys.__iter__()

# класс серии действительных чисел - отображение чего-нибудь (например, QDate) на действительные числа
class CDoubleSeries(CBaseSeries):
    def __init__(self, default=0.0):
        CBaseSeries.__init__(self, default)


#    def __setitem__(self, key, value):
#        CBaseSeries.__setitem__(self, key, float(value))


# Хранилище серий
# h = CSeriesHolder(CDoubleSeries)
# данные можно добвалять так -
# h.append('var1', QDate(2010,1,1), 1.0)
# h.append('var1', QDate(2012,1,1), 1.5)
# h.append('var1', QDate(2015,1,1), 1.7)
# или так:
# h['var2'][QDate(2015,1,1)] = 0.2
# h['var2'][QDate(2016,1,1)] = 0.25
# доступ к данным - так:
# h['var2'][QDate.currentDate()]

class CSeriesHolder:
    def __init__(self, seriesClass=CBaseSeries):
        self.seriesClass = seriesClass
        self.mapIdToSeries = {}


    def __getitem__(self, key):
        series = self.mapIdToSeries.get(key)
        if series is None:
            series = self.mapIdToSeries[key] = self.seriesClass()
        return series


    def append(self, seriesId, key, value):
        series = self.mapIdToSeries.get(seriesId)
        if series is None:
            series = self.mapIdToSeries[seriesId] = self.seriesClass()
        series[key] = value


if __name__ == '__main__':

    def test(series, pairs, res):
        for key, value in pairs:
            series[key] = value

#        low  = min(pairs)[0]-2
#        high = max(pairs)[0]+2
#        for key in xrange(low, high+1):
#            print key, series[key]
        for key, val in res.iteritems():
            if series[key] != val:
                print 'test failed', key, val, series[key]
                return
        print 'ok'

    res = {-1: None,
            0: None,
            1: 10, 2:10,
            3: 30, 4:30,
            5: 50, 6:50, 7:50
          }
    print 'fill 1-3-5'
    test( CBaseSeries(), ((1, 10), (3, 30), (5, 50), ), res)
    print 'fill 1-5-3'
    test( CBaseSeries(), ((1, 10), (5, 50), (3, 30), ), res)
    print 'fill 3-1-5'
    test( CBaseSeries(), ((3, 30), (1, 10), (5, 50), ), res)
    print 'fill 3-5-1'
    test( CBaseSeries(), ((3, 30), (5, 50), (1, 10), ), res)
    print 'fill 5-1-3'
    test( CBaseSeries(), ((5, 50), (1, 10), (3, 30), ), res)
    print 'fill 5-3-1'
    test( CBaseSeries(), ((5, 50), (3, 30), (1, 10), ), res)
    print 'fill 5-3-1-1-3-5'
    test( CBaseSeries(), ((5, 500), (3, 300), (1, 100), (1, 10), (3, 30), (5, 50),), res)
    print 'fill 5-3-3-1-1-5'
    test( CBaseSeries(), ((5, 500), (3, 300), (3, 30),  (1, 100), (1, 10), (5, 50),), res)
