# -*- coding: utf-8 -*-
import sys
import os
from time import gmtime, strftime
from PyQt4 import QtCore, QtSql

from library import database
from library.Preferences import CPreferences
from library.Utils import forceString, forceRef, toVariant, anyToUnicode

from suds.client import Client, WebFault
from suds.cache import NoCache
import logging
logging.basicConfig(level=logging.INFO)

class CWarrantNumberUpdater(QtCore.QCoreApplication):
       
    
    def __init__(self, args):
        QtCore.QCoreApplication.__init__(self, args)
        self.db = None
        self.preferences = None
        self.connectionName = 'WarrantNumberUpdater'
        self.iniFileName = '/root/.config/samson-vista/WarrantNumberUpdater.ini'
        self.SOAP = None
        self.auth = None


    def openDatabase(self):
        self.db = None
        try:
            self.db = database.connectDataBase(self.preferences.dbDriverName,
                                     self.preferences.dbServerName,
                                     self.preferences.dbServerPort,
                                     self.preferences.dbDatabaseName,
                                     self.preferences.dbUserName,
                                     self.preferences.dbPassword,
                                     compressData=self.preferences.dbCompressData,
                                     connectionName=self.connectionName)
        except Exception as e:
            print(anyToUnicode(e))


    def closeDatabase(self):
        if self.db:
            self.db.close()
            self.db = None
            if QtSql.QSqlDatabase.contains(self.connectionName):
                QtSql.QSqlDatabase.removeDatabase(self.connectionName)
        
        
    def loadPreferences(self):
        self.preferences = CPreferences(self.iniFileName)
        iniFileName = self.preferences.getSettings().fileName()
        if not os.path.exists(iniFileName):
            print(u"ini file ({0:s}) not exists".format(iniFileName))
            app.quit()
        self.preferences.load()
               
        
    def connectService(self):
        url = forceString(self.preferences.appPrefs.get('url', None))
        user = forceString(self.preferences.appPrefs.get('user', None))
        password = forceString(self.preferences.appPrefs.get('pass', None))
        try:
            self.SOAP = Client(url, cache=NoCache())
        except WebFault as e:
            print anyToUnicode(e)
        except Exception as e:
            print(anyToUnicode(e))
        self.auth = self.SOAP.factory.create('authInfo')
        self.auth._userName = user
        self.auth._pass = password
        

    def main(self):
        print(u'====start {0:s}==='.format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
        self.loadPreferences()
        if self.preferences:
            self.openDatabase()
            if self.db:
                self.connectService()
                if self.SOAP:
                    self.downloadWarrantNumbers()
        self.closeDatabase()
        print(u'====end {0:s}==='.format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
        
        
    def getData(self):
        stmt = u"""
SELECT 
  apNumber.id AS apNumber, aptNumber.id AS aptNumber,
  apInternalNumber.id AS apInternalNumber, aptInternalNumber.id AS aptInternalNumber,
  Number.value as Number,
  CONCAT_WS(':', 'web', o.infisCode, InternalNumber.value) as InternalNumber,
  a.id as actionId
  FROM Action a
  left JOIN Event e on e.id = a.event_id
  left JOIN Person p ON p.id = e.execPerson_id
  LEFT JOIN Organisation o ON o.id = p.org_id
  left JOIN ActionType at on at.id = a.actionType_id
  LEFT JOIN ActionPropertyType aptNumber ON aptNumber.actionType_id = at.id AND aptNumber.deleted = 0 AND aptNumber.name = 'warrantNum'
  LEFT JOIN ActionPropertyType aptInternalNumber ON aptInternalNumber.actionType_id = at.id AND aptInternalNumber.deleted = 0 AND aptInternalNumber.name = 'Внутренний номер направления'
  left JOIN ActionProperty apNumber ON apNumber.action_id = a.id AND apNumber.type_id = aptNumber.id AND apNumber.deleted = 0
  left JOIN ActionProperty apInternalNumber ON apInternalNumber.action_id = a.id AND apInternalNumber.type_id = aptInternalNumber.id AND apInternalNumber.deleted = 0
  left JOIN ActionProperty_String Number ON Number.id = apNumber.id
  left JOIN ActionProperty_String InternalNumber ON InternalNumber.id = apInternalNumber.id
  WHERE at.code = 'soc001' AND e.setDate >= SUBDATE(NOW(),INTERVAL 30 DAY)
  AND LENGTH(IFNULL(Number.value, '')) = 0
  AND LENGTH(InternalNumber.value) > 0;
"""
        return self.db.query(stmt)
        
    def fillActionProperty(self, id, typeId, table, actionId, value):
        db = self.db
        if id:
            item = db.getRecordEx(table, '*', table['id'].eq(id))
            item.setValue('value', toVariant(value))
            db.updateRecord(table, item)
        else:
            mainItem = self.tableActionProperty.newRecord()
            item = table.newRecord()
            mainItem.setValue('action_id', toVariant(actionId))
            mainItem.setValue('type_id', toVariant(typeId))
            id = db.insertRecord(self.tableActionProperty, mainItem)
            item.setValue('id', toVariant(id))
            item.setValue('value', toVariant(value))
            db.insertRecord(table, item)


    def downloadWarrantNumbers(self):
        query = self.getData()
        print('count warrants: {0:d}'.format(query.size()))
        if query.size() > 0:
            db = self.db
            cntWarrantNumberUpdates = 0
            self.tableActionProperty = db.table(u'ActionProperty')
            tableActionProperty_String = db.table('ActionProperty_String')
            print(u'{0:s}: start exchange'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
            while query.next():
                record = query.record()
                actionId = forceRef(record.value('actionId'))
                try:
                    InternalNumber = forceString(record.value('InternalNumber'))
                    if InternalNumber:
                        res = self.SOAP.service.getWarrantByIdMIS(self.auth, InternalNumber)
                        if res:
                            cntWarrantNumberUpdates += 1
                            aptNumber = forceRef(record.value('aptNumber'))
                            apNumber = forceRef(record.value('apNumber'))
                            self.fillActionProperty(apNumber, aptNumber, tableActionProperty_String, actionId, forceString(res))
                except WebFault as e:
                    print anyToUnicode(e)
                except Exception as e:
                    print(anyToUnicode(e))
            print(u'Warrant Number Updates: {0:d}'.format(cntWarrantNumberUpdates))
            print(u'{0:s}: exchange completed'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))


if __name__ == '__main__':
    app = CWarrantNumberUpdater(sys.argv)
    app.main()
