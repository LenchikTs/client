# -*- coding: utf-8 -*-


from PyQt4         import QtGui
from PyQt4.QtCore  import *

from library.database     import CTableRecordCache
from library.DialogBase   import CConstructHelperMixin
from library.TableModel   import CTableModel, CDateCol, CEnumCol, CTextCol
from library.TableView    import CTableView
from library.Utils        import *

from Registry.ClientEditDialog import CClientEditDialog

from Users.Rights import urAdmin, urRegTabWriteRegistry, urRegTabReadRegistry

from Ui_ClientSearchDialog import Ui_ClientSearchDialog

class CClientSearchDialog(QtGui.QDialog, Ui_ClientSearchDialog, CConstructHelperMixin):
    def __init__(self, parent, defaultFilter={}, addInfo=None):
        QtGui.QWidget.__init__(self, parent)
        self.defaultFilter = defaultFilter
        self.limit = 100
        self.addModels('Clients', CClientsModel(self))
        self.addObject('actEditClient', QtGui.QAction(u'Открыть регистрационную карточку', self))
        self.setupUi(self)
        self.actEditClient.setEnabled(QtGui.qApp.userHasAnyRight([urAdmin, urRegTabWriteRegistry, urRegTabReadRegistry]))
        self.tblClients.createPopupMenu([self.actEditClient])
        self.setModels(self.tblClients, self.modelClients, self.selectionModelClients)
        self.setDefaultFilter()
        self.updateClientsList()
        if addInfo:
            self.txtAddInfo.setText(addInfo)
        else:
            self.lblAddInfo.setVisible(False)
            self.txtAddInfo.setVisible(False)
    
    def setDefaultFilter(self):
        lastName = self.defaultFilter.get('lastName')
        if not lastName:
            self.chkFilterLastName.setChecked(False)
        else:
            self.chkFilterLastName.setChecked(True)
            self.edtFilterLastName.setText(lastName)
        firstName = self.defaultFilter.get('firstName')
        if not firstName:
            self.chkFilterFirstName.setChecked(False)
        else:
            self.chkFilterFirstName.setChecked(True)
            self.edtFilterFirstName.setText(firstName)
        patrName = self.defaultFilter.get('patrName')
        if not patrName:
            self.chkFilterPatrName.setChecked(False)
        else:
            self.chkFilterPatrName.setChecked(True)
            self.edtFilterPatrName.setText(patrName)
        birthDate = self.defaultFilter.get('birthDate')
        if not (birthDate and birthDate.isValid()):
            self.chkFilterBirthDate.setChecked(False)
            self.chkFilterBirthDateEnd.setChecked(False)
        else:
            self.chkFilterBirthDate.setChecked(True)
            self.edtFilterBirthDate.setDate(birthDate)
            birthDateEnd = self.defaultFilter.get('birthDateEnd')
            if not (birthDateEnd and birthDateEnd.isValid()):
                self.chkFilterBirthDateEnd.setChecked(False)
            else:
                self.chkFilterBirthDateEnd.setChecked(True)
                self.edtFilterBirthDateEnd.setDate(birthDateEnd)
        sex = self.defaultFilter.get('sex')
        if sex not in [1, 2]:
            self.chkFilterSex.setChecked(False)
        else:
            self.chkFilterSex.setChecked(True)
            self.cmbFilterSex.setCurrentIndex(sex)

    def updateClientsList(self):
        db = QtGui.qApp.db
        query = self.modelClients.table()
        where = [
            'Client.deleted = 0'
        ]
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
        if self.chkFilterBirthDate.isChecked():
            birthDate = self.edtFilterBirthDate.date().toString('yyyy-MM-dd')
            if self.chkFilterBirthDateEnd.isChecked():
                birthDateEnd = self.edtFilterBirthDateEnd.date().toString('yyyy-MM-dd')
                where.append("Client.birthDate between '%s' and '%s'" % (birthDate, birthDateEnd))
            else:
                where.append("Client.birthDate = '%s'" % birthDate)
        if self.chkFilterSex.isChecked():
            sex = self.cmbFilterSex.currentIndex
            if sex in [1, 2]:
                where.append("Client.sex = %d" % sex)
        order = 'Client.lastName, Client.firstName, Client.patrName'
        limit = self.limit
        idList = db.getIdList(query, idCol='Client.id', where=where, order=order, limit=limit)
        self.modelClients.setIdList(idList)
        count = len(idList)
        if count == 0:
            self.lblClientsCount.setText(u'Список пуст')
        if count < limit:
            formatString = agreeNumberAndWord(count, (u'Найден %d пациент', u'Найдено %d пациента', u'Найдено %d пациентов'))
            self.lblClientsCount.setText(formatString % count)
        else:
            self.lblClientsCount.setText(u'Найдено больше %d пациентов, показаны первые %d' % (count, count))
        self.currentClientChanged()
        
    def applyFilter(self):
        self.updateClientsList()
    
    def resetFilter(self):
        self.setDefaultFilter()
        self.updateClientsList()
    
    def currentClientChanged(self):
        self.currentClientId = self.tblClients.currentItemId()
        buttonOk = self.buttonBox.button(QtGui.QDialogButtonBox.Ok)
        buttonOk.setEnabled(self.currentClientId is not None)
    
    def accept(self):
        self.clientId = self.tblClients.currentItemId()
        QtGui.QDialog.accept(self)

    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelClients_currentRowChanged(self, current, previous):
        self.currentClientChanged()

    @pyqtSignature('QAbstractButton*')
    def on_filterButtonBox_clicked(self, button):
        buttonCode = self.filterButtonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.applyFilter()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.resetFilter()

    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.accept()
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.reject()

    @pyqtSignature('int')
    def on_chkFilterLastName_stateChanged(self, state):
        self.edtFilterLastName.setEnabled(state == Qt.Checked)

    @pyqtSignature('int')
    def on_chkFilterFirstName_stateChanged(self, state):
        self.edtFilterFirstName.setEnabled(state == Qt.Checked)

    @pyqtSignature('int')
    def on_chkFilterPatrName_stateChanged(self, state):
        self.edtFilterPatrName.setEnabled(state == Qt.Checked)

    @pyqtSignature('int')
    def on_chkFilterBirthDate_stateChanged(self, state):
        self.edtFilterBirthDate.setEnabled(state == Qt.Checked)
        self.chkFilterBirthDateEnd.setEnabled(state == Qt.Checked)

    @pyqtSignature('')
    def on_actEditClient_triggered(self):
        clientId = self.tblClients.currentItemId()
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
                    self.updateClientsList()
            finally:
                if dialog:
                    dialog.deleteLater()

class CExternalClientSearchDialog(CClientSearchDialog):
    def __init__(self, parent, defaultFilter={}, addInfo=None):
        self.externalInfo = {}
        self.clientInfo = {}
        self.infoFields = [
            (u"ФИО", ('lastName', 'firstName', 'patrName')),
            (u"Пол", 'sex'),
            (u"Дата рождения", 'birthDate'),
        ]
        CClientSearchDialog.__init__(self, parent, defaultFilter, addInfo)

    def infoStringValue(self, variant):
        if variant.isNull():
            return None
        string = forceStringEx(variant)
        return string if string else None

    def infoDateValue(self, variant):
        if variant.isNull():
            return None
        date = forceDate(variant)
        return date.toString('dd.MM.yyyy') if date.isValid() else None
    
    def formatInfoValue(self, field):
        externalValue = self.externalInfo.get(field)
        if externalValue is None:
            return None
        formattedExternalValue = ("<b>%s</b>" % externalValue)
        if not self.currentClientId:
            return formattedExternalValue
        clientValue = self.clientInfo.get(field)
        if externalValue == clientValue:
            color = "#0c0"
        else:
            color = "#c00"
        return ("<font color=\"%s\">%s</font>" % (color, formattedExternalValue))

    def currentClientChanged(self):
        CClientSearchDialog.currentClientChanged(self)
        self.updateClientInfo()
        self.updateInfoText()

    def updateClientInfo(self):
        clientRecord = self.tblClients.currentItem()
        self.clientInfo = {}
        if clientRecord:
            self.clientInfo['lastName'] = self.infoStringValue(clientRecord.value('lastName'))
            self.clientInfo['firstName'] = self.infoStringValue(clientRecord.value('firstName'))
            self.clientInfo['patrName'] = self.infoStringValue(clientRecord.value('patrName'))
            clientSex = forceInt(clientRecord.value('sex'))
            self.clientInfo['sex'] = {1: u"М", 2: u"Ж"}.get(clientSex)
            self.clientInfo['birthDate'] = self.infoDateValue(clientRecord.value('birthDate'))

    def updateInfoText(self):
        html = []
        for caption, fields in self.infoFields:
            if isinstance(fields, tuple):
                formattedValues = []
                for field in fields:
                    formattedValue = self.formatInfoValue(field)
                    if formattedValue:
                        formattedValues.append(formattedValue)
                if formattedValues:
                    formattedValues = " ".join(formattedValues)
                    html.append(u"%s: %s" % (caption, formattedValues))
            else:
                formattedValue = self.formatInfoValue(fields)
                if formattedValue:
                    html.append(u"%s: %s" % (caption, formattedValue))
        html = "<br>".join(html)
        self.txtAddInfo.setHtml(html)

class CClientsModel(CTableModel):
    def __init__(self, parent):
        self.clientInfoDict = {}
        CTableModel.__init__(self, parent)
        self.addColumn(CTextCol(u'Фамилия', ['lastName'], 30))
        self.addColumn(CTextCol(u'Имя', ['firstName'], 30))
        self.addColumn(CTextCol(u'Отчество', ['patrName'], 30))
        self.addColumn(CEnumCol(u'Пол', ['sex'], ['', u'М', u'Ж'], 10))
        self.addColumn(CDateCol(u'Дата рождения', ['birthDate'], 20, highlightRedDate=False))
        self.setTable('Client')
