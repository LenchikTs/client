# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import QAbstractItemView

from Orgs.Utils import getOrgStructureDescendants
from library.Calendar import monthName
from library.DialogBase import CConstructHelperMixin
from library.TableModel import CTableModel, CCol, CDesignationCol, CIntCol, CTextCol, CEnumCol
from library.Utils        import *

from Registry.ClientEditDialog import CClientEditDialog

from Reports.ReportBase import CReportBase, createTable
from Reports.ReportView     import CReportViewDialog, CPageFormat

from Exchange.ExportDispPlanDiagnosisDialog import CExportDispPlanDiagnosisDialog
from Exchange.ImportDispExportedPlanDiagnosisDialog import CImportDispExportedPlanDiagnosisDialog

from Users.Rights import urAdmin, urRegTabWriteRegistry, urRegTabReadRegistry

from Ui_DispExchangeDiagnosisPage   import Ui_DispExchangeDiagnosisPage

class CDispExchangeDiagnosisPage(QtGui.QWidget, Ui_DispExchangeDiagnosisPage, CConstructHelperMixin):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.addModels('DiagnosisDispansPlaned', CDiagnosisDispansPlanedModel(self))
        self.addModels('PlanExportErrors', CPlanExportErrorsModel(self))
        self.addObject('actEditClient', QtGui.QAction(u'Открыть регистрационную карточку', self))
        self.setupUi(self)
        self.actEditClient.setEnabled(QtGui.qApp.userHasAnyRight([urAdmin, urRegTabWriteRegistry, urRegTabReadRegistry]))
        self.setModels(self.tblDiagnosisDispansPlaned, self.modelDiagnosisDispansPlaned, self.selectionModelDiagnosisDispansPlaned)
        self.setModels(self.tblPlanExportErrors, self.modelPlanExportErrors, self.selectionModelPlanExportErrors)
        currentDate = QDate.currentDate()
        self.orderFieldByColumn = [
            'Client.lastName',
            'Client.firstName',
            'Client.patrName',
            'Client.birthDate',
            'Client.sex',
            'AttachOrgStructure.name',
            'Diagnosis.MKB',
            'DDP.year',
            'DDP.month',
            'Person.code'
        ]
        self.order = (0, True)
        self.sbYear.setValue(currentDate.year())
        self.updateDDPList()
        self.updateDDPDetails()
        header = self.tblDiagnosisDispansPlaned.horizontalHeader()
        header.setSortIndicatorShown(True)
        header.setSortIndicator(0, Qt.AscendingOrder)
        QObject.connect(header, SIGNAL('sectionClicked(int)'), self.setDDPSort)
        self.tblDiagnosisDispansPlaned.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def contextMenuEvent(self, event):
        self.menu = QtGui.QMenu(self)
        selectedRows = self.getSelectedRows(self.tblDiagnosisDispansPlaned)
        if len(selectedRows) == 1:
            self.menu.addAction(self.actEditClient)
        self.menu.popup(QtGui.QCursor.pos())

    def getSelectedRows(self, tbl):
        return [index.row() for index in tbl.selectionModel().selectedRows()]

    def updateDDPList(self):
        try:
            db = QtGui.qApp.db
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))
            tableClient = db.table('Client')
            year = self.sbYear.value()
            month = self.cmbMonth.currentIndex()

            attachTypeIds = db.getIdList('rbAttachType', where="code in ('1', '2')")

            sql = u"""
            select DDP.id,
                Client.id as client_id,
                Client.lastName,
                Client.firstName,
                Client.patrName,
                Client.birthDate,
                (case Client.sex when 1 then 'М' when 2 then 'Ж' end) as sex,
                AttachOrgStructure.name as attachName,
                Diagnosis.MKB,
                concat(Person.code, ' | ', formatPersonName(Person.id), ', ', rbSpeciality.name) as personName,
                PlanExport.id as planExport_id
            from DiagnosisDispansPlaned as DDP
                left join Client on Client.id = DDP.client_id
                left join ClientAttach as Attach on Attach.id = (
                    select max(Attach.id)
                    from ClientAttach as Attach
                    where Attach.client_id = Client.id
                        and Attach.deleted = 0
                        and Attach.endDate is null
                        and Attach.attachType_id in (%(attachTypeIds)s)
                )
                LEFT JOIN ClientWork ON ClientWork.client_id = Client.id AND ClientWork.id = (
                    SELECT
                    MAX(CW.id)
                    FROM ClientWork AS CW
                    WHERE CW.client_id = Client.id
                    AND CW.deleted = 0)
                left join Diagnosis on Diagnosis.id = DDP.diagnosis_id
                left join Person on Person.id = DDP.person_id
                left join rbSpeciality on rbSpeciality.id = Person.speciality_id
                left join disp_PlanExport as PlanExport on PlanExport.exportKind = 'DiagnosisDispansPlaned' and PlanExport.row_id = DDP.id
                left join OrgStructure as AttachOrgStructure on AttachOrgStructure.id = Attach.orgStructure_id
            """ % {
                "attachTypeIds": ', '.join([str(id) for id in attachTypeIds])
            }
            where = [
                "DDP.year = %d" % year,
                'DDP.deleted = 0',
                'Client.deleted = 0'
            ]
            if month > 0:
                where.append("DDP.month = %d" % month)
            if self.chkFilterLastName.isChecked():
                lastName = forceStringEx(self.edtFilterLastName.text())
                if lastName:
                    where.append("Client.lastName like '%s%%'" % lastName)
            if self.chkFilterFirstName.isChecked():
                firstName = forceStringEx(self.edtFilterFirstName.text())
                if firstName:
                    where.append("Client.firstName like '%s%%'" % firstName)
            if self.chkFilterPatrName.isChecked():
                patrName = forceStringEx(self.edtFilterPatrName.text())
                if patrName:
                    where.append("Client.patrName like '%s%%'" % patrName)
            if self.chkFilterBirthDay.isChecked():
                birthDate = self.edtFilterBirthDay.date()
                if not birthDate:
                    birthDate = None
                if self.chkFilterEndBirthDay.isChecked():
                    endBirthDate = self.edtFilterEndBirthDay.date()
                    if not endBirthDate:
                        endBirthDate = None
                    where.append(tableClient['birthDate'].dateGe(birthDate))
                    where.append(tableClient['birthDate'].dateLe(endBirthDate))
                else:
                    where.append(tableClient['birthDate'].eq(birthDate))
            if self.chkFilterAddressOrgStructure.isChecked():
                orgStructureId = self.cmbFilterAddressOrgStructure.value()
                if orgStructureId:
                    orgStructureIdList = getOrgStructureDescendants(orgStructureId)
                    tableClientAttach = db.table('ClientAttach').alias('Attach')
                    where.append(tableClientAttach['orgStructure_id'].inlist(orgStructureIdList))
            if self.chkFilterSex.isChecked():
                sex = self.cmbFilterSex.currentIndex()
                if sex:
                    where.append(tableClient['sex'].eq(sex))
            if self.cmbBusyness.currentIndex() == 1:
                where.append(u"IF((ClientWork.org_id is not null or IFNULL(ClientWork.freeInput, '') <> '') and IFNULL(ClientWork.post, '') <> '', 1, 0) = 1")
            elif self.cmbBusyness.currentIndex() == 2:
                where.append(u"IF((ClientWork.org_id is not null or IFNULL(ClientWork.freeInput, '') <> '') and IFNULL(ClientWork.post, '') <> '', 1, 0) = 0")
            if self.chkFilterPerson.isChecked():
                personId = self.cmbFilterPerson.value()
                if personId:
                    where.append('DDP.person_id = %d' % personId)
            if self.chkFilterMKB.isChecked():
                mkbFrom = forceString(self.edtFilterMKBFrom.text())
                mkbTo = forceString(self.edtFilterMKBTo.text())
                if mkbFrom:
                    where.append("Diagnosis.MKB >= '%s'" % mkbFrom)
                if mkbTo:
                    where.append("Diagnosis.MKB <= '%s'" % mkbTo)
            statusFilter = []
            if self.chkNotExported.isChecked():
                statusFilter.append('PlanExport.id is null')
            if self.chkExportedSuccessfully.isChecked():
                statusFilter.append('PlanExport.exportSuccess = 1')
            if self.chkExportedWithErrors.isChecked():
                statusFilter.append('PlanExport.exportSuccess = 0')
            if len(statusFilter) > 0 and len(statusFilter) < 3:
                where.append('(' + ' or '.join(statusFilter) + ')')
            sql += (' where ' + ' and '.join(where))

            order = self.getOrderField()
            sql += (' order by ' + order)

            idList = []
            infoDict = self.modelDiagnosisDispansPlaned.infoDict
            infoDict.clear()
            query = db.query(sql)
            while query.next():
                record = query.record()
                clientId = forceRef(record.value('id'))
                idList.append(clientId)
                infoDict[clientId] = record
            self.modelDiagnosisDispansPlaned.setIdList(idList)
            count = len(idList)
            self.lblRowCount.setText(formatRecordsCount(count))
        finally:
            QtGui.QApplication.restoreOverrideCursor()

    def updateDDPDetails(self):
        ddp_id = self.tblDiagnosisDispansPlaned.currentItemId()
        ddpInfo = self.modelDiagnosisDispansPlaned.infoDict.get(ddp_id)
        planExport_id = forceRef(ddpInfo.value('planExport_id')) if ddpInfo else None
        self.modelPlanExportErrors.update(planExport_id)
        self.tabWidget.setTabText(0, u'Ошибки (%d)' % self.modelPlanExportErrors.rowCount())

    def getOrderField(self):
        column, asc = self.order
        direction = ' asc' if asc else ' desc'
        field = self.orderFieldByColumn[column] + direction
        return field
    
    def setDDPSort(self, newColumn):
        newOrderField = self.orderFieldByColumn[newColumn]
        if newOrderField is None:
            return
        column, asc = self.order
        if column == newColumn:
            newAsc = not asc
        else:
            newAsc = True
        self.order = (newColumn, newAsc)
        self.updateDDPList()

    def showReport(self):
        def showReportInt():
            report = CDispExchangeReport(self, self.modelDiagnosisDispansPlaned)
            description = self.reportDescription()
            reportTxt = report.build(description)
            view = CReportViewDialog(self)
            view.setWindowTitle(report.title())
            view.setText(reportTxt)
            if report.pageFormat:
                view.setPageFormat(report.pageFormat)
            return view
        view = QtGui.qApp.callWithWaitCursor(self, showReportInt)
        view.exec_()
    
    def reportDescription(self):
        year = self.sbYear.value()
        month = self.cmbMonth.currentIndex()
        lines = []
        lines.append(u'Год: %d' % year)
        if month > 0:
            monthText = self.cmbMonth.currentText()
            lines.append(u'Месяц: %s' % monthText)
        if self.chkFilterLastName.isChecked():
            lastName = forceStringEx(self.edtFilterLastName.text())
            lines.append(u'Фамилия: %s' % lastName)
        if self.chkFilterFirstName.isChecked():
            firstName = forceStringEx(self.edtFilterFirstName.text())
            lines.append(u'Имя: %s' % firstName)
        if self.chkFilterPatrName.isChecked():
            patrName = forceStringEx(self.edtFilterPatrName.text())
            lines.append(u'Отчество: %s' % patrName)
        statusLines = []
        if self.chkNotExported.isChecked():
            statusLines.append(u'- запланированные, не отправленные')
        if self.chkExportedSuccessfully.isChecked():
            statusLines.append(u'- отправленные успешно')
        if self.chkExportedWithErrors.isChecked():
            statusLines.append(u'- отправленные с ошибками')
        if len(statusLines) > 0 and len(statusLines) < 3:
            lines.append(u'Статус:')
            lines += statusLines
        return '\n'.join(lines)

    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelDiagnosisDispansPlaned_currentRowChanged(self, current, previous):
        self.updateDDPDetails()

    @pyqtSignature('')
    def on_btnApplyFilter_clicked(self):
        self.updateDDPList()

    @pyqtSignature('')
    def on_btnResetFilter_clicked(self):
        self.cmbMonth.setCurrentIndex(0)
        self.chkFilterLastName.setChecked(False)
        self.chkFilterFirstName.setChecked(False)
        self.chkFilterPatrName.setChecked(False)
        self.chkFilterBirthDay.setChecked(False)
        self.chkFilterEndBirthDay.setChecked(False)
        self.chkFilterAddressOrgStructure.setChecked(False)
        self.chkFilterSex.setChecked(False)
        self.chkFilterPerson.setChecked(False)
        self.chkFilterMKB.setChecked(False)
        self.cmbBusyness.setCurrentIndex(0)
        self.chkNotExported.setChecked(True)
        self.chkExportedSuccessfully.setChecked(False)
        self.chkExportedWithErrors.setChecked(False)
        self.updateDDPList()

    @pyqtSignature('int')
    def on_chkFilterLastName_stateChanged(self, state):
        self.edtFilterLastName.setEnabled(state == Qt.Checked)
        if self.chkFilterLastName.isChecked():
            self.edtFilterLastName.setFocus()

    @pyqtSignature('int')
    def on_chkFilterFirstName_stateChanged(self, state):
        self.edtFilterFirstName.setEnabled(state == Qt.Checked)
        if self.chkFilterFirstName.isChecked():
            self.edtFilterFirstName.setFocus()

    @pyqtSignature('int')
    def on_chkFilterPatrName_stateChanged(self, state):
        self.edtFilterPatrName.setEnabled(state == Qt.Checked)
        if self.chkFilterPatrName.isChecked():
            self.edtFilterPatrName.setFocus()

    @pyqtSignature('bool')
    def on_chkFilterBirthDay_toggled(self, checked):
        if checked:
            self.edtFilterBirthDay.setEnabled(checked)
            self.chkFilterEndBirthDay.setEnabled(checked)
            self.edtFilterEndBirthDay.setEnabled(self.chkFilterEndBirthDay.isChecked())
            self.edtFilterBirthDay.setFocus()
        else:
            self.edtFilterBirthDay.setEnabled(False)
            self.chkFilterEndBirthDay.setEnabled(False)
            self.edtFilterEndBirthDay.setEnabled(False)

    @pyqtSignature('bool')
    def on_chkFilterAddressOrgStructure_toggled(self, checked):
        self.cmbFilterAddressOrgStructure.setEnabled(checked)

    @pyqtSignature('bool')
    def on_chkFilterEndBirthDay_toggled(self, checked):
        self.edtFilterEndBirthDay.setEnabled(checked)
        if self.chkFilterEndBirthDay.isChecked():
            self.edtFilterEndBirthDay.setFocus()

    @pyqtSignature('bool')
    def on_chkFilterSex_toggled(self, checked):
        self.cmbFilterSex.setEnabled(checked)

    @pyqtSignature('bool')
    def on_chkFilterPerson_toggled(self, checked):
        self.cmbFilterPerson.setEnabled(checked)

    @pyqtSignature('bool')
    def on_chkFilterMKB_toggled(self, checked):
        self.edtFilterMKBFrom.setEnabled(checked)
        self.edtFilterMKBTo.setEnabled(checked)

    @pyqtSignature('')
    def on_btnPutEvPlanList_clicked(self):
        CExportDispPlanDiagnosisDialog(self).exec_()

    @pyqtSignature('')
    def on_btnExportedPlan_clicked(self):
        CImportDispExportedPlanDiagnosisDialog(self).exec_()

    @pyqtSignature('')
    def on_actEditClient_triggered(self):
        ddpId = self.tblDiagnosisDispansPlaned.currentItemId()
        infoRecord = self.modelDiagnosisDispansPlaned.infoDict.get(ddpId)
        clientId = forceRef(infoRecord.value('client_id')) if infoRecord else None
        if clientId is not None and QtGui.qApp.userHasAnyRight([urAdmin, urRegTabWriteRegistry, urRegTabReadRegistry]):
            dialog = None
            QtGui.qApp.setWaitCursor()
            try:
                try:
                    dialog = CClientEditDialog(self)
                    dialog.load(clientId)
                finally:
                    QtGui.qApp.restoreOverrideCursor()
                if dialog.exec_():
                    self.update()
            finally:
                if dialog:
                    dialog.deleteLater()

    @pyqtSignature('')
    def on_btnShowReport_clicked(self):
        self.showReport()

class CDiagnosisDispansPlanedModel(CTableModel):
    class CInfoCol(CTextCol):
        def __init__(self, title, infoField, infoDict, defaultWidth, alignment='l'):
            CTextCol.__init__(self, title, ['id'], defaultWidth, alignment)
            self.infoDict = infoDict
            self.infoField = infoField

        def format(self, values):
            id = forceRef(values[0])
            record = self.infoDict.get(id)
            if record:
                return QVariant(forceString(record.value(self.infoField)))
            else:
                return CCol.invalid

    def __init__(self, parent):
        self.infoDict = {}
        CTableModel.__init__(self, parent)
        self.parent = parent
        self.addColumn(self.CInfoCol(u'Фамилия', 'lastName', self.infoDict, 15))
        self.addColumn(self.CInfoCol(u'Имя', 'firstName', self.infoDict, 15))
        self.addColumn(self.CInfoCol(u'Отчество', 'patrName', self.infoDict, 15))
        self.addColumn(self.CInfoCol(u'Дата рожд.', 'birthDate', self.infoDict, 15))
        self.addColumn(self.CInfoCol(u'Пол', 'sex', self.infoDict, 15, alignment='c'))
        self.addColumn(self.CInfoCol(u'Участок', 'attachName', self.infoDict, 15))
        self.addColumn(self.CInfoCol(u'Код МКБ', 'MKB', self.infoDict, 15))
        self.addColumn(CIntCol(u'Год', ['year'], 15))
        self.addColumn(CEnumCol(u'Месяц', ['month'], monthName, 15))
        self.addColumn(self.CInfoCol(u'Врач', 'personName', self.infoDict, 15))
        self.setTable('DiagnosisDispansPlaned')

class CPlanExportErrorsModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent, [
            CIntCol(u'Код ошибки', ['errorType_id'], 20),
            CDesignationCol(u'Текст ошибки', ['errorType_id'], ('disp_ErrorTypes', 'name'), 20)
            ], 'disp_PlanExportErrors')

    def update(self, planExport_id):
        if planExport_id is None:
            idList = []
        else:
            db = QtGui.qApp.db
            table = db.table('disp_PlanExportErrors')
            where = [
                table['planExport_id'].eq(planExport_id)
                ]
            idList = db.getIdList(table, idCol=table['id'], where=where)
        self.setIdList(idList)

class CDispExchangeReport(CReportBase):
    def __init__(self, parent, model):
        CReportBase.__init__(self, parent)
        self.model = model
        self.setTitle(u'Диспансерные осмотры')
        self.pageFormat = CPageFormat(pageSize=CPageFormat.A4, orientation=CPageFormat.Landscape, leftMargin=1, topMargin=1, rightMargin=1,  bottomMargin=1)
        
    def build(self, description):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(description)
        cursor.insertBlock()

        tableColumns = [
            ('15%', [u'Фамилия'       ], CReportBase.AlignLeft),
            ('15%', [u'Имя'           ], CReportBase.AlignLeft),
            ('15%', [u'Отчество'      ], CReportBase.AlignLeft),
            ('10%', [u'Дата рождения' ], CReportBase.AlignLeft),
            ('5%',  [u'Пол'           ], CReportBase.AlignLeft),
            ('10%', [u'Участок'       ], CReportBase.AlignLeft),
            ('10%', [u'Код МКБ'       ], CReportBase.AlignLeft),
            ('5%',  [u'Год'           ], CReportBase.AlignLeft),
            ('5%',  [u'Месяц'         ], CReportBase.AlignLeft),
            ('10%', [u'Врач'          ], CReportBase.AlignLeft),
        ]
        table = createTable(cursor, tableColumns)
        n = 0
        rowCount = self.model.rowCount()
        columnCount = self.model.columnCount()
        for row in xrange(0, rowCount):
            tableRow = table.addRow()
            for column in xrange(0, columnCount):
                (modelColumn, values) = self.model.getRecordValues(column, row)
                text = forceString(modelColumn.format(values))
                table.setText(tableRow, column, text)
        return doc
