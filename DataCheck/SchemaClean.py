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
from PyQt4.QtCore import pyqtSignature

from library.DialogBase import CDialogBase
from library.Utils      import anyToUnicode, forceString

from DataCheck.Ui_SchemaClean import Ui_SchemaCleanDialog


def DoSchemaClean():
    dlg = CSchemaCleanDialog()
    dlg.exec_()


class CSchemaCleanDialog(CDialogBase,  Ui_SchemaCleanDialog):
    def __init__(self,  parent=None):
        CDialogBase.__init__(self, parent)
        self.parent = parent #wtf? скрывать Qt-шный parent - это плохая затея
        self.setupUi(self)
        self.showLog = True
        self.progressBar.setFormat('%p%')
        self.progressBar.setValue(0)
        self.db = QtGui.qApp.db

        tables = self.getTableList(self.db)
        self.tblTables.setRowCount(len(tables))
        self.tblTables.setColumnCount(2)
        self.tblTables.setHorizontalHeaderLabels([u'Имя таблицы', u' Описание'])
        self.tblTables.verticalHeader().hide()
        self.tblTables.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblTables.horizontalHeader().setStretchLastSection(True)

        for (name,  desc) in tables:
            n = tables.index((name,  desc))
            self.tblTables.setItem(n, 0, QtGui.QTableWidgetItem(name))
            self.tblTables.setItem(n, 1, QtGui.QTableWidgetItem(desc))


    def getSelectedTables(self):
        result = []

        if self.chkSelectAll.isChecked():
            for x in range(0, self.tblTables.rowCount()):
                result.append(forceString(self.tblTables.item(x, 0).text()))
        else:
            for x in self.tblTables.selectedIndexes():
                tableName = forceString(self.tblTables.item(x.row(), 0).text())
                if not tableName in result:
                    result.append(forceString(self.tblTables.item(x.row(), 0).text()))

        return result


    def log(self, str,  forceLog = False):
        if self.showLog or forceLog:
            self.logBrowser.append(str)
            self.logBrowser.update()


    def cleanTables(self,  db):
        #self.progressBar.setText(u'Получение списка таблиц')
        QtGui.qApp.processEvents()
        tableList = self.getSelectedTables()
        self.progressBar.setMaximum(len(tableList))
        self.progressBar.setValue(0)
        list = []

        for table in tableList:
            self.log(u' *  Проверка таблицы "%s"' % table)
            QtGui.qApp.processEvents()
            columnList = self.getColumnList(db,  table)

            if 'deleted' in columnList:
                self.log(u' +  Найдено поле  "deleted", будем чистить')
                list.append(u' LOCK TABLE `%s`.`%s` WRITE;' % \
                                        (db.db.databaseName(),  table))
                list.append(u' DELETE FROM `%s`.`%s` WHERE deleted != 0;' % \
                                        (db.db.databaseName(),  table))
                list.append(u'UNLOCK TABLES;')
            else:
                self.log(u' +  Поле  "deleted" не обнаружено')

            self.progressBar.step()

        if len(list)>0:
            self.progressBar.setText(u'Запись изменений в БД')
            self.progressBar.setMaximum(len(list))
            self.progressBar.setValue(0)

            for stmt in list:
                db.query(stmt)
                QtGui.qApp.processEvents()
                self.progressBar.step()

        self.btnClean.setEnabled(False)


    def getColumnList(self,  db,  tableName):
        stmt = """
            SHOW FULL COLUMNS
            FROM `%s`.`%s`;
        """ % (db.db.databaseName(),  tableName)

        query = db.query(stmt)
        columnList = []

        while (query.next()):
            record = query.record()
            columnList.append(forceString(record.value("Field")))
        return columnList


    def getTableList(self,  db):
        stmt = """SELECT table_name, table_comment
            FROM information_schema.tables
            WHERE table_schema = '%s' AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """ % db.db.databaseName()

        query = db.query(stmt)
        tableList = []

        while (query.next()):
            record = query.record()
            tableList.append((
                             forceString(record.value('table_name')),
                             forceString(record.value('table_comment'))
            ))

        return tableList


    def schemaClean(self):
        try:
            self.logBrowser.clear()
            self.cleanTables(self.db)
            self.progressBar.setText(u'Готово')
        except IOError, e:
            QtGui.qApp.logCurrentException()
            msg=''
            if hasattr(e, 'filename'):
                msg = u'%s:\n[Errno %s] %s' % (e.filename, e.errno, anyToUnicode(e.strerror))
            else:
                msg = u'[Errno %s] %s' % (e.errno, anyToUnicode(e.strerror))
            QtGui.QMessageBox.critical (self.parent,
                u'Произошла ошибка ввода-вывода', unicode(msg), QtGui.QMessageBox.Close)
            return False
        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical (self.parent,
                u'Произошла ошибка', unicode(e), QtGui.QMessageBox.Close)
            return False

        return True


    @pyqtSignature('')
    def on_btnClose_clicked(self):
        self.close()


    @pyqtSignature('')
    def on_btnClean_clicked(self):
        self.schemaClean()


    @pyqtSignature('bool')
    def on_chkSelectAll_toggled(self, checked):
        self.tblTables.setEnabled(not checked)
