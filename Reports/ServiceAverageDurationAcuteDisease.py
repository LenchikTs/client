# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################


from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignature, SIGNAL, QAbstractTableModel, QDate, QDateTime, QVariant

from library.DialogBase   import CConstructHelperMixin #, CDialogBase
from library.TableModel   import CTextCol
from library.InDocTable   import CBoolInDocTableCol
from library.Utils        import forceDate, forceInt, forceString, getPref, getPrefDate, getPrefInt, getPrefString, setPref, toVariant

from Reports.ReportBase   import CReportBase, createTable
from Reports.ReportView   import CReportViewDialog

from Ui_ADAcuteDiseaseEditor import Ui_ADAcuteDiseaseEditor
from Ui_ADAcuteDiseaseSetup import Ui_ADAcuteDiseaseSetup


class CADAcuteDiseaseSetup(QtGui.QDialog, Ui_ADAcuteDiseaseSetup):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        MKBFilter = params.get('MKBFilter', 0)
        self.cmbMKBFilter.setCurrentIndex(MKBFilter if MKBFilter else 0)
        self.edtMKBFrom.setText(params.get('MKBFrom', 'A00'))
        self.edtMKBTo.setText(params.get('MKBTo',   'Z99.9'))


    def params(self):
        result = {}
        result['begDate'] = forceDate(self.edtBegDate.date())
        result['endDate'] = forceDate(self.edtEndDate.date())
        result['MKBFilter'] = forceInt(self.cmbMKBFilter.currentIndex())
        result['MKBFrom']   = unicode(self.edtMKBFrom.text())
        result['MKBTo']     = unicode(self.edtMKBTo.text())
        return result


    @pyqtSignature('int')
    def on_cmbMKBFilter_currentIndexChanged(self, index):
        mode = bool(index)
        for widget in (self.edtMKBFrom, self.edtMKBTo):
            widget.setEnabled(mode)


class CAverageDurationAcuteDiseaseBase(object):
    def __init__(self, parent=None):
        self.__parent = parent
        self.__title  = ''
        self.__preferences = ''


    def exec_(self):
        QtGui.qApp.call(self.__parent, self.reportLoop)


    def getMinimumDateLUD(self):
        db = QtGui.qApp.db
        tableDiagnosis = db.table('Diagnosis')
        tablerbDiseaseCharacter = db.table('rbDiseaseCharacter')
        tableMKB = db.table('MKB')
        cols = ['MIN(Diagnosis.setDate) AS minSetDate']

        cond = [tableDiagnosis['deleted'].eq(0),
                    tablerbDiseaseCharacter['replaceInDiagnosis'].eq(1),
                    tableDiagnosis['setDate'].isNotNull(),
                    tableDiagnosis['endDate'].isNotNull()
                    ]
        queryTable = tableDiagnosis.innerJoin(tablerbDiseaseCharacter, tableDiagnosis['character_id'].eq(tablerbDiseaseCharacter['id']))
        queryTable = queryTable.innerJoin(tableMKB, tableMKB['DiagID'].eq(tableDiagnosis['MKB']))
        record = db.getRecordEx(queryTable, cols, cond)
        return forceDate(record.value('setDate')) if record else QDate.currentDate()


    def reportLoop(self):
        params = self.getDefaultParams()
        while True:
            setupDialog = CADAcuteDiseaseSetup(self.__parent)
            setupDialog.setParams(params)
            if not setupDialog.exec_():
                break
            params = setupDialog.params()
            self.saveDefaultParams(params)
            dialog = CAverageDurationAcuteDiseaseDialog(self.__parent)
            dialog.params = params
            dialog.loadDataItems(dialog.params)
            try:
                if dialog.exec_():
                    pass
            finally:
                done = dialog.retry
                dialog.deleteLater()
            if not done:
                break


    def getDefaultParams(self):
        result = {}
        prefs = getPref(QtGui.qApp.preferences.reportPrefs, self.__preferences, {})
        result['begDate']     = getPrefDate(prefs, 'begDate', self.getMinimumDateLUD())
        result['endDate']     = getPrefDate(prefs, 'endDate', QDate.currentDate())
        result['MKBFilter']   = getPrefInt(prefs, 'MKBFilter', 0) # 0-нет фильтра, 1-интервал, 2-нет кода
        result['MKBFrom']     = getPrefString(prefs, 'MKBFrom', 'A00')
        result['MKBTo']       = getPrefString(prefs, 'MKBTo', 'Z99.9')
        return result


    def saveDefaultParams(self, params):
        prefs = {}
        for param, value in params.iteritems():
            setPref(prefs, param, value)
        setPref(QtGui.qApp.preferences.reportPrefs, self.__preferences, prefs)


class CAverageDurationAcuteDiseaseDialog(QtGui.QDialog, CConstructHelperMixin,  Ui_ADAcuteDiseaseEditor):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.addModels('AcuteDisease',   CAcuteDiseaseModel(self))
        self.setupUi(self)
        self.setModels(self.tblAcuteDisease, self.modelAcuteDisease, self.selectionModelAcuteDisease)
        self.params = {}
        self.retry = False


    def loadDataItems(self, params):
        self.modelAcuteDisease.loadItems(params)


    @pyqtSignature('')
    def on_btnSave_clicked(self):
        self.modelAcuteDisease.saveItems()
        self.retry = False
        self.close()


    @pyqtSignature('')
    def on_btnPrint_clicked(self):
        self.retry = False
        model = self.modelAcuteDisease
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Расчет средней длительности острых заболеваний\n')
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(u'\nОтчёт составлен: ' + forceString(QDateTime.currentDateTime()))
        cursor.insertBlock()
        colWidths  = [ self.tblAcuteDisease.columnWidth(i) for i in xrange(model.columnCount()-1) ]
        colWidths.insert(0,10)
        totalWidth = sum(colWidths)
        tableColumns = []
        iColNumber = False
        for iCol, colWidth in enumerate(colWidths):
            widthInPercents = str(max(1, colWidth*90/totalWidth))+'%'
            if iColNumber == False:
                tableColumns.append((widthInPercents, [u'№'], CReportBase.AlignRight))
                iColNumber = True
            tableColumns.append((widthInPercents, [forceString(model.column[iCol])], CReportBase.AlignLeft))
        table = createTable(cursor, tableColumns)
        for iModelRow in xrange(model.rowCount()):
            iTableRow = table.addRow()
            table.setText(iTableRow, 0, iModelRow+1)
            for iModelCol in xrange(model.columnCount()):
                index = model.createIndex(iModelRow, iModelCol)
                text = forceString(model.data(index))
                table.setText(iTableRow, iModelCol+1, text)
        html = doc.toHtml('utf-8')
        view = CReportViewDialog(self)
        view.setText(html)
        view.exec_()


    @pyqtSignature('')
    def on_btnClose_clicked(self):
        self.retry = False
        self.close()


    @pyqtSignature('')
    def on_btnRetry_clicked(self):
        self.retry = True
        self.close()


class CAcuteDiseaseModel(QAbstractTableModel):
    column = [u'Включить',u'Шифр МКБ', u'Число случаев в ЛУД', u'Общая длительность', u'Текущая средняя длительность', u'Расчетная средняя длительность']

    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self._items = []
        self.cols()


    def items(self):
        return  self._items


    def cols(self):
        self._cols = [CBoolInDocTableCol( u'Включить',  'include', 10),
                            CTextCol(u'Шифр МКБ', ['MKB'], 20, 'l'),
                            CTextCol(u'Число случаев в ЛУД',  ['countAcuteDisease'],  20, 'l'),
                            CTextCol(u'Общая длительность', ['sumDuration'],  20, 'l'),
                            CTextCol(u'Текущая средняя длительность', [ 'duration'],  20, 'l'),
                            CTextCol(u'Расчетная средняя длительность', ['temperature'], 20, 'l')
                            ]
        return self._cols


    def columnCount(self, index = None):
        return len(self._cols)


    def rowCount(self, index = None):
        return len(self._items)


    def flags(self, index=None):
        column = index.column()
        result = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if column == 0:
            result |= Qt.ItemIsUserCheckable
        return result


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.column[section])
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            if column != 0:
                item = self._items[row]
                return toVariant(item[column])
        elif role == Qt.EditRole:
            if column != 0:
                item = self._items[row]
                return toVariant(item[column])
        elif role == Qt.CheckStateRole:
            if column == 0:
                return QVariant(Qt.Checked if self._items[row][column] else Qt.Unchecked)
        return QVariant()


    def setData(self, index, value, role=Qt.EditRole):
        column = index.column()
        row = index.row()
        if role == Qt.CheckStateRole:
            if column == 0:
                self._items[row][column] = forceInt(value) == Qt.Checked
                self.emitCellChanged(row, column)
        return False


    def emitCellChanged(self, row, column):
        index = self.index(row, column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)


    def emitRowChanged(self, row):
        self.emitRowsChanged(row, row)


    def emitRowsChanged(self, begRow, endRow):
        index1 = self.index(begRow, 0)
        index2 = self.index(endRow, self.columnCount())
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)


    def emitColumnChanged(self, column):
        index1 = self.index(0, column)
        index2 = self.index(self.rowCount(), column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)


    def emitAllChanged(self):
        index1 = self.index(0, 0)
        index2 = self.index(self.rowCount(), self.columnCount())
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)


    def createEditor(self, column, parent):
        return self._cols[column].createEditor(parent)


    def setEditorData(self, column, editor, value, record):
        return self._cols[column].setEditorData(editor, value, record)


    def getEditorData(self, column, editor):
        return self._cols[column].getEditorData(editor)


    def afterUpdateEditorGeometry(self, editor, index):
        pass


    def loadItems(self, params):
        self._items = []
        begDate = params.get('begDate', QDate.currentDate())
        endDate = params.get('endDate', QDate.currentDate())
        MKBFilter = params.get('MKBFilter', 0)
        MKBFrom = params.get('MKBFrom', 'A00')
        MKBTo = params.get('MKBTo',   'Z99.9')
        db = QtGui.qApp.db
        tableDiagnosis = db.table('Diagnosis')
        tablerbDiseaseCharacter = db.table('rbDiseaseCharacter')
        tableMKB = db.table('MKB')
        cols = [tableDiagnosis['MKB'],
                    tableMKB['duration'],
                    tableDiagnosis['setDate'],
                    tableDiagnosis['endDate']
                   ]
        cols.append('COUNT(*) AS countAcuteDisease')
        cond = [tableDiagnosis['deleted'].eq(0),
                    tablerbDiseaseCharacter['replaceInDiagnosis'].eq(1),
                    tableDiagnosis['setDate'].isNotNull(),
                    tableDiagnosis['setDate'].le(endDate),
                    tableDiagnosis['endDate'].isNotNull(),
                    tableDiagnosis['endDate'].ge(begDate)
                    ]
        if MKBFilter:
            cond.append('Diagnosis.MKB >= \'%s\' AND Diagnosis.MKB <= \'%s\''%(MKBFrom, MKBTo))
        queryTable = tableDiagnosis.innerJoin(tablerbDiseaseCharacter, tableDiagnosis['character_id'].eq(tablerbDiseaseCharacter['id']))
        queryTable = queryTable.innerJoin(tableMKB, tableMKB['DiagID'].eq(tableDiagnosis['MKB']))
        records = db.getRecordListGroupBy(queryTable, cols, cond, u'Diagnosis.MKB,Diagnosis.setDate,Diagnosis.endDate',u'Diagnosis.MKB')
        mkbList = {}
        for record in records:
            MKB = forceString(record.value('MKB'))
            reportList = mkbList.get(MKB, [0, 0, 0, 0])
            setDate = forceDate(record.value('setDate'))
            endDate = forceDate(record.value('endDate'))
            countDays = setDate.daysTo(endDate) + 1
            countAcuteDisease = forceInt(record.value('countAcuteDisease'))
            reportList[0] += countAcuteDisease
            reportList[1] += countDays * countAcuteDisease
            reportList[2] = forceInt(record.value('duration'))
            reportList[3] += (countDays/countAcuteDisease) if countAcuteDisease else 0
            mkbList[MKB] = reportList
        mkbKeys = mkbList.keys()
        mkbKeys.sort()
        for mkbKey in mkbKeys:
            reportListVal = mkbList.get(mkbKey, [0, 0, 0, 0])
            item = [False,
                         mkbKey,
                         reportListVal[0],
                         reportListVal[1],
                         reportListVal[2],
                        (reportListVal[1]/reportListVal[0]) if reportListVal[0] else 0
                        ]
            self._items.append(item)
        self.reset()


    def saveItems(self):
        if self._items is not None:
            db = QtGui.qApp.db
            tableMKB = db.table('MKB')
            for item in self._items:
                if item[0]:
                    MKB = item[1]
                    if MKB:
                        newDuration = item[5]
                        record = db.getRecordEx(tableMKB, '*', [tableMKB['DiagID'].eq(MKB)])
                        if record:
                            record.setValue('duration', toVariant(newDuration))
                            db.updateRecord(tableMKB, record)

