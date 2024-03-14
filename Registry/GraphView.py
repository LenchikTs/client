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

import math

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QString, QLineF, QPoint, QRectF, QLocale

from library.Utils  import forceString


class CGraphView(QtGui.QGraphicsView):
    def __init__(self, parent):
        QtGui.QGraphicsView.__init__(self, parent)
        self.setMouseTracking(True)
        self.dataList = {}
        self.toolTitlePoints = {}
        self.dataListXCurve = []
        self.dataListYCurve = []
        self.isMonth = False
        self.valueTypeY = 0 # 0-int, 1-float
        self.valueTypeX = 0 # 0-int, 1-float
        self.lowValue = 0.0   # Минимальное значение для оси Y.
        self.highValue = 0.0  # Максимальное значение для оси Y.


    def setValueTypeY(self, valueType):
        self.valueTypeY = valueType


    def setValueTypeX(self, valueType):
        self.valueTypeX = valueType


    def setIsMonth(self, isMonth):
        self.isMonth = isMonth


    def setDataList(self, dataList, lowValue=0.0, highValue=0.0):
        self.lowValue = lowValue
        self.highValue = highValue
        self.dataList = dataList
        self.dataListXCurve = []
        self.dataListYCurve = []
        dateKeys = self.dataList.keys()
        if self.isMonth:
            dateKeys.sort(key=lambda x: (x[1], x[0]))
        else:
            dateKeys.sort()
        for i, date in enumerate(dateKeys):
            value = self.dataList.get(date, 0)
            self.dataListXCurve.append((i+1, date))
            self.dataListYCurve.append(value)


    def drawAxes(self, painter, rect):
        self.toolTitlePoints = {}

        def setToolTitlePoints(p, x, y):
            toolTitleLine = self.toolTitlePoints.get((p.x(), p.y()), [])
            toolTitleLine.append(u'%s, %s'%(x, y))
            self.toolTitlePoints[(p.x(), p.y())] = toolTitleLine

        if self.dataListXCurve and self.dataListYCurve:
            dataListY = []
            dataListX = []
            #self.dataListYCurve = [10, 15, 20, 25, 30, 50]
            #self.dataListYCurve = [1000, 150, 20, 25, 305, 50]
            #self.dataListYCurve = [1, 2, 3, 4, 5, 6]
            #self.dataListXCurve = [1, 2, 3, 4, 5, 6]
            #self.dataListXCurve = [50, 100, 150, 180, 200, 250]
    #        self.dataListYCurve = [10.00, 15.025, 20.503, 25.75, 30.58, 50.55]
    #        self.dataListXCurve = [50, 100, 150, 180, 200, 250]
            dataListY.extend(self.dataListYCurve)
            dataListX.extend(self.dataListXCurve)
            dataListY.sort()
            dataListX.sort(key=lambda item: item[0])
            minValY = dataListY[0]
            maxValY = dataListY[len(dataListY)-1]
            minValX = dataListX[0][0]
            maxValX = dataListX[len(dataListX)-1][0]
            if self.lowValue < self.highValue:
                minValY = self.lowValue
                maxValY = self.highValue

            maxValYStr = QString(str(maxValY))
            maxValYFM = QtGui.QFontMetrics(QtGui.QFont(maxValYStr))
            hYFM = maxValYFM.height()
            wYFM = maxValYFM.width(maxValYStr)
            wYFM2 = maxValYFM.width(maxValYStr, 2) if len(maxValYStr) >= 2 else (2*wYFM)

            maxValXStr = QString(str(maxValX))
            maxValXFM = QtGui.QFontMetrics(QtGui.QFont(maxValXStr))
            hXFM = maxValXFM.height()
            wXFM = maxValXFM.width(maxValXStr)
            wXFM2 = maxValXFM.width(maxValXStr, 2) if len(maxValXStr) >= 2 else (2*wXFM)

            # метка по Y
            nameY = QString(u'__')
            nameYFM = QtGui.QFontMetrics(QtGui.QFont(nameY))
            wNameYFM = nameYFM.width(nameY)
            hNameYFM = nameYFM.height()

            # метка по X
            nameX = QString(u'|')
            nameXFM = QtGui.QFontMetrics(QtGui.QFont(nameX))
            wNameXFM = nameXFM.width(nameX)
            hNameXFM = nameXFM.height()

            y0 = int(rect.bottom()-(2*hYFM)-hNameXFM)
#            yN = int(rect.top()+(2*hYFM))
            yN = int(rect.top()+hYFM)
            x0 = int(rect.left()+wYFM+wNameYFM)
            xN = int(rect.right())
#            x0 = int(rect.left()+2*wYFM+wNameYFM)
#            xN = int(rect.right()-2*wXFM)

            #y количество меток
            n = abs(int((rect.top() - y0)/(2*hYFM)))
            #x количество меток
            m = abs(int((rect.right() - x0)/(2*wXFM + wXFM2)))

            # текст меток
            # math.fabs(X) - модуль X.
            # math.ceil(X) - округление до ближайшего большего числа.
            # math.floor(X) - округление вниз.
            # math.trunc(X) - усекает значение X до целого.
            # math.log(X, [base]) - логарифм X по основанию base. Если base не указан, вычисляется натуральный логарифм.
            # math.log1p(X) - натуральный логарифм (1 + X). При X → 0 точнее, чем math.log(1+X).
            # math.log10(X) - логарифм X по основанию 10.
            # math.log2(X) - логарифм X по основанию 2. Новое в Python 3.3.
            # math.pow(X, Y) - X в степени y.
            # math.sqrt(X) - квадратный корень из X.

            # по Y
            if self.valueTypeY:
                if minValY != 0:
                    yP = maxValY / minValY
                else:
                    yP = maxValY
                rYP = 1 + math.log10(abs(yP)) # число знаков отображения
                yPZNK = round(rYP) # округление до ближайшего целого
                maxValYR = maxValY * math.pow(10, yPZNK)
                maxValY = round(maxValYR)
                minValYR = minValY * math.pow(10, yPZNK)
                minValY = round(minValYR)
            dY = (maxValY - minValY)/float(1 if n == 0 else n)
            if dY >= 1:
                rY = math.log10(abs(dY))
                rOkrY = math.floor(rY) # округление в меньшую сторону? # округление до ближайшего целого
                MLTY = dY / math.pow(10, rOkrY)
                MOkrY = math.ceil(MLTY) # округление до ближайшего целого
                # dY1
                dY1 = math.pow(10, rOkrY) * MOkrY
                # dY2
                rY2 = math.log(abs(MLTY), 2)
                r2OkrY = math.ceil(rY2) # округление в меньшую сторону? # округление до ближайшего целого
                dY2 = math.pow(10, rOkrY) * math.pow(2, r2OkrY)
                # dY3
                rY3 = math.log(abs(MLTY), 3)
                r3OkrY = math.ceil(rY3) # округление в меньшую сторону? # округление до ближайшего целого
                dY3 = math.pow(10, rOkrY) * math.pow(3, r3OkrY)
                # dY5
                rY5 = math.log(abs(MLTY), 5)
                r5OkrY = math.ceil(rY5) # округление в меньшую сторону? # округление до ближайшего целого
                dY5 = math.pow(10, rOkrY) * math.pow(5, r5OkrY)
                #dYMin
                tempMinDY = abs(abs(dY) - abs(dY1))
                dYLT = dY1
                tempMinDY2 = abs(abs(dY) - abs(dY2))
                if tempMinDY2 < tempMinDY and abs(dY) <= abs(dY2):
                    tempMinDY = tempMinDY2
                    dYLT = dY2
                tempMinDY3 = abs(abs(dY) - abs(dY3))
                if tempMinDY3 < tempMinDY and abs(dY) <= abs(dY3):
                    tempMinDY = tempMinDY3
                    dYLT = dY3
                tempMinDY5 = abs(abs(dY) - abs(dY5))
                if tempMinDY5 < tempMinDY and abs(dY) <= abs(dY5):
                    tempMinDY = tempMinDY5
                    dYLT = dY5
                NLTY = minValY / dYLT
                NYOkr = math.ceil(NLTY) # округление до ближайшего целого
                yMinLT = NYOkr * dYLT
            else:
                n = maxValY - minValY + 1
                if n == 0:
                    n = 1
                dYLT = (rect.top() - y0) / float(n)
                yMinLT = 0

            # по X
            if self.valueTypeX:
                if minValX != 0:
                    xP = maxValX / minValX
                else:
                    xP = maxValX
                rXP = 1 + math.log10(abs(xP)) # число знаков отображения
                xPZNK = round(rXP) # округление до ближайшего целого
                maxValXR = maxValX * math.pow(10, xPZNK)
                maxValX = round(maxValXR)
                minValXR = minValX * math.pow(10, xPZNK)
                minValX = round(minValXR)
            dX = (maxValX - minValX)/float(1 if m == 0 else m)
            if dX >= 1:
                rX = math.log10(abs(dX))
                rOkrX = math.floor(rX) # округление в меньшую сторону? # округление до ближайшего целого
                MLTX = dX / math.pow(10, rOkrX)
                MOkrX = math.ceil(MLTX) # округление до ближайшего целого
                # dX1
                dX1 = math.pow(10, rOkrX) * MOkrX
                # dX2
                rX2 = math.log(abs(MLTX), 2)
                r2OkrX = math.ceil(rX2) # округление в меньшую сторону? # округление до ближайшего целого
                dX2 = math.pow(10, rOkrX) * math.pow(2, r2OkrX)
                # dX3
                rX3 = math.log(abs(MLTX), 3)
                r3OkrX = math.ceil(rX3) # округление в меньшую сторону? # округление до ближайшего целого
                dX3 = math.pow(10, rOkrX) * math.pow(3, r3OkrX)
                # dX5
                rX5 = math.log(abs(MLTX), 5)
                r5OkrX = math.ceil(rX5) # округление в меньшую сторону? # округление до ближайшего целого
                dX5 = math.pow(10, rOkrX) * math.pow(5, r5OkrX)
                #dXMin
                tempMinDX = abs(abs(dX) - abs(dX1))
                dXLT = dX1
                tempMinDX2 = abs(abs(dX) - abs(dX2))
                if tempMinDX2 < tempMinDX and abs(dX) <= abs(dX2):
                    tempMinDX = tempMinDX2
                    dXLT = dY2
                tempMinDX3 = abs(abs(dX) - abs(dX3))
                if tempMinDX3 < tempMinDX and abs(dX) <= abs(dX3):
                    tempMinDX = tempMinDX3
                    dXLT = dY3
                tempMinDX5 = abs(abs(dX) - abs(dX5))
                if tempMinDY5 < tempMinDX and abs(dX) <= abs(dX5):
                    tempMinDX = tempMinDX5
                    dXLT = dX5
                NLTX = minValX / dXLT
                NXOkr = math.ceil(NLTX) # округление до ближайшего целого
                xMinLT = NXOkr * dXLT
            else:
                m = maxValX - minValX + 1
                if m == 0:
                    m = 1
                dXLT = (rect.right() - x0) / float(m)
                xMinLT = 0

            # метки (пиксели)
            yLabelList = []
            x = int(x0 - wNameYFM)
            if dY >= 1:
                for i in range(0, n+1):
                    y = int(y0 - (i*2*hYFM))
                    yLabelList.append((x, y)) # координаты меток по Y
            else:
                for i in range(0, n):
                    y = int(y0 + (dYLT*i))
                    yLabelList.append((x, y)) # координаты меток по Y

            xLabelList = []
            if dX >= 1:
                y = int(y0 + hNameXFM)
                for i in range(0, m+1):
                    x = int(x0 + (i*(2*wXFM + wXFM2)))
                    xLabelList.append((x, y)) # координаты меток по X
            else:
                y = int(y0 + hNameXFM)
                for i in range(0, m):
                    x = int(x0 + (dXLT*i))
                    xLabelList.append((x, y)) # координаты меток по X

            pen = QtGui.QPen()
            pen.setWidth(0)
            oldTransform = QtGui.QTransform(painter.transform())
            painter.setTransform(QtGui.QTransform(1, 0, 0, 1, oldTransform.dx(), oldTransform.dy()))
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            pen.setColor(Qt.black)
            painter.setPen(pen)

            # оси координат
            painter.drawLines(QLineF(x0, y0, x0, yN))
            painter.drawLines(QLineF(x0, y0, xN, y0))

            # метки
            # по Y
            for x, y in yLabelList:
                painter.drawText(QPoint(x, y), nameY)
            # по X
            for x, y in xLabelList:
                painter.drawText(QPoint(x, y), nameX)

            # текст
            locale = QLocale()
            # по Y
            if dY >= 1:
                for i, (x, y) in enumerate(yLabelList):
                    if self.valueTypeY:
                        nameY = locale.toString(float((yMinLT + dYLT * i) / math.pow(10, yPZNK)), 'f', 2)
                    else:
                        nameY = forceString(int(yMinLT + dYLT * i))
                    painter.drawText(QPoint(x - wYFM, y), nameY)
            else:
                for i, (x, y) in enumerate(yLabelList):
                    if self.valueTypeY:
                        nameY = locale.toString(float((i+1) / math.pow(10, yPZNK)), 'f', 2)
                    else:
                        nameY = forceString(i + 1)
                    painter.drawText(QPoint(x - wYFM, y), nameY)
            # по X
            if dX >= 1:
                for i, (x, y) in enumerate(xLabelList):
                    if self.valueTypeX:
                        nameX = locale.toString(float((xMinLT + dXLT * i) / math.pow(10, xPZNK)), 'f', 2)
                    else:
                        if not self.isMonth:
                            nameX = forceString(dataListX[i][1])
                        else:
                            month, year = dataListX[i][1]
                            nameX = forceString(month) + forceString(u'/') + forceString(year)
                            #nameX = forceString(int(xMinLT + dXLT * i)) # для отображения расчётной шкалы по X, не для отображения Дат
                    painter.drawText(QPoint(x, y + hNameXFM), nameX)
            else:
                for i, (x, y) in enumerate(xLabelList):
                    if self.valueTypeX:
                        nameX = locale.toString(float((i+1) / math.pow(10, xPZNK)), 'f', 2)
                    else:
                        #nameX = forceString(i + 1)
                        if not self.isMonth:
                            nameX = forceString(dataListX[i][1])
                        else:
                            month, year = dataListX[i][1]
                            nameX = forceString(month) + forceString(u'/') + forceString(year)
                            #nameX = forceString(i + 1) # для отображения расчётной шкалы по X, не для отображения Дат
                    painter.drawText(QPoint(x, y + hNameXFM), nameX)

            pen.setColor(Qt.red)
            painter.setPen(pen)
            # кривая
            # по Y
            yMax = yMinLT + dYLT * n
            #Ky = (yMax - yMinLT) / (yN - y0)
            Ky = round((yMax - yMinLT) / (yN - y0), 3)
            # по X
            xMax = xMinLT + dXLT * m
            Kx = (xMax - xMinLT) / (xN - x0)
            # массив точек
            dataListCurve = []
            for i, yi in enumerate(self.dataListYCurve):
                if self.valueTypeY:
                    if dY >= 1:
                        yPi = int(round(y0 + ((yi * math.pow(10, yPZNK)) - yMinLT) / Ky))
                    else:
                        yPi = int(round(y0 + (dYLT*(yi * math.pow(10, yPZNK))) - dYLT))
                else:
                    if dY >= 1:
                        yPi = int(round(y0 + (yi - yMinLT) / Ky))
                    else:
                        yPi = int(round(y0 + (dYLT*yi) - dYLT))
                xi = self.dataListXCurve[i][0]
                if self.valueTypeX:
                    if dX >= 1:
                        xPi = int(round(x0 + ((xi * math.pow(10, xPZNK)) - xMinLT) / Kx))
                    else:
                        xPi = int(round(x0 + (dXLT*(xi * math.pow(10, xPZNK))) - dXLT))
                else:
                    if dX >= 1:
                        xPi = int(round(x0 + (xi - xMinLT) / Kx))
                    else:
                        xPi = int(round(x0 + (dXLT*xi) - dXLT))
                point = QPoint(xPi, yPi)
                dataListCurve.append(point)
                if not self.isMonth:
                    xd = self.dataListXCurve[i][1].toString('dd.MM.yyyy')
                else:
                    month, year = self.dataListXCurve[i][1]
                    xd = forceString(month) + forceString(u'/') + forceString(year)
                setToolTitlePoints(point, forceString(xd), forceString(yi))
            painter.drawPolyline(QtGui.QPolygon(dataListCurve))
            self.drawDivisionOnScale(painter, dataListCurve, x0, y0, yN)
            painter.setTransform(oldTransform)


    def drawDivisionOnScale(self, painter, points, x0, y0, y1):
        for point in points:
            for d in range(x0, point.x(), 10):
                painter.drawPoints(QPoint(d, point.y()))
            for d in range(y0, y1, -10):
                painter.drawPoints(QPoint(point.x(), d))


    def drawBackground(self, painter, rect):
        QtGui.QGraphicsView.drawBackground(self, painter, rect)
        self.drawAxes(painter, rect)


#    def drawForeground(self, painter, rect):
#        self.drawAxes(painter, rect)


#    def mouseReleaseEvent(self,  mouseEvent):
#        self.setToolTipPointEvent(mouseEvent)
#        QtGui.QGraphicsView.mouseReleaseEvent(self, mouseEvent)


    def mouseMoveEvent(self,  mouseEvent):
        self.setToolTipPointEvent(mouseEvent)
        QtGui.QGraphicsView.mouseMoveEvent(self, mouseEvent)


    def setToolTipPointEvent(self, mouseEvent):
        def setToolTipPoint(key):
            toolTitleLine = self.toolTitlePoints.get(key, [])
            if toolTitleLine:
                self.setToolTip(u'|'.join(str(toolTitle) for toolTitle in toolTitleLine if toolTitle))
                return True
            return False
        self.setToolTip(u'')
        point = mouseEvent.pos()
        viewportTransform = self.viewportTransform()
        if point and viewportTransform:
            point.setX(point.x() - viewportTransform.dx())
            point.setY(point.y() - viewportTransform.dy())
            if point and (point.x(), point.y()) in self.toolTitlePoints.keys():
                setToolTipPoint((point.x(), point.y()))
            else:
                for i in range(-10, 11, 1):
                    if i != 0:
                        point.setX(point.x() + (1 if i > 0 else -1))
                    for j in range(-10, 11, 1):
                        if j != 0:
                            point.setY(point.y() + (1 if j > 0 else -1))
                        if point and (point.x(), point.y()) in self.toolTitlePoints.keys() and setToolTipPoint((point.x(), point.y())):
                            break


    def getVisibleSceneRect(self):
        topleft = self.mapToScene(0,0)
        bottomRight = self.mapToScene(self.width(), self.height())
        return QRectF(topleft, bottomRight)


    def sceneToImage(self):
        image = QtGui.QImage(self.getVisibleSceneRect().size().toSize(), QtGui.QImage.Format_ARGB32)
        image.fill(Qt.transparent)
#        painter = QtGui.QPainter(image)
#        painter.begin(printer)
#        self.render(painter)
#        painter.end()
        return image

