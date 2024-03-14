# -*- coding: utf-8 -*-
import re

import requests
from PyQt4 import QtGui
from PyQt4.QtCore import QDate, QDateTime

from Events.ActionInfo import CActionInfo
from library.PrintInfo import CInfoContext
from library.Utils import forceString, exceptionToUnicode, forceRef



def moveToStage(self, transitionId, comments=None, person=None):
    urlService = forceString(QtGui.qApp.db.translate('GlobalPreferences', 'code', 'TMKServiceUrl', 'value'))
    urlAuth = forceString(QtGui.qApp.db.translate('GlobalPreferences', 'code', 'TMKServiceAuth', 'value'))
    lpuCode = QtGui.qApp.db.getRecordEx('Organisation_Identification', 'value',
                                        'master_id = %s AND deleted=0 AND system_id in (SELECT id FROM rbAccountingSystem `as` WHERE `as`.urn="urn:oid:1.2.643.2.69.1.1.1.64")' % str(
                                            QtGui.qApp.currentOrgId()))

    record = QtGui.qApp.db.getRecord('TMK_Service', '*', self.tblTMKRequests.currentItemId())

    if record:
        processId = forceString(record.value('processId'))
        communication = forceString(record.value('communication'))
        scheduleItem_id = forceString(record.value('scheduleItem_id'))
        person_id = forceString(record.value('person_id'))
        if transitionId not in ('239e8005-462b-437d-ac33-2a1134187852','b9becd83-1b5b-4c23-95c7-d545466b2dbb','0c1912f0-947b-4c84-8e5d-35094847c3b7'):
            if scheduleItem_id:
                scheduleTimes = QtGui.qApp.db.getRecordEx('Schedule_Item', 'time, DATE_FORMAT(time,"%Y%m%d%H%i%S") as form',
                                                          'id = %s ' % str(scheduleItem_id))
                scheduleTime = forceString(scheduleTimes.value('time'))
                scheduleId = forceString(scheduleTimes.value('form'))
                if len(scheduleId + person_id) != 20:
                    IdAppointment = scheduleId + ('0' * (20 - len(scheduleId + person_id))) + person_id
                else:
                    IdAppointment = scheduleId + person_id


        if comments:
            id = QDateTime().currentDateTime().toString('dd-MM-yyyy hh:mm:ss')
            userId = QtGui.qApp.userId
            author = forceString(QtGui.qApp.db.translate('Person', 'id', userId, 'formatPersonName(id)')) if userId else False
            if transitionId in ('b9becd83-1b5b-4c23-95c7-d545466b2dbb', '239e8005-462b-437d-ac33-2a1134187852', '0c1912f0-947b-4c84-8e5d-35094847c3b7'):
                type_ = 1
            elif transitionId == '72af8a14-e276-4e33-9988-b51cf141f66f':
                type_ = 2
            elif transitionId == '1b2ff3f0-794a-466c-88c2-61bbff931fd9':
                type_ = 3
            elif transitionId == '1f973a5f-9d8c-466a-abc2-a27d1ed1072d':
                type_ = 0
            comment = u"""
            "processContext": {
            "communication": [
            {
                "id": "%(id)s",
                "isDeleted": false,
                "author": "%(author)s",
                "type": "%(type_)s",
                "comment": "%(comments)s"
            }
        ]
        },
            """ % {'comments': comments, 'type_': type_, 'author': author, 'id': id}
        else:
            if person and scheduleItem_id:
                comment = u""" "processContext": {
            "appointment": {
                "start": "%(scheduleTime)s",
                "end": "%(scheduleTime)s",
                    "couponId": "%(IdAppointment)s"
            },
            "performerPractitioner": {
                "identityDocument": {
                    "system": "223",
                    "code": "%(snils)s"
                },
                "fullName": "%(fullName)s",
                "position": "%(post)s",
                "specialty": "%(spec)s",
                "department": "%(org)s",
                "telecom": {
                    "phone": "%(phone)s",
                    "email": "%(mail)s"
                }
            }
        },""" % {'snils': forceString(person.value(5)), 'fullName': forceString(person.value(6)),
                 'spec': forceString(person.value(0)), 'post': forceString(person.value(1)),
                 'org': forceString(person.value(2))
                    , 'phone': forceString(person.value(3)), 'mail': forceString(person.value(4)),
                 'scheduleTime': scheduleTime, 'IdAppointment': IdAppointment}
            else:
                comment = ''

        stmt = u"""
    
        {
        "processId": "%(processId)s",
            "transitionId": "%(transitionId_)s",
            %(comment)s
            "roleContext": [
               {
                    "Role": "HEAD_DOCTOR",
                    "Organization": "%(lpuCode)s",
                    "SNILS": "777-777-777"
                }
            ]
    
        }
        """ % {"lpuCode": forceString(lpuCode.value(0)), 'processId': processId,
               'transitionId_': transitionId, 'comment': comment}

        headers = {"authorization": urlAuth, "content-type": "application/json"}

        try:
            response = requests.post(urlService+'/Commands/MoveToStage',
                                     data=stmt.encode('UTF-8'), headers=headers, timeout=60)
            if response.status_code == 200 and response.json()['success']:
                return 1
            else:
                QtGui.QMessageBox.warning(self,
                                          u'Невозможно определить статус текущей заявки',
                                          exceptionToUnicode(response.status_code),
                                          QtGui.QMessageBox.Ok,
                                          QtGui.QMessageBox.Ok)
        except Exception, e:
            QtGui.QMessageBox.critical(self,
                                       u'Ошибка при создании заявки',
                                       exceptionToUnicode(e),
                                       QtGui.QMessageBox.Ok,
                                       QtGui.QMessageBox.Ok)

            return 0
    else:
        QtGui.QMessageBox.critical(self,
                                   u'Ошибка',
                                   '',
                                   QtGui.QMessageBox.Ok,
                                   QtGui.QMessageBox.Ok)
        return 0


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

def clientMPI(clientInfo, idLPU):
    from suds.client import Client, WebFault

    MPI_MIS = QtGui.qApp.db.getRecordEx('ClientIdentification', 'identifier',
                                        'client_id = %s AND accountingSystem_id = (SELECT id FROM rbAccountingSystem WHERE urn = "url:oid:MPI_PIX") AND deleted=0' % str(
                                            clientInfo.id))
    if MPI_MIS:
        return forceString(MPI_MIS.value(0))

    url = 'http://10.0.1.179/EMK/PixService.svc?wsdl'
    client = Client(url)

    patient = client.factory.create('patient')

    lpuCode = QtGui.qApp.preferences.dbDatabaseName
    if lpuCode in ('s11_01527', 's11_17020', 's11_11007', 's11_15001', 's11_13516', 's11_11031'):
        patient.IdPatientMIS = str(clientInfo.id)+'_'
    else:
        patient.IdPatientMIS = clientInfo.id

    url_portal = QtGui.qApp.preferences.dbServerName
    response = requests.post('http://' + url_portal + '/EMK_V3/indexV2.php?clientId='+str(clientInfo.id)+'?snils=1?lastName=tmk?firstName=tmk?patronymic=tmk?mo=10')

    try:
        a = client.service.GetPatient(guid='0B9D35AB-B191-4BDD-AC37-9015CC89CB2E',
                                      idLPU=idLPU, patient=patient, idSource='Reg')
        return a['PatientDto'][0]['IdGlobal']
    except WebFault as e:
        print forceString(e)
    except Exception as e:
        print forceString(e)


def TMKStartNewProcess(self, action, record):
    urlService = forceString(QtGui.qApp.db.translate('GlobalPreferences', 'code', 'TMKServiceUrl', 'value'))
    urlAuth = forceString(QtGui.qApp.db.translate('GlobalPreferences', 'code', 'TMKServiceAuth', 'value'))
    urgencyList = [
        u'Экстренная',
        u'Неотложная',
        u'Плановая',
    ]
    reasonCodeList = [
        u'Определение (подтверждение) диагноза',
        u'Определение (подтверждение) тактики лечения и методов диагностики',
        u'Согласование направления пациента в медицинскую организацию',
        u'Согласование перевода пациента в медицинскую организацию',
        u'Интерпретация результатов диагностического исследования',
        u'Получение экспертного мнения по результату диагностического исследования',
        u'Разбор клинического случая',
        u'Дистанционное наблюдение за пациентом',
        u'Другое'
    ]
    primaryAppealList = [
        u'первично',
        u'повторно',
    ]

    context = CInfoContext()
    actionInfo = context.getInstance(CActionInfo, forceRef(record.value('id')))
    postPerson = actionInfo.person.post.identify('urn:oid:1.2.643.5.1.13.13.99.2.181')

    specialityPerson = actionInfo.person.speciality.identify('urn:oid:1.2.643.5.1.13.13.11.1066')
    phonePerson = actionInfo[u'Телефон направителя'].value
    mailPerson = QtGui.qApp.db.getRecordEx('Organisation', 'email', 'id = %s AND deleted=0 ' % str(QtGui.qApp.currentOrgId()))

    lpuCode = QtGui.qApp.db.getRecordEx('Organisation_Identification', 'value',
                                        'master_id = %s AND deleted=0 AND system_id in (SELECT id FROM rbAccountingSystem `as` WHERE `as`.urn="urn:oid:1.2.643.2.69.1.1.1.64")' % str(
                                            QtGui.qApp.currentOrgId()))
    performerOrganization = QtGui.qApp.db.getRecordEx('Organisation_Identification', 'value',
                                                      'master_id = %s AND deleted=0 AND system_id in (SELECT id FROM rbAccountingSystem `as` WHERE `as`.urn="urn:oid:1.2.643.2.69.1.1.1.64")' % str(
                                                          actionInfo[u'Куда направляется'].value.id))

    anamnez = actionInfo[u'Анамнез заболевания'].value.replace('"',"'").replace('\\','/')
    reasonCode = actionInfo[u'Цель телемедицинской консультации'].value

    category = QtGui.qApp.db.getRecordEx('rbMedicalAidProfile', 'federalCode',
                                         'id = %s ' % str(actionInfo[u'Профиль'].value.id))

    primaryAppeal = actionInfo[u'Повторный приём'].value
    urgency = actionInfo[u'Срочность выполнения'].value

    clientInfo = actionInfo.event.client
    clientFIo = clientInfo.lastName + u' ' + clientInfo.firstName + u' ' + clientInfo.patrName
    clientBirthDate = clientInfo.birthDate
    if lpuCode:
        client = clientMPI(clientInfo, forceString(lpuCode.value(0)))
    if clientInfo.document and clientInfo.document.serial and clientInfo.document.number:
        clientDoc = forceString(clientInfo.document.serial).replace(' ', '') + ':' + forceString(clientInfo.document.number)
    else:
        clientDoc = forceString(clientInfo.document.serial) if clientInfo.document.serial else forceString(
            clientInfo.document.number) if clientInfo.document.number else None
    if clientInfo.document:
        clientDocCode = forceString(clientInfo.document.type.identify('urn:oid:1.2.643.5.1.13.13.99.2.48'))
    else:
        clientDocCode = None

    files = ''
    idx = 1
    if len(action._attachedFileItemList) > 0:
        for record_attach in action._attachedFileItemList:
            if record_attach.comment == u'':
                doc = uploadFiles(self, record_attach, lpuCode, True)
                record_attach.getRecord('Action_FileAttach').setValue('comment', doc)
            else:
                doc = record_attach.comment

            if idx != 1:
                files += ','
            files += u"""
                    {
                    "id": "%(idx)s",
                    "fileURL": "%(fileURL)s",
                    "isDeleted": false
                }""" % {'idx': idx, 'fileURL': doc}
            idx += 1

    if postPerson and specialityPerson and phonePerson and mailPerson and lpuCode and performerOrganization and anamnez and reasonCode and category and primaryAppeal and urgency and client and clientBirthDate and clientDoc and clientDocCode:
        stmt = u"""
            {
        "workflowId": "db648adb-aa34-4b08-a4b0-e4a11a6b9e44",
        "name": "Телемедицинская консультация",
        "initialTransitionId": "a36157a6-42ad-46bd-a75b-fe3e3e099f4b",
        "processContext": {
            "patient": {
                "idMPI": "%(clientMPI)s",
                "identityDocument": {
                    "system": "%(clientDocCode)s",
                    "code": "%(clientDoc)s"
                },
                "birthDate": "%(clientBirthDate)s",
                "gender": "%(sex)s",
                "fullName": "%(clientFIo)s",
                "registeredInTheRegion": true
            },
            "requesterPractitioner": {
                "identityDocument": {
                    "system": "223",
                    "code": "%(PersSnils)s"
                },
                "fullName": "%(PersonFull)s",
                "position": "%(postPerson)s",
                "specialty": "%(specialityPerson)s",
                "department": "%(lpuCode)s",
                "telecom": {
                    "phone": "%(phonePerson)s",
                    "email": "%(mailPerson)s"
                }
            },
            "serviceRequest": {
                "urgency": "%(urgency)s",
                "primaryAppeal": "%(primaryAppeal)s",
                "requesterOrganization": "%(lpuCode)s",
                "performerOrganization": "%(performerOrganization)s",
                "category": "%(category)s",
                "reasonCode": "%(reasonCode)s"
            },
            "requesterCondition": {
                "codeMKB": "%(codeMKB)s",
                "anamnesis": "%(anamnez)s"
            },
            "attachedfiles": [%(files)s]
        },
        "roleContext": []
    }

            """ % {"lpuCode": forceString(lpuCode.value(0)), 'mailPerson': forceString(mailPerson.value(0)),
                   'phonePerson': phonePerson, 'postPerson': postPerson,
                   'specialityPerson': forceString(specialityPerson),
                   'performerOrganization': forceString(performerOrganization.value(0)),
                   'PersonFull': actionInfo.person.fullName, 'PersSnils': actionInfo.person.SNILS,
                   'codeMKB': actionInfo.MKB, 'category': forceString(category.value(0)),
                   'anamnez': anamnez, 'reasonCode': reasonCodeList.index(reasonCode) + 1,
                   'primaryAppeal': primaryAppealList.index(primaryAppeal) + 1,
                   'urgency': urgencyList.index(urgency) + 1, 'clientMPI': client,
                   'clientFIo': clientFIo, 'clientBirthDate': clientBirthDate, 'sex': clientInfo.sexCode,
                   'clientDoc': clientDoc, 'clientDocCode': clientDocCode, 'files': files}

        headers = {"authorization": urlAuth, "content-type": "application/json"}

        try:
            response = requests.post(urlService+'/Commands/StartNewProcess',
                                     data=stmt.encode('UTF-8'), headers=headers, timeout=60)

            if response.status_code == 200 and response.json()['success']:
                response_Json = response.json()
                action[u'Статус'] = StatusDict[response_Json["stageId"]]
                action[u'Идентификатор статуса'] = response_Json["stageId"]
                action[u'Идентификатор направления'] = response_Json["processId"]
                action[u'Номер заявки'] = response_Json["humanFriendlyId"]
                action.getRecord().setValue('status', 1)
                return 1
            else:
                QtGui.QMessageBox.warning(self,
                                          u'Ошибка при создании заявки',
                                          exceptionToUnicode(response.status_code),
                                          QtGui.QMessageBox.Ok,
                                          QtGui.QMessageBox.Ok)
            return
        except Exception, e:
            QtGui.QMessageBox.critical(self,
                                       u'Ошибка при создании заявки',
                                       exceptionToUnicode(e),
                                       QtGui.QMessageBox.Ok,
                                       QtGui.QMessageBox.Ok)

            return
    else:

        textError = ''

        if not postPerson:
            textError += u'Не указана идентификация для должности исполнителя по справочнику 1.2.643.5.1.13.13.99.2.181 \n'
        if not specialityPerson:
            textError += u'Не указана идентификация для специальности исполнителя по справочнику 1.2.643.5.1.13.13.11.1066 \n'
        if not phonePerson:
            textError += u'Не указан телефон для связи в направлении \n'
        if not mailPerson:
            textError += u'Не указана электронная почта (находится в карточке организации, поле "E-mail") \n'
        if not lpuCode:
            textError += u'Не указана идентификация для МО - направителя по справочнику 1.2.643.2.69.1.1.1.64 \n'
        if not performerOrganization:
            textError += u'Не указана идентификация для целевой МО по справочнику 1.2.643.2.69.1.1.1.64 \n'
        if not anamnez:
            textError += u'В направлении не заполнено свойство "Анамнез" \n'
        if not reasonCode:
            textError += u'В направлении не указана "Цель телемедицинской консультации" \n'
        if not category:
            textError += u'В справочнике профилей мед. помощи не заполнен федеральный код по скравочнику 1.2.643.2.69.1.1.1.56 \n'
        if not primaryAppeal:
            textError += u'В направлении не заполнено свойство "Повторный прием" \n'
        if not urgency:
            textError += u'В направлении не заполнено свойство "Срочность выполнения" \n'
        if not client:
            textError += u'Не удалось определить идентификатор пациента в MPI \n'
        if not clientBirthDate:
            textError += u'У пациента не указана дата рождения \n'
        if not clientDoc:
            textError += u'У пациента не указан документ УДЛ \n'
        if not clientDocCode:
            textError += u'У докумена УДЛ не указана идентификация по справочнику 1.2.643.2.69.1.1.1.6 \n'

        QtGui.QMessageBox.warning(self,
                                  u'Внимание!',
                                  u'"%s"!' % textError,
                                  QtGui.QMessageBox.Ok,
                                  QtGui.QMessageBox.Ok
                                  )
        return


def moveToStage_action(self, action, transitionId, comments = None):
    urlService = forceString(QtGui.qApp.db.translate('GlobalPreferences', 'code', 'TMKServiceUrl', 'value'))
    urlAuth = forceString(QtGui.qApp.db.translate('GlobalPreferences', 'code', 'TMKServiceAuth', 'value'))

    lpuCode = QtGui.qApp.db.getRecordEx('Organisation_Identification', 'value',
                                        'master_id = %s AND deleted=0 AND system_id in (SELECT id FROM rbAccountingSystem `as` WHERE `as`.urn="urn:oid:1.2.643.2.69.1.1.1.64")' % str(
                                            QtGui.qApp.currentOrgId()))


    status = action[u'Идентификатор статуса']
    MKB = forceString(action._record.value('MKB'))
    dopInfo = action[u'Запрос дополнительных сведений о пациенте']
    dopInfoEx = action[u'Дополнительные медицинские сведения о пациенте']
    files = ''

    if status == 'fff74636-1c39-448a-bbae-0f14f8c1f6a5':
        transitionId = '92d181d2-9881-4f7d-9d7a-694fbcf3a24b'

    if status == '85dad08c-1eb7-479f-8bf5-66b3ea5e4a02' and transitionId == '72af8a14-e276-4e33-9988-b51cf141f66f':
        id = QDateTime().currentDateTime().toString('dd-MM-yyyy hh:mm:ss')
        userId = QtGui.qApp.userId
        author = forceString(QtGui.qApp.db.translate('Person', 'id', userId, 'formatPersonName(id)')) if userId else ''
        comment = u"""
            "processContext": {
            "communication": [
            {
                "id": "%(id)s",
                "isDeleted": false,
                "author": "%(author)s",
                "type": "2",
                "comment": "%(dopInfo)s"
            }
        ]
        },
            """ % {'dopInfo': dopInfo, 'author': author, 'id': id}
    elif status == 'f0093882-61f3-4684-aa0e-52094991cbf8' and transitionId == '1f973a5f-9d8c-466a-abc2-a27d1ed1072d':
        idx = 1
        id = QDateTime().currentDateTime().toString('dd-MM-yyyy hh:mm:ss')
        userId = QtGui.qApp.userId
        author = forceString(QtGui.qApp.db.translate('Person', 'id', userId, 'formatPersonName(id)')) if userId else ''
        if len(action._attachedFileItemList) > 0:
            for record_attach in action._attachedFileItemList:
                if record_attach.comment == u'':
                    doc = uploadFiles(self, record_attach, lpuCode, True)
                    record_attach.getRecord('Action_FileAttach').setValue('comment', doc)
                else:
                    doc = record_attach.comment

                if idx != 1:
                    files += ','
                files += u"""
                            {
                            "id": "%(idx)s",
                            "fileURL": "%(fileURL)s",
                            "isDeleted": false
                        }""" % {'idx': idx, 'fileURL': doc}
                idx += 1
        comment = u"""
                "processContext": {
            "communication": [
            {
                "id": "%(id)s",
                "isDeleted": false,
                "author": "%(author)s",
                "type": "0",
                "comment": "%(dopInfoEx)s"
            }
        ],
                    "attachedfiles": [%(files)s]
                },
                    """ % {'dopInfoEx': dopInfoEx, 'files': files, 'author': author, 'id': id}
    else:
        comment = ''


    if transitionId == 'e0403d8b-aedc-446e-942d-c47822b67e3c':
        # fileAttach = QtGui.qApp.db.getRecordEx('Action_FileAttach a',
        #                                        'SUBSTRING_INDEX(a.path, "/", -1) as name, a.path, a.respSignatureBytes',
        #                                        'master_id = %s AND a.deleted=0 and a.path LIKE "%%.pdf" ' % str(
        #                                            forceRef(action._record.value('id'))))

        doc = uploadFiles(self, action._attachedFileItemList[-1], lpuCode, True)
        if not doc:
            return
        RecordPerson = u"""            
        SELECT s.value AS spec, pi.value AS post, oo.value AS org, pc_phone.contact AS phone, pc_mail.contact AS mail, SNILS, CONCAT(p.lastName,' ',p.firstName,' ',p.patrName)
  FROM Person p
  LEFT JOIN rbSpeciality_Identification s ON s.master_id=p.speciality_id AND s.system_id = (SELECT id FROM rbAccountingSystem WHERE urn = "urn:oid:1.2.643.5.1.13.13.11.1066")
  LEFT JOIN rbPost_Identification pi ON pi.master_id=p.post_id AND pi.system_id = (SELECT id FROM rbAccountingSystem WHERE urn = "urn:oid:1.2.643.5.1.13.13.99.2.181")
  LEFT JOIN Organisation_Identification oo ON p.org_id = oo.master_id AND oo.deleted=0 AND oo.system_id in (SELECT id FROM rbAccountingSystem `as` WHERE `as`.urn="urn:oid:1.2.643.2.69.1.1.1.64" )
  LEFT JOIN Person_Contact pc_phone ON p.id = pc_phone.master_id AND pc_phone.deleted=0 and pc_phone.contactType_id in (SELECT id FROM rbContactType WHERE (name LIKE "%%рабоч%%") OR (name LIKE "%%мобил%%"))
  LEFT JOIN Person_Contact pc_mail ON p.id = pc_mail.master_id AND pc_mail.deleted=0 and pc_mail.contactType_id in (SELECT id FROM rbContactType WHERE (name LIKE "%%mail%%") OR (name LIKE "%%почт%%"))
  WHERE p.id = %(personId)s;
                    """ % {"personId": forceString(action._record.value('person_id'))}

        records = QtGui.qApp.db.query(RecordPerson)
        if records.first():
            record = records.record()
        else:
            return
        comment = u"""
                    "processContext": {
        "performerCondition": {
            "codeMKB": "%(MKB)s"
        },
        "diagnosticReport": {
            "documentNumber": "%(documentNumber)s",
            "OutpatientCoupon": "%(coupon)s",
            "conclusion": "Консультативное заключение"
        },
        "presentedForm": {
            "fileURL": "%(doc)s"
        },
        "performerPractitioner": {
                "position": "%(post)s",
                "telecom": {
                    "phone": "%(phone)s",
                    "email": "%(mail)s"
                }
            }
    },
                    """ % {"documentNumber": forceString(action._record.value('id')), 'MKB': MKB,
       'transitionId_': transitionId, 'comment': comment, 'doc': doc, 'coupon': action[u'Идентификатор талона'], 'post': forceString(record.value(1)),
                           'phone': forceString(record.value(3)), 'mail': forceString(record.value(4))}


    if transitionId == '92d181d2-9881-4f7d-9d7a-694fbcf3a24b':
        sign = uploadFiles(self, action._attachedFileItemList[-1], lpuCode, False)
        if not sign:
            return
        comment = u"""
                "processContext": {
                      "presentedForm": {
                          "signatureURL": "%s"
                      }
                  },
                    """ % forceString(sign)


    stmt = u"""
{
"processId": "%(processId)s",
    "transitionId": "%(transitionId_)s",
    %(comment)s
    "roleContext": [
       {
            "Role": "HEAD_DOCTOR",
            "Organization": "%(lpuCode)s",
            "SNILS": "777-777-777"
        }
    ]

}
""" % {"lpuCode": forceString(lpuCode.value(0)), 'processId': action[u'Идентификатор направления'],
       'transitionId_': transitionId, 'comment': comment}

    headers = {"authorization": urlAuth, "content-type": "application/json"}

    try:
        response = requests.post(urlService+'/Commands/MoveToStage',
                                 data=stmt.encode('UTF-8'), headers=headers, timeout=60)

        if response.status_code == 200 and response.json()['success']:
            response_Json = response.json()
            if u'stageId' in response_Json:
                action[u'Статус'] = StatusDict[response_Json["stageId"]]
                action[u'Идентификатор статуса'] = response_Json["stageId"]
                if response_Json["stageId"] and transitionId == '1b2ff3f0-794a-466c-88c2-61bbff931fd9':
                    action.getRecord().setValue('status', 3)
                elif response_Json["stageId"] and response_Json["stageId"] == '764f55f2-2c0e-43e3-81ce-3e5626682322':
                    action.getRecord().setValue('status', 6)
                elif response_Json["stageId"] and response_Json["stageId"] in ('ba65d940-8ebd-4583-a6cb-9a0f683ed331','ea0e8711-7b6e-4ad3-8bc2-904006eb569d'):
                    action.getRecord().setValue('status', 2)
                else:
                    action.getRecord().setValue('status', 1)
                if transitionId == '72af8a14-e276-4e33-9988-b51cf141f66f':
                    tempDopAction = action[u'Дополнительная информация участников процесса'] if action[u'Дополнительная информация участников процесса'] else ''
                    action[u'Дополнительная информация участников процесса'] = tempDopAction + u'\\n- Целевое МО запрашивает '+action[u'Запрос дополнительных сведений о пациенте']
                    action[u'Запрос дополнительных сведений о пациенте'] = ''
                if transitionId == 'e0403d8b-aedc-446e-942d-c47822b67e3c':
                    moveToStage_action(self, action, '92d181d2-9881-4f7d-9d7a-694fbcf3a24b')
            else:
                getProcess(self, action)
            return 200
        else:
            getProcess(self, action)
        return response.status_code
    except Exception, e:
        QtGui.QMessageBox.critical(self,
                                   u'Ошибка при создании заявки',
                                   exceptionToUnicode(e),
                                   QtGui.QMessageBox.Ok,
                                   QtGui.QMessageBox.Ok)

        return 1


def getProcessContext(self, action):
    urlService = forceString(QtGui.qApp.db.translate('GlobalPreferences', 'code', 'TMKServiceUrl', 'value'))
    urlAuth = forceString(QtGui.qApp.db.translate('GlobalPreferences', 'code', 'TMKServiceAuth', 'value'))
    lpuCode = QtGui.qApp.db.getRecordEx('Organisation_Identification', 'value',
                                        'master_id = %s AND deleted=0 AND system_id in (SELECT id FROM rbAccountingSystem `as` WHERE `as`.urn="urn:oid:1.2.643.2.69.1.1.1.64")' % str(
                                            QtGui.qApp.currentOrgId()))

    stmt = u"""
{
	"RoleContext": [
        {
            "Role": "HEAD_DOCTOR",
            "Organization": "%(lpuCode)s",
            "SNILS": "777-777-777"
        }
    ],
"processId": "%(processId)s"
}
""" % {"lpuCode": forceString(lpuCode.value(0)), 'processId': action[u'Идентификатор направления']}

    headers = {"authorization": urlAuth, "content-type": "application/json"}

    try:
        response = requests.post(urlService+'/Queries/GetProcessContext',
                                 data=stmt.encode('UTF-8'), headers=headers, timeout=60)

        if response.status_code == 200 and response.json()['success']:
            response_Json = response.json()
            action[u'Статус'] = StatusDict[response_Json["stageId"]]
            action[u'Идентификатор статуса'] = response_Json["stageId"]
            action.status = 1 if response_Json["stageId"] != '764f55f2-2c0e-43e3-81ce-3e5626682322' else 3
            return 200
        else:
            QtGui.QMessageBox.warning(self,
                                      u'Невозможно определить статус текущей заявки',
                                      exceptionToUnicode(response.status_code),
                                      QtGui.QMessageBox.Ok,
                                      QtGui.QMessageBox.Ok)
        return response.status_code
    except Exception, e:
        QtGui.QMessageBox.critical(self,
                                   u'Ошибка при создании заявки',
                                   exceptionToUnicode(e),
                                   QtGui.QMessageBox.Ok,
                                   QtGui.QMessageBox.Ok)

        return 1


def getProcess(self, action):
    urlService = forceString(QtGui.qApp.db.translate('GlobalPreferences', 'code', 'TMKServiceUrl', 'value'))
    urlAuth = forceString(QtGui.qApp.db.translate('GlobalPreferences', 'code', 'TMKServiceAuth', 'value'))
    headers = {"authorization": urlAuth, "content-type": "application/json"}

    try:
        response = requests.get(urlService+'/Queries/GetProcess/' + action[
            u'Идентификатор направления'].encode("UTF-8"), headers=headers,
                                timeout=60)

        if response.status_code == 200 and response.json()['success']:
            response_Json = response.json()
            status = response_Json['result']['currentStageId']
            action[u'Статус'] = StatusDict[status]
            action[u'Идентификатор статуса'] = status
            action.getRecord().setValue('status', 1 if status != '764f55f2-2c0e-43e3-81ce-3e5626682322' else 3)
            return 1
        else:
            QtGui.QMessageBox.warning(self,
                                      u'Невозможно определить статус текущей заявки',
                                      exceptionToUnicode(response.status_code),
                                      QtGui.QMessageBox.Ok,
                                      QtGui.QMessageBox.Ok)
        return response.status_code
    except Exception, e:
        QtGui.QMessageBox.critical(self,
                                   u'Ошибка при создании заявки',
                                   exceptionToUnicode(e),
                                   QtGui.QMessageBox.Ok,
                                   QtGui.QMessageBox.Ok)

        return 1


def moveToStageEdit(self, action, transitionId, record):
    urlService = forceString(QtGui.qApp.db.translate('GlobalPreferences', 'code', 'TMKServiceUrl', 'value'))
    urlAuth = forceString(QtGui.qApp.db.translate('GlobalPreferences', 'code', 'TMKServiceAuth', 'value'))
    urgencyList = [
        u'Экстренная',
        u'Неотложная',
        u'Плановая',
    ]
    reasonCodeList = [
        u'Определение (подтверждение) диагноза',
        u'Определение (подтверждение) тактики лечения и методов диагностики',
        u'Согласование направления пациента в медицинскую организацию',
        u'Согласование перевода пациента в медицинскую организацию',
        u'Интерпретация результатов диагностического исследования',
        u'Получение экспертного мнения по результату диагностического исследования',
        u'Разбор клинического случая',
        u'Дистанционное наблюдение за пациентом',
        u'Другое'
    ]
    primaryAppealList = [
        u'первично',
        u'повторно',
    ]

    context = CInfoContext()
    actionInfo = context.getInstance(CActionInfo, forceRef(record.value('id')))
    postPerson = actionInfo.person.post.identify('urn:oid:1.2.643.5.1.13.13.99.2.181')

    specialityPerson = QtGui.qApp.db.getRecordEx('rbSpeciality_Identification', 'value',
                                                 'master_id = %s and system_id = (SELECT id FROM rbAccountingSystem WHERE urn = "urn:oid:1.2.643.5.1.13.13.11.1066")' % str(
                                                     actionInfo.person.speciality.specialityId))
    phonePerson = actionInfo[u'Телефон направителя'].value
    mailPerson = QtGui.qApp.db.getRecordEx('Organisation', 'email', 'id = %s AND deleted=0 ' % str(QtGui.qApp.currentOrgId()))

    lpuCode = QtGui.qApp.db.getRecordEx('Organisation_Identification', 'value',
                                        'master_id = %s AND deleted=0 AND system_id in (SELECT id FROM rbAccountingSystem `as` WHERE `as`.urn="urn:oid:1.2.643.2.69.1.1.1.64")' % str(
                                            QtGui.qApp.currentOrgId()))
    performerOrganization = QtGui.qApp.db.getRecordEx('Organisation_Identification', 'value',
                                                      'master_id = %s AND deleted=0 AND system_id in (SELECT id FROM rbAccountingSystem `as` WHERE `as`.urn="urn:oid:1.2.643.2.69.1.1.1.64")' % str(
                                                          actionInfo[u'Куда направляется'].value.id))

    anamnez = actionInfo[u'Анамнез заболевания'].value.replace('"',"'").replace('\\','/')
    reasonCode = actionInfo[u'Цель телемедицинской консультации'].value

    category = QtGui.qApp.db.getRecordEx('rbMedicalAidProfile', 'federalCode',
                                         'id = %s ' % str(actionInfo[u'Профиль'].value.id))

    primaryAppeal = actionInfo[u'Повторный приём'].value
    urgency = actionInfo[u'Срочность выполнения'].value

    files = ''
    idx = 1
    if len(action._attachedFileItemList) > 0:
        for record_attach in action._attachedFileItemList:
            if record_attach.comment == u'':
                doc = uploadFiles(self, record_attach, lpuCode, True)
                record_attach.getRecord('Action_FileAttach').setValue('comment', doc)
            else:
                doc = record_attach.comment

            if idx != 1:
                files += ','
            files += u"""
                {
                "id": "%(idx)s",
                "fileURL": "%(fileURL)s",
                "isDeleted": false
            }""" %{'idx': idx, 'fileURL': doc}
            idx += 1


    clientInfo = actionInfo.event.client
    clientFIo = clientInfo.lastName + u' ' + clientInfo.firstName + u' ' + clientInfo.patrName
    clientBirthDate = clientInfo.birthDate
    if lpuCode:
        client = clientMPI(actionInfo.event.client.id, forceString(lpuCode.value(0)))
    if clientInfo.document and clientInfo.document.serial and clientInfo.document.number:
        clientDoc = forceString(clientInfo.document.serial).replace(' ', '') + ':' + forceString(clientInfo.document.number)
    else:
        clientDoc = forceString(clientInfo.document.serial) if clientInfo.document.serial else forceString(
            clientInfo.document.number) if clientInfo.document.number else None
    if clientInfo.document and u'n3.DocumentType' in clientInfo.document.identification.byCode:
        clientDocCode = forceString(clientInfo.document.identification.byCode[u'n3.DocumentType'])
    else:
        clientDocCode = None
    if postPerson and specialityPerson and phonePerson and mailPerson and lpuCode and performerOrganization and anamnez and reasonCode and category and primaryAppeal and urgency and client and clientBirthDate and clientDoc and clientDocCode:
        stmt = u"""
                {
                "processId": "%(processId)s",
                "transitionId": "%(transitionId)s",
            "processContext": {
                "patient": {
                    "idMPI": "%(clientMPI)s",
                    "identityDocument": {
                        "system": "%(clientDocCode)s",
                        "code": "%(clientDoc)s"
                    },
                    "birthDate": "%(clientBirthDate)s",
                    "gender": "%(sex)s",
                    "fullName": "%(clientFIo)s",
                    "registeredInTheRegion": true
                },
                "requesterPractitioner": {
                    "identityDocument": {
                        "system": "223",
                        "code": "%(PersSnils)s"
                    },
                    "fullName": "%(PersonFull)s",
                    "position": "%(postPerson)s",
                    "specialty": "%(specialityPerson)s",
                    "department": "%(lpuCode)s",
                    "telecom": {
                        "phone": "%(phonePerson)s",
                        "email": "%(mailPerson)s"
                    }
                },
                "serviceRequest": {
                    "urgency": "%(urgency)s",
                    "primaryAppeal": "%(primaryAppeal)s",
                    "performerOrganization": "%(performerOrganization)s",
                    "category": "%(category)s",
                    "reasonCode": "%(reasonCode)s"
                },
                "requesterCondition": {
                    "codeMKB": "%(codeMKB)s",
                    "anamnesis": "%(anamnez)s"
                },
                "attachedfiles": [%(files)s]
            },
            "RoleContext": [
            {
                "Role": "HEAD_DOCTOR",
                "Organization": "%(lpuCode)s",
                "SNILS": "777-777-777"
            }
             ],
        }

                """ % {"lpuCode": forceString(lpuCode.value(0)), 'mailPerson': forceString(mailPerson.value(0)),
                       'phonePerson': phonePerson, 'postPerson': postPerson,
                       'specialityPerson': forceString(specialityPerson.value(0)),
                       'performerOrganization': forceString(performerOrganization.value(0)),
                       'PersonFull': actionInfo.person.fullName, 'PersSnils': actionInfo.person.SNILS,
                       'codeMKB': actionInfo.MKB, 'category': forceString(category.value(0)),
                       'anamnez': anamnez, 'reasonCode': reasonCodeList.index(reasonCode) + 1,
                       'primaryAppeal': primaryAppealList.index(primaryAppeal) + 1,
                       'urgency': urgencyList.index(urgency) + 1, 'clientMPI': client,
                       'clientFIo': clientFIo, 'clientBirthDate': clientBirthDate, 'sex': clientInfo.sexCode,
                       'clientDoc': clientDoc, 'clientDocCode': clientDocCode,
                       'processId': action[u'Идентификатор направления'].encode("UTF-8"), 'transitionId': transitionId, 'files': files}

        headers = {"authorization": urlAuth, "content-type": "application/json"}

        try:
            response = requests.post(urlService+'/Commands/MoveToStage',
                                     data=stmt.encode('UTF-8'), headers=headers, timeout=60)

            if response.status_code == 200 and response.json()['success']:
                action.getRecord().setValue('status', 1)
                return 1
            else:
                QtGui.QMessageBox.warning(self,
                                          u'Ошибка при создании заявки',
                                          exceptionToUnicode(response.status_code),
                                          QtGui.QMessageBox.Ok,
                                          QtGui.QMessageBox.Ok)
            return
        except Exception, e:
            QtGui.QMessageBox.critical(self,
                                       u'Ошибка при создании заявки',
                                       exceptionToUnicode(e),
                                       QtGui.QMessageBox.Ok,
                                       QtGui.QMessageBox.Ok)

            return
    else:

        textError = ''

        if not postPerson:
            textError += u'Не указана идентификация для должности исполнителя по справочнику 1.2.643.5.1.13.13.99.2.181 \n'
        if not specialityPerson:
            textError += u'Не указана идентификация для специальности исполнителя по справочнику 1.2.643.5.1.13.13.11.1066 \n'
        if not phonePerson:
            textError += u'Не указан телефон для связи в направлении \n'
        if not mailPerson:
            textError += u'Не указана электронная почта (находится в карточке организации, поле "E-mail") \n'
        if not lpuCode:
            textError += u'Не указана идентификация для МО - направителя по справочнику 1.2.643.2.69.1.1.1.64 \n'
        if not performerOrganization:
            textError += u'Не указана идентификация для целевой МО по справочнику 1.2.643.2.69.1.1.1.64 \n'
        if not anamnez:
            textError += u'В направлении не заполнено свойство "Анамнез" \n'
        if not reasonCode:
            textError += u'В направлении не указана "Цель телемедицинской консультации" \n'
        if not category:
            textError += u'В справочнике профилей мед. помощи не заполнен федеральный код по скравочнику 1.2.643.2.69.1.1.1.56 \n'
        if not primaryAppeal:
            textError += u'В направлении не заполнено свойство "Повторный прием" \n'
        if not urgency:
            textError += u'В направлении не заполнено свойство "Срочность выполнения" \n'
        if not client:
            textError += u'Не удалось определить идентификатор пациента в MPI \n'
        if not clientBirthDate:
            textError += u'У пациента не указана дата рождения \n'
        if not clientDoc:
            textError += u'У пациенте не указан документ УДЛ \n'
        if not clientDocCode:
            textError += u'У докумена УДЛ не указана идентификация по справочнику 1.2.643.2.69.1.1.1.6 \n'

        QtGui.QMessageBox.warning(self,
                                  u'Внимание!',
                                  u'"%s"!' % textError,
                                  QtGui.QMessageBox.Ok,
                                  QtGui.QMessageBox.Ok
                                  )
        return

def uploadFiles(self, fileAttach, lpuCode, is_File = False):
    urlService = forceString(QtGui.qApp.db.translate('GlobalPreferences', 'code', 'TMKServiceUrl', 'value'))
    urlServiceFiles = forceString(QtGui.qApp.db.translate('GlobalPreferences', 'code', 'TMKServiceUrlFiles', 'value'))
    urlAuth = forceString(QtGui.qApp.db.translate('GlobalPreferences', 'code', 'TMKServiceAuth', 'value'))
    sabre = forceString(QtGui.qApp.db.translate('GlobalPreferences', 'code', 'WebDAV', 'value'))
    lpu = forceString(forceString(lpuCode.value(0)))

    # tempLPU = '05a6a944-f754-47d5-a9ef-acef307a7369' 5054263
    def latinizator(letter, dic):
        for i, j in dic.items():
            letter = letter.replace(i, j)
        return letter

    legend = {u' ': '_', u',': '', u'а': 'a', u'б': 'b', u'в': 'v', u'г': 'g', u'д': 'd', u'е': 'e', u'ё': 'yo',
              u'ж': 'zh', u'з': 'z', u'и': 'i', u'й': 'y', u'к': 'k', u'л': 'l', u'м': 'm', u'н': 'n', u'о': 'o',
              u'п': 'p', u'р': 'r', u'с': 's', u'т': 't', u'у': 'u', u'ф': 'f', u'х': 'h', u'ц': 'c', u'ч': 'ch',
              u'ш': 'sh', u'щ': 'shch', u'ъ': 'y', u'ы': 'y', u'ь': "'", u'э': 'e', u'ю': 'yu', u'я': 'ya',
              u'А': 'A', u'Б': 'B', u'В': 'V', u'Г': 'G', u'Д': 'D', u'Е': 'E', u'Ё': 'Yo', u'Ж': 'Zh', u'З': 'Z',
              u'И': 'I', u'Й': 'Y', u'К': 'K', u'Л': 'L', u'М': 'M', u'Н': 'N', u'О': 'O', u'П': 'P', u'Р': 'R',
              u'С': 'S', u'Т': 'T', u'У': 'U', u'Ф': 'F', u'Х': 'H', u'Ц': 'Ts', u'Ч': 'Ch', u'Ш': 'Sh', u'Щ': 'Shch',
              u'Ъ': 'Y', u'Ы': 'Y', u'Ь': "'", u'Э': 'E', u'Ю': 'Yu', u'Я': 'Ya',
              }


    url = urlServiceFiles+"/orgs/files?org_id="+lpu+"&apikey=9C51C68C-C01C-4864-A627-A2D7DCED86C2&token="+urlAuth.split(' ')[1]
    # url = urlServiceFiles+"/orgs/files?org_id="+lpu+"&apikey=9C51C68C-C01C-4864-A627-A2D7DCED86C2&token="+urlAuth.split(' ')[1]
   # url = "https://r78-rc.tm.zdrav.netrika.ru/api/orgs/files?org_id=05a6a944-f754-47d5-a9ef-acef307a7369&apikey=a2bb4a653d913adb57d8ba3604ef61bb&token=36fc79c8-956e-4ebb-ad0a-5fcdd25b1ad7"

    path = fileAttach.persistentDir
    name = fileAttach.newName
    respSignatureBytes = forceString(fileAttach.getRecord('Action_FileAttach').value('respSignatureBytes'))

    def normalization(prepared_request):
        filename = name.encode('utf-8')
        prepared_request.body = re.sub(b'filename\*=.*', b'filename="' + filename+'"', prepared_request.body)
        return prepared_request

    if is_File:
        file = requests.get(sabre + '/' + path + '/' + name, verify=False)


        if file.status_code == 200:
            # file_new = latinizator(name, legend)

            files = {'file': (name, file.content)}

            resDoc = requests.post(url, verify=False, files=files, auth=normalization)

            if resDoc.status_code == 200:
                return resDoc.json()['info']['download_url']
            else:
                QtGui.QMessageBox.warning(self,
                                          u'Внимание!',
                                          u'Не удалось отправить файл заявки!\n'+resDoc.json()['error'],
                                          QtGui.QMessageBox.Ok,
                                          QtGui.QMessageBox.Ok
                                          )
                return
        else:
            QtGui.QMessageBox.warning(self,
                                      u'Внимание!',
                                      u'Не удалось загрузить файл заявки!\n'+file.json()['error'],
                                      QtGui.QMessageBox.Ok,
                                      QtGui.QMessageBox.Ok
                                      )
            return
    else:
        files = {'file': respSignatureBytes}
        res = requests.post(url, verify=False, files=files)

        if res.status_code == 200:
            return res.json()['info']['download_url']
        else:
            QtGui.QMessageBox.warning(self,
                                      u'Внимание!',
                                      u'Не удалось отправить подпись!',
                                      QtGui.QMessageBox.Ok,
                                      QtGui.QMessageBox.Ok
                                      )
            return