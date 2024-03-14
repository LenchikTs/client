# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\DataCheck\WarningControlDublesDialog.ui'
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

class Ui_WarningControlDublesDialog(object):
    def setupUi(self, WarningControlDublesDialog):
        WarningControlDublesDialog.setObjectName(_fromUtf8("WarningControlDublesDialog"))
        WarningControlDublesDialog.setWindowModality(QtCore.Qt.NonModal)
        WarningControlDublesDialog.resize(600, 401)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WarningControlDublesDialog.sizePolicy().hasHeightForWidth())
        WarningControlDublesDialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(WarningControlDublesDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblInformationTextDoubleCancel = QtGui.QLabel(WarningControlDublesDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblInformationTextDoubleCancel.setFont(font)
        self.lblInformationTextDoubleCancel.setAlignment(QtCore.Qt.AlignCenter)
        self.lblInformationTextDoubleCancel.setWordWrap(True)
        self.lblInformationTextDoubleCancel.setObjectName(_fromUtf8("lblInformationTextDoubleCancel"))
        self.gridLayout.addWidget(self.lblInformationTextDoubleCancel, 1, 0, 1, 3)
        self.btnOkCancel = QtGui.QDialogButtonBox(WarningControlDublesDialog)
        self.btnOkCancel.setEnabled(True)
        self.btnOkCancel.setOrientation(QtCore.Qt.Horizontal)
        self.btnOkCancel.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.btnOkCancel.setCenterButtons(False)
        self.btnOkCancel.setObjectName(_fromUtf8("btnOkCancel"))
        self.gridLayout.addWidget(self.btnOkCancel, 2, 0, 1, 3)
        self.scrollArea = QtGui.QScrollArea(WarningControlDublesDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 586, 333))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout_2 = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lblInformationTextTitle = QtGui.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.lblInformationTextTitle.setFont(font)
        self.lblInformationTextTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lblInformationTextTitle.setWordWrap(True)
        self.lblInformationTextTitle.setIndent(-1)
        self.lblInformationTextTitle.setObjectName(_fromUtf8("lblInformationTextTitle"))
        self.gridLayout_2.addWidget(self.lblInformationTextTitle, 0, 0, 1, 1)
        self.lblInformationTextBaseLineTitle = QtGui.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblInformationTextBaseLineTitle.setFont(font)
        self.lblInformationTextBaseLineTitle.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lblInformationTextBaseLineTitle.setWordWrap(True)
        self.lblInformationTextBaseLineTitle.setObjectName(_fromUtf8("lblInformationTextBaseLineTitle"))
        self.gridLayout_2.addWidget(self.lblInformationTextBaseLineTitle, 1, 0, 1, 1)
        self.splitter = QtGui.QSplitter(self.scrollAreaWidgetContents)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.lblInformationTextBaseLine = QtGui.QLabel(self.splitter)
        self.lblInformationTextBaseLine.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lblInformationTextBaseLine.setWordWrap(True)
        self.lblInformationTextBaseLine.setIndent(10)
        self.lblInformationTextBaseLine.setObjectName(_fromUtf8("lblInformationTextBaseLine"))
        self.lblInformationTextDoubleLineTitle = QtGui.QLabel(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblInformationTextDoubleLineTitle.sizePolicy().hasHeightForWidth())
        self.lblInformationTextDoubleLineTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblInformationTextDoubleLineTitle.setFont(font)
        self.lblInformationTextDoubleLineTitle.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lblInformationTextDoubleLineTitle.setWordWrap(True)
        self.lblInformationTextDoubleLineTitle.setObjectName(_fromUtf8("lblInformationTextDoubleLineTitle"))
        self.lblInformationTextDoubleLine = QtGui.QLabel(self.splitter)
        self.lblInformationTextDoubleLine.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lblInformationTextDoubleLine.setWordWrap(True)
        self.lblInformationTextDoubleLine.setIndent(10)
        self.lblInformationTextDoubleLine.setObjectName(_fromUtf8("lblInformationTextDoubleLine"))
        self.gridLayout_2.addWidget(self.splitter, 2, 0, 1, 1)
        self.btnSelectBaseLine = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.btnSelectBaseLine.setObjectName(_fromUtf8("btnSelectBaseLine"))
        self.gridLayout_2.addWidget(self.btnSelectBaseLine, 3, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 3)

        self.retranslateUi(WarningControlDublesDialog)
        QtCore.QObject.connect(self.btnOkCancel, QtCore.SIGNAL(_fromUtf8("accepted()")), WarningControlDublesDialog.accept)
        QtCore.QObject.connect(self.btnOkCancel, QtCore.SIGNAL(_fromUtf8("rejected()")), WarningControlDublesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(WarningControlDublesDialog)

    def retranslateUi(self, WarningControlDublesDialog):
        WarningControlDublesDialog.setWindowTitle(_translate("WarningControlDublesDialog", "Внимание!", None))
        self.lblInformationTextDoubleCancel.setText(_translate("WarningControlDublesDialog", "Подтвердите эти действия.", None))
        self.lblInformationTextTitle.setText(_translate("WarningControlDublesDialog", "Будет произведено удаление дублей.", None))
        self.lblInformationTextBaseLineTitle.setText(_translate("WarningControlDublesDialog", "За основную взята строка:", None))
        self.lblInformationTextBaseLine.setText(_translate("WarningControlDublesDialog", "Нет строки!", None))
        self.lblInformationTextDoubleLineTitle.setText(_translate("WarningControlDublesDialog", "Следующие дубли будут удалены, вся связанная с ними информация, вкючая сведения о группе крови, медикаментозной непереносимости, аллергиях и др., будет уничтожена, соответствующие дублям  диагнозы ЛУДа и события будут связаны с клиентом базовой строки:", None))
        self.lblInformationTextDoubleLine.setText(_translate("WarningControlDublesDialog", "Нет строки!", None))
        self.btnSelectBaseLine.setText(_translate("WarningControlDublesDialog", "Изменить базовую строку", None))

