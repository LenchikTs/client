# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EventNotesPageProtocol.ui'
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

class Ui_EventNotesPageWidget(object):
    def setupUi(self, EventNotesPageWidget):
        EventNotesPageWidget.setObjectName(_fromUtf8("EventNotesPageWidget"))
        EventNotesPageWidget.resize(748, 455)
        self.gridLayoutEventNotes = QtGui.QGridLayout(EventNotesPageWidget)
        self.gridLayoutEventNotes.setMargin(4)
        self.gridLayoutEventNotes.setSpacing(4)
        self.gridLayoutEventNotes.setObjectName(_fromUtf8("gridLayoutEventNotes"))
        self.lblEventModifyDateTime = QtGui.QLabel(EventNotesPageWidget)
        self.lblEventModifyDateTime.setObjectName(_fromUtf8("lblEventModifyDateTime"))
        self.gridLayoutEventNotes.addWidget(self.lblEventModifyDateTime, 3, 0, 1, 1)
        self.lblEventCreateDateTimeValue = QtGui.QLabel(EventNotesPageWidget)
        self.lblEventCreateDateTimeValue.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblEventCreateDateTimeValue.setFrameShadow(QtGui.QFrame.Sunken)
        self.lblEventCreateDateTimeValue.setText(_fromUtf8(""))
        self.lblEventCreateDateTimeValue.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lblEventCreateDateTimeValue.setObjectName(_fromUtf8("lblEventCreateDateTimeValue"))
        self.gridLayoutEventNotes.addWidget(self.lblEventCreateDateTimeValue, 1, 1, 1, 2)
        self.lblEventCreateDateTime = QtGui.QLabel(EventNotesPageWidget)
        self.lblEventCreateDateTime.setObjectName(_fromUtf8("lblEventCreateDateTime"))
        self.gridLayoutEventNotes.addWidget(self.lblEventCreateDateTime, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 206, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayoutEventNotes.addItem(spacerItem, 7, 0, 1, 1)
        self.lblEventCreatePersonValue = QtGui.QLabel(EventNotesPageWidget)
        self.lblEventCreatePersonValue.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblEventCreatePersonValue.setFrameShadow(QtGui.QFrame.Sunken)
        self.lblEventCreatePersonValue.setText(_fromUtf8(""))
        self.lblEventCreatePersonValue.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lblEventCreatePersonValue.setObjectName(_fromUtf8("lblEventCreatePersonValue"))
        self.gridLayoutEventNotes.addWidget(self.lblEventCreatePersonValue, 2, 1, 1, 2)
        self.lblEventNote = QtGui.QLabel(EventNotesPageWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblEventNote.sizePolicy().hasHeightForWidth())
        self.lblEventNote.setSizePolicy(sizePolicy)
        self.lblEventNote.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblEventNote.setObjectName(_fromUtf8("lblEventNote"))
        self.gridLayoutEventNotes.addWidget(self.lblEventNote, 6, 0, 1, 1)
        self.edtEventNote = QtGui.QTextEdit(EventNotesPageWidget)
        self.edtEventNote.setObjectName(_fromUtf8("edtEventNote"))
        self.gridLayoutEventNotes.addWidget(self.edtEventNote, 6, 1, 2, 2)
        self.lblEventModifyPersonValue = QtGui.QLabel(EventNotesPageWidget)
        self.lblEventModifyPersonValue.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblEventModifyPersonValue.setFrameShadow(QtGui.QFrame.Sunken)
        self.lblEventModifyPersonValue.setText(_fromUtf8(""))
        self.lblEventModifyPersonValue.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lblEventModifyPersonValue.setObjectName(_fromUtf8("lblEventModifyPersonValue"))
        self.gridLayoutEventNotes.addWidget(self.lblEventModifyPersonValue, 4, 1, 1, 2)
        self.lblEventIdValue = QtGui.QLabel(EventNotesPageWidget)
        self.lblEventIdValue.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblEventIdValue.setFrameShadow(QtGui.QFrame.Sunken)
        self.lblEventIdValue.setText(_fromUtf8(""))
        self.lblEventIdValue.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lblEventIdValue.setObjectName(_fromUtf8("lblEventIdValue"))
        self.gridLayoutEventNotes.addWidget(self.lblEventIdValue, 0, 1, 1, 2)
        self.lblEventModifyDateTimeValue = QtGui.QLabel(EventNotesPageWidget)
        self.lblEventModifyDateTimeValue.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblEventModifyDateTimeValue.setFrameShadow(QtGui.QFrame.Sunken)
        self.lblEventModifyDateTimeValue.setText(_fromUtf8(""))
        self.lblEventModifyDateTimeValue.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lblEventModifyDateTimeValue.setObjectName(_fromUtf8("lblEventModifyDateTimeValue"))
        self.gridLayoutEventNotes.addWidget(self.lblEventModifyDateTimeValue, 3, 1, 1, 2)
        self.lblEventId = QtGui.QLabel(EventNotesPageWidget)
        self.lblEventId.setObjectName(_fromUtf8("lblEventId"))
        self.gridLayoutEventNotes.addWidget(self.lblEventId, 0, 0, 1, 1)
        self.lblEventModifyPerson = QtGui.QLabel(EventNotesPageWidget)
        self.lblEventModifyPerson.setObjectName(_fromUtf8("lblEventModifyPerson"))
        self.gridLayoutEventNotes.addWidget(self.lblEventModifyPerson, 4, 0, 1, 1)
        self.lblEventCreatePerson = QtGui.QLabel(EventNotesPageWidget)
        self.lblEventCreatePerson.setObjectName(_fromUtf8("lblEventCreatePerson"))
        self.gridLayoutEventNotes.addWidget(self.lblEventCreatePerson, 2, 0, 1, 1)
        self.lblIsClosed = QtGui.QLabel(EventNotesPageWidget)
        self.lblIsClosed.setObjectName(_fromUtf8("lblIsClosed"))
        self.gridLayoutEventNotes.addWidget(self.lblIsClosed, 5, 0, 1, 1)
        self.chkIsClosed = QtGui.QCheckBox(EventNotesPageWidget)
        self.chkIsClosed.setText(_fromUtf8(""))
        self.chkIsClosed.setObjectName(_fromUtf8("chkIsClosed"))
        self.gridLayoutEventNotes.addWidget(self.chkIsClosed, 5, 1, 1, 1)
        self.lblEventNote.setBuddy(self.edtEventNote)

        self.retranslateUi(EventNotesPageWidget)
        QtCore.QMetaObject.connectSlotsByName(EventNotesPageWidget)
        EventNotesPageWidget.setTabOrder(self.chkIsClosed, self.edtEventNote)

    def retranslateUi(self, EventNotesPageWidget):
        EventNotesPageWidget.setWindowTitle(_translate("EventNotesPageWidget", "Form", None))
        self.lblEventModifyDateTime.setText(_translate("EventNotesPageWidget", "Дата и время последнего изменения", None))
        self.lblEventCreateDateTime.setText(_translate("EventNotesPageWidget", "Дата и время создания", None))
        self.lblEventNote.setText(_translate("EventNotesPageWidget", "Примечания", None))
        self.lblEventId.setText(_translate("EventNotesPageWidget", "Идентификатор записи", None))
        self.lblEventModifyPerson.setText(_translate("EventNotesPageWidget", "Автор последнего изменения", None))
        self.lblEventCreatePerson.setText(_translate("EventNotesPageWidget", "Автор", None))
        self.lblIsClosed.setText(_translate("EventNotesPageWidget", "Событие закрыто", None))

