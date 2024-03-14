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

from PyQt4 import QtGui
from PyQt4.QtCore import  Qt, SIGNAL, QDate, QObject


from library.Utils import forceInt


__all__ = [ 'monthName',
            'monthNameGC',
            'dayNameGC',
            'dowName',
            'wpFiveDays',
            'wpSixDays',
            'wpSevenDays',
            'countWorkDays',
            'addWorkDays',
            'getNextWorkDay',
            'CCalendarInfo',
          ]

monthName =   ('', u'январь', u'февраль', u'март', u'апрель', u'май', u'июнь', u'июль', u'август', u'сентябрь', u'октябрь', u'ноябрь', u'декабрь')
monthNameGC = ('', u'января', u'февраля', u'марта', u'апреля', u'мая', u'июня', u'июля', u'августа', u'сентября', u'октября', u'ноября', u'декабря')
dayNameGC = ('', u'первое', u'второе', u'третье', u'четвертое', u'пятое', u'шестое', u'седьмое', u'восьмое', u'девятое', u'десятое', u'одинадцатое', u'двенадцатое', u'тринадцатое', u'четырнадцатое', u'пятнадцатое', u'шестнадцатое', u'семнадцатое', u'восемнадцатое', u'девятнадцатое', u'двадцатое', u'двадцать первое', u'двадцать второе', u'двадцать третье', u'двадцать четвертое', u'двадцать пятое', u'двадцать шестое', u'двадцать седьмое', u'двадцать восьмое', u'двадцать девятое', u'тридцатое', u'тридцать первое')

dowName     = ('', u'понедельник', u'вторник', u'среда',  u'четверг', u'пятница', u'суббота', u'воскресенье' )

wpFiveDays = frozenset((Qt.Monday, Qt.Tuesday, Qt.Wednesday, Qt.Thursday, Qt.Friday))
wpSixDays  = frozenset((Qt.Monday, Qt.Tuesday, Qt.Wednesday, Qt.Thursday, Qt.Friday, Qt.Saturday))
wpSevenDays= frozenset((Qt.Monday, Qt.Tuesday, Qt.Wednesday, Qt.Thursday, Qt.Friday, Qt.Saturday, Qt.Sunday))


def countWorkDays(startDate, stopDate, weekProfile):
    # определение количества рабочих дней в заданном отрезке дат
    # учитывается и начальная и конечная дата
    getDayOfWeek = QtGui.qApp.calendarInfo.getDayOfWeek
    result = 0
    date = QDate(startDate)
    while date <= stopDate:
        if getDayOfWeek(date) in weekProfile:
            result += 1
        date = date.addDays(1)
    return result


def addWorkDays(startDate, duration, weekProfile):
    # добавление к дате периода в рабочих днях, 1 - это след.день
    # длительность с учётом начальной и конечной даты

    getDayOfWeek = QtGui.qApp.calendarInfo.getDayOfWeek
    date = QDate(startDate)
    while duration>=1:
        date = date.addDays(1)
        if getDayOfWeek(date) in weekProfile:
            duration -= 1
    return date


def getNextWorkDay(date, weekProfile):
    return addWorkDays(date, 1, weekProfile)


class CCalendarInfo(QObject):
    __pyqtSignals__ = ('loaded()',
                      )

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self.rawExceptions = []
        self.mapYMDtoDow = {}
        self.preparedYears = set()


    def clear(self):
        del self.rawExceptions[:]
        self.mapYMDtoDow.clear()
        self.preparedYears.clear()


    def addRawException(self, begYear, endYear, month, day, dow):
        self.rawExceptions.append( (begYear, endYear, month, day, dow) )


    def load(self):
        self.clear()
        try:
            query = QtGui.qApp.db.query('SELECT begYear, endYear, month, day, dow FROM CalendarException WHERE deleted=0')
            while query.next():
                record = query.record()
                begYear = forceInt(record.value('begYear'))
                endYear = forceInt(record.value('endYear'))
                month   = forceInt(record.value('month'))
                day     = forceInt(record.value('day'))
                dow     = forceInt(record.value('dow'))
                self.addRawException(begYear, endYear, month, day, dow)
        except Exception:
            QtGui.qApp.logCurrentException()
            return
        finally:
            self.emit(SIGNAL('loaded()'))


    def getDayOfWeek(self, date):
        result = self.getDayOfWeekInt(*date.getDate())
        if result is None:
            result = date.dayOfWeek()
        return result


    def getDayOfWeekInt(self, year, month, day):
        if year not in self.preparedYears:
            self.__prepareYear(year)
        return self.mapYMDtoDow.get((year, month, day))


    def __prepareYear(self, year):
        for begYear, endYear, month, day, dow in self.rawExceptions:
            if begYear <= year <= endYear:
                self.mapYMDtoDow[(year, month, day)] = dow
        self.preparedYears.add(year)
