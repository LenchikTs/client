# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Resources/TreatmentAppointmentDialog.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_TreatmentAppointmentDialog(object):
    def setupUi(self, TreatmentAppointmentDialog):
        TreatmentAppointmentDialog.setObjectName(_fromUtf8("TreatmentAppointmentDialog"))
        TreatmentAppointmentDialog.resize(871, 796)
        self.gridLayout_5 = QtGui.QGridLayout(TreatmentAppointmentDialog)
        self.gridLayout_5.setMargin(4)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.splitter_2 = QtGui.QSplitter(TreatmentAppointmentDialog)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.tblEvents = CTableView(self.widget)
        self.tblEvents.setObjectName(_fromUtf8("tblEvents"))
        self.gridLayout.addWidget(self.tblEvents, 1, 0, 1, 1)
        self.widget_2 = QtGui.QWidget(self.splitter)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.widget_2)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_5 = QtGui.QLabel(self.widget_2)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.tblSchedule = CTableView(self.widget_2)
        self.tblSchedule.setObjectName(_fromUtf8("tblSchedule"))
        self.gridLayout_2.addWidget(self.tblSchedule, 1, 0, 1, 1)
        self.widget_3 = QtGui.QWidget(self.splitter_2)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.widget_3)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.splitter_3 = QtGui.QSplitter(self.widget_3)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName(_fromUtf8("splitter_3"))
        self.calendar = QtGui.QCalendarWidget(self.splitter_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendar.sizePolicy().hasHeightForWidth())
        self.calendar.setSizePolicy(sizePolicy)
        self.calendar.setObjectName(_fromUtf8("calendar"))
        self.tblResources = CTreatmentResourcesInDocTableView(self.splitter_3)
        self.tblResources.setObjectName(_fromUtf8("tblResources"))
        self.gridLayout_3.addWidget(self.splitter_3, 1, 0, 1, 1)
        self.label = QtGui.QLabel(self.widget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.widget_4 = QtGui.QWidget(self.splitter_2)
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        self.gridLayout_4 = QtGui.QGridLayout(self.widget_4)
        self.gridLayout_4.setMargin(4)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_9 = QtGui.QLabel(self.widget_4)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_4.addWidget(self.label_9, 0, 0, 1, 1)
        self.tblActions = CTreatmentActionsTableView(self.widget_4)
        self.tblActions.setObjectName(_fromUtf8("tblActions"))
        self.gridLayout_4.addWidget(self.tblActions, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.splitter_2, 0, 0, 1, 2)
        self.lblCountEvents = QtGui.QLabel(TreatmentAppointmentDialog)
        self.lblCountEvents.setObjectName(_fromUtf8("lblCountEvents"))
        self.gridLayout_5.addWidget(self.lblCountEvents, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(TreatmentAppointmentDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_5.addWidget(self.buttonBox, 1, 1, 1, 1)

        self.retranslateUi(TreatmentAppointmentDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TreatmentAppointmentDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TreatmentAppointmentDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TreatmentAppointmentDialog)

    def retranslateUi(self, TreatmentAppointmentDialog):
        TreatmentAppointmentDialog.setWindowTitle(_translate("TreatmentAppointmentDialog", "Назначение мероприятий по циклам", None))
        self.label_4.setText(_translate("TreatmentAppointmentDialog", "Список проживающих", None))
        self.label_5.setText(_translate("TreatmentAppointmentDialog", "Календарь назначений", None))
        self.label.setText(_translate("TreatmentAppointmentDialog", "Доступные ресурсы", None))
        self.label_9.setText(_translate("TreatmentAppointmentDialog", "Состав группы", None))
        self.lblCountEvents.setText(_translate("TreatmentAppointmentDialog", "Контингент всего: 0.  Контингент в группе: 0", None))

from Resources.TreatmentActionsTableView import CTreatmentActionsTableView
from Resources.TreatmentResourcesInDocTableView import CTreatmentResourcesInDocTableView
from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TreatmentAppointmentDialog = QtGui.QDialog()
    ui = Ui_TreatmentAppointmentDialog()
    ui.setupUi(TreatmentAppointmentDialog)
    TreatmentAppointmentDialog.show()
    sys.exit(app.exec_())

