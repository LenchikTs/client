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

import traceback

from PyQt4 import QtGui
from PyQt4.QtCore import QDate, pyqtSignal, Qt, pyqtSignature, QTime, SIGNAL, QDateTime, QAbstractTableModel, QVariant

from Reports.ReportBase import CReportBase, createTable
from Reports.ReportView import CReportViewDialog
from Ui_SimpleProgress import Ui_SimpleProgress
from Ui_ImportCovidDialog import Ui_ImportCovidDialog
from library.DialogBase import CDialogBase
from library.TableModel import CCol
from library.Utils import forceString, parseSex, forceRef, formatDate, unformatSNILS, forceDate


def unFmtDate(date):
    if date and date != '01.01.1900':
        return QDate().fromString(date, 'dd.MM.yyyy')
    return QDate()


class CCovidImportDialog(QtGui.QDialog, Ui_SimpleProgress):
    startWork = pyqtSignal()

    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.startWork.connect(self.work, Qt.QueuedConnection)
        self.working = False
        self.inTransaction = False
        self.canceled = False
        self.mapColumnLetterToFieldName = {'A': ('createDate', unFmtDate),
                                           'B': ('identifier', forceString),
                                           'C': ('modifyDate', unFmtDate),
                                           'D': ('SNILS', unformatSNILS),
                                           'E': ('fullName', forceString),
                                           'F': ('sex', parseSex),
                                           'G': ('birthDate', unFmtDate),
                                           'H': ('covidMKB', forceString),
                                           'I': ('diagnosDate', unFmtDate),
                                           'J': ('comlicationMKB', forceString),
                                           'K': ('region', forceString),
                                           'L': ('organisation', forceString),
                                           'M': ('medicalAidType', forceString),
                                           'N': ('resultDate', unFmtDate),
                                           'O': ('resultTitle', forceString),
                                           'P': ('severity', forceString),
                                           'Q': ('deathDiagnos', forceString),
                                           'R': ('tfomsLastName', forceString),
                                           'S': ('tfomsFirstName', forceString),
                                           'T': ('tfomsPatrName', forceString),
                                           'U': ('tfomsBirthDate', unFmtDate),
                                           'V': ('tfomsSNILS', unformatSNILS),
                                           'W': ('tfomsSmoCode', forceString),
                                           'X': ('tfomsMoCode', forceString)}
        self.time = QTime()
        self.totalTime = QTime()
        self.startPos = 0
        self.oldSpeed = 0

    def exec_(self):
        self.startWork.emit()
        return QtGui.QDialog.exec_(self)

    def work(self):
        self.inTransaction = False
        self.canceled = False
        self.working = True

        try:
            from openpyxl.reader.excel import load_workbook
            covidImportFileName = forceString(self.parent().edtCovidReestrFileName.text())
            self.progressInitialize(u'Чтение данных из файла', 7)
            db = QtGui.qApp.db
            tableListCovid = db.table('soc_listCovid')
            inserted = 0
            wb = load_workbook(filename=covidImportFileName)
            sheet = wb.worksheets[0]
            self.progressStep()
            QtGui.qApp.db.transaction()
            db.query('delete from soc_listCovid')
            for row in sheet.rows:
                self.progressStep()
                if row[0].row < 6:
                    continue
                record = tableListCovid.newRecord()

                for cell in row:
                    colName, func = self.mapColumnLetterToFieldName.get(cell.column_letter, (None, forceRef))
                    if colName:
                        record.setValue(colName, func(cell.value))
                db.insertRecord(tableListCovid, record)
                inserted += 1
                self.progressStep()
            wb.close()
            self.logInfo(u'Данные Ковидного регистра загружены: %s' % inserted)
            self.progressStep()
            self.logInfo(u'Поиск соответствий в БД...')
            self.progressStep()
            stmt = u"""UPDATE soc_listCovid s
                       LEFT JOIN Client c ON CONCAT_WS(' ', c.lastName, c.firstName, c.patrName) = s.fullName AND c.birthDate = s.birthDate AND c.deleted = 0
                       SET s.client_id = c.id"""
            query = db.query(stmt)
            self.logInfo(u'Соответствий найдено: %s' % (query.numRowsAffected()))
            self.progressStep()

            self.logInfo(u'Обновление найденных идентификаторов...')
            stmt = u"""
            UPDATE soc_listCovid s
              INNER JOIN Client c on c.id = s.client_id
              LEFT JOIN rbAccountingSystem `as` ON `as`.code = 'ReestrCOVID'
              LEFT JOIN ClientIdentification ci ON  ci.accountingSystem_id = `as`.id AND ci.client_id = c.id AND ci.deleted = 0
              SET ci.identifier = s.identifier, ci.checkDate = IFNULL(s.modifyDate, s.createDate), ci.modifyDatetime = NOW()"""
            query = db.query(stmt)
            self.logInfo(u'Идентификаторов обновлено: %s' % (query.numRowsAffected()))
            self.progressStep()

            self.logInfo(u'Добавление идентификаторов пациентам...')
            stmt = u"""insert INTO ClientIdentification (createDatetime, modifyDatetime, deleted, client_id,
                accountingSystem_id, identifier, checkDate)
            SELECT NOW(), NOW(), 0, c.id, `as`.id, s.identifier, IFNULL(s.modifyDate, s.createDate)
            FROM soc_listCovid s
              INNER JOIN Client c on c.id = s.client_id
              LEFT JOIN rbAccountingSystem `as` ON `as`.code = 'ReestrCOVID'
            WHERE NOT EXISTS(SELECT NULL FROM ClientIdentification ci WHERE ci.accountingSystem_id = `as`.id
                AND ci.client_id = c.id AND ci.deleted = 0)"""
            query = db.query(stmt)
            self.logInfo(u'Идентификаторов добавлено: %s' % (query.numRowsAffected()))
            self.progressStep()

            if self.canceled:
                QtGui.qApp.db.rollback()
            else:
                QtGui.qApp.db.commit()
            if not self.canceled:
                self.progressDone(u'Импорт завершен')
                self.working = False
                self.btnCancel.setText(u'Закрыть')
                listWithoutId = []
                query = db.query(u"""SELECT fullName, birthDate, formatSNILS(SNILS) as SNILS
  FROM soc_listCovid
  WHERE client_id is NULL""")
                while query.next():
                    record = query.record()
                    listWithoutId.append((forceString(record.value('fullName')),
                                          forceDate(record.value('birthDate')),
                                          forceString(record.value('SNILS'))))
                if listWithoutId:
                    dial = CImportCovidDialog(self, listWithoutId, title=u"Внимание!")
                    dial.exec_()
        except Exception as e:
            self.logError(unicode(e) or repr(e))
            traceback.print_exc()
            if self.inTransaction:
                QtGui.qApp.db.rollback()
            self.working = False
            self.btnCancel.setText(u'Закрыть')

    def progressInitialize(self, caption, maxCount=1):
        self.lblProgress.setText(caption)
        self.prbProgress.setMaximum(maxCount)
        self.prbProgress.setValue(0)
        self.lblElapsed.setVisible(True)
        self.lblElapsed.setText(u'Текущая операция: ??? зап/с, окончание в ??:??:??')
        self.time = QTime()
        self.time.start()
        self.totalTime = QTime()
        self.totalTime.start()
        self.startPos = 0
        self.oldSpeed = 0

    def progressStep(self, minimumDifference=1):
        self.prbProgress.setValue(self.prbProgress.value() + 1)

        elapsed = self.time.elapsed()
        difference = self.prbProgress.value() - self.startPos
        if elapsed != 0 and (difference >= minimumDifference):
            self.startPos = self.prbProgress.value()
            self.oldSpeed = difference * 1000 / elapsed
            newSpeed = (self.oldSpeed + difference * 1000 / elapsed) / 2
            if newSpeed != 0:
                totalElapsed = self.totalTime.elapsed()
                partRemaining = float(self.prbProgress.maximum()) / self.prbProgress.value() - 1

                finishTime = QTime().currentTime().addSecs(totalElapsed * partRemaining / 1000)
                self.lblElapsed.setText(
                    u'Текущая операция: %01.f зап/с, окончание в %s' % (newSpeed, finishTime.toString('hh:mm:ss')))
                self.time.restart()

    def progressDone(self, caption):
        self.lblProgress.setText(caption)
        self.prbProgress.setMaximum(1)
        self.prbProgress.setValue(1)
        self.lblElapsed.setVisible(False)

    def logInfo(self, text):
        if isinstance(text, basestring):
            self.txtLog.append(text)
        else:
            for _str in text:
                self.txtLog.append(_str)
        self.txtLog.append('')

    def logError(self, text):
        if isinstance(text, basestring):
            self.txtLog.append(u'<b><font color=red>Ошибка:</font></b> %s' % text)
        else:
            self.txtLog.append(u'<b><font color=red>Ошибка:</font></b> %s' % text[0])
            for _str in text[1:]:
                self.txtLog.append(_str)
        self.txtLog.append('')

    def logRecord(self, record):
        for i in xrange(0, record.count()):
            self.txtLog.append("%s = %s" % (unicode(record.fieldName(i)), unicode(record.value(i).toString())))
        self.txtLog.append('')

    @pyqtSignature("")
    def on_btnCancel_clicked(self):
        if self.working:
            self.canceled = True
        else:
            self.accept()


class CImportCovidDialog(CDialogBase, Ui_ImportCovidDialog):
    def __init__(self, parent, items, title=None, message=None):
        CDialogBase.__init__(self,  parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.title = title
        self.message = message
        self.setWindowTitleEx(self.title)
        if self.message:
            self.label.setText(self.message)
        else:
            self.message = self.label.text()
        self.addModels('NoKeys', CNoKeysModel(self))
        self.tblAccountItems.setModel(self.modelNoKeys)
        self.tblAccountItems.setSortingEnabled(True)
        self.connect(self.tblAccountItems.horizontalHeader(), SIGNAL('sectionClicked(int)'), self.setSort)
        items.sort(key=lambda x: x[0])
        self.items = items
        self.modelNoKeys.loadItems(self.items)
        self.addObject('btnPrint', QtGui.QPushButton(u'Печать', self))
        self.buttonBox.addButton(self.btnPrint, QtGui.QDialogButtonBox.ActionRole)
        self.connect(self.btnPrint, SIGNAL('clicked()'), self.on_btnPrint_clicked)
        self.headerSortIndicator = None
        self.labelCount.setText(u'Всего персональных счетов: {0}'.format(len(self.items)))

    def setSort(self, col):
        model = self.tblAccountItems.model()
        header = self.tblAccountItems.horizontalHeader()
        header.setSortIndicatorShown(True)
        if self.headerSortIndicator == Qt.DescendingOrder:
            self.headerSortIndicator = Qt.AscendingOrder
        else:
            self.headerSortIndicator = Qt.DescendingOrder
        header.setSortIndicator(col, self.headerSortIndicator)
        items = model.items()
        items.sort(key=lambda x: x[col], reverse=self.headerSortIndicator == Qt.DescendingOrder)
        model.reset()

    @pyqtSignature('')
    def on_btnPrint_clicked(self):
        rowSize = 3
        report = CReportBase()
        params = report.getDefaultParams()
        report.saveDefaultParams(params)
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.message)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(u'отчёт составлен: ' + forceString(QDateTime().currentDateTime()))
        cursor.insertHtml('<br/><br/>')
        table = createTable(cursor, [
            ('50%', [u'ФИО'], CReportBase.AlignLeft),
            ('10%', [u'Дата рождения'], CReportBase.AlignCenter),
            ('10%', [u'СНИЛС'], CReportBase.AlignCenter),
        ]
                            )
        for item in self.modelNoKeys.items():
            row = table.addRow()
            for col in xrange(rowSize):
                if col == 1:
                    table.setText(row, col, formatDate(item[col]))
                else:
                    table.setText(row, col, item[col])
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertHtml('<br/><br/>')

        reportView = CReportViewDialog(self)
        reportView.setWindowTitle(self.title)
        reportView.setOrientation(QtGui.QPrinter.Portrait)
        reportView.setText(doc)
        reportView.exec_()


class CNoKeysModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self)
        self._items = []
        self.tableName = None
        self._parent = parent
        self.aligments = [CCol.alg['l'], CCol.alg['c'], CCol.alg['c']]

    def setTable(self, tableName):
        self.tableName = tableName

    def loadItems(self, items):
        self._items = items
        self.reset()

    def items(self):
        return self._items

    def columnCount(self, index=None, *args, **kwargs):
        return 3

    def rowCount(self, index=None, *args, **kwargs):
        return len(self._items)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant((u'ФИО', u'Дата рождения', u'СНИЛС')[section])
        return QVariant()

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            item = self._items[row]
            return QVariant(item[column])
        elif role == Qt.TextAlignmentRole:
            column = index.column()
            return self.aligments[column]
        return QVariant()
