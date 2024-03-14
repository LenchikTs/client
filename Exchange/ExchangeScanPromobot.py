# -*- coding: utf-8 -*-
import requests
from PyQt4 import QtGui
from PyQt4.QtCore import QDate
from requests import HTTPError, ConnectionError

from library.Utils import forceRef, forceString


def scanning():
    params = {}
    newData = {}
    try:
        url = forceString(QtGui.qApp.preferences.appPrefs.get('ScanPromobotAddress'))
        if not url:
            QtGui.QMessageBox().warning(None, u'Внимание!', u'Не указан адрес сканера в настройках')
            return newData
        response = requests.get(url + '/scan_and_rec', timeout=10)
        response.raise_for_status()
    except HTTPError, e:
        QtGui.QMessageBox().warning(None, u'Ошибка получения данных', e.message)
        return newData
    except ConnectionError, e:
        QtGui.QMessageBox().warning(None, u'Ошибка подключения к сканеру', e.message.message.decode('utf-8'))
        return newData

    data = response.json()

    if data.get('status', None) == 'OK':
        for res in data['results']:
            if res['is_accepted']:
                params[res['name']] = res['value']
    else:
        QtGui.QMessageBox().warning(None, u'Внимание!', u'Ошибка распознавания документа. Повторите сканирование')
    if params:
        db = QtGui.qApp.db
        newData['doc_type'] = data['doc_type']
        newData['lastName'] = params.get('surname', '')
        newData['firstName'] = params.get('name', '')
        newData['patrName'] = params.get('patronymic', '')
        if params.get('birth_date', None):
            newData['birthDate'] = QDate().fromString(params['birth_date'], 'dd.MM.yyyy')
        else:
            newData['birthDate'] = None
        if params.get('gender', None):
            if data['doc_type'] in ['rus.snils.type1', 'rus.snils.type2']:
                if u'M' in params['gender']:
                    newData['sex'] = 1
                elif u'F' in params['gender']:
                    newData['sex'] = 2
                else:
                    newData['sex'] = 0
            elif data['doc_type'] in ['rus.passport.national', 'rus.birth_certificate.type1',
                                      'rus.birth_certificate.type2']:
                if u'М' in params['gender']:
                    newData['sex'] = 1
                elif u'Ж' in params['gender']:
                    newData['sex'] = 2
                else:
                    newData['sex'] = 0
        else:
            newData['sex'] = 0

        if data['doc_type'] in ['rus.birth_certificate.type1', 'rus.birth_certificate.type2']:
            newData['docTypeId'] = forceRef(db.translate('rbDocumentType', 'regionalCode', '3', 'id'))
            newData['docTypeTitle'] = forceString(db.translate('rbDocumentType', 'regionalCode', '3', 'title'))
            if params.get('series', None) and len(params['series'].split('-')) == 2:
                newData['serialLeft'] = params.get('series').split('-')[0]
                newData['serialRight'] = params.get('series').split('-')[1]
                newData['serial'] = '-'.join([newData.get('serialLeft'), newData.get('serialRight')])
        elif data['doc_type'] == 'rus.passport.national':
            newData['docTypeId'] = forceRef(db.translate('rbDocumentType', 'regionalCode', '14', 'id'))
            newData['docTypeTitle'] = forceString(db.translate('rbDocumentType', 'regionalCode', '14', 'title'))
            if params.get('series', None):
                newData['serialLeft'] = params['series'][:2]
                newData['serialRight'] = params['series'][2:]
                newData['serial'] = ''.join([newData['serialLeft'], newData['serialRight']])
        else:
            newData['docTypeId'] = None
            newData['docTypeTitle'] = u'СНИЛС'
            newData['serial'] = ''
            newData['serialLeft'] = None
            newData['serialRight'] = None

        newData['number'] = params.get('number', '')
        if params.get('issue_date', None):
            newData['issueDate'] = QDate().fromString(params['issue_date'], 'dd.MM.yyyy')
        else:
            newData['issueDate'] = None
        newData['docOrigin'] = params.get('authority', '')
        newData['docOriginCode'] = params.get('authority_code', '')
        newData['birthPlace'] = params.get('birth_place', '')
    return newData
