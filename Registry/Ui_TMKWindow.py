# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\SVN\Samson\UP_s11\client\Registry\TMKWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_TMKWindow(object):
    def setupUi(self, TMKWindow):
        TMKWindow.setObjectName(_fromUtf8("TMKWindow"))
        TMKWindow.resize(909, 796)
        self.gridLayout_3 = QtGui.QGridLayout(TMKWindow)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.grpTables = QtGui.QWidget(TMKWindow)
        self.grpTables.setObjectName(_fromUtf8("grpTables"))
        self.verticalLayout = QtGui.QVBoxLayout(self.grpTables)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter_2 = QtGui.QSplitter(self.grpTables)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setHandleWidth(4)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setHandleWidth(4)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.txtClientInfoBrowser = CTextBrowser(self.splitter)
        self.txtClientInfoBrowser.setObjectName(_fromUtf8("txtClientInfoBrowser"))
        self.tblTMKRequests = CTableView(self.splitter)
        self.tblTMKRequests.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblTMKRequests.setObjectName(_fromUtf8("tblTMKRequests"))
        self.textEdit = CReportBrowser(self.splitter)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout.addWidget(self.splitter_2)
        self.lblRecordCount = QtGui.QLabel(self.grpTables)
        self.lblRecordCount.setObjectName(_fromUtf8("lblRecordCount"))
        self.verticalLayout.addWidget(self.lblRecordCount)
        self.gridLayout_3.addWidget(self.grpTables, 0, 0, 1, 3)
        self.grpFilter = QtGui.QGroupBox(TMKWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grpFilter.sizePolicy().hasHeightForWidth())
        self.grpFilter.setSizePolicy(sizePolicy)
        self.grpFilter.setMinimumSize(QtCore.QSize(100, 0))
        self.grpFilter.setMaximumSize(QtCore.QSize(250, 16777215))
        self.grpFilter.setFlat(False)
        self.grpFilter.setObjectName(_fromUtf8("grpFilter"))
        self.gridLayout = QtGui.QGridLayout(self.grpFilter)
        self.gridLayout.setMargin(2)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBoxFilter = CApplyResetDialogButtonBox(self.grpFilter)
        self.buttonBoxFilter.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxFilter.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Reset)
        self.buttonBoxFilter.setObjectName(_fromUtf8("buttonBoxFilter"))
        self.gridLayout.addWidget(self.buttonBoxFilter, 1, 0, 1, 1)
        self.tabFilter = QtGui.QTabWidget(self.grpFilter)
        self.tabFilter.setTabPosition(QtGui.QTabWidget.North)
        self.tabFilter.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabFilter.setObjectName(_fromUtf8("tabFilter"))
        self.tabFind = QtGui.QWidget()
        self.tabFind.setObjectName(_fromUtf8("tabFind"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabFind)
        self.gridLayout_2.setMargin(1)
        self.gridLayout_2.setSpacing(1)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.edtFilterFirstName = QtGui.QLineEdit(self.tabFind)
        self.edtFilterFirstName.setEnabled(False)
        self.edtFilterFirstName.setObjectName(_fromUtf8("edtFilterFirstName"))
        self.gridLayout_2.addWidget(self.edtFilterFirstName, 5, 0, 1, 3)
        self.edtFilterLastName = QtGui.QLineEdit(self.tabFind)
        self.edtFilterLastName.setEnabled(False)
        self.edtFilterLastName.setObjectName(_fromUtf8("edtFilterLastName"))
        self.gridLayout_2.addWidget(self.edtFilterLastName, 3, 0, 1, 3)
        self.chkFilterEndBirthDay = QtGui.QCheckBox(self.tabFind)
        self.chkFilterEndBirthDay.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkFilterEndBirthDay.sizePolicy().hasHeightForWidth())
        self.chkFilterEndBirthDay.setSizePolicy(sizePolicy)
        self.chkFilterEndBirthDay.setObjectName(_fromUtf8("chkFilterEndBirthDay"))
        self.gridLayout_2.addWidget(self.chkFilterEndBirthDay, 9, 0, 1, 1)
        self.chkFilterFirstName = QtGui.QCheckBox(self.tabFind)
        self.chkFilterFirstName.setObjectName(_fromUtf8("chkFilterFirstName"))
        self.gridLayout_2.addWidget(self.chkFilterFirstName, 4, 0, 1, 3)
        self.cmbFilterSex = QtGui.QComboBox(self.tabFind)
        self.cmbFilterSex.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbFilterSex.sizePolicy().hasHeightForWidth())
        self.cmbFilterSex.setSizePolicy(sizePolicy)
        self.cmbFilterSex.setObjectName(_fromUtf8("cmbFilterSex"))
        self.cmbFilterSex.addItem(_fromUtf8(""))
        self.cmbFilterSex.setItemText(0, _fromUtf8(""))
        self.cmbFilterSex.addItem(_fromUtf8(""))
        self.cmbFilterSex.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.cmbFilterSex, 10, 1, 1, 2)
        self.lblFilterStatus = QtGui.QLabel(self.tabFind)
        self.lblFilterStatus.setObjectName(_fromUtf8("lblFilterStatus"))
        self.gridLayout_2.addWidget(self.lblFilterStatus, 15, 0, 1, 1)
        self.chkFilterSex = QtGui.QCheckBox(self.tabFind)
        self.chkFilterSex.setObjectName(_fromUtf8("chkFilterSex"))
        self.gridLayout_2.addWidget(self.chkFilterSex, 10, 0, 1, 1)
        self.edtFilterEndBirthDay = CDateEdit(self.tabFind)
        self.edtFilterEndBirthDay.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtFilterEndBirthDay.sizePolicy().hasHeightForWidth())
        self.edtFilterEndBirthDay.setSizePolicy(sizePolicy)
        self.edtFilterEndBirthDay.setCalendarPopup(True)
        self.edtFilterEndBirthDay.setObjectName(_fromUtf8("edtFilterEndBirthDay"))
        self.gridLayout_2.addWidget(self.edtFilterEndBirthDay, 9, 1, 1, 2)
        self.cmbFilterCategory = CRBComboBox(self.tabFind)
        self.cmbFilterCategory.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbFilterCategory.sizePolicy().hasHeightForWidth())
        self.cmbFilterCategory.setSizePolicy(sizePolicy)
        self.cmbFilterCategory.setObjectName(_fromUtf8("cmbFilterCategory"))
        self.gridLayout_2.addWidget(self.cmbFilterCategory, 12, 0, 1, 3)
        self.chkFilterBirthDay = QtGui.QCheckBox(self.tabFind)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkFilterBirthDay.sizePolicy().hasHeightForWidth())
        self.chkFilterBirthDay.setSizePolicy(sizePolicy)
        self.chkFilterBirthDay.setObjectName(_fromUtf8("chkFilterBirthDay"))
        self.gridLayout_2.addWidget(self.chkFilterBirthDay, 8, 0, 1, 1)
        self.chkFilterPatrName = QtGui.QCheckBox(self.tabFind)
        self.chkFilterPatrName.setObjectName(_fromUtf8("chkFilterPatrName"))
        self.gridLayout_2.addWidget(self.chkFilterPatrName, 6, 0, 1, 3)
        self.edtFilterBegBirthDay = CDateEdit(self.tabFind)
        self.edtFilterBegBirthDay.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtFilterBegBirthDay.sizePolicy().hasHeightForWidth())
        self.edtFilterBegBirthDay.setSizePolicy(sizePolicy)
        self.edtFilterBegBirthDay.setCalendarPopup(True)
        self.edtFilterBegBirthDay.setObjectName(_fromUtf8("edtFilterBegBirthDay"))
        self.gridLayout_2.addWidget(self.edtFilterBegBirthDay, 8, 1, 1, 2)
        self.edtFilterPatrName = QtGui.QLineEdit(self.tabFind)
        self.edtFilterPatrName.setEnabled(False)
        self.edtFilterPatrName.setObjectName(_fromUtf8("edtFilterPatrName"))
        self.gridLayout_2.addWidget(self.edtFilterPatrName, 7, 0, 1, 3)
        self.chkFilterCategory = QtGui.QCheckBox(self.tabFind)
        self.chkFilterCategory.setObjectName(_fromUtf8("chkFilterCategory"))
        self.gridLayout_2.addWidget(self.chkFilterCategory, 11, 0, 1, 3)
        self.cmbFilterStatus = QtGui.QComboBox(self.tabFind)
        self.cmbFilterStatus.setObjectName(_fromUtf8("cmbFilterStatus"))
        self.gridLayout_2.addWidget(self.cmbFilterStatus, 15, 1, 1, 2)
        self.cmbFilterPerson = CPersonComboBoxEx(self.tabFind)
        self.cmbFilterPerson.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbFilterPerson.sizePolicy().hasHeightForWidth())
        self.cmbFilterPerson.setSizePolicy(sizePolicy)
        self.cmbFilterPerson.setObjectName(_fromUtf8("cmbFilterPerson"))
        self.gridLayout_2.addWidget(self.cmbFilterPerson, 14, 0, 1, 3)
        self.cmbFilterUrgency = QtGui.QComboBox(self.tabFind)
        self.cmbFilterUrgency.setObjectName(_fromUtf8("cmbFilterUrgency"))
        self.gridLayout_2.addWidget(self.cmbFilterUrgency, 16, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 18, 0, 1, 3)
        self.lblFilterUrgency = QtGui.QLabel(self.tabFind)
        self.lblFilterUrgency.setObjectName(_fromUtf8("lblFilterUrgency"))
        self.gridLayout_2.addWidget(self.lblFilterUrgency, 16, 0, 1, 1)
        self.chkFilterPerson = QtGui.QCheckBox(self.tabFind)
        self.chkFilterPerson.setObjectName(_fromUtf8("chkFilterPerson"))
        self.gridLayout_2.addWidget(self.chkFilterPerson, 13, 0, 1, 3)
        self.chkFilterLastName = QtGui.QCheckBox(self.tabFind)
        self.chkFilterLastName.setObjectName(_fromUtf8("chkFilterLastName"))
        self.gridLayout_2.addWidget(self.chkFilterLastName, 2, 0, 1, 3)
        self.label = QtGui.QLabel(self.tabFind)
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 2)
        self.chkDirection = QtGui.QCheckBox(self.tabFind)
        self.chkDirection.setChecked(True)
        self.chkDirection.setObjectName(_fromUtf8("chkDirection"))
        self.gridLayout_2.addWidget(self.chkDirection, 0, 0, 1, 2)
        self.edtFilterLastName.raise_()
        self.cmbFilterPerson.raise_()
        self.chkFilterSex.raise_()
        self.cmbFilterSex.raise_()
        self.chkFilterPerson.raise_()
        self.chkFilterPatrName.raise_()
        self.edtFilterPatrName.raise_()
        self.edtFilterBegBirthDay.raise_()
        self.chkFilterFirstName.raise_()
        self.edtFilterFirstName.raise_()
        self.chkFilterEndBirthDay.raise_()
        self.chkFilterLastName.raise_()
        self.chkFilterBirthDay.raise_()
        self.edtFilterEndBirthDay.raise_()
        self.chkFilterCategory.raise_()
        self.cmbFilterCategory.raise_()
        self.cmbFilterStatus.raise_()
        self.lblFilterStatus.raise_()
        self.lblFilterUrgency.raise_()
        self.cmbFilterUrgency.raise_()
        self.chkDirection.raise_()
        self.label.raise_()
        self.tabFilter.addTab(self.tabFind, _fromUtf8(""))
        self.tabFindEx = QtGui.QWidget()
        self.tabFindEx.setObjectName(_fromUtf8("tabFindEx"))
        self.gridLayout_27 = QtGui.QGridLayout(self.tabFindEx)
        self.gridLayout_27.setMargin(1)
        self.gridLayout_27.setSpacing(1)
        self.gridLayout_27.setObjectName(_fromUtf8("gridLayout_27"))
        self.edtFilterExEndCreateDate = CDateEdit(self.tabFindEx)
        self.edtFilterExEndCreateDate.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtFilterExEndCreateDate.sizePolicy().hasHeightForWidth())
        self.edtFilterExEndCreateDate.setSizePolicy(sizePolicy)
        self.edtFilterExEndCreateDate.setMinimumSize(QtCore.QSize(0, 0))
        self.edtFilterExEndCreateDate.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.edtFilterExEndCreateDate.setCalendarPopup(True)
        self.edtFilterExEndCreateDate.setObjectName(_fromUtf8("edtFilterExEndCreateDate"))
        self.gridLayout_27.addWidget(self.edtFilterExEndCreateDate, 1, 1, 1, 1)
        self.edtFilterExBegCreateDate = CDateEdit(self.tabFindEx)
        self.edtFilterExBegCreateDate.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtFilterExBegCreateDate.sizePolicy().hasHeightForWidth())
        self.edtFilterExBegCreateDate.setSizePolicy(sizePolicy)
        self.edtFilterExBegCreateDate.setMinimumSize(QtCore.QSize(0, 0))
        self.edtFilterExBegCreateDate.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.edtFilterExBegCreateDate.setCalendarPopup(True)
        self.edtFilterExBegCreateDate.setObjectName(_fromUtf8("edtFilterExBegCreateDate"))
        self.gridLayout_27.addWidget(self.edtFilterExBegCreateDate, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(84, 181, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_27.addItem(spacerItem1, 3, 0, 1, 3)
        self.chkFilterExCreateDate = QtGui.QCheckBox(self.tabFindEx)
        self.chkFilterExCreateDate.setObjectName(_fromUtf8("chkFilterExCreateDate"))
        self.gridLayout_27.addWidget(self.chkFilterExCreateDate, 0, 0, 1, 3)
        self.tabFilter.addTab(self.tabFindEx, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabFilter, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.grpFilter, 0, 3, 2, 1)
        self.btnPrint = CPrintButton(TMKWindow)
        self.btnPrint.setObjectName(_fromUtf8("btnPrint"))
        self.gridLayout_3.addWidget(self.btnPrint, 1, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(216, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 1, 2, 1, 1)
        self.lblFilterStatus.setBuddy(self.cmbFilterStatus)

        self.retranslateUi(TMKWindow)
        self.tabFilter.setCurrentIndex(0)
        QtCore.QObject.connect(self.chkFilterLastName, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFilterLastName.setEnabled)
        QtCore.QObject.connect(self.chkFilterFirstName, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFilterFirstName.setEnabled)
        QtCore.QObject.connect(self.chkFilterPatrName, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFilterPatrName.setEnabled)
        QtCore.QObject.connect(self.chkFilterBirthDay, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFilterBegBirthDay.setEnabled)
        QtCore.QObject.connect(self.chkFilterBirthDay, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.chkFilterEndBirthDay.setEnabled)
        QtCore.QObject.connect(self.chkFilterEndBirthDay, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFilterEndBirthDay.setEnabled)
        QtCore.QObject.connect(self.chkFilterSex, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbFilterSex.setEnabled)
        QtCore.QObject.connect(self.chkFilterCategory, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbFilterCategory.setEnabled)
        QtCore.QObject.connect(self.chkFilterPerson, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbFilterPerson.setEnabled)
        QtCore.QObject.connect(self.chkFilterExCreateDate, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFilterExBegCreateDate.setEnabled)
        QtCore.QObject.connect(self.chkFilterExCreateDate, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFilterExEndCreateDate.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(TMKWindow)
        TMKWindow.setTabOrder(self.txtClientInfoBrowser, self.tblTMKRequests)
        TMKWindow.setTabOrder(self.tblTMKRequests, self.tabFilter)
        TMKWindow.setTabOrder(self.tabFilter, self.chkFilterLastName)
        TMKWindow.setTabOrder(self.chkFilterLastName, self.edtFilterLastName)
        TMKWindow.setTabOrder(self.edtFilterLastName, self.chkFilterFirstName)
        TMKWindow.setTabOrder(self.chkFilterFirstName, self.edtFilterFirstName)
        TMKWindow.setTabOrder(self.edtFilterFirstName, self.chkFilterPatrName)
        TMKWindow.setTabOrder(self.chkFilterPatrName, self.edtFilterPatrName)
        TMKWindow.setTabOrder(self.edtFilterPatrName, self.chkFilterBirthDay)
        TMKWindow.setTabOrder(self.chkFilterBirthDay, self.edtFilterBegBirthDay)
        TMKWindow.setTabOrder(self.edtFilterBegBirthDay, self.chkFilterEndBirthDay)
        TMKWindow.setTabOrder(self.chkFilterEndBirthDay, self.edtFilterEndBirthDay)
        TMKWindow.setTabOrder(self.edtFilterEndBirthDay, self.chkFilterSex)
        TMKWindow.setTabOrder(self.chkFilterSex, self.cmbFilterSex)
        TMKWindow.setTabOrder(self.cmbFilterSex, self.chkFilterCategory)
        TMKWindow.setTabOrder(self.chkFilterCategory, self.cmbFilterCategory)
        TMKWindow.setTabOrder(self.cmbFilterCategory, self.chkFilterPerson)
        TMKWindow.setTabOrder(self.chkFilterPerson, self.cmbFilterPerson)
        TMKWindow.setTabOrder(self.cmbFilterPerson, self.cmbFilterStatus)
        TMKWindow.setTabOrder(self.cmbFilterStatus, self.chkFilterExCreateDate)
        TMKWindow.setTabOrder(self.chkFilterExCreateDate, self.edtFilterExBegCreateDate)
        TMKWindow.setTabOrder(self.edtFilterExBegCreateDate, self.edtFilterExEndCreateDate)
        TMKWindow.setTabOrder(self.edtFilterExEndCreateDate, self.buttonBoxFilter)

    def retranslateUi(self, TMKWindow):
        TMKWindow.setWindowTitle(_translate("TMKWindow", "Сервис телемедицины", None))
        self.lblRecordCount.setText(_translate("TMKWindow", "Список пуст", None))
        self.grpFilter.setTitle(_translate("TMKWindow", "Фильтр", None))
        self.chkFilterEndBirthDay.setText(_translate("TMKWindow", "по", None))
        self.chkFilterFirstName.setText(_translate("TMKWindow", "Имя", None))
        self.cmbFilterSex.setItemText(1, _translate("TMKWindow", "М", None))
        self.cmbFilterSex.setItemText(2, _translate("TMKWindow", "Ж", None))
        self.lblFilterStatus.setText(_translate("TMKWindow", "Статус", None))
        self.chkFilterSex.setText(_translate("TMKWindow", "Пол", None))
        self.chkFilterBirthDay.setText(_translate("TMKWindow", "Дата рожд", None))
        self.chkFilterPatrName.setText(_translate("TMKWindow", "Отчество", None))
        self.chkFilterCategory.setText(_translate("TMKWindow", "Профиль", None))
        self.lblFilterUrgency.setText(_translate("TMKWindow", "Срочность", None))
        self.chkFilterPerson.setText(_translate("TMKWindow", "Врач", None))
        self.chkFilterLastName.setText(_translate("TMKWindow", "Фамилия", None))
        self.chkDirection.setText(_translate("TMKWindow", "Целевое МО", None))
        self.tabFilter.setTabText(self.tabFilter.indexOf(self.tabFind), _translate("TMKWindow", "&Поиск", None))
        self.chkFilterExCreateDate.setText(_translate("TMKWindow", "Дата создания", None))
        self.tabFilter.setTabText(self.tabFilter.indexOf(self.tabFindEx), _translate("TMKWindow", "&Расширенный поиск", None))
        self.btnPrint.setText(_translate("TMKWindow", "Печать (F6)", None))
        self.btnPrint.setShortcut(_translate("TMKWindow", "F6", None))

from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from Reports.ReportBrowser import CReportBrowser
from library.DateEdit import CDateEdit
from library.DialogButtonBox import CApplyResetDialogButtonBox
from library.PrintTemplates import CPrintButton
from library.TableView import CTableView
from library.TextBrowser import CTextBrowser
from library.crbcombobox import CRBComboBox
