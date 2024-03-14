# -*- coding: utf-8 -*-
import requests
from PyQt4 import QtGui
from PyQt4.QtCore import *

from Events.ActionInfo import CActionInfo
from Exchange.TMK.TMK_Method import moveToStage, moveToStage_action
from library.DialogBase import CConstructHelperMixin
from library.PrintInfo import CInfoContext
from library.Utils import exceptionToUnicode, forceString, forceRef

from TMKServiceClient import CTMKServiceClient

from Ui_TMKAppointmentsTableDialog import Ui_TMKAppointmentsTableDialog

StatusDict = {
    '85dad08c-1eb7-479f-8bf5-66b3ea5e4a02': u"Передано врачу",
    'f2eead71-c257-4f12-827c-cfe86776f1b4': u"Черновик",
    'f6917177-a702-4c7f-981a-84552c91addf': u"Направлено в МО",
    'd56f26ed-3947-4c4b-b1c2-414eb11cd576': u"Подготовка заключения консилиумом",
    '26e048e2-6c52-4e2f-9545-35e37b3cf013': u"Подпись заключения участниками консилиума",
    '1e658872-795b-445b-8632-cb70798f4dd5': u"Организация консилиума",
    'f0093882-61f3-4684-aa0e-52094991cbf8': u"Запрашивается дополнительная информация",
    'fff74636-1c39-448a-bbae-0f14f8c1f6a5': u"Подготовка заключения",
    '764f55f2-2c0e-43e3-81ce-3e5626682322': u"Отклонено",
    '425a04fc-b21e-4009-bf45-67625abddff6': u"В листе ожидания",
    'f869ab89-c111-4e65-a896-661f14d1d2db': u"На подписи у председателя консилиума",
    'ba65d940-8ebd-4583-a6cb-9a0f683ed331': u"Заключение готово",
    'ea0e8711-7b6e-4ad3-8bc2-904006eb569d': u"Заключение консилиума готово",
    '0': u"Все",
}

urgencyDict = {
    '1': u"Экстренная",
    '2': u"Неотложная",
    '3': u"Плановая",
    '4': u"Все",
}

primaryAppealList = {
        '1': u'первично',
        '2': u'повторно',
}


reasonCodeDict = {
    '1': u"Определение (подтверждение) диагноза",
    '2': u"Определение (подтверждение) тактики лечения и методов диагностики",
    '3': u"Согласование направления пациента в медицинскую организацию",
    '4': u"Согласование перевода пациента в медицинскую организацию",
    '5': u"Интерпретация результатов диагностического исследования",
    '6': u"Получение экспертного мнения по результату диагностического исследования",
    '7': u"Разбор клинического случая",
    '8': u"Дистанционное наблюдение за пациентом",
    '9': u"Другое",
}

AllowedStatuses = ['85dad08c-1eb7-479f-8bf5-66b3ea5e4a02',
    'f2eead71-c257-4f12-827c-cfe86776f1b4',
    'f6917177-a702-4c7f-981a-84552c91addf',
    'd56f26ed-3947-4c4b-b1c2-414eb11cd576',
    '26e048e2-6c52-4e2f-9545-35e37b3cf013',
    '1e658872-795b-445b-8632-cb70798f4dd5',
    'f0093882-61f3-4684-aa0e-52094991cbf8',
    'fff74636-1c39-448a-bbae-0f14f8c1f6a5',
    '764f55f2-2c0e-43e3-81ce-3e5626682322',
    '425a04fc-b21e-4009-bf45-67625abddff6',
    'f869ab89-c111-4e65-a896-661f14d1d2db',
    'ba65d940-8ebd-4583-a6cb-9a0f683ed331',
    'ea0e8711-7b6e-4ad3-8bc2-904006eb569d',
                   '0']

AllowedUrgency = ['1', '2', '3', '4']


def organisation(org):
    db = QtGui.qApp.db
    orgVal = ''
    orgValue = db.getRecordEx(
        'Organisation',
        'concat(title," ",infisCode)',
        'usishCode="%s" and deleted = 0 and isActive = 1' % org)
    if orgValue:
        orgVal = forceString(orgValue.value(0))
    else:
        orgValue = db.getRecordEx(
            'Organisation o LEFT JOIN Organisation_Identification oi ON o.id = oi.master_id ',
            'concat(o.title," ",o.infisCode)',
            'oi.value="%s" and o.deleted = 0 and o.isActive = 1' % org)
        if orgValue:
            orgVal = forceString(orgValue.value(0))
    return orgVal

class CTMKAppointmentsTableDialog(QtGui.QDialog, CConstructHelperMixin, Ui_TMKAppointmentsTableDialog):
    def __init__(self, parent, action):
        QtGui.QDialog.__init__(self, parent)
        self.addModels('Doctors', CTMKDoctorsListModel(self))
        self.addModels('Appointments', CTMKAppointmentsTableModel(self))
        self.setupUi(self)
        self.setModels(self.lvDoctors, self.modelDoctors, self.selectionModelDoctors)
        self.setModels(self.tblAppointments, self.modelAppointments, self.selectionModelAppointments)
        self.btnSetAppointment.setEnabled(False)
        self.btnSetWaitingList.setEnabled(True)
        self.action = action
        self.orgId = action[u'Куда направляется']
        self.profileId = action[u'Профиль']
        h = self.tblAppointments.fontMetrics().height()
        self.tblAppointments.verticalHeader().setDefaultSectionSize(3 * h / 2)
        self.tblAppointments.verticalHeader().hide()
        w = self.tblAppointments.fontMetrics().width('00.00.0000')
        self.tblAppointments.horizontalHeader().setDefaultSectionSize(w + h * 2)
        self.actionChanged = False

    def showEvent(self, event):
        QTimer.singleShot(0, self.updateList)

    def enableControls(self, enabled):
        self.lvDoctors.setEnabled(enabled)
        self.tblAppointments.setEnabled(enabled)
        self.btnUpdateList.setEnabled(enabled)
        self.btnSetAppointment.setEnabled(enabled and self.selectionModelAppointments.hasSelection())
        self.btnClose.setEnabled(enabled)

    def updateList(self):
        self.modelAppointments.setList(None)
        self.modelDoctors.setList(None)
        self.lblStatus.setText(u"Загрузка списка талонов...")
        self.lblStatus.setVisible(True)
        self.enableControls(False)
        QtGui.qApp.setWaitCursor()
        try:
            QtGui.qApp.processEvents()
            client = CTMKServiceClient()
          #  serviceData = client.getAvailableAppointments(self.orgId, self.profileId)
            serviceData = None
            self.modelDoctors.setList(serviceData)
        except Exception, e:
            QtGui.QMessageBox.critical(self,
                                       u'Ошибка при получении списка доступных талонов',
                                       exceptionToUnicode(e),
                                       QtGui.QMessageBox.Ok,
                                       QtGui.QMessageBox.Ok)
        QtGui.qApp.restoreOverrideCursor()
        self.enableControls(True)
        if len(self.modelDoctors.rows) > 0:
            self.lblStatus.setVisible(False)
        else:
            self.lblStatus.setText(u'Нет доступных талонов')

    def getSelectedDoctor(self):
        index = self.selectionModelDoctors.currentIndex()
        if index.isValid():
            return self.modelDoctors.getDoctorByIndex(index)
        else:
            return None

    def getSelectedAppointment(self):
        index = self.selectionModelAppointments.currentIndex()
        if index.isValid():
            return self.modelAppointments.getAppointmentByIndex(index)
        else:
            return None

    @pyqtSignature('')
    def on_btnUpdateList_clicked(self):
        self.updateList()

    @pyqtSignature('')
    def on_btnSetAppointment1_clicked(self):
        if self.action[u'Идентификатор талона']:
            return
        client = CTMKServiceClient()
        self.lblStatus.setText(u"Регистрация направления и запись на прием...")
        self.lblStatus.setVisible(True)
        self.enableControls(False)
        QtGui.qApp.setWaitCursor()
        try:
            if not self.action[u'Идентификатор направления']:
                QtGui.QMessageBox.critical(self,
                   u'Ошибка',
                   u'Не удалось определить идентификатор направления',
                   QtGui.QMessageBox.Ok,
                   QtGui.QMessageBox.Ok)
                return
            self.lblStatus.setText(u"Запись на прием...")
            QtGui.qApp.processEvents()
            doctor = self.getSelectedDoctor()
            appointment = self.getSelectedAppointment()
            appointmentId = appointment['id']
            doctorId = doctor['id']
            specialityId = doctor['specialityId']
            try:
                client.setAppointment(self.action, specialityId, doctorId, appointmentId)
                self.actionChanged = True
            except Exception, e:
                QtGui.QMessageBox.critical(self,
                                           u'Ошибка при записи на прием',
                                           exceptionToUnicode(e),
                                           QtGui.QMessageBox.Ok,
                                           QtGui.QMessageBox.Ok)
                return
            QtGui.QMessageBox.information(self,
                                          u'Внимание!',
                                          u'Запись на прием выполнена успешно',
                                          QtGui.QMessageBox.Ok,
                                          QtGui.QMessageBox.Ok)
            self.accept()
        finally:
            QtGui.qApp.restoreOverrideCursor()
            self.enableControls(True)
            self.lblStatus.setVisible(False)

    @pyqtSignature('')
    def on_btnSetWaitingList_clicked(self):
        if self.action[u'Идентификатор талона']:
            return
        self.lblStatus.setText(u"Отправка заявки в лист ожидания...")
        self.lblStatus.setVisible(True)
        self.enableControls(False)
        QtGui.qApp.setWaitCursor()
        try:
            if not self.action[u'Идентификатор направления']:
                QtGui.QMessageBox.critical(self,
                                           u'Ошибка',
                                           u'Не удалось определить идентификатор направления',
                                           QtGui.QMessageBox.Ok,
                                           QtGui.QMessageBox.Ok)
                return
            try:
                moveToStage_action(self, self.action, '51cc43fd-b2d9-4fb6-baf1-f1052c068a55')
                self.actionChanged = True
            except Exception, e:
                QtGui.QMessageBox.critical(self,
                                           u'Ошибка при отправке заявки',
                                           exceptionToUnicode(e),
                                           QtGui.QMessageBox.Ok,
                                           QtGui.QMessageBox.Ok)
                return
            QtGui.QMessageBox.information(self,
                                          u'Внимание!',
                                          u'Отправка заявки выполнена успешно',
                                          QtGui.QMessageBox.Ok,
                                          QtGui.QMessageBox.Ok)
            self.accept()
        finally:
            QtGui.qApp.restoreOverrideCursor()
            self.enableControls(True)
            self.lblStatus.setVisible(False)

    @pyqtSignature('')
    def on_btnClose_clicked(self):
        self.reject()

    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelDoctors_currentChanged(self, current, previous):
        if current.isValid():
            doctor = self.modelDoctors.getDoctorByIndex(current)
            self.modelAppointments.setList(doctor['appointments'])
        else:
            self.modelAppointments.setList(None)

    @pyqtSignature('')
    def on_modelDoctors_modelReset(self):
        self.btnSetAppointment.setEnabled(False)

    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelAppointments_currentChanged(self, current, previous):
        if current.isValid():
            appointment = self.modelAppointments.getAppointmentByIndex(current)
        else:
            appointment = None
        if appointment:
            self.btnSetAppointment.setEnabled(True)
        else:
            self.btnSetAppointment.setEnabled(False)

    @pyqtSignature('')
    def on_modelAppointments_modelReset(self):
        self.btnSetAppointment.setEnabled(False)


class CTMKDoctorsListModel(QAbstractItemModel):
    def __init__(self, parent):
        QAbstractItemModel.__init__(self, parent)
        self.rows = []
        self.doctors = {}

    def index(self, row, col, parent):
        return self.createIndex(row, col, None)

    def parent(self, child):
        return QModelIndex()

    def setList(self, serviceData):
        self.rows = []
        self.doctors = {}
        if serviceData:
            for speciality in serviceData['specialityList']:
                for doctor in speciality['doctorList']:
                    if doctor['appointmentList']:
                        key = speciality['id'] + '|' + doctor['id']
                        self.doctors[key] = {
                            'id': doctor['id'],
                            'name': u"%s, %s" % (doctor['name'], speciality['name']),
                            'specialityId': speciality['id'],
                            'appointments': doctor['appointmentList']
                        }
            self.rows = sorted(self.doctors.keys(), key=lambda k: self.doctors[k]['name'])
        self.reset()

    def columnCount(self, parent):
        return 1

    def rowCount(self, parent):
        return len(self.rows)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            if col == 0:
                key = self.rows[row]
                return QVariant(self.doctors[key]['name'])
        return QVariant()

    def getDoctorByIndex(self, index):
        row = index.row()
        key = self.rows[row]
        return self.doctors[key]


class CTMKAppointmentsTableModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self.appointmentsByDate = {}
        self.maxRowCount = 0
        self.columns = []

    def setList(self, serviceData):
        self.appointmentsByDate = {}
        self.maxRowCount = 0
        if serviceData:
            for appointment in serviceData:
                visitStart = QDateTime.fromString(appointment['visitStart'], Qt.ISODate)
                visitEnd = QDateTime.fromString(appointment['visitEnd'], Qt.ISODate)
                appointmentDate = visitStart.date().toString('dd.MM.yyyy')
                if appointmentDate not in self.appointmentsByDate:
                    self.appointmentsByDate[appointmentDate] = []
                self.appointmentsByDate[appointmentDate].append({
                    'id': appointment['id'],
                    'start': visitStart.time(),
                    'end': visitEnd.time(),
                    'address': appointment['address'],
                    'num': appointment['num'],
                    'room': appointment['room'],
                })
        for appointments in self.appointmentsByDate.values():
            appointments.sort(key=lambda appointment: appointment['start'])
            if len(appointments) > self.maxRowCount:
                self.maxRowCount = len(appointments)
        self.columns = sorted(self.appointmentsByDate.keys())
        self.reset()

    def columnCount(self, index=None):
        return len(self.columns)

    def rowCount(self, index=None):
        return self.maxRowCount

    def data(self, index, role):
        appointment = self.getAppointmentByIndex(index)
        if appointment:
            if role == Qt.DisplayRole:
                return QVariant(appointment['start'].toString('hh:mm'))
            elif role == Qt.TextAlignmentRole:
                return Qt.AlignHCenter + Qt.AlignVCenter
            elif role == Qt.ToolTipRole:
                toolTip = []
                toolTip.append(u"Начало: %s" % appointment['start'].toString('hh:mm'))
                toolTip.append(u"Окончание: %s" % appointment['end'].toString('hh:mm'))
                if appointment['address']:
                    toolTip.append(u"Адрес: %s" % appointment['address'])
                if appointment['room']:
                    toolTip.append(u"Кабинет: %s" % appointment['room'])
                if appointment['num']:
                    toolTip.append(u"Номер талона: %s" % appointment['num'])
                return QVariant('\n'.join(toolTip))
        return QVariant()

    def flags(self, index):
        appointment = self.getAppointmentByIndex(index)
        if appointment:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.NoItemFlags

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return QVariant(self.columns[section])
        return QVariant()

    def getAppointmentByIndex(self, index):
        row = index.row()
        col = index.column()
        date = self.columns[col]
        appointments = self.appointmentsByDate[date]
        if 0 <= row < len(appointments):
            return appointments[row]
        else:
            return None





