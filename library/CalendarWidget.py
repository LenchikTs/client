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
from PyQt4.QtCore import Qt, SIGNAL, QDate, QDateTime, QTimer
#from library.Utils import *


__all__ = [ 'CCalendarWidget',
          ]


class CCalendarWidget(QtGui.QCalendarWidget):
    u'Календарь с подсветкой выходных дней и праздников'

    def __init__(self, parent):
        QtGui.QCalendarWidget.__init__(self, parent)
        self.setFirstDayOfWeek(Qt.Monday)
        self.connect(self, SIGNAL('currentPageChanged(int,int)'), self.onCurrentPageChanged)
        self.connect(QtGui.qApp.calendarInfo, SIGNAL('loaded()'), self.onCalendarInfoLoaded)
        # Очень хочется в календаре специальным образом показывать текущую дату.
        # Например - жирным (варианты:курсивом, подчёркиванием, другим шрифтом)
        # Согласитесь, что при смене даты отметка текущей даты должна измениться.
        # так как специального сигнала "дата изменилась" у меня нет,
        # будем использовать таймер для перехода на новую дату
        # недостаток: плохо работает при ручном изменении даты или времени.
        self.prepareTimer()
        self.updateFormats()


    def prepareTimer(self):
        currentDateTime = QDateTime.currentDateTime()
        sleep = currentDateTime.secsTo(QDateTime(currentDateTime.date().addDays(1)))*1000+100
        QTimer.singleShot(sleep, self.onTimer)


    def onCurrentPageChanged(self, year, month):
        self.updateFormats()


    def onCalendarInfoLoaded(self):
        self.updateFormats()


    def onTimer(self):
        self.updateFormats()
        self.prepareTimer()


    def updateFormats(self):
        getDayOfWeek = QtGui.qApp.calendarInfo.getDayOfWeek
        normalFormat = QtGui.QTextCharFormat()
        normalFormat.setForeground(self.palette().color(QtGui.QPalette.Text))
        holidayFormat = QtGui.QTextCharFormat()
        holidayFormat.setForeground(Qt.red)
        currentDate = QDate.currentDate()
        currentDateFormat = QtGui.QTextCharFormat()
        currentDateFormat.setFontWeight(QtGui.QFont.Bold)
        holidays = set((Qt.Saturday, Qt.Sunday))

        month = self.monthShown()
        year = self.yearShown()
        firstDate = QDate(year, month, 1)
        days = firstDate.daysInMonth()
        for i in xrange(days):
            date = firstDate.addDays(i)
            format = holidayFormat if getDayOfWeek(date) in holidays else normalFormat
            if date == currentDate:
                format = QtGui.QTextFormat(format).toCharFormat()
                format.merge(currentDateFormat)
            self.setDateTextFormat(date, format)

