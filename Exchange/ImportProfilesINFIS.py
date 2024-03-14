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
from PyQt4.QtCore import QDir, pyqtSignature

from library.dbfpy.dbf import Dbf
from library.DbfViewDialog import CDbfViewDialog
from library.Utils import forceInt, forceString, forceStringEx, toVariant


from Exchange.Cimport import CDBFimport

from Exchange.Utils import getId, tbl

from Exchange.Ui_ImportProfilesINFIS import Ui_Dialog

def ImportProfilesINFIS(widget):
    dlg=CImportProfilesINFIS(widget)
    dlg.edtFileName.setText(forceString(QtGui.qApp.preferences.appPrefs.get('ImportProfilesINFISFileName', '')))
    dlg.edtRbNetFileName.setText(forceString(QtGui.qApp.preferences.appPrefs.get('ImportProfilesINFISRbNetFileName', '')))
    dlg.edtRbTypeFileName.setText(forceString(QtGui.qApp.preferences.appPrefs.get('ImportProfilesINFISRbTypeFileName', '')))
    dlg.exec_()
    QtGui.qApp.preferences.appPrefs['ImportProfilesINFISFileName'] = \
        toVariant(dlg.edtFileName.text())
    QtGui.qApp.preferences.appPrefs['ImportProfilesINFISRbNetFileName'] = \
        toVariant(dlg.edtRbNetFileName.text())
    QtGui.qApp.preferences.appPrefs['ImportProfilesINFISRbTypeFileName'] = \
        toVariant(dlg.edtRbTypeFileName.text())


class CImportProfilesINFIS(QtGui.QDialog, Ui_Dialog, CDBFimport):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        CDBFimport.__init__(self, self.logBrowser)
        self.progressBar.setFormat('%v')
        self.tblService=tbl('rbService')
        self.n = 0
        self.nAdded = 0
        self.nFound = 0
        self.filterGTS = None
        self.filterNet = None
        self.filterType = None
        self.mapNet = {}
        self.mapType = {}


    def exec_(self):
        self.updateRbNetButtons()
        self.updateRbTypeButtons()

        if not self.edtRbNetFileName.text().isEmpty():
            self.loadNetFilter()

        if not self.edtRbTypeFileName.text().isEmpty():
            self.loadTypeFilter()

        QtGui.QDialog.exec_(self)


    def updateRbNetButtons(self):
        self.btnLoadRbNet.setEnabled(not self.edtRbNetFileName.text().isEmpty())
        self.btnViewRbNet.setEnabled(not self.edtRbNetFileName.text().isEmpty())


    def updateRbTypeButtons(self):
        self.btnLoadRbType.setEnabled(not self.edtRbTypeFileName.text().isEmpty())
        self.btnViewRbType.setEnabled(not self.edtRbTypeFileName.text().isEmpty())


    def startImport(self):
        self.progressBar.setFormat('%p%')

        n=0
        self.nAdded=0
        self.nFound=0

        self.filterGTS = forceStringEx(self.cmbGTS.currentText()) if self.chkGTS.isChecked() else None

        self.filterNet = self.mapNet.get(forceString(self.cmbNet.currentText())) \
            if self.chkNet.isChecked() else None

        self.filterType = self.mapType.get(forceString(self.cmbType.currentText())) \
            if self.chkType.isChecked() else None

        dbfFileName = forceStringEx(self.edtFileName.text())
        dbfProfiles = Dbf(dbfFileName, readOnly=True, encoding='cp866')

        dbfLen=len(dbfProfiles)
        self.progressBar.setMaximum(dbfLen-1)
        self.labelNum.setText(u'всего записей в источнике: '+str(dbfLen))

        for row in dbfProfiles:
            QtGui.qApp.processEvents()
            if self.abort:
                break
            self.n=n+1
            self.processRow(row)
            n+=1
            self.progressBar.setValue(n)
            statusText = u'добавлено %d, найдено %d' % (self.nAdded, self.nFound)
            self.statusLabel.setText(statusText)

        self.log.append(u'добавлено %d, найдено %d' % (self.nAdded, self.nFound))
        self.log.append(u'готово')
#        self.progressBar.setValue(n-1)


    def processRow(self, row):
        infisCode = forceString(row['CODE'])

        if self.filterNet and (forceString(row['HSNET']) != self.filterNet):
            return

        if self.filterGTS and (forceString(row['GTS']) != self.filterGTS):
            return

        if self.filterType and (forceString(row['TYPE']) != self.filterType):
            return

        serviceId = None
        record = self.db.getRecordEx(self.tblService, '*', self.tblService['infis'].eq(infisCode))
        self.nFound += 1

        if record:
            serviceId=forceInt(record.value('id'))
            self.log.append(u'код: "%s" -- найдена совпадающая запись id="%d"' % (infisCode,  serviceId))
        else:
            self.nAdded += 1
            name = forceString(row['NAME'])
            rbServiceFields=[
                ('code', infisCode), ('name', name),
                ('eisLegacy', 1), ('infis', infisCode)]
            serviceId=getId(self.tblService, rbServiceFields)
            self.log.append(u'код: "%s" -- добавлена запись id="%d"' % (infisCode,  serviceId))


    def err2log(self, e):
        if self.logBrowser:
            self.logBrowser.append(u'запись '+str(self.n)+': '+e)


    def loadNetFilter(self):
        try:
            dbfFileName = forceString(self.edtRbNetFileName.text())
            dbfNet = Dbf(dbfFileName, readOnly=True, encoding='cp866')
            self.log.append(u'всего записей в справочнике сетей: '+str(len(dbfNet)))
            self.cmbNet.clear()
            self.mapNet = {}

            for row in dbfNet:
                self.cmbNet.addItem(forceString(row['NAME']))
                self.mapNet[row['NAME']] = forceString(row['CODE'])

            dbfNet.close()
        except:
            self.cmbNet.clear()
            self.mapNet = {}
            self.chkNet.setEnabled(False)
            return

        self.chkNet.setEnabled(True)


    def loadTypeFilter(self):
        try:
            dbfFileName = forceString(self.edtRbTypeFileName.text())
            dbfType = Dbf(dbfFileName, readOnly=True, encoding='cp866')
            self.log.append(u'всего записей в справочнике типов: '+str(len(dbfType)))
            self.cmbType.clear()
            self.mapType = {}

            for row in dbfType:
                self.cmbType.addItem(forceString(row['NAME']))
                self.mapType[row['NAME']] = forceString(row['CODE'])

            dbfType.close()
        except:
            self.cmbType.clear()
            self.mapType = {}
            self.chkType.setEnabled(False)
            return

        self.chkType.setEnabled(True)


    @pyqtSignature('bool')
    def on_btnLoadGTS_clicked(self, val):
        try:
            existsGts = []
            dbfFileName = forceStringEx(self.edtFileName.text())
            dbfProfiles = Dbf(dbfFileName, readOnly=True, encoding='cp866')
            self.cmbGTS.clear()
            for data in dbfProfiles:
                gts = unicode(data['GTS'])
                if gts not in existsGts:
                    self.cmbGTS.addItem(gts)
                    existsGts.append(gts)
        except:
            pass

    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
        fileName = QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите файл с данными', self.edtFileName.text(), u'Файлы DBF (*.dbf)')
        if fileName != '':
            self.edtFileName.setText(QDir.toNativeSeparators(fileName))
            self.btnImport.setEnabled(True)
            dbfFileName = forceStringEx(self.edtFileName.text())
            dbfProfiles = Dbf(dbfFileName, readOnly=True, encoding='cp866')
            self.labelNum.setText(u'всего записей в источнике: '+str(len(dbfProfiles)))


    @pyqtSignature('')
    def on_btnSelectFileRbNet_clicked(self):
        fileName = QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите файл с данными', self.edtRbNetFileName.text(), u'Файлы DBF (*.dbf)')
        if fileName != '':
            self.edtRbNetFileName.setText(QDir.toNativeSeparators(fileName))

        self.updateRbNetButtons()


    @pyqtSignature('')
    def on_btnSelectFileRbType_clicked(self):
        fileName = QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите файл с данными', self.edtRbTypeFileName.text(), u'Файлы DBF (*.dbf)')
        if fileName != '':
            self.edtRbTypeFileName.setText(QDir.toNativeSeparators(fileName))

        self.updateRbTypeButtons()


    @pyqtSignature('')
    def on_btnViewRbNet_clicked(self):
        fname=unicode(forceStringEx(self.edtRbNetFileName.text()))
        if fname:
            CDbfViewDialog(self, fileName=fname).exec_()


    @pyqtSignature('')
    def on_btnLoadRbNet_clicked(self):
        self.loadNetFilter()


    @pyqtSignature('')
    def on_btnLoadRbType_clicked(self):
        self.loadTypeFilter()


    @pyqtSignature('')
    def on_btnViewRbType_clicked(self):
        fname=unicode(forceStringEx(self.edtRbTypeFileName.text()))
        if fname:
            CDbfViewDialog(self, fileName=fname).exec_()


    @pyqtSignature('QString')
    def on_edtRbTypeFileName_textChanged(self, text):
        self.updateRbTypeButtons()


    @pyqtSignature('QString')
    def on_edtRbNetFileName_textChanged(self, text):
        self.updateRbNetButtons()
