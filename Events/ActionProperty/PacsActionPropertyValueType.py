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
from PyQt4.QtCore import QVariant, QUrl, SIGNAL

import json
import socket
import subprocess
import shlex
import os

# from library.Pacs.RestToolbox  import postRequest, getRequest
# from library.Pacs.Explorer     import CPacsExplorer
# from library.DbEntityCache     import CDbEntityCache
from library.Utils             import forceInt, forceString

from ActionPropertyValueType   import CActionPropertyValueType


class CPacsActionPropertyValueType(CActionPropertyValueType):
    name         = 'PacsImages'
    variantType  = QVariant.String


    def __init__(self, domain = None):
        CActionPropertyValueType.__init__(self, domain)


    class CPropEditor(QtGui.QPushButton):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            QtGui.QPushButton.__init__(self, parent)
            self.setText(u'Открыть')
            self.connect(self, SIGNAL('clicked()'), self.onClick)
            self._value = None
            self._clientId = clientId

        def setValue(self, value):
            self._value = value
            self.setEnabled(bool(value))


        def value(self):
            return self._value


        def onClick(self):
            try:
                values = json.loads(forceString(self._value))
            except:
                QtGui.QMessageBox.critical(self,
                    u'Внимание!',
                    u'Ошибка данных пакс сервера',
                    QtGui.QMessageBox.Ok,
                    QtGui.QMessageBox.Ok)
                return
            appPrefs = QtGui.qApp.preferences.appPrefs
            type = forceInt(appPrefs.get('pacsType'))
            path = forceString(appPrefs.get('pacsParams'))
            wado = forceString(appPrefs.get('pacsWado'))
            if not path:
                path = forceString(appPrefs.get('pacsImagesBrowser'))
            if not path:
                path = QtGui.qApp._globalPreferences.get('pacs', None)
                type = 2
            if not path:
                QtGui.QMessageBox.critical(self,
                    u'Внимание!',
                    u'Просмотр изображений не настроен',
                    QtGui.QMessageBox.Ok,
                    QtGui.QMessageBox.Ok)
                return
            path = path.replace('{StudyUID}', values.get('StudyUID', ''))
            path = path.replace('{StudyID}', values.get('StudyID', ''))
            path = path.replace('{PatientID}', unicode(self._clientId))
            if type == 0:
                path.replace('\\', '/')
                args = shlex.split(path)
                subprocess.Popen(args, cwd=os.path.dirname(args[0]))
            elif type == 1:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    s.connect(('127.0.0.1', 17179))
                    s.recv(10000)
                    s.send('dicom:close --all\n\r')
                    s.send('dicom:get -w %s\n\r'%(wado + '/study/%s'%values.get('StudyUID', '')))
                    s.close()
                except:
                    path.replace('\\', '/')
                    subprocess.Popen([path, ('$dicom:get -w ' + wado + '/study/%s'%values.get('StudyUID', ''))])
            elif type == 2:
                if not QtGui.QDesktopServices.openUrl(QUrl.fromEncoded(path)):
                    QtGui.QMessageBox.critical(self,
                    u'Внимание!',
                    u'Невозможно открыть браузер',
                    QtGui.QMessageBox.Ok,
                    QtGui.QMessageBox.Ok)
                return


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceString(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def toInfo(self, context, v):
        return v

    def toText(self, v):
        if v is None or v == '':
            return u'Снимки не зарегистрированы'
        try:
            d = json.loads(v)
            return d.get('ShowText', u'Снимки получены')
        except Exception as e:
            QtGui.qApp.logCurrentException()
            return u'Снимки не зарегистрированы'
