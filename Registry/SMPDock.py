# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtSql
from PyQt4.QtCore import *

from collections import namedtuple

from library.JsonRpc.client   import CJsonRpcClent
from library.Utils            import *
from library.DockWidget       import CDockWidget
from library.DialogBase       import CConstructHelperMixin
from library.PreferencesMixin import *
from Events.Action            import *
from Registry.Utils           import *
from SMPAddEventDialog        import CSMPAddEventDialog
from types import NoneType

from Ui_SMPDockContent   import Ui_Form


class CSMPDockWidget(CDockWidget):
    def __init__(self, parent):
        CDockWidget.__init__(self, parent)
        self.setWindowTitle(u'СМП')
        self.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.content = None
        self.contentPreferences = {}
        self.connect(QtGui.qApp, QtCore.SIGNAL('dbConnectionChanged(bool)'), self.onConnectionChanged)


    def loadPreferences(self, preferences):
        self.contentPreferences = getPref(preferences, 'content', {})
        CDockWidget.loadPreferences(self, preferences)
        if isinstance(self.content, CPreferencesMixin):
            self.content.loadPreferences(self.contentPreferences)


    def savePreferences(self):
        result = CDockWidget.savePreferences(self)
        self.updateContentPreferences()
        setPref(result,'content',self.contentPreferences)
        return result


    def updateContentPreferences(self):
        if isinstance(self.content, CPreferencesMixin):
            self.contentPreferences = self.content.savePreferences()


    def onConnectionChanged(self, value):
        if value:
            self.onDBConnected()
        else:
            self.onDBDisconnected()


    def onDBConnected(self):
        self.setWidget(None)
        if self.content:
            self.content.setParent(None)
            self.content.deleteLater()
        self.content = CSMPDockContent(self)
        self.content.loadPreferences(self.contentPreferences)
        self.setWidget(self.content)
        self.emit(SIGNAL('contentCreated(QDockWidget*)'), self)


    def onDBDisconnected(self):
        self.setWidget(None)
        if self.content:
            self.updateContentPreferences()
            self.content.setParent(None)
            self.content.deleteLater()
        self.content = QtGui.QLabel(u'необходимо\nподключение\nк базе данных', self)
        self.content.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.content.setDisabled(True)
        self.setWidget(self.content)
        self.emit(SIGNAL('contentDestroyed(QDockWidget*)'), self)



class CSMPDockContent(QtGui.QWidget, Ui_Form, CConstructHelperMixin, CContainerPreferencesMixin):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.addModels('CallInfo', CCallInfoModel(self))
        self.setModels(self.tblCallInfo, self.modelCallInfo, self.selectionModelCallInfo)
        self.selectionModelCallInfo.currentRowChanged.connect(self.selectionChanged)
        self.modelCallInfo.modelReset.connect(self.selectionChanged)
        self.tblCallInfo.contextMenuEvent = self.tblCallInfoContextMenuEvent

        column = namedtuple('column', 'show, caption, sql')
        self.columns = [
            column(True,  u'Дата вызова',      u"callInfo.callDate"), 
            column(True,  u'Время звонка',     u"eventItem.eventTime"), 
            column(True,  u'Статус вызова',    u"eventType.name"), 
            column(True,  u'Фамилия',          u"callInfo.lastName"), 
            column(True,  u'Имя',              u"callInfo.name"), 
            column(True,  u'Отчество',         u"callInfo.patronymic"),
            column(True,  u'Вызов загружен ',  u"DATE_FORMAT(eventItem.createDateTime, '%d.%m.%y %H:%i')"),
            column(True,  u'Подтверждение получения', u"case eventItem.updEvent when 0 then 'Нет подтверждения' when 1 then 'Подтверждение отправлено' end"), 
            column(True,  u'Сообщение',        u"eventItem.note"), 
            column(True,  u'ФИО передавшего вызов', u"eventItem.transferUser"), 
            column(True,  u'Тип вызова',       u"case callInfo.Type when 0 then 'НМП' when 1 then '03' end"), 
            column(False, u'Пол',              u"callInfo.sex"), 
            column(False, u'Лет',              u"callInfo.ageYears"), 
            column(False, u'Месяцев',          u"callInfo.ageMonths"), 
            column(False, u'Дней',             u"callInfo.ageDays"), 
            column(False, u'Время приёма вызова', u"callInfo.endReceivingCall"), 
            column(False, u'Время окончания приёма вызова', u"callInfo.receptionEndingTime"), 
            column(False, u'Основной диагноз', u"callInfo.diseaseBasic"), 
            column(False, u'Результат выезда', u"callInfo.resultDeparture"), 
            column(False, u'Категория срочности вызова', u"callInfo.urgencyCategory"), 
            column(False, u'Вид вызова',       u"callInfo.callKind"), 
            column(False, u'Повод к вызову',   u"callInfo.callOccasion"), 
            column(False, u'Вызов повторный?', u"case callInfo.isRepeated when 0 then 'нет' when 1 then 'да' end"), 
            column(False, u'ФИО вызывающего',  u"callInfo.callerName"), 
            column(False, u'Место вызова',     u"callInfo.callPlace"), 
            column(False, u'ФИО принявшего вызов', u"callInfo.userReceiver"), 
            column(False, u'Населенный пункт', u"callInfo.settlement"), 
            column(False, u'Улица',            u"callInfo.street"), 
            column(False, u'Номер дома',       u"concat(cast(callInfo.house as char), case when char_length(callInfo.houseFract) > 0 then concat('/', callInfo.houseFract) else '' end)"), 
            column(False, u'Корпус',           u"callInfo.building"), 
            column(False, u'Квартира',         u"callInfo.flat"), 
            column(False, u'Подъезд',          u"callInfo.porch"), 
            column(False, u'Код домофона',     u"callInfo.porchCode"), 
            column(False, u'Этаж',             u"callInfo.floor"), 
            column(False, u'Ориентиры',        u"callInfo.landmarks"), 
            column(False, u'Телефон',          u"callInfo.telephone"), 
            column(False, u'rId',              u"eventItem.rId"), 
            column(False, u'updEvent',         u"eventItem.updEvent"), 
            column(False, u'OMS_CODE',         u"callInfo.OMS_CODE"), 
            column(False, u'idCallNumber',     u"callInfo.idCallNumber"), 
            column(False, u'Type',             u"callInfo.Type")
        ]
        
        self.addComboBoxItems(self.cmbEventType, u"select id, Name from smp_sprcalleventtype")
        self.addComboBoxItems(self.cmbOrganisation, u"""select bookkeeperCode,
                                                            concat(bookkeeperCode, ' - ', name) as name
                                                        from OrgStructure
                                                        where length(bookkeeperCode) > 0
                                                        order by bookkeeperCode, name""")

        self.updateCallList()
        
        for index, column in enumerate(self.columns):
            self.tblCallInfo.setColumnHidden(index, not column.show)
            
        self.refreshTimer = QTimer()
        self.refreshTimer.timeout.connect(self.getNewEvents)
        self.refreshTimer.start(1000 * 60)
        self.getNewEvents()
        
        self.addEventDialog = CSMPAddEventDialog(self)
        self.addComboBoxItems(self.addEventDialog.cmbEventType, u"select id, Name from smp_sprcalleventtype where eventAccess = 1 and isDeleted = 0")
            
    def tblCallInfoContextMenuEvent(self, event):
        self.menu = QtGui.QMenu(self)
        findClient = QtGui.QAction(u'Найти в картотеке', self)
        self.menu.addAction(findClient)
        findClient.triggered.connect(lambda: self.findClient(event))
        self.menu.popup(QtGui.QCursor.pos())

    def findClient(self, event):
        currentRow = self.tblCallInfo.currentRow()
        app = QtGui.qApp
        mainWindow = app.mainWindow
        if mainWindow.registry:
            if not isinstance(currentRow, NoneType):
                data = self.modelCallInfo.record(currentRow)
                lastName = forceString(data.value(u'Фамилия'))
                firstName = forceString(data.value(u'Имя'))
                patrName = forceString(data.value(u'Отчество'))
                mainWindow.registry.chkFilterLastName.setChecked(True)
                mainWindow.registry.chkFilterFirstName.setChecked(True)
                mainWindow.registry.chkFilterPatrName.setChecked(True)
                mainWindow.registry.edtFilterLastName.setText(lastName)
                mainWindow.registry.edtFilterFirstName.setText(firstName)
                mainWindow.registry.edtFilterPatrName.setText(patrName)
                mainWindow.registry.on_buttonBoxClient_apply()
        else:
            QtGui.QMessageBox.warning(self, u'Внимание!',
                                      u'Для поиска необходимо открыть окно картотеки!',
                                      QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

    def addComboBoxItems(self, comboBox, sql):
        query = QtGui.qApp.db.query(sql)
        while query.next():
            id   = query.value(0)
            name = query.value(1).toString()
            comboBox.addItem(name, id)

    def updateCallList(self):
        
        sql = u"""
            select %s
            from smp_callinfo as callInfo
                left join smp_eventitem as eventItem on eventItem.idCallNumber = callInfo.idCallNumber
                left join smp_sprcalleventtype as eventType on eventType.id = eventItem.idCallEventType
        """ % ', '.join(u"%s as `%s`" % (column.sql, column.caption) for column in self.columns)
        
        where = []
        
        where.append(u"callInfo.callDate = '%s'" % str(self.calDate.selectedDate().toString('yyyy-MM-dd')))

        where.append(u"callInfo.OMS_CODE = '%s'" % str(self.cmbOrganisation.itemData(self.cmbOrganisation.currentIndex()).toString()))
        
        typeList = []
        if self.chbNMP.isChecked():
            typeList.append(0)
        if self.chb03.isChecked():
            typeList.append(1)
        if typeList:
            where.append(u"callInfo.Type in (%s)" % ','.join(str(type) for type in typeList))
            
        if self.chbEventType.isChecked() and self.cmbEventType.currentIndex != 0:
            eventTypeId = self.cmbEventType.itemData(self.cmbEventType.currentIndex()).toInt()[0]
            where.append(u"eventItem.idCallEventType = %d" % eventTypeId)
            
        where = ' and '.join(where)
        if where:
            sql += " where " + where
            
        self.modelCallInfo.setQuery(sql)
        self.tblCallInfo.show()
        self.tblCallInfo.resizeColumnsToContents()
        
    def updateCalendarDates(self):
        self.calDate.setDateTextFormat(QDate(), QtGui.QTextCharFormat())
        db = QtGui.qApp.db
        
        sql = u"""select distinct callInfo.callDate 
            from smp_callinfo as callInfo
            left join smp_eventitem as eventItem on eventItem.idCallNumber = callInfo.idCallNumber
        """
        
        where = []
        
        where.append(u"callInfo.callDate is not null")
        
        where.append(u"callInfo.OMS_CODE = '%s'" % str(self.cmbOrganisation.itemData(self.cmbOrganisation.currentIndex()).toString()))
        
        typeList = []
        if self.chbNMP.isChecked():
            typeList.append(0)
        if self.chb03.isChecked():
            typeList.append(1)
        if typeList:
            where.append(u"callInfo.Type in (%s)" % ','.join(str(type) for type in typeList))
            
        if self.chbEventType.isChecked() and self.cmbEventType.currentIndex != 0:
            eventTypeId = self.cmbEventType.itemData(self.cmbEventType.currentIndex()).toInt()[0]
            where.append(u"eventItem.idCallEventType = %d" % eventTypeId)
            
        where = ' and '.join(where)
        if where:
            sql += " where " + where
        
        query = db.query(sql)
        bold = QtGui.QTextCharFormat()
        bold.setFontWeight(QtGui.QFont.Bold)
        while query.next():
            date = query.value(0).toDate()
            self.calDate.setDateTextFormat(date, bold)
        
    def canUpdEvent(self, record):
        rId = record.value(u'rId')
        if not rId or rId.isNull():
            return False
        type = record.value(u'Type')
        if not type or type.isNull() or type.toInt()[0] != 0:
            return False
        updEvent = record.value(u'updEvent')
        if not updEvent or updEvent.isNull() or updEvent.toInt()[0] != 0:
            return False
        return True
        
    def canAddEvent(self, record):
        type = record.value(u'Type')
        if not type or type.isNull() or type.toInt()[0] != 0:
            return False
        updEvent = record.value(u'updEvent')
        if not updEvent or updEvent.isNull() or updEvent.toInt()[0] == 0:
            return False
        return True
        
    def selectionChanged(self, current = QModelIndex(), previous = QModelIndex()):
        if not current.isValid():
            self.txtCallInfo.clear()
            self.btnUpdEvent.setEnabled(False)
            self.btnAddEvent.setEnabled(False)
            self.btnPrintCallInfo.setEnabled(False)
            return
            
        record = self.modelCallInfo.record(current.row())
        
        self.btnUpdEvent.setEnabled(self.canUpdEvent(record))
        self.btnAddEvent.setEnabled(self.canAddEvent(record))
        self.btnPrintCallInfo.setEnabled(True)

        def formatField(name):
            value = record.value(name)
            if value.isNull() or len(forceString(value).strip()) == 0:
                return u''
            else:
                return u'<div><b>%s:</b> %s</div>' % (name, forceString(value))
                
        text = u'''<style> 
            .header {
                font: bold large; 
                margin-bottom: 5px; 
                margin-left: 20px;
            }
            </style>'''
        
        text += u'<div class="header">Пациент</div>'
        text += formatField(u'Фамилия')
        text += formatField(u'Имя')
        text += formatField(u'Отчество')
        text += formatField(u'Пол')
        age = []
        ageParts = [
            (u'Лет', (u'год', u'года', u'лет')), 
            (u'Месяцев', (u'месяц', u'месяца', u'месяцев')), 
            (u'Дней', (u'день', u'дня', u'дней'))
        ]
        for partName, words in ageParts:
            part = record.value(partName)
            if not part.isNull():
                part = forceInt(part)
                age.append(u'%d %s' % (part, agreeNumberAndWord(part, words)))
        if age:
            text += u'<div><b>Возраст:</b> %s</div>' % ', '.join(age)
        text += u'<hr>'

        text += u'<div class="header">Вызов</div>'
        text += formatField(u'Дата вызова')
        text += formatField(u'Время приёма вызова')
        text += formatField(u'Время окончания приёма вызова')
        text += formatField(u'Основной диагноз')
        text += formatField(u'Результат выезда')
        text += formatField(u'Категория срочности вызова')
        text += formatField(u'Вид вызова')
        text += formatField(u'Повод к вызову')
        text += formatField(u'Вызов повторный?')
        text += formatField(u'ФИО вызывающего')
        text += formatField(u'Место вызова')
        text += formatField(u'ФИО принявшего вызов')
        text += u'<hr>'
        
        text += u'<div class="header">Адрес и контактные данные</div>'
        text += formatField(u'Населенный пункт')
        text += formatField(u'Улица')
        text += formatField(u'Номер дома')
        text += formatField(u'Корпус')
        text += formatField(u'Квартира')
        text += formatField(u'Подъезд')
        text += formatField(u'Код домофона')
        text += formatField(u'Этаж')
        text += formatField(u'Ориентиры')
        text += formatField(u'Телефон')
        text += u'<hr>'
        
        self.txtCallInfo.setText(text)
        
    def getNewEvents(self):
        if (QtGui.qApp.isBusyReconnect == 1):
            return
        sql = u"""select callInfo.callDate 
                  from smp_callinfo as callInfo
                  inner join smp_eventitem as eventItem on eventItem.idCallNumber = callInfo.idCallNumber
                  where eventItem.updEvent = 0 and callInfo.Type = 0
                    and callInfo.OMS_CODE = '%s'
                  order by callInfo.callDate
                  limit 1""" % str(self.cmbOrganisation.itemData(self.cmbOrganisation.currentIndex()).toString())
        if QtGui.qApp.db:
            query = QtGui.qApp.db.query(sql)
            if query.first():
                date = query.value(0).toDate()
                self.lblNewEvents.setText(u'Новые вызовы СМП (дата: <a href="setdate:%s">%s</a>)' % (date.toString(Qt.ISODate), forceString(date)))
                self.setTabNotification(True)
            else:
                self.lblNewEvents.setText(u"")
                self.setTabNotification(False)
    
    def setTabNotification(self, hasNewEvents):
        tabBar, tabIndex = QtGui.qApp.mainWindow.findDockTab(self.parent())
        if tabBar:
            if hasNewEvents:
                tabBar.setTabTextColor(tabIndex, Qt.red)
                tabBar.setTabIcon(tabIndex, self.style().standardIcon(QtGui.QStyle.SP_MessageBoxWarning))
            else:
                tabBar.setTabTextColor(tabIndex, Qt.black)
                tabBar.setTabIcon(tabIndex, QtGui.QIcon())

    @QtCore.pyqtSignature('bool')
    def on_chbEventType_toggled(self, checked):
        self.cmbEventType.setEnabled(checked)
        self.updateCalendarDates()
        self.updateCallList()
        
    @QtCore.pyqtSignature('bool')
    def on_chb03_toggled(self, checked):
        self.updateCalendarDates()
        self.updateCallList()
        
    @QtCore.pyqtSignature('bool')
    def on_chbNMP_toggled(self, checked):
        self.updateCalendarDates()
        self.updateCallList()
        
    @QtCore.pyqtSignature('')
    def on_calDate_selectionChanged(self):
        self.updateCallList()
        
    @QtCore.pyqtSignature('int')
    def on_cmbEventType_currentIndexChanged(self, index):
        self.updateCalendarDates()
        self.updateCallList()
        
    @QtCore.pyqtSignature('int')
    def on_cmbOrganisation_currentIndexChanged(self, index):
        self.updateCalendarDates()
        self.updateCallList()
        
    @QtCore.pyqtSignature('')
    def on_btnUpdEvent_clicked(self):
        record = self.modelCallInfo.record(self.selectionModelCallInfo.currentIndex().row())
        if not self.canUpdEvent(record):
            return

        rId = record.value(u'rId').toInt()[0]
        operFIO = QtGui.qApp.userInfo.name()
        
        clent = CJsonRpcClent("http://%s/smp/handler.php" % QtGui.qApp.preferences.dbServerName)
        try:
            result = clent.call('updEvent', {'id': rId, 'operFIO': operFIO})
            if result:
                QtGui.QMessageBox.information(self, u'Информация', u'Подтверждение отправлено', QtGui.QMessageBox.Close, QtGui.QMessageBox.Close)
                self.updateCalendarDates()
                self.updateCallList()
                self.getNewEvents()
            else:
                QtGui.QMessageBox.critical(self, u'Ошибка', u'Подтверждение не отправлено', QtGui.QMessageBox.Close, QtGui.QMessageBox.Close)
        except Exception, e:
            QtGui.QMessageBox.critical(self, u'Ошибка', unicode(e), QtGui.QMessageBox.Close, QtGui.QMessageBox.Close)
            
    @QtCore.pyqtSignature('')
    def on_btnRefresh_clicked(self):
        self.updateCalendarDates()
        self.updateCallList()
        
    @QtCore.pyqtSignature('')
    def on_btnAddEvent_clicked(self):
        record = self.modelCallInfo.record(self.selectionModelCallInfo.currentIndex().row())
        if not self.canAddEvent(record):
            return
        if self.addEventDialog.exec_() == QtGui.QDialog.Accepted:
            eventTypeId = self.addEventDialog.eventTypeId()
            note = self.addEventDialog.note()
            lpuCode = forceString(record.value(u'OMS_CODE'))
            idCallNumber = record.value(u'idCallNumber').toLongLong()[0]
            operFIO = QtGui.qApp.userInfo.name()
            clent = CJsonRpcClent("http://%s/smp/handler.php" % QtGui.qApp.preferences.dbServerName)
            try:
                result = clent.call('addEvent', {'lpuCode': lpuCode, 'idCallNumber': idCallNumber, 'note': note, 'idCallEventType': eventTypeId, 'operFIO': operFIO})
                if result == -1:
                    QtGui.QMessageBox.critical(self, u'Ошибка', u'Результат вызова не отправлен (-1)', QtGui.QMessageBox.Close, QtGui.QMessageBox.Close)
                else:
                    QtGui.QMessageBox.information(self, u'Информация', u'Данные отправлены успешно', QtGui.QMessageBox.Close, QtGui.QMessageBox.Close)
                    self.updateCallList()
                    self.updateCalendarDates()
                    self.getNewEvents()
            except Exception, e:
                QtGui.QMessageBox.critical(self, u'Ошибка', unicode(e), QtGui.QMessageBox.Close, QtGui.QMessageBox.Close)
                
    @QtCore.pyqtSignature('QString')
    def on_lblNewEvents_linkActivated(self, link):
        link = str(link)
        if link[:8] == u"setdate:":
            date = QDate.fromString(link[8:], Qt.ISODate)
            self.calDate.setSelectedDate(date)
            
    @QtCore.pyqtSignature('')
    def on_btnPrintCallInfo_clicked(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        dialog = QtGui.QPrintDialog(printer, self)
        if dialog.exec_():
            self.txtCallInfo.print_(printer)


class CCallInfoModel(QtSql.QSqlQueryModel):
    def __init__(self, parent):
        QtSql.QSqlQueryModel.__init__(self, parent)
