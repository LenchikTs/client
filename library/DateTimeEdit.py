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
from PyQt4.QtCore import Qt, SIGNAL, QDate, QDateTime, QEvent, QObject, QSize, QTime

from library.CalendarWidget      import CCalendarWidget
from library.adjustPopup import adjustPopupToWidget


class CDateValidator(QtGui.QValidator):
    def __init__(self, parent, format, canBeEmpty):
        QtGui.QValidator.__init__(self, parent)
        self.min=QDateTime(1900, 1, 1, 0, 0, 0)
        self.max=QDateTime(2099,12,31, 0, 0, 0)
        self.format=format
        self.canBeEmpty = canBeEmpty


    def inputIsEmpty(self, input):
        return not unicode(input).strip(' 0.-')


    def validate(self, input, pos):
        if self.inputIsEmpty(input):
            if self.canBeEmpty:
                return (QtGui.QValidator.Acceptable, pos)
            else:
                return (QtGui.QValidator.Intermediate, pos)
        else:
            d = QDateTime.fromString(input, self.format)
            if d.isValid():
                if self.min!=None and d<self.min:
                    return (QtGui.QValidator.Intermediate, pos)
                elif self.max!=None and d>self.max:
                    return (QtGui.QValidator.Intermediate, pos)
                else:
                    return (QtGui.QValidator.Acceptable, pos)
            else:
                return (QtGui.QValidator.Intermediate, pos)


    def fixup(self, input):
        if self.inputIsEmpty(input) and self.canBeEmpty:
            newInput = ''
        else:
            d = QDateTime.fromString(input, self.format)
            newInput = d.toString(self.format)
        if not newInput:
            input.clear()


class CCalendarPopup(QtGui.QFrame):
    def __init__(self, parent = None):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setAttribute(Qt.WA_WindowPropagation)
        self.initialDate = QDateTime()
        self.dateChanged = False
        self.calendar = CCalendarWidget(self)
        self.calendar.setVerticalHeaderFormat(QtGui.QCalendarWidget.NoVerticalHeader)
        self.widgetLayout = QtGui.QVBoxLayout(self)
        self.widgetLayout.setMargin(0)
        self.widgetLayout.setSpacing(0)
        self.widgetLayout.addWidget(self.calendar)
        self.connect(self.calendar, SIGNAL('activated(QDate)'), self.dateSelected)
        self.connect(self.calendar, SIGNAL('clicked(QDate)'), self.dateSelectionChanged)
        self.connect(self.calendar, SIGNAL('selectionChanged()'), self.dateSelectionChanged)
        self.connect(self.calendar, SIGNAL('newDateSelected(QDate)'), self.dateSelectionChanged)
        self.calendar.setFocus()


    def setInitialDate(self, date):
        self.initialDate = date
        self.dateChanged = False
        self.calendar.setSelectedDate(date)


    def dateSelected(self, date):
        self.dateChanged=True
        self.emit(SIGNAL('activated(QDate)'), date)
        self.close()


    def mousePressEvent(self, event):
        dateTime = self.parentWidget()
        if dateTime!=None:
            opt=QtGui.QStyleOptionComboBox()
            opt.init(dateTime)
            arrowRect = dateTime.style().subControlRect(
                QtGui.QStyle.CC_ComboBox, opt, QtGui.QStyle.SC_ComboBoxArrow, dateTime)
            arrowRect.moveTo(dateTime.mapToGlobal(arrowRect.topLeft()))
            if (arrowRect.contains(event.globalPos()) or self.rect().contains(event.pos())):
                self.setAttribute(Qt.WA_NoMouseReplay)
        QtGui.QFrame.mousePressEvent(self, event)


    def mouseReleaseEvent(self, event):
        self.parent().mouseReleaseEvent(event)
        pass


    def event(self, event):
        if event.type()==QEvent.KeyPress:
            if event.key()==Qt.Key_Escape:
                self.dateChanged = False
        return QtGui.QFrame.event(self, event)


    def dateSelectionChanged(self):
        self.dateChanged=True
        self.emit(SIGNAL('newDateSelected(QDate)'), self.calendar.selectedDate())


    def hideEvent(self, event):
        if not self.dateChanged:
            self.dateSelected(self.initialDate)


class CDateTimeEdit(QtGui.QComboBox):
    __pyqtSignals__ = ('dateChanged(const QDateTime &)',
                      )

    def __init__(self, parent = None):
        QtGui.QComboBox.__init__(self, parent)
        self.setMinimumContentsLength(10)
        self.highlightRedDate = QtGui.qApp.highlightRedDate()
        self.lineEdit=QtGui.QLineEdit()
        self.lineEdit.setInputMask('99.99.9999 00:00')
        self.validator=CDateValidator(self, 'dd.MM.yyyy HH:mm', False)
        self.lineEdit.setValidator(self.validator)
        self.setLineEdit(self.lineEdit)
        self.lineEdit.setText(QDateTime.currentDateTime().toString(self.validator.format))
        self.lineEdit.setCursorPosition(0)
        width = self.lineEdit.minimumSizeHint().width() * 4
        height = self.lineEdit.minimumSizeHint().height() * 1.2
        self.setMinimumSize(width, height)
        self.calendarPopup=None
        self.connect(self.lineEdit, SIGNAL('textEdited(QString)'), self.onTextChange)


    def minimumDate(self):
        return self.validator.min


    def setMinimumDate(self, min):
        if isinstance(min, QDateTime) and min.isValid():
            max =self.validator.max
            if max.isValid() and max<min:
                max = min
            self.setDateRange(min, max)


    def clearMinimumDate(self):
        self.setMinimumDate(QDateTime())


    def maximumDate(self):
        return self.validator.max


    def setMaximumDate(self, max):
        if isinstance(max, QDateTime) and max.isValid():
            min=self.validator.min
            if min.isValid() and min>max:
                min=max
            self.setDateRange(min, max)


    def clearMaximumDate(self):
        self.setMaximumDate(QDateTime())


    def setDateRange(self, min, max):
        if  isinstance(min, QDateTime) and isinstance(max, QDateTime) and min.isValid() and max.isValid():
            self.validator.min=min
            self.validator.max=max


    def displayFormat(self):
        return self.format()


    def setDisplayFormat(self, format):
        self.setFormat(format)


    def format(self):
        return self.validator.format


    def setFormat(self, format):
        self.validator.format=format


    def canBeEmpty(self, value=True):
        self.validator.canBeEmpty = value


    def setHighlightRedDate(self, value=True):
        self.highlightRedDate = value and QtGui.qApp.highlightRedDate()


    def setCalendarPopup(self, value=True):
        pass


    def showPopup(self):
        if not self.calendarPopup:
            self.calendarPopup = CCalendarPopup(self)
            #self.connect(self.calendarPopup, SIGNAL('newDateSelected(QDate)'), self.setDate)  #Иначе обработчик вызывается по 3 раза.
            self.connect(self.calendarPopup, SIGNAL('activated(QDate)'), self.setDate)
            #self.connect(self.calendarPopup, SIGNAL('activated(QDate)'), self.calendarPopup.close) #Иначе обработчик вызывается по 3 раза.

        self.calendarPopup.calendar.setMinimumDate(self.minimumDate().date())
        self.calendarPopup.calendar.setMaximumDate(self.maximumDate().date())
        datetime = self.date()
        date = datetime.date()
        if not date:
            date = QDate.currentDate()
        self.calendarPopup.setInitialDate(date)
        adjustPopupToWidget(self, self.calendarPopup, True)
        self.calendarPopup.show()


    def setDate(self, date):
        if isinstance(date, QDateTime):
            newDate = date
        else:
            if date == QDate.currentDate():
                newDate = QDateTime(date, QTime.currentTime())
            else:
                newDate = QDateTime(date, QTime())
        if newDate is None:
            newDate = QDateTime()
        self.setColor(newDate)
        self.lineEdit.setText(newDate.toString(self.validator.format))
        self.lineEdit.setCursorPosition(0)
        self.emit(SIGNAL('dateChanged(QDateTime)'), newDate)


    def setColor(self, date):
        palette = QtGui.QPalette()
        if self.highlightRedDate and date.date() and QtGui.qApp.calendarInfo.getDayOfWeek(date.date()) in (6,7):
            palette.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 0, 0))
        self.lineEdit.setPalette(palette)


    def setInvalidColor(self):
        palette = QtGui.QPalette()
        if QtGui.qApp.highlightInvalidDate():
            palette.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 0, 255))
        self.lineEdit.setPalette(palette)


    def selectAll(self):
        self.lineEdit.selectAll()
        self.lineEdit.setCursorPosition(0)


    def setCursorPosition(self,  pos=0):
        self.lineEdit.setCursorPosition(pos)


    def text(self):
        return self.lineEdit.text()


    def date(self):
        return QDateTime.fromString(self.text(), self.validator.format)


    def onTextChange(self, text):
        state, pos = self.validator.validate(self.text(), 0)
        if state == QtGui.QValidator.Acceptable:
            date = self.date()
            self.setColor(date)
            self.emit(SIGNAL('dateChanged(QDateTime)'), date)
        else:
            if not unicode(text).replace('.', ''):
                self.emit(SIGNAL('dateChanged(QDateTime)'), QDateTime())
            self.setInvalidColor()


    def currentSection(self):
        pos = self.lineEdit.cursorPosition()
        if pos>=6:
            return QtGui.QDateTimeEdit.YearSection
        elif pos>=3:
            return QtGui.QDateTimeEdit.MonthSection
        else:
            return QtGui.QDateTimeEdit.DaySection


    def event(self, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Equal or (key == Qt.Key_Space and not self.date().isValid()):
                    self.setDate(QDateTime.currentDateTime())
                    event.accept()
                    return True
            if key in (Qt.Key_Plus, Qt.Key_Minus):
                d = self.date()
                if not d.isValid():
                    d = QDateTime.currentDateTime()
                step = 1 if key  == Qt.Key_Plus else -1
                if self.currentSection() == QtGui.QDateTimeEdit.YearSection:
                    d = d.addYears(step)
                elif self.currentSection() == QtGui.QDateTimeEdit.MonthSection:
                    d = d.addMonths(step)
                else:
                    d = d.addDays(step)
                pos = self.lineEdit.cursorPosition()
                self.setDate(d)
                self.lineEdit.setCursorPosition(pos)
                event.accept()
                return True
        return QtGui.QComboBox.event(self, event)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dialog = QtGui.QDialog()
    gridlayout = QtGui.QGridLayout(dialog)
    gridlayout.setMargin(9)
    gridlayout.setSpacing(6)
    cv = CDateTimeEdit(dialog)
    gridlayout.addWidget(cv,0,0,1,1)
    out = QtGui.QLabel()
    gridlayout.addWidget(out,1,0,1,1)
    dialog.resize(QSize(300, 300))
    out.setText('00.00.0000 00:00')
    le=cv.lineEdit
    QObject.connect(le,SIGNAL("returnPressed()"), lambda :(out.setText(le.text())))
    dialog.show()
    sys.exit(app.exec_())
