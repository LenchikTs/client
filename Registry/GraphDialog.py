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
#import pyqtgraph
#import pyqtgraph as pg
import codecs
import os.path
import re

from PyQt4.QtCore import Qt, pyqtSignature, QByteArray, QFileInfo, QRectF, QSizeF, QSize, QString,  QVariant, QChar, QLineF, QLine, QDate

from PyQt4 import QtGui
from PyQt4 import QtSvg
from PyQt4 import QtXml

from library.Utils      import forceInt, forceDouble, forceDate, forceString
from library.DialogBase import CDialogBase
from Registry.Utils     import getClientString
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportView import CReportViewDialog

from Ui_GraphDialog import Ui_GraphDialog


def showGraph(widget, name, content, canvases, pageFormat):
    view = CGraphDialog(pageFormat, widget)
    view.setDocName(name)
    view.setContent(content, canvases)
    view.exec_()

def printGraph(name, content, printer):
    doc = CGraphDocument(content)
    doc.print_(name, printer)


class CGraphDocument(QtXml.QDomDocument):
    def __init__(self, content=None):
            QtXml.QDomDocument.__init__(self)
            if content:
                self.setContent(content)


    def setContent(self, content):
        self.srcContent = content
        ok, errorMsg, errorLine, errorColumn = QtXml.QDomDocument.setContent(self, QByteArray(content.encode('utf-8')), False)
        if not ok:
            raise Exception(u'%s at (%d, %d)' % (errorMsg, errorLine, errorColumn))


    def isValid(self):
        svgElement = self.firstChildElement('svg')
        return svgElement is not None and not svgElement.isNull()


    def findPages(self):
        pageIdList = []
        svgElement = self.firstChildElement('svg')
        if svgElement:
            pageElement = svgElement.firstChildElement('g')
            while pageElement and not pageElement.isNull():
                pageId = unicode(pageElement.attribute('id'))
                if pageId.startswith('page'):
                    pageIdList.append(pageId)
#                    pageElement.setAttribute('visibility', 'hidden')
                pageElement = pageElement.nextSiblingElement('g')
        return pageIdList


    def getPageRectSizeF(self):
        def parseLength(txt):
            s = re.search(r'^\s*((?:\d+\.?\d*)|(?:\d*\.\d+))\s*([^ ]*)\s*$',txt)
            if s:
                qnt, unit = s.groups()
                result = float(qnt) if qnt and qnt != '.' else 0
                if unit == 'mm':
                    return result
                elif unit == 'sm':
                    return result*10
                elif unit == 'in':
                    return result*25.4
                else:
                    return result*25.4/72
            else:
                return None

        svgElement = self.firstChildElement('svg')
        if svgElement:
            width = parseLength(unicode(svgElement.attribute('width')))
            height = parseLength(unicode(svgElement.attribute('height')))
        else:
            width = height = None
        if width and height:
            return QSizeF(width, height)
        else:
            return None


    def hideAllPagesExceptOne(self, visiblePageId):
        svgElement = self.firstChildElement('svg')
        if svgElement:
            pageElement = svgElement.firstChildElement('g')
            while pageElement and not pageElement.isNull():
                pageId = unicode(pageElement.attribute('id'))
                if pageId.startswith('page'):
                    if pageId == visiblePageId:
                        pageElement.setAttribute('visibility', 'visible')
                    else:
                        pageElement.setAttribute('visibility', 'hidden')
                pageElement = pageElement.nextSiblingElement('g')


    def print_(self, docName, printer, svgItem = None):
        size = self.getPageRectSizeF()
        if size:
            w = size.width()
            h = size.height()
            if w < h:
                printer.setOrientation(QtGui.QPrinter.Portrait)
            else:
                size.transpose()
                printer.setOrientation(QtGui.QPrinter.Landscape)
            printer.setPaperSize(size, 0)

        printer.setFullPage(True)
        printer.setPageMargins(0,0,0,0,0)
        printer.setCreator('samson')
        printer.setDocName(docName)
        printer.setFontEmbeddingEnabled(True)
        painter = QtGui.QPainter()

        renderer = QtSvg.QSvgRenderer()
        painter.begin(printer)
#        if printer.orientation() == QtGui.QPrinter.Landscape:
#            painterRect = painter.viewport()
#            painter.translate(0, painterRect.height())
#            painter.rotate(270)

        pageIdList = self.findPages()
        if pageIdList:
            fromPage = printer.fromPage()
            toPage   = printer.fromPage()
            if fromPage and toPage:
                pageIdList = pageIdList[fromPage-1:toPage]
            if printer.pageOrder == QtGui.QPrinter.LastPageFirst:
                pageIdList.reverse()
            firstPage = True
            for pageId in pageIdList:
                self.hideAllPagesExceptOne(pageId)
                renderer.load(self.toByteArray(0))
                if not firstPage:
                    printer.newPage()
                renderer.render(painter)
                firstPage = False
        else:
            if svgItem:
                dx = svgItem.x()
                dy = svgItem.y()
                rect = svgItem.boundingRect()
                painter.setWindow(rect.x()-dx, rect.y()-dy, rect.width()-dx, rect.height()-dy)
                svgItem.paint(painter, QtGui.QStyleOptionGraphicsItem())
            else:
                renderer.load(self.toByteArray())
                renderer.render(painter)
#        del renderer
        painter.end()


class CGraphDialog(CDialogBase, Ui_GraphDialog):
    def __init__(self, parent, pageFormat, actionIdList, valueTypeX=0, valueTypeY = 0):
        CDialogBase.__init__(self, parent)
        self.btnPrint = QtGui.QPushButton(u'Печатать', self)
        self.btnPrint.setObjectName('btnPrint')
        self.btnPrint.setDefault(True)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowState(Qt.WindowMaximized)
        self.setValueTypeX(valueTypeX)
        self.setValueTypeY(valueTypeY)
        self.cmbPropertyType.addPropertyItem(actionIdList)
        self.graphicsView.setScene(QtGui.QGraphicsScene(self.graphicsView))
        #self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn); # Qt.ScrollBarAlwaysOff, Qt.ScrollBarAlwaysOn, Qt.ScrollBarAsNeeded
        #self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn);
        self.doc = CGraphDocument()
        self.pageFormat = pageFormat
        self.pageList = []
        self.buttonBox.addButton(self.btnPrint, QtGui.QDialogButtonBox.ActionRole)
        self.setDocName(u'График')
        self.showMaximized()
        self.dataList = {}
        self.begDatePeriod = None
        self.endDatePeriod = None
        self.lowValue = 0.0
        self.highValue = 0.0
        self.year = None
        self.lblCurrentYear.setText(forceString(QDate.currentDate().year()))
        #self.initItems()


    def initItems(self):
        scene = self.graphicsView.scene()
        scene.clearSelection()
        self.svgItem = QtSvg.QGraphicsSvgItem()
        self.svgItem.setFlags(QtGui.QGraphicsItem.ItemIsSelectable)
        self.svgItem.setZValue(0)
        scene.addItem(self.svgItem)
        self.graphicsView.setScene(scene)


    def setPeriod(self, begDate, endDate):
        self.begDatePeriod = begDate
        self.endDatePeriod = endDate
        date = self.endDatePeriod
        if not date:
            date = self.begDatePeriod
        if not date:
            date = QDate().currentDate()
        self.setYear(date.year() if date else None)


    def setYear(self, year):
        self.year = year


    def setPageList(self, pageList, lowValue=0.0, highValue=0.0):
        self.pageList = pageList
        self.lowValue = lowValue
        self.highValue = highValue
        self.setupPagesControl()


    def setValueTypeX(self, valueType):
        self.valueTypeX = valueType
        self.graphicsView.valueTypeX = self.valueTypeX


    def setValueTypeY(self, valueType):
        self.valueTypeY = valueType
        self.graphicsView.valueTypeY = self.valueTypeY


    def setIsMonth(self, isMonth):
        self.graphicsView.setIsMonth(isMonth)


    def setDataList(self, dataList):
        self.graphicsView.setDataList(dataList, self.lowValue, self.highValue)


    def setDocName(self, name):
        self.docName = name
        self.setWindowTitle(name)
        fileName = name
        for x in ':?|()[]\"\';!*/\\':
            fileName = fileName.replace(x, '')
        self.fileName = fileName


    def setContent(self, content, canvases):
        try:
            self.doc.setContent(content)
        except:
            pass

        if self.doc.isValid():
            self.pageList = self.doc.findPages()
            self.svgItem.renderer().load(QByteArray(content.encode('utf-8')))
            self.svgItem.setElementId('') # for recalc item.boundRect()
            self.svgItem.setX(forceInt(QtGui.qApp.preferences.appPrefs.get(self.docName+'_svgX', QVariant())))
            self.svgItem.setY(forceInt(QtGui.qApp.preferences.appPrefs.get(self.docName+'_svgY', QVariant())))
            self.label.setText(u'Сдвиг x: %i, y %i'%(self.svgItem.x(), self.svgItem.y()))
            boundingRect = self.svgItem.boundingRect()
            self.shadowItem.setRect(boundingRect.adjusted(-1, -1, 2, 2))
            self.frameItem.setRect(boundingRect.adjusted(-1, -1, 2, 2))
            self.graphicsView.scene().setSceneRect(boundingRect.adjusted(-3, -3, 10, 10))
            if canvases:
                self.frameItem.setBrush(QtGui.QBrush(canvases[canvases.keys()[0]].image.scaled(boundingRect.width(), boundingRect.height())))
            self.setupPagesControl()


    def setupPagesControl(self):
        isGotoPage = 0
        if self.chkMonth.isChecked():
            currentDate = QDate.currentDate()
            currentYear = currentDate.year()
            for n, (valueIntList, valueDoubleList) in enumerate(self.pageList):
                for intKey in valueIntList.keys():
                    if currentYear == intKey[1]:
                        isGotoPage = n
                        break
                if not isGotoPage:
                    for doubleKeys in valueDoubleList.keys():
                        if currentYear == doubleKeys[1]:
                            isGotoPage = n
                            break
        self.gotoPage(isGotoPage)
        self.edtPageNum.setRange(1, len(self.pageList))
        self.grpPager.setVisible(len(self.pageList) > 1)
        self.grpPager.setEnabled(len(self.pageList) > 1)


    def gotoPage(self, n):
        self.btnFirstPage.setEnabled(n > 0)
        self.btnLastPage.setEnabled((n + 1) < len(self.pageList))
        self.edtPageNum.setValue(n + 1)
        if 0 <= n < len(self.pageList):
            valueIntList, valueDoubleList = self.pageList[n]
            self.updateGraph(valueIntList, valueDoubleList)
            #self.graphicsView.updateScene(self.graphicsView.sceneRect())
        elif not self.pageList:
            self.updateGraph({}, {})


    def saveAsFile(self):
        defaultFileName = QtGui.qApp.getSaveDir()
        if self.fileName:
            defaultFileName = os.path.join(defaultFileName, self.fileName)

        saveFormats = [u'изображение SVG (*.svg)',
                       u'Portable Document Format (*.pdf)',
                       u'PostScript (*.ps)',
                      ]
        selectedFilter = QString('')

        fileName = QtGui.QFileDialog.getSaveFileName(
            self,
            u'Выберите имя файла',
            defaultFileName,
            ';;'.join(saveFormats),
            selectedFilter)
        if not fileName.isEmpty():
            exts = selectedFilter.section('(*.',1,1).section(')',0,0).split(';*.')
            ext = QFileInfo(fileName).suffix()
            if exts and not exts.contains(ext, Qt.CaseInsensitive):
                ext = exts[0]
                fileName.append('.'+ext)
            fileName = unicode(fileName)
            ext = unicode(ext)
            if ext.lower() == 'pdf':
                self.saveAsPdfOrPS(fileName, QtGui.QPrinter.PdfFormat)
            elif ext.lower() == 'ps':
                self.saveAsPdfOrPS(fileName, QtGui.QPrinter.PostScriptFormat)
            else:
                self.saveAsSvg(fileName)


    def saveAsPdfOrPS(self, fileName, format):
        QtGui.qApp.setSaveDir(fileName)
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        printer.setOutputFormat(format)
        printer.setOutputFileName(fileName)
        printer.setFontEmbeddingEnabled(True)
        self.pageFormat.setupPrinter(printer)
        self.doc.print_(self.docName, printer)


    def saveAsSvg(self, fileName):
        QtGui.qApp.setSaveDir(fileName)
        file = codecs.open(unicode(fileName), encoding='utf-8', mode='w+')
        file.write(self.doc.srcContent)
        file.close()


    @pyqtSignature('int')
    def on_cmbPropertyType_currentIndexChanged(self, index):
        lowValue = 0.0
        highValue = 0.0
        valueIntList = {}
        valueDoubleList = {}
        pageList = []
        pageListYear = {}
        isGotoPage = False
        propertyTypeId = self.cmbPropertyType.value()
        if propertyTypeId:
            actionIdList = self.cmbPropertyType.getActionIdList()
            if actionIdList:
                db = QtGui.qApp.db
                tableAction = db.table('Action')
                tableAP = db.table('ActionProperty')
                tableAPT = db.table('ActionPropertyType')
                tableAPInt = db.table('ActionProperty_Integer')
                tableAPDouble = db.table('ActionProperty_Double')
                queryTable = tableAction.innerJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
                queryTable = queryTable.innerJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
                queryTable = queryTable.leftJoin(tableAPInt, tableAPInt['id'].eq(tableAP['id']))
                queryTable = queryTable.leftJoin(tableAPDouble, tableAPDouble['id'].eq(tableAP['id']))
                cond = [tableAction['id'].inlist(actionIdList),
                        tableAction['deleted'].eq(0),
                        tableAP['deleted'].eq(0),
                        tableAPT['deleted'].eq(0),
                        tableAction['endDate'].isNotNull(),
                        db.joinOr([tableAPInt['value'].isNotNull(), tableAPDouble['value'].isNotNull()])
                        ]
                cols = [tableAPInt['value'].alias('valueInt'),
                        tableAPDouble['value'].alias('valueDouble'),
                        tableAction['endDate'],
                        tableAPT['lowValue'],
                        tableAPT['highValue']
                        ]
                if self.chkMonth.isChecked():
                    order=u'Action.endDate DESC'
                else:
                    order=u'Action.endDate ASC'
                cnt = 0
                records = db.getRecordList(queryTable, cols, cond, order=order)
                for record in records:
                    isGotoPage = False
                    endDate = forceDate(record.value('endDate'))
                    valueInt = forceInt(record.value('valueInt'))
                    lowValue = forceDouble(record.value('lowValue'))
                    highValue = forceDouble(record.value('highValue'))
                    if self.chkMonth.isChecked():
                        if valueInt and endDate:
                            month = endDate.month()
                            year = endDate.year()
                            if (month, year) not in valueIntList.keys():
                                valueIntList[(month, year)] = valueInt
                        valueDouble = forceDouble(record.value('valueDouble'))
                        if valueDouble and endDate:
                            month = endDate.month()
                            year = endDate.year()
                            if (month, year) not in valueDoubleList.keys():
                                valueDoubleList[(month, year)] = valueDouble
                        if len(valueIntList) >= 12 or len(valueDoubleList) >= 12:
                            pageListYear[cnt] = (valueIntList, valueDoubleList)
                            valueIntList = {}
                            valueDoubleList = {}
                            isGotoPage = True
                            cnt += 1
                    else:
                        if valueInt and endDate:
                            valueIntList[endDate] = valueInt
                        valueDouble = forceDouble(record.value('valueDouble'))
                        if valueDouble and endDate:
                            valueDoubleList[endDate] = valueDouble
                        if len(valueIntList) >= 12 or len(valueDoubleList) >= 12:
                            pageList.append((valueIntList, valueDoubleList))
                            valueIntList = {}
                            valueDoubleList = {}
                            isGotoPage = True
                if self.chkMonth.isChecked():
                    if not isGotoPage and (0 < len(valueIntList) < 12 or 0 < len(valueDoubleList) < 12):
                        pageListYear[cnt] = (valueIntList, valueDoubleList)
                else:
                    if not isGotoPage and (len(valueIntList) < 12 or len(valueDoubleList) < 12):
                        pageList.append((valueIntList, valueDoubleList))
        if self.chkMonth.isChecked():
            yearKeys = pageListYear.keys()
            yearKeys.sort(reverse = True)
            for yearKey in yearKeys:
                valueIntList, valueDoubleList = pageListYear.get(yearKey, ({}, {}))
                if len(valueIntList) > 0 or len(valueDoubleList) > 0:
                    pageList.append((valueIntList, valueDoubleList))
        self.setPageList(pageList, lowValue, highValue)


    def updateGraph(self, valueIntList, valueDoubleList):
        if valueIntList:
            self.graphicsView.setValueTypeX(0)
            self.graphicsView.setValueTypeY(0)
            self.setDataList(valueIntList)
            self.graphicsView.viewport().update()
        elif valueDoubleList:
            self.graphicsView.setValueTypeX(0)
            self.graphicsView.setValueTypeY(1)
            self.setDataList(valueDoubleList)
            self.graphicsView.viewport().update()
        else:
            self.graphicsView.setValueTypeX(0)
            self.graphicsView.setValueTypeY(0)
            self.setDataList({})
            self.graphicsView.viewport().update()


    @pyqtSignature('bool')
    def on_chkMonth_clicked(self, value):
        self.setIsMonth(value)
        self.on_cmbPropertyType_currentIndexChanged(self.cmbPropertyType.currentIndex())


    @pyqtSignature('')
    def on_btnFirstPage_clicked(self):
        self.edtPageNum.setValue(self.edtPageNum.minimum())


    @pyqtSignature('')
    def on_btnLastPage_clicked(self):
        self.edtPageNum.setValue(self.edtPageNum.maximum())


    @pyqtSignature('int')
    def on_edtPageNum_valueChanged(self, val):
        self.gotoPage(val - 1)


#QPrinter printer(QPrinter::HighResolution);
#    printer.setPageSize(QPrinter::A4);
#    printer.setOutputFormat(QPrinter::PdfFormat);
#    printer.setOutputFileName(QString("./report.pdf"));
#    printer.setPageMargins(0,0,0,0,QPrinter::Millimeter);
#    QPainter painter(&printer);
#    ui->view->scene()->render(&painter);


# QPrinter printer;
#    if (QPrintDialog(&printer).exec() == QDialog::Accepted) {
#        printer.setResolution(QPrinter::HighResolution);
#        printer.setOutputFormat(QPrinter::NativeFormat);
#        printer.setPageSize(QPrinter::A4);
#        printer.setPaperSize(QSize(210,297),QPrinter::Millimeter);
#        printer.setPageMargins(0,0,0,0,QPrinter::Millimeter);
#        QPainter painter(&printer);
#        painter.setRenderHint(QPainter::Antialiasing);
#        ui->view->scene()->render(&painter);
#     }


    @pyqtSignature('')
    def on_btnPrint_clicked(self):
    #QGraphicsScene scene;
    #scene.addRect(QRectF(0, 0, 100, 200), QPen(Qt::black), QBrush(Qt::green));
    #
    #QPrinter printer;
    #if (QPrintDialog(&printer).exec() == QDialog::Accepted) {
    #    QPainter painter(&printer);
    #    painter.setRenderHint(QPainter::Antialiasing);
    #    scene.render(&painter);
    #}

# ################################################################################
        printer = QtGui.QPrinter()
        dialog = QtGui.QPrintDialog(printer, self)
        if dialog.exec_():
            rect = self.graphicsView.viewport().rect()
            pixmap = QtGui.QPixmap(rect.size())
            painter = QtGui.QPainter(printer)
            #pixmap.save('/path/to/file.png')
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setViewport(rect)
            painter.begin(printer)
            painter.drawPixmap(0, 0, pixmap)
            #self.graphicsView.render(painter, QRectF(pixmap.rect()), rect)
            self.graphicsView.render(painter)
            #self.graphicsView.render(painter, QRectF(0, printer.height(), printer.width(), printer.height()), viewport.adjusted(0, 0, 0, -viewport.height()))
            painter.end()


# ################################################################################
#        printer = QtGui.QPrinter()
#        printer.setResolution(QtGui.QPrinter.HighResolution);
##        printer.setOutputFormat(QtGui.QPrinter.NativeFormat);
#        printer.setPageSize(QtGui.QPrinter.A4);
##        printer.setPaperSize(QSizeF(0, 0), QtGui.QPrinter.DevicePixel);
##        printer.setPageMargins(0,0,0,0,QtGui.QPrinter.DevicePixel);
#        printer.setOrientation(QtGui.QPrinter.Landscape)
#        printer.setFullPage(True)
#        dialog = QtGui.QPrintDialog(printer, self)
#        if dialog.exec_():
#            painter = QtGui.QPainter(printer)
#            painter.setRenderHint(QtGui.QPainter.Antialiasing)
#            painter.begin(printer)
#            viewport = self.graphicsView.viewport().rect()
#            #self.graphicsView.render(painter)
#            self.graphicsView.render(painter, QRectF(printer.rect()), viewport)
#            #self.graphicsView.render(painter, QRectF(0, printer.height(), printer.width(), printer.height()))
#            #self.graphicsView.render(painter, QRectF(0, printer.height(), printer.width(), printer.height()), viewport.adjusted(0, 0, 0, -viewport.height()))
#            painter.end()


# ########################################################################################

#        defaultPrinterInfo = QtGui.QPrinterInfo.defaultPrinter()
#        if not defaultPrinterInfo.isNull():
#            printer = QtGui.QPrinter(defaultPrinterInfo, QtGui.QPrinter.HighResolution)
#        else:
#            printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
#        printer.setPrintRange(printer.AllPages)
#        printer.setOrientation(printer.Portrait)
#        printer.setPaperSize(printer.A4)
#        printer.setFullPage(False)
#        if hasattr(printer, 'setNumCopies'):
#            printer.setNumCopies(1)
#        if hasattr(printer, 'setCopyCount'):
#            printer.setCopyCount(1)
#
#        self.pageFormat.setupPrinter(printer)
#        if (defaultPrinterInfo.isNull() or (QtGui.qApp.keyboardModifiers() & Qt.ControlModifier)) or not QtGui.qApp.enableFastPrint():
#            dialog = QtGui.QPrintDialog(printer, self)
#            dialog.setMinMax(1, max(1, len(self.pageList)))
#            if dialog.exec_() != QtGui.QDialog.Accepted:
#                return
#        self.print_(u'График', printer)


#    @pyqtSignature('')
#    def on_btnPrint_clicked(self):
##        printer = QtGui.QPrinter()
##        printer.setOrientation(QtGui.QPrinter.Landscape)
##        dialog = QtGui.QPrintDialog(printer, self)
##        if dialog.exec_():
##            painter = QtGui.QPainter(printer)
##            painter.setRenderHint(QtGui.QPainter.Antialiasing)
##            painter.begin(printer)
##            painter.drawImage
##            self.graphicsView.render(painter)
##            painter.end()
#        defaultPrinterInfo = QtGui.QPrinterInfo.defaultPrinter()
#        if not defaultPrinterInfo.isNull():
#            printer = QtGui.QPrinter(defaultPrinterInfo, QtGui.QPrinter.HighResolution)
#        else:
#            printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
#        printer.setPrintRange(printer.AllPages)
#        printer.setOrientation(printer.Portrait)
#        printer.setPaperSize(printer.A4)
#        printer.setFullPage(False)
#        if hasattr(printer, 'setNumCopies'):
#            printer.setNumCopies(1)
#        if hasattr(printer, 'setCopyCount'):
#            printer.setCopyCount(1)
#
#        self.pageFormat.setupPrinter(printer)
#        if (defaultPrinterInfo.isNull() or (QtGui.qApp.keyboardModifiers() & Qt.ControlModifier)) or not QtGui.qApp.enableFastPrint():
#            dialog = QtGui.QPrintDialog(printer, self)
#            dialog.setMinMax(1, max(1, len(self.pageList)))
#            if dialog.exec_() != QtGui.QDialog.Accepted:
#                return
#        self.print_(u'График', printer)



    #QGraphicsScene scene;
    #scene.addRect(QRectF(0, 0, 100, 200), QPen(Qt::black), QBrush(Qt::green));
    #
    #QPrinter printer;
    #if (QPrintDialog(&printer).exec() == QDialog::Accepted) {
    #    QPainter painter(&printer);
    #    painter.setRenderHint(QPainter::Antialiasing);
    #    scene.render(&painter);
    #}



    def print_(self, docName, printer):
#
#        size = self.getPageRectSizeF()
#        if size:
#            w = size.width()
#            h = size.height()
#            if w < h:
#                printer.setOrientation(QtGui.QPrinter.Portrait)
#            else:
#                size.transpose()
#                printer.setOrientation(QtGui.QPrinter.Landscape)
#            printer.setPaperSize(size, 0)
        printer.setOrientation(QtGui.QPrinter.Landscape)
#        printer.setPaperSize(QSizeF(self.graphicsView.sceneRect().x(),self.graphicsView.sceneRect().y()),0)
#        printer.setPaperSize(QSizeF(self.graphicsView.viewport().size()),0)
        printer.setFullPage(True)
#        printer.setPageMargins(0,0,0,0,0)
        printer.setCreator('samson')
        printer.setDocName(docName)
        printer.setFontEmbeddingEnabled(True)
#
#        #renderer = QtSvg.QSvgRenderer()
##        if printer.orientation() == QtGui.QPrinter.Landscape:
##            painterRect = painter.viewport()
##            painter.translate(0, painterRect.height())
##            painter.rotate(270)


#        viewportTransform = self.graphicsView.viewportTransform()
#        dx = viewportTransform.dx()
#        dy = viewportTransform.dy()
#        rect = self.graphicsView.viewport().rect()
#        #printer.setPaperSize(QSizeF(rect.width(), rect.height()), 0)
#
#        #painter.fillRect(self.graphicsView.getVisibleSceneRect(), self.graphicsView.backgroundBrush())

#        image = self.graphicsView.sceneToImage()
#
#
        painter = QtGui.QPainter(printer)
#
#        rect = painter.viewport()
#
#        size = image.size()
#
#        size.scale(rect.size(), Qt.KeepAspectRatio)
#
#        painter.setViewport(rect.x(),  rect.y(), size.width(), size.height())
#
#        painter.setWindow (image.rect())
#
#        painter.drawImage(0, 0, image)



        viewport = self.graphicsView.viewport().rect()
        #self.graphicsView.render(painter, QRectF(0, printer.height() / 2, printer.width(), printer.height() / 2),viewport.adjusted(0, 0, 0, -viewport.height() / 2))



        #painter.setWindow(viewport.x(), viewport.y(), printer.width(), printer.height())
        #painter.begin(printer)
        self.graphicsView.render(painter, QRectF(0, printer.height() / 2, printer.width(), printer.height() / 2),viewport.adjusted(0, 0, 0, -viewport.height() / 2), Qt.KeepAspectRatio)
        painter.end()



#        painter = QtGui.QPainter(printer)
#
#        target = QRectF(100.0, 200.0, 800.0, 600.0)
#        source = QRectF(0.0, 0.0, 700.0, 400.0)
#
#
#        painter.drawImage(target, image, source)
##        self.graphicsView.render(painter)
#
#
##        painter.drawImage(self.graphicsView.getVisibleSceneRect(), image)
#        #painter.begin(printer)
#        #self.graphicsView.render(painter)
#        painter.end()
#
#
#
##        painter = QtGui.QPainter() # QtGui.QPainter(printer)
##        painter.setRenderHint(QtGui.QPainter.Antialiasing)
##        painter.drawRect(self.graphicsView.viewport().rect())
##
###        dx = svgItem.x()
###        dy = svgItem.y()
###        rect = svgItem.boundingRect()  width()
###        painter.setWindow(rect.x()-dx, rect.y()-dy, rect.width()-dx, rect.height()-dy)
###        svgItem.paint(painter, QtGui.QStyleOptionGraphicsItem())
##
##
##        #painter.setWindow(rect.x()-dx, rect.y()-dy, rect.width()-dx, rect.height()-dy)
##
##
##        painter.begin(printer)
##        #scene = self.graphicsView.scene()
##        #scene.render(painter)
##        self.graphicsView.render(painter) # sceneRect
##        painter.end()





#    @pyqtSignature('')
#    def on_btnPrint_clicked(self):
#        printer = QtGui.QPrinter()
#        printer.setOrientation(QtGui.QPrinter.Portrait)
#        dialog = QtGui.QPrintDialog(printer, self)
#        if dialog.exec_():
#            painter = QtGui.QPainter(printer)
#            self.scrollArea.widget().render(painter)
#            painter.end()


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Close:
            self.reject()
        elif buttonCode == QtGui.QDialogButtonBox.Retry:
            self.accept()
        elif buttonCode == QtGui.QDialogButtonBox.Save:
            QtGui.qApp.call(self, self.saveAsFile)
        else:
            pass


    def keyPressEvent(self, event):
        key = event.text().at(0)
        if key == QChar(0x77) or key == QChar(0x446): # w|ц
            self.svgItem.setY(self.svgItem.y()-1)
            QtGui.qApp.preferences.appPrefs[self.docName+'_svgY'] = QVariant(self.svgItem.y())
            self.label.setText(u'Сдвиг x: %i, y %i'%(self.svgItem.x(), self.svgItem.y()))
        elif key == QChar(0x73) or key == QChar(0x44b): # s|ы
            self.svgItem.setY(self.svgItem.y()+1)
            QtGui.qApp.preferences.appPrefs[self.docName+'_svgY'] = QVariant(self.svgItem.y())
            self.label.setText(u'Сдвиг x: %i, y %i'%(self.svgItem.x(), self.svgItem.y()))
        elif key == QChar(0x61) or key == QChar(0x444): # a|ф
            self.svgItem.setX(self.svgItem.x()-1)
            QtGui.qApp.preferences.appPrefs[self.docName+'_svgX'] = QVariant(self.svgItem.x())
            self.label.setText(u'Сдвиг x: %i, y %i'%(self.svgItem.x(), self.svgItem.y()))
        elif key == QChar(0x64) or key == QChar(0x432): # d|в
            self.svgItem.setX(self.svgItem.x()+1)
            QtGui.qApp.preferences.appPrefs[self.docName+'_svgX'] = QVariant(self.svgItem.x())
            self.label.setText(u'Сдвиг x: %i, y %i'%(self.svgItem.x(), self.svgItem.y()))
        self.parent().keyPressEvent(event)

