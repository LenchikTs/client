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
from PyQt4.QtCore import Qt, QAbstractTableModel, QDate, QModelIndex, QString, QTime, QVariant

from library.Utils import forceRef, forceString, toVariant


class CPropertyOtherModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self.headers = []
        self.items = {}
        self.dates = []


    def columnCount(self, index = None):
        return len(self.headers)


    def rowCount(self, index = None):
        return len(self.dates)


    def flags(self, index = QModelIndex()):
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                header = self.headers[section]
                if header:
                    return QVariant(header[1])
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            if row < len(self.dates):
                date = self.dates[row]
                if column == 0:
                    if date:
                        return QVariant(date[1])
                else:
                    if self.headers[column] and self.headers[column][0] and (date in self.items.keys()):
                        item = self.items.get(date, {})
                        other = item.get(self.headers[column][0], None)
                        if other:
                            return toVariant(other)
        return QVariant()


    def loadHeader(self, diseaseDayList, multipleDimension):
        self.headers = [[None, u'']]
        resultList = self.getHeader(diseaseDayList, multipleDimension)
        tempSortKey = resultList.keys()
        tempSortKey.sort()
        for key in tempSortKey:
            periodDay = resultList.get(key, u'')
            diseaseDay, endTime, endDate = key
            header = [key,
                      QDate(endDate).toString('dd.MM.yyyy') + QString(u'\n') + QTime(endTime).toString('hh:mm') + QString(u'\n') + QString(periodDay) + QString(u'\n') + QString(str(diseaseDay + 1))
                      ]
            self.headers.append(header)
        self.reset()


    def items(self):
        return self.items


    def loadData(self, eventId, diseaseDayList, actionIdList, begDate, endDate, actionTypeIdList):
        self.items = {}
        self.dates = []
        if eventId:
            self.getPropertyOther('ActionProperty_Integer', diseaseDayList, eventId, actionIdList, begDate, endDate, actionTypeIdList)
            self.getPropertyOther('ActionProperty_String', diseaseDayList, eventId, actionIdList, begDate, endDate, actionTypeIdList)
            self.getPropertyOther('ActionProperty_Double', diseaseDayList, eventId, actionIdList, begDate, endDate, actionTypeIdList)
        self.reset()


    def getPropertyOther(self, tableName, diseaseDayList, eventId, actionIdList, begDate, endDate, actionTypeIdList):
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableAPT = db.table('ActionPropertyType')
        tableAP = db.table('ActionProperty')
        tableProperty = db.table(tableName)
        condOther = [tableAPT['deleted'].eq(0),
                     tableAction['id'].inlist(actionIdList),
                     tableAPT['actionType_id'].inlist(actionTypeIdList),
                     tableAPT['name'].notlike(u'День болезни'),
                     tableAPT['typeName'].notlike(u'Temperature'),
                     tableAPT['name'].notlike(u'АД-макс'),
                     tableAPT['name'].notlike(u'АД-мин'),
                     tableAPT['typeName'].notlike(u'Pulse'),
                     tableAP['deleted'].eq(0),
                     tableAP['action_id'].eq(tableAction['id']),
                     tableAction['deleted'].eq(0),
                     tableAction['event_id'].eq(eventId)
                    ]
        condOther.append(db.joinAnd([tableAction['endDate'].dateGe(begDate), tableAction['endDate'].dateLe(endDate)]))
        tableQuery = tableAction.innerJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
        tableQuery = tableQuery.innerJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
        tableQuery = tableQuery.innerJoin(tableProperty, tableProperty['id'].eq(tableAP['id']))
        records = db.getRecordList(tableQuery, [tableAPT['id'].alias('aptId'), tableAPT['name'].alias('aptName'), tableProperty['value'], tableAP['action_id']], condOther, u'Action.endDate')
        for record in records:
            actionId = forceRef(record.value('action_id'))
            aptId = forceRef(record.value('aptId'))
            aptName = forceString(record.value('aptName'))
            valueAP = forceString(record.value('value'))
            for key, value in diseaseDayList.items():
                if actionId == value:
                    valueList = self.items.get((aptId, aptName), {})
                    valueList[key] = valueAP
                    self.items[(aptId, aptName)] = valueList
                    if (aptId, aptName) not in self.dates:
                        self.dates.append((aptId, aptName))
                    break


    def getHeader(self, diseaseDayList, multipleDimension):
        periodDayTwoList = {1:u'у', 2:u'в'}
        periodDayThreeList = {1:u'у', 2:u'д', 3:u'в'}
        periodDayFourList = {1:u'у', 2:u'д', 3:u'в', 4:u'н'}
        periodDayAllList = {1:{1:u'д'}, 2:periodDayTwoList, 3:periodDayThreeList, 4:periodDayFourList}
        tempSort = diseaseDayList.keys()
        tempSort.sort()
        titleList = {}
        dayMinutes = 24*60
        multipleDimensionMinutes = dayMinutes / multipleDimension
        periodHours = {}
        begHour = 0
        for i in range(1, multipleDimension+1):
            if begHour >= dayMinutes:
                break
            dimensionMinutes = begHour + multipleDimensionMinutes
            if dimensionMinutes >= dayMinutes:
                endHours = dayMinutes - 1
            else:
                endHours = dimensionMinutes
            periodHours[i] = (begHour, endHours)
            begHour += multipleDimensionMinutes
        periodDayList = periodDayAllList.get(multipleDimension, {})
        for key in tempSort:
            diseaseDay, endTimeStr, endDateStr = key
            endTime = QTime(endTimeStr)
            hours = endTime.hour()
            minutes = endTime.minute()
            endHourMinutes = hours * 60 + minutes
            keyHours = periodHours.keys()
            keyHours.sort()
            for keyHour in keyHours:
                periodHour = periodHours.get(keyHour, None)
                if periodHour and endHourMinutes > periodHour[0] and endHourMinutes <= periodHour[1]:
                    periodDay = periodDayList.get(keyHour, u'')
                    titleList[key] = periodDay
                    break
        return titleList


    def saveData(self, masterId):
        pass
