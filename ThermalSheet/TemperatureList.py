# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignature, QByteArray, QDate, QDateTime, QTime

import matplotlib.pyplot as plt
from PyQt4.QtGui import QSizePolicy
from matplotlib import ticker
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanavas

from Registry.Utils import clientIdToText
from library.DialogBase import CDialogBase
from library.Utils import forceBool, forceDate, forceDouble, forceInt, forceRef, forceString, forceTime, pyDate, \
    toVariant

# from Registry.Utils     import getClientString
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportView import CReportViewDialog

from PropertyOtherModel import CPropertyOtherModel
from Ui_TemperatureListDialog import Ui_TemperatureListDialog
from Ui_TemperatureListParameters import Ui_TemperatureListParameters


class TempListCanavas(FigureCanavas):
    def __init__(self, fig, parent=None):
        self.fig = fig
        FigureCanavas.__init__(self, self.fig)
        FigureCanavas.setSizePolicy(self, QSizePolicy.Fixed, QSizePolicy.Fixed)
        FigureCanavas.updateGeometry(self)


class CCreateGraph(object):
    def __init__(self, parent):
        self.parent = parent

    def getCanavas(self, xa, ya, titleList, yticks, color='r', title=u'Температура'):
        if len(xa) != 0:
            xalist = []
            for x in xa:
                time = forceString(titleList[x][1])
                date = forceString(titleList[x][2])
                datetime = date + '\n ' + time
                xalist.append(datetime)
            x = xa
            y = ya
            fig, ax = plt.subplots()
            ax.plot(x, y, color=color, linewidth=3)
            ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
            ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
            plt.title(title)
            ax.set_xticks(xa)
            ax.set_xticklabels(xalist)
            ax.set_yticks(yticks)
            ax.grid(which='major', color='k')
            ax.minorticks_on()
            ax.grid(which='minor',
                    color='gray',
                    linestyle=':')
            fig.set_figwidth(8)
            fig.set_figheight(4)
            canavas = TempListCanavas(fig)
            return canavas


class CTemperatureList(CDialogBase, Ui_TemperatureListDialog):
    def __init__(self, parent, params, clientId, eventId):
        CDialogBase.__init__(self, parent)
        self.addModels('TemperatureSheet', CTemperatureListModel(self))
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setModels(self.tblTemperatureSheet,  self.modelTemperatureSheet, self.selectionModelTemperatureSheet)
        self.parent = parent #wtf? скрывать Qt-шный parent - это плохая затея
        self.params = params
        self.eventId = eventId
        self.clientId = clientId
        self.minValue = 0.0
        self.maxValue = 0.0
        self.dimension = 0
        self.multipleDimension = 0
        self.countGraphic = 0
        self.qwtPlotList = []
        self.y = 0
        self.x = 0
        self.canavas1 = None
        self.canavas2 = None
        self.canavas3 = None
        self.canavas4 = None


    @pyqtSignature('')
    def on_btnClose_clicked(self):
        self.close()


    @pyqtSignature('')
    def on_btnRetry_clicked(self):
        self.close()
        dialog = CTemperatureListParameters(self.parent, self.eventId)
        dialog.setParams()
        if dialog.exec_():
            demo = CTemperatureList(self.parent, dialog.params(), self.clientId, self.eventId)
            demo.getInfo()
            demo.exec_()


    @pyqtSignature('')
    def on_btnPrint_clicked(self):
        widgetIndex = self.tabWidget.currentIndex()
        if widgetIndex == 1:
            model = self.modelTemperatureSheet
            doc = QtGui.QTextDocument()
            cursor = QtGui.QTextCursor(doc)
            cursor.setCharFormat(CReportBase.ReportTitle)
            cursor.insertText(u'Таблица температурного листа\n')
            cursor.insertBlock()
            cursor.setCharFormat(CReportBase.ReportBody)
            cursor.insertText(u'Пациент: %s' % (clientIdToText(self.clientId) if self.clientId else u'не известен'))
            cursor.insertText(u'\nОтчёт составлен: ' + forceString(QDateTime.currentDateTime()))
            cursor.insertBlock()
            colWidths  = [ self.tblTemperatureSheet.columnWidth(i) for i in xrange(model.columnCount()-1) ]
            colWidths.insert(0,10)
            totalWidth = sum(colWidths)
            tableColumns = []
            iColNumber = False
            for iCol, colWidth in enumerate(colWidths):
                widthInPercents = str(max(1, colWidth*90/totalWidth))+'%'
                if iColNumber == False:
                    tableColumns.append((widthInPercents, [u'№'], CReportBase.AlignRight))
                    iColNumber = True
                headers = model.headers
                tableColumns.append((widthInPercents, [forceString(headers[iCol][1])], CReportBase.AlignLeft))
            table = createTable(cursor, tableColumns)
            for iModelRow in xrange(model.rowCount()):
                iTableRow = table.addRow()
                table.setText(iTableRow, 0, iModelRow+1)
                for iModelCol in xrange(model.columnCount()):
                    index = model.createIndex(iModelRow, iModelCol)
                    text = forceString(model.data(index))
                    table.setText(iTableRow, iModelCol+1, text)
            html = doc.toHtml(QByteArray('utf-8'))
            view = CReportViewDialog(self)
            view.setText(html)
            view.exec_()
        else:
            printer = QtGui.QPrinter()
            printer.setOrientation(QtGui.QPrinter.Portrait)
            dialog = QtGui.QPrintDialog(printer, self)
            if dialog.exec_():
                painter = QtGui.QPainter()
                painter.begin(printer)
                printer.setPageMargins(0, 10, 10, 10, QtGui.QPrinter.Millimeter)
                listCanavas = []
                if self.canavas1:
                    listCanavas.append(self.canavas1)
                if self.canavas2:
                    listCanavas.append(self.canavas2)
                if self.canavas3:
                    listCanavas.append(self.canavas3)
                if self.canavas4:
                    listCanavas.append(self.canavas4)
                count = len(listCanavas)
                if count <= 2:
                    self.scrollArea.widget().render(painter)
                else:
                    for canavas in listCanavas:
                        canavas.render(painter)
                        count -= 1
                        if count != 0:
                            printer.newPage()
                painter.end()


    def getInfo(self):
        if self.eventId and self.params:
            valueAPIList = {}
            valueAPSList = {}
            valueAPDList = {}
            APMaxList = {}
            APMinList = {}
            temperatureList = {}
            pulseList = {}
            chkTemperature = self.params.get('chkTemperature', 0)
            chkPulse = self.params.get('chkPulse', 0)
            chkAPMax = self.params.get('chkAPMax', 0)
            chkAPMin = self.params.get('chkAPMin', 0)
            self.multipleDimension = self.params.get('multipleDimension', 0)
            begDate = self.params.get('begDate', None)
            endDate = self.params.get('endDate', None)
            if begDate and endDate and (begDate <= endDate):
                self.multipleDays = 2 if begDate == endDate else (begDate.daysTo(endDate) + 2)
                if (begDate and endDate and chkTemperature or chkPulse or chkAPMax or chkAPMin) and self.multipleDimension and self.multipleDays:
                    db = QtGui.qApp.db
                    tableEvent = db.table('Event')
                    tableAction = db.table('Action')
                    tableAPT = db.table('ActionPropertyType')
                    tableAT = db.table('ActionType')
                    tableAP = db.table('ActionProperty')
                    # tableAPA = db.table('ActionProperty_Action')
                    # tableAPAP = db.table('ActionProperty_ArterialPressure')
                    tableAPPulse = db.table('ActionProperty_Pulse')
                    tableAPTemperature = db.table('ActionProperty_Temperature')
                    tableAPAP = db.table('ActionProperty_ArterialPressure')
                    tableAPInteger = db.table('ActionProperty_Integer')
                    actionTypeIdList = db.getDistinctIdList(tableAT, [tableAT['id']], [tableAT['deleted'].eq(0),
                                                                tableAT['flatCode'].like(u'temperatureSheet%')])
                    condDiseaseDay = [ tableAPT['deleted'].eq(0),
                                        tableAPT['actionType_id'].inlist(actionTypeIdList),
                                        tableAPT['name'].like(u'День болезни'),
                                        tableAP['deleted'].eq(0),
                                        tableAction['deleted'].eq(0),
                                        tableAction['event_id'].eq(self.eventId)
                                      ]
                    condDiseaseDay.append(db.joinAnd([tableAction['endDate'].dateGe(begDate),
                                                      tableAction['endDate'].dateLe(endDate)]))
                    tableQuery = tableAction.innerJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
                    tableQuery = tableQuery.innerJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
                    tableQuery = tableQuery.innerJoin(tableAPInteger, tableAPInteger['id'].eq(tableAP['id']))
                    recordsDiseaseDay = db.getRecordList(tableQuery, [tableAPInteger['value'], tableAP['action_id'],
                                                        tableAction['endDate']], condDiseaseDay, u'Action.endDate')
                    diseaseDayList = {}
                    actionIdList = []
                    for recordDiseaseDay in recordsDiseaseDay:
                        actionId = forceRef(recordDiseaseDay.value('action_id'))
                        actionIdList.append(actionId)
                        diseaseDay = forceInt(recordDiseaseDay.value('value')) - 1
                        endDate = forceDate(recordDiseaseDay.value('endDate'))
                        endDateStr = pyDate(endDate)
                        endTime = forceTime(recordDiseaseDay.value('endDate'))
                        endTimeStr = pyTime(endTime)
                        if (diseaseDay, endTimeStr, endDateStr) not in diseaseDayList.keys():
                            diseaseDayList[(diseaseDay, endTimeStr, endDateStr)] = actionId
                    self.modelTemperatureSheet.setChecked(chkTemperature=chkTemperature, chkAPMax=chkAPMax,
                                                          chkAPMin=chkAPMin, chkPulse=chkPulse)
                    self.modelTemperatureSheet.loadHeader(diseaseDayList, self.multipleDimension)
                    self.modelTemperatureSheet.loadData(self.eventId, diseaseDayList, actionIdList,
                                                        begDate, endDate, actionTypeIdList)
                    if chkTemperature:
                        condTemperature = [ tableAPT['deleted'].eq(0),
                                            tableAction['id'].inlist(actionIdList),
                                            tableAPT['actionType_id'].inlist(actionTypeIdList),
                                            tableAPT['typeName'].like(u'Temperature'),
                                            tableAP['deleted'].eq(0),
                                            tableAction['deleted'].eq(0),
                                            tableAction['event_id'].eq(self.eventId)
                                          ]
                        condTemperature.append(db.joinAnd([tableAction['endDate'].dateGe(begDate), tableAction['endDate'].dateLe(endDate)]))
                        tableQuery = tableAction.innerJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
                        tableQuery = tableQuery.innerJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
                        tableQuery = tableQuery.innerJoin(tableAPTemperature, tableAPTemperature['id'].eq(tableAP['id']))
                        recordsTemperature = db.getRecordList(tableQuery, [tableAPTemperature['value'], tableAP['action_id']], condTemperature, u'Action.endDate')
                        for recordTemperature in recordsTemperature:
                            actionId = forceRef(recordTemperature.value('action_id'))
                            temperature = forceDouble(recordTemperature.value('value'))
                            for key, value in diseaseDayList.items():
                                if actionId == value:
                                    temperatureList[key] = temperature
                                    break
                    if chkAPMax:
                        condArterialPressureMax = [ tableAPT['deleted'].eq(0),
                                                    tableAction['id'].inlist(actionIdList),
                                                    tableAPT['actionType_id'].inlist(actionTypeIdList),
                                                    tableAPT['typeName'].like(u'ArterialPressure'),
                                                    tableAPT['name'].like(u'АД-макс'),
                                                    tableAP['deleted'].eq(0),
                                                    tableAction['deleted'].eq(0),
                                                    tableAction['event_id'].eq(self.eventId)
                                                  ]
                        condArterialPressureMax.append(db.joinAnd([tableAction['endDate'].dateGe(begDate), tableAction['endDate'].dateLe(endDate)]))
                        tableQuery = tableAction.innerJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
                        tableQuery = tableQuery.innerJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
                        tableQuery = tableQuery.innerJoin(tableAPAP, tableAPAP['id'].eq(tableAP['id']))
                        recordsAPMax = db.getRecordList(tableQuery, [tableAPAP['value'], tableAP['action_id']], condArterialPressureMax, u'Action.endDate')
                        for recordAPMax in recordsAPMax:
                            actionId = forceRef(recordAPMax.value('action_id'))
                            APMax = forceInt(recordAPMax.value('value'))
                            for key, value in diseaseDayList.items():
                                if actionId == value:
                                    APMaxList[key] = APMax
                                    break
                    if chkAPMin:
                        condArterialPressureMin = [ tableAPT['deleted'].eq(0),
                                                    tableAction['id'].inlist(actionIdList),
                                                    tableAPT['actionType_id'].inlist(actionTypeIdList),
                                                    tableAPT['typeName'].like(u'ArterialPressure'),
                                                    tableAPT['name'].like(u'АД-мин'),
                                                    tableAP['deleted'].eq(0),
                                                    tableAction['deleted'].eq(0),
                                                    tableAction['event_id'].eq(self.eventId)
                                                  ]
                        condArterialPressureMin.append(db.joinAnd([tableAction['endDate'].dateGe(begDate), tableAction['endDate'].dateLe(endDate)]))
                        tableQuery = tableAction.innerJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
                        tableQuery = tableQuery.innerJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
                        tableQuery = tableQuery.innerJoin(tableAPAP, tableAPAP['id'].eq(tableAP['id']))
                        recordsAPMin = db.getRecordList(tableQuery, [tableAPAP['value'], tableAP['action_id']], condArterialPressureMin, u'Action.endDate')
                        for recordAPMin in recordsAPMin:
                            actionId = forceRef(recordAPMin.value('action_id'))
                            APMin = forceInt(recordAPMin.value('value'))
                            for key, value in diseaseDayList.items():
                                if actionId == value:
                                    APMinList[key] = APMin
                                    break
                    if chkPulse:
                        condPulse = [ tableAPT['deleted'].eq(0),
                                      tableAction['id'].inlist(actionIdList),
                                      tableAPT['actionType_id'].inlist(actionTypeIdList),
                                      tableAPT['typeName'].like(u'Pulse'),
                                      tableAP['deleted'].eq(0),
                                      tableAction['deleted'].eq(0),
                                      tableAction['event_id'].eq(self.eventId)
                                    ]
                        condPulse.append(db.joinAnd([tableAction['endDate'].dateGe(begDate), tableAction['endDate'].dateLe(endDate)]))
                        tableQuery = tableAction.innerJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
                        tableQuery = tableQuery.innerJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
                        tableQuery = tableQuery.innerJoin(tableAPPulse, tableAPPulse['id'].eq(tableAP['id']))
                        recordsPulse = db.getRecordList(tableQuery, [tableAPPulse['value'], tableAP['action_id']], condPulse, u'Action.endDate')
                        for recordPulse in recordsPulse:
                            actionId = forceRef(recordPulse.value('action_id'))
                            pulse = forceInt(recordPulse.value('value'))
                            for key, value in diseaseDayList.items():
                                if actionId == value:
                                    pulseList[key] = pulse
                                    break
                cnt = 0
                self.dimension = round(1 / float(self.multipleDimension), 2)
                self.countGraphic = 0
                if chkTemperature:
                    self.countGraphic += 1
                if chkAPMax:
                    self.countGraphic += 1
                if chkAPMin:
                    self.countGraphic += 1
                if chkPulse:
                    self.countGraphic += 1

                self.qwtPlotList = []
                self.scrollArea.setStyleSheet("QWidget {background-color: #FFFFFF}")
                plotLayout = QtGui.QVBoxLayout(QtGui.QFrame(self.scrollArea.widget()))
                if chkTemperature:
                    xa, ya, minValue1, maxValue1, titleList = self.getXY(temperatureList)
                    minVal = minValue1 if minValue1 < 35 else 35.0
                    maxVal = maxValue1 if maxValue1 > 40 else 40.0
                    yticks = self.float_range(minVal, maxVal, 0.5)
                    graph = CCreateGraph(self)
                    gCanavas1 = graph.getCanavas(xa, ya, titleList, yticks, color='r', title=u'Температура')
                    self.canavas1 = gCanavas1
                    plotLayout.addWidget(gCanavas1)
                    cnt += 1
                if chkAPMax:
                    xa2, ya2, minValue2, maxValue2, titleList = self.getXY(APMaxList)
                    minVal2 = minValue2 if minValue2 < 50 else 50
                    maxVal2 = maxValue2 if maxValue2 > 175 else 175
                    minVal2 = minVal2 - (minVal2 % 10)
                    yticks2 = self.float_range(minVal2, maxVal2, 25)
                    graph = CCreateGraph(self)
                    gCanavas2 = graph.getCanavas(xa2, ya2, titleList, yticks2, color='b', title=u'Давление максимальное')
                    self.canavas2 = gCanavas2
                    plotLayout.addWidget(gCanavas2)
                if chkAPMin:
                    xa3, ya3, minValue3, maxValue3, titleList = self.getXY(APMinList)
                    minVal3 = minValue3 if minValue3 < 50 else 50
                    maxVal3 = maxValue3 if maxValue3 > 175 else 175
                    minVal3 = minVal3 - (minVal3 % 10)
                    yticks3 = self.float_range(minVal3, maxVal3, 25)
                    graph = CCreateGraph(self)
                    gCanavas3 = graph.getCanavas(xa3, ya3, titleList, yticks3, color='b', title=u'Давление минимальное')
                    self.canavas3 = gCanavas3
                    plotLayout.addWidget(gCanavas3)
                if chkPulse:
                    xa4, ya4, minValue4, maxValue4, titleList = self.getXY(pulseList)
                    minVal4 = minValue4 if minValue4 < 60 else 60
                    maxVal4 = maxValue4 if maxValue4 > 120 else 120
                    minVal4 = minVal4 - (minVal4 % 10)
                    yticks4 = self.float_range(minVal4, maxVal4, 10)
                    graph = CCreateGraph(self)
                    gCanavas4 = graph.getCanavas(xa4, ya4, titleList, yticks4, color='g', title=u'Пульс')
                    self.canavas4 = gCanavas4
                    plotLayout.addWidget(gCanavas4)
                widgetLayout = QtGui.QWidget()
                widgetLayout.setLayout(plotLayout)
                self.scrollArea.setWidget(widgetLayout)

    def float_range(self, start, stop, step):
        rangeList = []
        currentValue = start
        while currentValue < stop:
            currentValue += step
            rangeList.append(currentValue)
        return rangeList

    def getXY(self, infoList):
        periodDayTwoList = {1:u'у', 2:u'в'}
        periodDayThreeList = {1:u'у', 2:u'д', 3:u'в'}
        periodDayFourList = {1:u'у', 2:u'д', 3:u'в', 4:u'н'}
        periodDayAllList = {1:{1:u'д'}, 2:periodDayTwoList, 3:periodDayThreeList, 4:periodDayFourList}
        tempSort = infoList.keys()
        tempSort.sort()
        xList = []
        yList = []
        titleList = {}
        minValue = 0.0
        maxValue = 0.0
        firstIn = True
        dayMinutes = 24*60
        multipleDimensionMinutes = dayMinutes / self.multipleDimension
        periodHours = {}
        begHour = 0
        for i in range(1, self.multipleDimension+1):
            if begHour >= dayMinutes:
                break
            dimensionMinutes = begHour + multipleDimensionMinutes
            if dimensionMinutes >= dayMinutes:
                endHours = dayMinutes - 1
            else:
                endHours = dimensionMinutes
            periodHours[i] = (begHour, endHours)
            begHour += multipleDimensionMinutes
        periodDayList = periodDayAllList.get(self.multipleDimension, {})
        for key in tempSort:
            value = infoList.get(key, 0)
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
                    if firstIn:
                        minValue = value
                        maxValue = value
                        firstIn = False
                    if minValue > value:
                        minValue = value
                    if maxValue < value:
                        maxValue = value
                    yList.append(round(value, 2))
                    x = round(len(yList), 2)
                    xList.append(x)
                    periodDay = periodDayList.get(keyHour, u'')
                    titleList[x] = (diseaseDay+1, endTime, QDate(endDateStr), periodDay)
                    break
        return xList, yList, minValue, maxValue, titleList

class CTemperatureListModel(CPropertyOtherModel):
    def __init__(self, parent):
        CPropertyOtherModel.__init__(self, parent)
        self.headers = []
        self.items = {}
        self.dates = []
        self.chkTemperature = False
        self.chkPulse = False
        self.chkAPMax = False
        self.chkAPMin = False

    def setChecked(self, chkTemperature, chkPulse, chkAPMax, chkAPMin):
        self.chkTemperature = chkTemperature
        self.chkPulse = chkPulse
        self.chkAPMax = chkAPMax
        self.chkAPMin = chkAPMin

    def loadData(self, eventId, diseaseDayList, actionIdList, begDate, endDate, actionTypeIdList):
        self.items = {}
        self.dates = []
        if eventId:
            if self.chkTemperature:
                self.getPropertyOther('ActionProperty_Temperature', diseaseDayList, eventId, actionIdList, begDate, endDate, actionTypeIdList)
            if self.chkAPMax:
                self.getPropertyOther('ActionProperty_ArterialPressure', diseaseDayList, eventId, actionIdList, begDate, endDate, actionTypeIdList, True)
            if self.chkAPMin:
                self.getPropertyOther('ActionProperty_ArterialPressure', diseaseDayList, eventId, actionIdList, begDate, endDate, actionTypeIdList)
            if self.chkPulse:
                self.getPropertyOther('ActionProperty_Pulse', diseaseDayList, eventId, actionIdList, begDate, endDate, actionTypeIdList)
            self.getPropertyOther('ActionProperty_Integer', diseaseDayList, eventId, actionIdList, begDate, endDate, actionTypeIdList)
            self.getPropertyOther('ActionProperty_String', diseaseDayList, eventId, actionIdList, begDate, endDate, actionTypeIdList)
            self.getPropertyOther('ActionProperty_Double', diseaseDayList, eventId, actionIdList, begDate, endDate, actionTypeIdList)
        self.reset()

    def getPropertyOther(self, tableName, diseaseDayList, eventId, actionIdList, begDate, endDate, actionTypeIdList, isMax = False):
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableAPT = db.table('ActionPropertyType')
        tableAP = db.table('ActionProperty')
        tableProperty = db.table(tableName)
        condOther = []
        cond = [tableAPT['deleted'].eq(0),
                tableAction['id'].inlist(actionIdList),
                tableAPT['actionType_id'].inlist(actionTypeIdList),
                tableAP['deleted'].eq(0),
                tableAP['action_id'].eq(tableAction['id']),
                tableAction['deleted'].eq(0),
                tableAction['event_id'].eq(eventId)
                ]
        if tableName == 'ActionProperty_Temperature':
            cond.append(tableAPT['typeName'].like(u'Temperature'))
            cond.append(db.joinAnd([tableAction['endDate'].dateGe(begDate), tableAction['endDate'].dateLe(endDate)]))
        elif tableName == 'ActionProperty_ArterialPressure' and isMax:
            cond.append(tableAPT['typeName'].like(u'ArterialPressure'))
            cond.append(tableAPT['name'].like(u'АД-макс'))
            cond.append(db.joinAnd([tableAction['endDate'].dateGe(begDate), tableAction['endDate'].dateLe(endDate)]))
        elif tableName == 'ActionProperty_ArterialPressure':
            cond.append(tableAPT['typeName'].like(u'ArterialPressure'))
            cond.append(tableAPT['name'].like(u'АД-мин'))
            cond.append(db.joinAnd([tableAction['endDate'].dateGe(begDate), tableAction['endDate'].dateLe(endDate)]))
        elif tableName == 'ActionProperty_Pulse':
            cond.append(tableAPT['typeName'].like(u'Pulse'))
            cond.append(db.joinAnd([tableAction['endDate'].dateGe(begDate), tableAction['endDate'].dateLe(endDate)]))
        else:
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
            condOther.append(db.joinAnd([tableAction['endDate'].dateGe(begDate),
                                         tableAction['endDate'].dateLe(endDate)]))
        tableQuery = tableAction.innerJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
        tableQuery = tableQuery.innerJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
        tableQuery = tableQuery.innerJoin(tableProperty, tableProperty['id'].eq(tableAP['id']))
        if condOther:
            records = db.getRecordList(tableQuery, [tableAPT['id'].alias('aptId'), tableAPT['name'].alias('aptName'),
                                                    tableProperty['value'], tableAP['action_id']], condOther,
                                       u'Action.endDate')
        else:
            records = db.getRecordList(tableQuery, [tableAPT['id'].alias('aptId'), tableAPT['name'].alias('aptName'),
                                                    tableProperty['value'], tableAP['action_id']], cond,
                                       u'Action.endDate')
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


class CTemperatureListParameters(CDialogBase, Ui_TemperatureListParameters):
    def __init__(self,  parent, eventId):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        currentDate = QDate.currentDate()
        month = currentDate.month()
        year = currentDate.year()
        self.eventId = eventId
        self.parent = parent #wtf? скрывать Qt-шный parent - это плохая затея
        self.edtMultipleDimension.setValue(2)
        self.getPeriodDate()


    def getPeriodDate(self):
        if self.eventId:
            db = QtGui.qApp.db
            tableAction = db.table('Action')
            tableAPT = db.table('ActionPropertyType')
            tableAP = db.table('ActionProperty')
            tableAT =  db.table('ActionType')
            actionTypeIdList = db.getDistinctIdList(tableAT, [tableAT['id']], [tableAT['deleted'].eq(0),
                                                        tableAT['flatCode'].like(u'temperatureSheet%')])
            cond = [ tableAPT['deleted'].eq(0),
                     tableAPT['actionType_id'].inlist(actionTypeIdList),
                     tableAction['deleted'].eq(0),
                     tableAction['event_id'].eq(self.eventId)
                   ]
            tableQuery = tableAction.innerJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
            tableQuery = tableQuery.innerJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
            recordMIN = db.getRecordEx(tableQuery, 'MIN(Action.begDate) AS begDate', cond)
            recordMAX = db.getRecordEx(tableQuery, 'MAX(Action.begDate) AS begDate', cond)
            begDateMIN = None
            begDateMAX = None
            if recordMIN:
                begDateMIN = forceDate(recordMIN.value('begDate'))
            if recordMAX:
                begDateMAX = forceDate(recordMAX.value('begDate'))
            if not begDateMIN and hasattr(self.parent, 'edtBegDate'):
                begDateMIN = self.parent.edtBegDate.date()
            if not begDateMAX and hasattr(self.parent, 'edtEndDate'):
                begDateMAX = self.parent.edtEndDate.date()
            if not begDateMAX:
                begDateMAX = QDate.currentDate()
            self.edtBegDate.setDate(begDateMIN)
            self.edtEndDate.setDate(begDateMAX)
        else:
            begDate = self.parent.edtBegDate.date()
            endDate = self.parent.edtEndDate.date()
            if not begDate and not endDate:
                begDate = QDate.currentDate()
                endDate = QDate.currentDate()
            elif not begDate and endDate:
                begDate = endDate
            elif begDate and not endDate:
                endDate = begDate
            self.edtBegDate.setDate(begDate)
            self.edtEndDate.setDate(endDate)


    def setParams(self):
        currentDate = QDate.currentDate()
        month = currentDate.month()
        year = currentDate.year()
        begDate = forceDate(QtGui.qApp.preferences.appPrefs.get('begDate', None))
        if not begDate:
            begDate = QDate(year, month, 1)
        self.edtBegDate.setDate(begDate)
        endDate = forceDate(QtGui.qApp.preferences.appPrefs.get('endDate', None))
        if not endDate:
            endDate = QDate(year, month, 15)
        self.edtEndDate.setDate(endDate)
        self.chkTemperature.setChecked(forceBool(QtGui.qApp.preferences.appPrefs.get('chkTemperature', False)))
        self.chkPulse.setChecked(forceBool(QtGui.qApp.preferences.appPrefs.get('chkPulse', False)))
        self.chkAPMax.setChecked(forceBool(QtGui.qApp.preferences.appPrefs.get('chkAPMax', False)))
        self.chkAPMin.setChecked(forceBool(QtGui.qApp.preferences.appPrefs.get('chkAPMin', False)))
        multipleDimension = forceInt(QtGui.qApp.preferences.appPrefs.get('multipleDimension', 0))
        if not multipleDimension:
            multipleDimension = 2
        self.edtMultipleDimension.setValue(multipleDimension)


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['chkTemperature'] = self.chkTemperature.isChecked()
        result['chkPulse'] = self.chkPulse.isChecked()
        result['chkAPMax'] = self.chkAPMax.isChecked()
        result['chkAPMin'] = self.chkAPMin.isChecked()
        result['multipleDimension'] = self.edtMultipleDimension.value()
        QtGui.qApp.preferences.appPrefs['begDate'] = toVariant(self.edtBegDate.date())
        QtGui.qApp.preferences.appPrefs['endDate'] = toVariant(self.edtEndDate.date())
        QtGui.qApp.preferences.appPrefs['chkTemperature'] = toVariant(self.chkTemperature.isChecked())
        QtGui.qApp.preferences.appPrefs['chkPulse'] = toVariant(self.chkPulse.isChecked())
        QtGui.qApp.preferences.appPrefs['chkAPMax'] = toVariant(self.chkAPMax.isChecked())
        QtGui.qApp.preferences.appPrefs['chkAPMin'] = toVariant(self.chkAPMin.isChecked())
        QtGui.qApp.preferences.appPrefs['multipleDimension'] = toVariant(self.edtMultipleDimension.value())
        return result


def pyTime(time):
    if time and time.isValid():
        return time.toPyTime()
    else:
        return None
