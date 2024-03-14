# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDateTime, QIODevice, QVariant

from library.crbcombobox import CRBComboBox
from library.Utils import ( forceDate,
                            forceDouble,
                            forceInt,
                            forceRef,
                            forceString,
                            oops,
                            toVariant,
                          )


__all__ = [ 'getCheckBoxValue',
            'setCheckBoxValue',
            'getComboBoxData',
            'setComboBoxData',
            'getComboBoxValue',
            'setComboBoxValue',
            'getDateEditValue',
            'setDateEditValue',
            'getDatetimeEditValue',
            'setDatetimeEditValue',
            'getDbComboBoxTextValue',
            'setDbComboBoxTextValue',
            'getDoubleBoxValue',
            'setDoubleBoxValue',
            'getLabelImageValue',
            'setLabelImageValue',
            'getLabelText',
            'setLabelText',
            'getLineEditValue',
            'setLineEditValue',
            'getRadioButtonValue',
            'setRadioButtonValue',
            'getRBComboBoxValue',
            'setRBComboBoxValue',
            'getRBMultivalueComboBoxValue',
            'setRBMultivalueComboBoxValue',
            'getSpinBoxValue',
            'setSpinBoxValue',
            'getTextEditHTML',
            'setTextEditHTML',
            'getTextEditValue',
            'setTextEditValue',
            'getWidgetValue',
            'setWidgetValue',
          ]


def getCheckBoxValue(checkBox, record, fieldName):
    record.setValue(fieldName, QVariant(1 if checkBox.isChecked() else 0))


def setCheckBoxValue(checkBox, record, fieldName):
    checkBox.setChecked(forceInt(record.value(fieldName))!=0)


def getComboBoxData(comboBox, record, fieldName):
    record.setValue(fieldName, comboBox.itemData(comboBox.currentIndex()))


def setComboBoxData(comboBox, record, fieldName):
    comboBox.setCurrentIndex(comboBox.findData(record.value(fieldName)))


def getComboBoxValue(comboBox, record, fieldName):
    record.setValue(fieldName, QVariant(comboBox.currentIndex()))


def setComboBoxValue(comboBox, record, fieldName):
    comboBox.setCurrentIndex(forceInt(record.value(fieldName)))


def getDateEditValue(dateEdit, record, fieldName):
    record.setValue(fieldName, toVariant(dateEdit.date()))


def setDateEditValue(dateEdit, record, fieldName):
    dateEdit.setDate(forceDate(record.value(fieldName)))


def getDatetimeEditValue(dateEdit, timeEdit, record, fieldName, useTime):
    date = dateEdit.date()
    if date:
        if useTime:
            value = QDateTime(date, timeEdit.time())
        else:
            value = QDateTime(date)
    else:
        value = QDateTime()
    record.setValue(fieldName, QVariant(value))


def setDatetimeEditValue(dateEdit, timeEdit, record, fieldName):
    value = record.value(fieldName).toDateTime()
    dateEdit.setDate(value.date())
    timeEdit.setTime(value.time())


def getDbComboBoxTextValue(comboBox, record, fieldName):
    record.setValue(fieldName, toVariant(comboBox.text()))


def setDbComboBoxTextValue(comboBox, record, fieldName):
    comboBox.setText(forceString(record.value(fieldName)))


def getDoubleBoxValue(spinBox, record, fieldName):
    record.setValue(fieldName, QVariant(spinBox.value()))


def setDoubleBoxValue(spinBox, record, fieldName):
    spinBox.setValue(forceDouble(record.value(fieldName)))


#def getLabelImageValue(image, record, fieldName, tableName):
#    if image:
#        image.open(QIODevice.ReadOnly)
#        ba = image.readAll()
#        image.close()
#        stmt = QString()
#        db = QtGui.qApp.db
#        db.insertOrUpdate(db.table(tableName), record)
#        stream = QTextStream(stmt, QIODevice.WriteOnly)
#        stream << ('UPDATE %s SET image=x\'' % tableName)
#        stream << ba.toHex()
#        stream << ('\' WHERE id=\'%d\'' %(forceInt(record.value('id'))))
#        db.query(stmt)

def getLabelImageValue(image, record, fieldName):
    if image:
        image.open(QIODevice.ReadOnly)
        ba = image.readAll()
        image.close()
        record.setValue(fieldName, QVariant(ba))


def setLabelImageValue(label, record, fieldName):
    ba = record.value(fieldName).toByteArray()
    image = QtGui.QImage().fromData(ba)
    pixmap = QtGui.QPixmap().fromImage(image)
    label.setGeometry(0, 0,
                      pixmap.size().width(),
                      pixmap.size().height())
    label.setPixmap(pixmap)


def getLabelText(label, record, fieldName):
    record.setValue(fieldName, QVariant(label.text()))


def setLabelText(label, record, fieldName):
    label.setTextFormat(Qt.PlainText)
    label.setText(record.value(fieldName).toString())


def getLineEditValue(lineEdit, record, fieldName):
    record.setValue(fieldName, QVariant(lineEdit.text().simplified()))


def setLineEditValue(lineEdit, record, fieldName):
    lineEdit.setText(record.value(fieldName).toString())
    lineEdit.setCursorPosition(0)


def getRadioButtonValue(radioButtons, record, fieldName):
    if isinstance(radioButtons, QtGui.QButtonGroup):
        value = radioButtons.checkedId()
        if not radioButtons.button(value):
            value = None
        record.setValue(fieldName, value)
    else:
        oops()


def setRadioButtonValue(radioButtons, record, fieldName):
    value = forceInt(record.value(fieldName))
    if isinstance(radioButtons, QtGui.QButtonGroup):
        button = radioButtons.button(value)
        if button:
            button.setChecked(True)
    else:
        oops()


def getRBComboBoxValue(comboBox, record, fieldName):
    record.setValue(fieldName, toVariant(comboBox.value()))


def setRBComboBoxValue(comboBox, record, fieldName):
    comboBox.setValue(forceRef(record.value(fieldName)))


def getRBMultivalueComboBoxValue(comboBox, record, fieldName):
    record.setValue(fieldName, toVariant(comboBox.value()))


def setRBMultivalueComboBoxValue(comboBox, record, fieldName):
    comboBox.setValue(forceString(record.value(fieldName)))


def getSpinBoxValue(spinBox, record, fieldName):
    record.setValue(fieldName, QVariant(spinBox.value()))


def setSpinBoxValue(spinBox, record, fieldName):
    spinBox.setValue(forceInt(record.value(fieldName)))


def getTextEditHTML(textEdit, record, fieldName):
    record.setValue(fieldName, QVariant(textEdit.toHtml()))


def setTextEditHTML(textEdit, record, fieldName):
    textEdit.setHtml(record.value(fieldName).toString())
#    textEdit.setPosition(0, QtGui.QTextCursor.MoveAnchor)


def getTextEditValue(textEdit, record, fieldName):
    record.setValue(fieldName, QVariant(textEdit.toPlainText()))


def setTextEditValue(textEdit, record, fieldName):
    textEdit.setPlainText(record.value(fieldName).toString())


def getWidgetValue(widget, record, fieldName):
    if isinstance(widget, QtGui.QLineEdit):
        getLineEditValue(widget, record, fieldName)
    elif isinstance(widget, CRBComboBox):
        getRBComboBoxValue(widget, record, fieldName)
    elif isinstance(widget, QtGui.QDateEdit):
        getDateEditValue(widget, record, fieldName)
    elif isinstance(widget, QtGui.QSpinBox):
        getSpinBoxValue(widget, record, fieldName)
    elif isinstance(widget, QtGui.QCheckBox):
        getCheckBoxValue(widget, record, fieldName)
    else:
        oops()


def setWidgetValue(widget, record, fieldName):
    if isinstance(widget, QtGui.QLineEdit):
        setLineEditValue(widget, record, fieldName)
    elif isinstance(widget, CRBComboBox):
        setRBComboBoxValue(widget, record, fieldName)
    elif isinstance(widget, QtGui.QDateEdit):
        setDateEditValue(widget, record, fieldName)
    elif isinstance(widget, QtGui.QSpinBox):
        setSpinBoxValue(widget, record, fieldName)
    elif isinstance(widget, QtGui.QCheckBox):
        setCheckBoxValue(widget, record, fieldName)
    else:
        oops()
