#!/usr/bin/env python
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
from PyQt4.QtCore import Qt, QFile, QXmlStreamWriter, pyqtSignature, SIGNAL

from library.crbcombobox import CRBModelDataCache, CRBComboBox
from library.DialogBase import CConstructHelperMixin
from library.TableModel import CTableModel, CBoolCol, CEnumCol, CTextCol
from library.Utils      import addDots, anyToUnicode, exceptionToUnicode, forceBool, forceDate, forceInt, forceRef, forceString, toVariant


from Exchange.Utils import compressFileInRar
from RefBooks.Tables import rbCode,  rbName

from Exchange.Ui_ExportRbService_Wizard_1 import Ui_ExportRbService_Wizard_1
from Exchange.Ui_ExportRbService_Wizard_2 import Ui_ExportRbService_Wizard_2

rbServiceFields = ('code', 'name', 'eisLegacy', 'nomenclatureLegacy', 'license',
                    'infis', 'begDate', 'endDate', 'adultUetDoctor',  'adultUetAverageMedWorker',
                    'childUetDoctor',  'childUetAverageMedWorker', 'qualityLevel',
                    'superviseComplexityFactor')

rbServiceRefFields = ('medicalAidProfile_id', 'medicalAidType_id', 'medicalAidKind_id')
rbServiceRefTables = ('rbMedicalAidProfile', 'rbMedicalAidType', 'rbMedicalAidKind')

rbServiceProfileRefFields = ('speciality_id', )
rbServiceProfileRefTable = ('rbSpeciality', )


def ExportRbService(parent):
    fileName = forceString(QtGui.qApp.preferences.appPrefs.get('ExportRbServiceFileName', ''))
    exportAll = forceBool(QtGui.qApp.preferences.appPrefs.get('ExportRbServiceExportAll', 'False'))
    compressRAR = forceBool(QtGui.qApp.preferences.appPrefs.get('ExportRbServiceCompressRAR', 'False'))
    dlg = CExportRbService(fileName, exportAll,  compressRAR,  parent)
    dlg.exec_()
    QtGui.qApp.preferences.appPrefs['ExportRbServiceFileName'] = toVariant(dlg.fileName)
    QtGui.qApp.preferences.appPrefs['ExportRbServiceExportAll'] = toVariant(dlg.exportAll)
    QtGui.qApp.preferences.appPrefs['ExportRbServiceCompressRAR'] = toVariant(dlg.compressRAR)


class CMyXmlStreamWriter(QXmlStreamWriter):
    def __init__(self,  parent, idList):
        QXmlStreamWriter.__init__(self)
        self.parent = parent
        self.setAutoFormatting(True)
        self._idList = idList
        self.refValueCache = {}
        self.profiles = {}
        for field, tableName in zip(rbServiceRefFields+rbServiceProfileRefFields, rbServiceRefTables+rbServiceProfileRefTable):
            self.refValueCache[field] = CRBModelDataCache.getData(tableName, True)


    def createQuery(self,  idList):
        db = QtGui.qApp.db
        stmt = """SELECT  * FROM rbService"""
        if idList:
            stmt+=' WHERE id in ('+', '.join([str(et) for et in idList])+')'

        query = db.query(stmt)
        return query

    def getServiceProfiles(self, idList):
        db = QtGui.qApp.db
        stmt = '''SELECT * from rbService_Profile'''
        if idList:
            stmt+=' WHERE rbService_Profile.master_id in ('+', '.join([str(et) for et in idList])+')'
        query = db.query(stmt)
        while query.next():
            record = query.record()
            id = forceInt(record.value('id'))
            idx = forceString(record.value('idx'))
            masterId = forceInt(record.value('master_id'))
            sex = forceString(record.value('sex'))
            age = forceString(record.value('age'))
            mkbRegExp = forceString(record.value('mkbRegExp'))
            specialityId = forceRef(record.value('speciality_id'))
            medicalAidProfileId = forceRef(record.value('medicalAidProfile_id'))
            medicalAidTypeId = forceRef(record.value('medicalAidType_id'))
            medicalAidKindId = forceRef(record.value('medicalAidKind_id'))
            self.profiles.setdefault(masterId, []).append({'id':id, 'idx':idx, 'age':age, 'sex':sex, 'mkbRegExp':mkbRegExp,
                'specialityId': specialityId,
                'medicalAidProfileId': medicalAidProfileId,
                'medicalAidTypeId': medicalAidTypeId,
                'medicalAidKindId': medicalAidKindId})


    def writeRecord(self, record):
        self.writeStartElement("ServiceElement")

        # все свойства действия экспортируем как атрибуты
        for x in rbServiceFields:
            if x in ('begDate',  'endDate'):
                date = forceDate(record.value(x)).toString(Qt.ISODate)
                self.writeAttribute(x, forceString(date))
            else:
                self.writeAttribute(x, forceString(record.value(x)))

        for fieldName in rbServiceRefFields:
            elementName = fieldName[:-3]
            self.writeStartElement(elementName)
            value = forceRef(record.value(fieldName))
            if value:
                cache = self.refValueCache[fieldName]
                self.writeAttribute('code', cache.getStringById(value, CRBComboBox.showCode))
                self.writeAttribute('name', cache.getStringById(value, CRBComboBox.showName))
            self.writeEndElement()

        id = forceInt(record.value('id'))
        profiles = self.profiles.get(id, [])
        for profile in profiles:
            self.writeStartElement('Profile')
            cacheSpec = self.refValueCache['speciality_id']
            cacheProf = self.refValueCache['medicalAidProfile_id']
            cacheKind = self.refValueCache['medicalAidKind_id']
            cacheType = self.refValueCache['medicalAidType_id']
            self.writeAttribute('idx', profile['idx'])
            self.writeAttribute('sex', profile['sex'])
            self.writeAttribute('age', profile['age'])
            self.writeAttribute('mkbRegExp', profile['mkbRegExp'])
            self.writeAttribute('specCode', cacheSpec.getStringById(profile['specialityId'], CRBComboBox.showCode))
            self.writeAttribute('specName', cacheSpec.getStringById(profile['specialityId'], CRBComboBox.showName))
            self.writeAttribute('profCode',  cacheProf.getStringById(profile['medicalAidProfileId'], CRBComboBox.showCode))
            self.writeAttribute('profName',  cacheProf.getStringById(profile['medicalAidProfileId'], CRBComboBox.showName))
            self.writeAttribute('typeCode',  cacheType.getStringById(profile['medicalAidTypeId'], CRBComboBox.showCode))
            self.writeAttribute('typeName',  cacheType.getStringById(profile['medicalAidTypeId'], CRBComboBox.showName))
            self.writeAttribute('kindCode',  cacheKind.getStringById(profile['medicalAidKindId'], CRBComboBox.showCode))
            self.writeAttribute('kindName',  cacheKind.getStringById(profile['medicalAidKindId'], CRBComboBox.showName))
            self.writeEndElement()

        self.writeEndElement() # ThesaurusElement


    def writeFile(self,  device,  progressBar):
        global lastChangedRev
        global lastChangedDate
        try:
            from buildInfo import lastChangedRev, lastChangedDate
        except:
            lastChangedRev  = 'unknown'
            lastChangedDate = 'unknown'

        try:
            progressBar.setText(u'Запрос данных')
            query = self.createQuery(self._idList)
            self.getServiceProfiles(self._idList)
            self.setDevice(device)
            progressBar.setMaximum(max(query.size(), 1))
            progressBar.reset()
            progressBar.setValue(0)

            self.writeStartDocument()
            self.writeDTD("<!DOCTYPE xRbService>")
            self.writeStartElement("RbServiceExport")
            self.writeAttribute("SAMSON",
                                "2.0 revision(%s, %s)" %(lastChangedRev, lastChangedDate))
            self.writeAttribute('version', "1.00")
            while (query.next()):
                self.writeRecord(query.record())
                progressBar.step()

            self.writeEndDocument()

        except IOError, e:
            QtGui.qApp.logCurrentException()
            msg=''
            if hasattr(e, 'filename'):
                msg = u'%s:\n[Errno %s] %s' % (e.filename, e.errno, anyToUnicode(e.strerror))
            else:
                msg = u'[Errno %s] %s' % (e.errno, anyToUnicode(e.strerror))
            QtGui.QMessageBox.critical (self.parent,
                u'Произошла ошибка ввода-вывода', msg, QtGui.QMessageBox.Close)
            return False
        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical (self.parent,
                u'Произошла ошибка', exceptionToUnicode(e), QtGui.QMessageBox.Close)
            return False

        return True

class CExportRbServiceWizardPage1(QtGui.QWizardPage, Ui_ExportRbService_Wizard_1, CConstructHelperMixin):
    def __init__(self, parent):
        QtGui.QWizardPage.__init__(self, parent)
        self.cols = [
            CTextCol(u'Код',                 [rbCode], 20),
            CTextCol(u'Наименование',        [rbName], 40),
            CBoolCol(u'Унаследовано из ЕИС', ['eisLegacy'], 10),
            CTextCol(u'ИНФИС код',           ['infis'], 20),
            CEnumCol(u'Лицензирование',      ['license'], [u'не требуется', u'требуется лицензия', u'требуется персональный сертификат'], 30),
            ]
        self.tableName = "rbService"
        self.filter = ''
        self.table = QtGui.qApp.db.table(self.tableName)
        self.order = ['code', 'name', 'id']
        self.parent = parent #wtf? скрывать Qt-шный parent - это плохая затея
        self.preSetupUi()
        self.setupUi(self)
        self.postSetupUi()
        self.setTitle(u'Параметры экспорта')
        self.setSubTitle(u'Выбор записей для экспорта')


    def isComplete(self):
        # проверим пустой ли у нас список выбранных элементов
        if self.parent.exportAll:
            return True
        else:
            return self.parent.selectedItems != []


    def preSetupUi(self):
        self.addModels('Table',CTableModel(self, self.cols, self.tableName))


    def postSetupUi(self):
        self.setModels(self.tblItems,   self.modelTable, self.selectionModelTable)
        self.tblItems.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        idList = self.select()
        self.modelTable.setIdList(idList)
        self.selectionModelTable.clearSelection()
        self.tblItems.setFocus(Qt.OtherFocusReason)
        self.tblItems.setEnabled(not self.parent.exportAll)
        self.btnSelectAll.setEnabled(not self.parent.exportAll)
        self.btnClearSelection.setEnabled(not self.parent.exportAll)
        self.gbFilter.setEnabled(not self.parent.exportAll)
        self.checkExportAll.setChecked(self.parent.exportAll)
        self.chkFilterEIS.setCheckState(Qt.PartiallyChecked)
        self.chkFilterNomenclature.setCheckState(Qt.PartiallyChecked)


    def select(self):
        return QtGui.qApp.db.getIdList(self.table,
                            'id', self.filter,  self.order)


    def selectItem(self):
        return self.exec_()


    def setCurrentItemId(self, itemId):
        self.tblItems.setCurrentItemId(itemId)


    def currentItemId(self):
        return self.tblItems.currentItemId()


    def renewListAndSetTo(self, itemId=None):
        if not itemId:
            itemId = self.tblItems.currentItemId()
        self.updateFilter()
        idList = self.select()
        self.tblItems.setIdList(idList, itemId)
        self.selectionModelTable.clearSelection()
        rows = []
        # восстанавливаем выбранные элементы в таблице

        for id in self.parent.selectedItems:
            if idList.count(id)>0:
                row = idList.index(id)
                rows.append(row)
        for row in rows:
            index = self.modelTable.index(row, 0)
            self.selectionModelTable.select(index, QtGui.QItemSelectionModel.Select|
                                                                QtGui.QItemSelectionModel.Rows)


    def resetFilter(self):
        self.chkFilterCode.setChecked(False)
        self.chkFilterEIS.setCheckState(Qt.PartiallyChecked)
        self.chkFilterNomenclature.setCheckState(Qt.PartiallyChecked)
        self.chkFilterPeriod.setChecked(False)
        self.filter = []


    def updateFilter(self):
        cond = []

        if self.chkFilterCode.isChecked():
            cond.append(self.table[rbCode].likeBinary( \
                addDots(forceString(self.edtFilterCode.text()))))

        if self.chkFilterEIS.checkState() != Qt.PartiallyChecked:
            cond.append(self.table['eisLegacy'].eq( \
                forceBool(self.chkFilterEIS.isChecked())))

        if self.chkFilterNomenclature.checkState() != Qt.PartiallyChecked:
            cond.append(self.table['nomenclatureLegacy'].eq( \
                forceBool(self.chkFilterNomenclature.isChecked())))

        if self.chkFilterPeriod.isChecked():
            cond.append(self.table['begDate'].ge( \
                forceString(self.edtFilterBegDate.date().toString(Qt.ISODate))))
            cond.append(self.table['endDate'].le( \
                forceString(self.edtFilterEndDate.date().toString(Qt.ISODate))))

        self.filter = QtGui.qApp.db.joinAnd(cond)


    @pyqtSignature('QModelIndex')
    def on_tblItems_clicked(self, index):
        self.parent.selectedItems = self.tblItems.selectedItemIdList()
        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('')
    def on_btnSelectAll_clicked(self):
        selectionList = self.modelTable.idList()
        self.parent.selectedItems = selectionList

        for id in selectionList:
            index = self.modelTable.index(selectionList.index(id), 0)
            self.selectionModelTable.select(index, QtGui.QItemSelectionModel.Select|
                                                                    QtGui.QItemSelectionModel.Rows)

        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('')
    def on_btnClearSelection_clicked(self):
        selectionList = self.modelTable.idList()

        for id in selectionList:
            index = self.modelTable.index(selectionList.index(id), 0)
            self.selectionModelTable.select(index, QtGui.QItemSelectionModel.Deselect|
                                                                    QtGui.QItemSelectionModel.Rows)
            self.parent.selectedItems.remove(id)
        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('')
    def on_checkExportAll_clicked(self):
        self.parent.exportAll = self.checkExportAll.isChecked()
        self.tblItems.setEnabled(not self.parent.exportAll)
        self.btnSelectAll.setEnabled(not self.parent.exportAll)
        self.btnClearSelection.setEnabled(not self.parent.exportAll)
        self.gbFilter.setEnabled(not self.parent.exportAll)
        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('')
    def on_chkFilterCode_clicked(self):
        self.edtFilterCode.setEnabled(self.chkFilterCode.isChecked())


    @pyqtSignature('')
    def on_chkFilterPeriod_clicked(self):
        self.edtFilterBegDate.setEnabled(self.chkFilterPeriod.isChecked())
        self.edtFilterEndDate.setEnabled(self.chkFilterPeriod.isChecked())


    @pyqtSignature('QAbstractButton*')
    def on_bbxFilter_clicked(self, button):
        buttonCode = self.bbxFilter.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.renewListAndSetTo()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.resetFilter()
            self.renewListAndSetTo()


class CExportRbServiceWizardPage2(QtGui.QWizardPage, Ui_ExportRbService_Wizard_2):
    def __init__(self,  parent):
        self.done = False
        QtGui.QWizardPage.__init__(self, parent)
        self.setupUi(self)
        self.parent=parent #wtf? скрывать Qt-шный parent - это плохая затея
        self.setTitle(u'Параметры сохранения')
        self.setSubTitle(u'Выбор места для сохранения')
        self.progressBar.setFormat('%p%')
        self.progressBar.setValue(0)
        self.edtFileName.setText(self.parent.fileName)
        self.btnExport.setEnabled(self.parent.fileName != '')
        self.checkRAR.setChecked(self.parent.compressRAR)

    def initializePage(self):
        self.btnExport.setEnabled(self.parent.fileName != '')
        self.done = False

    def isComplete(self):
        return self.done

    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
        fileName = QtGui.QFileDialog.getSaveFileName(
            self, u'Укажите файл с данными', self.edtFileName.text(), u'Файлы XML (*.xml)')
        if fileName != '':
            self.edtFileName.setText(fileName)
            self.parent.fileName = fileName
            self.btnExport.setEnabled(True)

    @pyqtSignature('')
    def on_btnExport_clicked(self):
        fileName = self.edtFileName.text()

        if fileName.isEmpty():
            return

        idList = []
        if not self.parent.exportAll:
            for key in self.parent.selectedItems:
                if key and key not in idList:
                    idList.append(key)

            if idList == []:
                QtGui.QMessageBox.warning(self, u'Экспорт справочника "Услуги"',
                                      u'Не выбрано ни одного элемента для выгрузки')
                self.parent.back() # вернемся на пред. страницу. пусть выбирают
                return


        outFile = QFile(fileName)
        if not outFile.open(QFile.WriteOnly | QFile.Text):
            QtGui.QMessageBox.warning(self, u'Экспорт справочника "Услуги"',
                                      u'Не могу открыть файл для записи %s:\n%s.' %\
                                      (fileName, outFile.errorString()))
            return

        myXmlStreamWriter = CMyXmlStreamWriter(self, idList)
        result=myXmlStreamWriter.writeFile(outFile,  self.progressBar)
        self.progressBar.setText(u'Готово' if result else u'Прервано')
        outFile.close()

        if self.checkRAR.isChecked() and result:
            self.progressBar.setText(u'Сжатие')
            compressFileInRar(fileName, fileName+'.rar')
            self.progressBar.setText(u'Сжато в "%s"' % (fileName+'.rar'))

        self.done = True
        self.btnExport.setEnabled(False)
        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('')
    def on_checkRAR_clicked(self):
        self.parent.compressRAR = self.checkRAR.isChecked()


    @pyqtSignature('QString')
    def on_edtFileName_textChanged(self):
        self.parent.fileName = self.edtFileName.text()
        self.btnExport.setEnabled(self.parent.fileName != '')
        self.emit(SIGNAL('completeChanged()'))


class CExportRbService(QtGui.QWizard):
    def __init__(self, fileName,  exportAll, compressRAR,  parent=None):
        QtGui.QWizard.__init__(self, parent, Qt.Dialog)
        self.setWizardStyle(QtGui.QWizard.ModernStyle)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(u'Экспорт справочника "Услуги"')
        self.selectedItems = []
        self.fileName= fileName
        self.exportAll = exportAll
        self.compressRAR = compressRAR
        self.addPage(CExportRbServiceWizardPage1(self))
        self.addPage(CExportRbServiceWizardPage2(self))
