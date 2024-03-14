# -*- coding: utf-8 -*-
# Модуль взаимодействия с региональным сегментом здравоохранения
#  Что это? кто это использует?

#import logging
import os
import shutil
from datetime import datetime, timedelta
from tempfile import gettempdir as tmp
from suds.client import Client
from suds.xsd.doctor import ImportDoctor,Import
#from suds.client import WebFault
from suds.plugin import MessagePlugin
from PyQt4.QtCore import QDate

class UnicodeFilter(MessagePlugin):
    def received(self, context):
        decoded = context.reply.decode('utf-8', errors='ignore')
        reencoded = decoded.encode('utf-8')
        context.reply = reencoded
class CRisExchange():
    def __init__(self,url,mocode,token,location=''):
        #Грузим библиотеки suds динамически
        shutil.rmtree(os.path.join(tmp(), 'suds'), True)
        #logging.basicConfig(level=logging.INFO)
        #logging.getLogger('suds.client').setLevel(logging.DEBUG)
        imp = Import('http://schemas.xmlsoap.org/soap/encoding/')
        doctor = ImportDoctor(imp)
        self.client = Client(url,doctor=doctor, plugins=[UnicodeFilter()])
        self.mocode = mocode
        self.token = token
        if len(location):
            self.client.options.location=location
    #Установка особых случаев, если необходимо для данного пациента,если необходимо
    def __checkExtraCases(self, pInfo):
        pInfo.extracases=[]
        #Отсутствует документ удостоверяющий личность
        if not isinstance(pInfo.documents, list):
            extracase = self.client.factory.create('extracase')
            extracase.extracase_code = '4'
            extracase.begindate = QDate.currentDate().toString('yyyy-MM-dd')
            pInfo.extracases.append(extracase)
        #Отсутствует отчество у пациента
        if not (unicode(pInfo.patrname).strip()):
            extracase = self.client.factory.create('extracase')
            extracase.extracase_code = '1'
            extracase.begindate = QDate.currentDate().toString('yyyy-MM-dd')
            pInfo.extracases.append(extracase)
        #Пациент неидентифицирован
        if unicode(pInfo.lname).upper() == u'НЕИЗВЕСТНО' or unicode(pInfo.fname).upper() == u'НЕИЗВЕСТНО' or unicode(pInfo.patrname).upper() == u'НЕИЗВЕСТНО' or not pInfo.birthdate:
            extracase = self.client.factory.create('extracase')
            extracase.extracase_code = '3'
            extracase.begindate = QDate.currentDate().toString('yyyy-MM-dd')
            pInfo.extracases.append(extracase)
        #Пациент новорожденный
        if (datetime.now()-datetime.strptime(unicode(pInfo.birthdate), '%Y-%m-%d')).days < 28:
            extracase = self.client.factory.create('extracase')
            extracase.extracase_code = '0'
            extracase.begindate = pInfo.birthdate
            extracase.enddate = (datetime.strptime(unicode(pInfo.birthdate), '%Y-%m-%d')+timedelta(days=27)).strftime('%Y-%m-%d')
            pInfo.extracases.append(extracase)





    #Поиск пациента в РИС
    def searchPatient(self, sInfo):
        searchInfo = self.client.factory.create('SearchPatientInfo')
        searchInfo.mocode = self.mocode
        searchInfo.token = self.token
        searchInfo.lname = sInfo['lname']
        searchInfo.fname = sInfo['fname']
        searchInfo.patrname = sInfo['pname']
        searchInfo.snils = sInfo['snils']
        searchInfo.birthdate = sInfo['birthdate']
        searchInfo.enp = sInfo['enp']
        if sInfo['document']:
            document = self.client.factory.create('document')
            document.code = sInfo['document']['code']
            document.seria = sInfo['document']['seria']
            document.number = sInfo['document']['number']
            searchInfo.documents=[document]
        #try:
        return self.client.service.searchPatient(searchInfo)
        #except WebFault, e:
        #    QtGui.QMessageBox.warning(None, u'Неверные данные пациента',unicode(e.fault.faultstring ),QtGui.QMessageBox.Ok)
    #Получение пациента из РИС
    def getPatient(self, patientID):
        getPatientInfo = self.client.factory.create('GetPatientInfo')
        getPatientInfo.mocode = self.mocode
        getPatientInfo.token = self.token
        getPatientInfo.patientId = patientID
        return self.client.service.getPatient(getPatientInfo)
    #Получение структуры для данных о пациенте
    def getAddPatientInfo(self):
        return self.client.factory.create('patientInfo')
    def getInsuranceType(self):
        return self.client.factory.create('insurance')
    def getAddressType(self):
        return self.client.factory.create('address')
    def getPAddressType(self):
        return self.client.factory.create('patient_address')
    def getBenefitType(self):
        return self.client.factory.create('benefit')
    def getContactType(self):
        return self.client.factory.create('contact')
    def getDocumentType(self):
        return self.client.factory.create('document')
    #Добавление пациента в РИС
    def addPatient(self, pInfo):
        addPatientInfo = self.client.factory.create('AddPatientInfo')
        addPatientInfo.mocode = self.mocode
        addPatientInfo.token = self.token
        self.__checkExtraCases(pInfo)
        addPatientInfo.patientinfo = pInfo
        #try:
        return self.client.service.addPatient(addPatientInfo)
        #except WebFault, e:
        #   QtGui.QMessageBox.warning(None, u'Ошибка передачи пациента в региональный сегмент',unicode(e.fault.faultstring ),QtGui.QMessageBox.Ok)
    #Объединение данных о пациентах РИС и МИС
    def changePatient(self,pInfo):
        addPatientInfo = self.client.factory.create('AddPatientInfo')
        addPatientInfo.mocode = self.mocode
        addPatientInfo.token = self.token
        self.__checkExtraCases(pInfo)
        addPatientInfo.patientinfo = pInfo
        return self.client.service.changePatient(addPatientInfo)
