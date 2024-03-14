# -*- coding: utf-8 -*-
import sys
import os
from time import gmtime, strftime
from PyQt4 import QtCore, QtSql

from library import database
from library.Preferences import CPreferences
from library.Utils import forceString, forceInt, forceDate, forceRef, toVariant, anyToUnicode

from suds.client import Client, WebFault
import logging
logging.basicConfig(level=logging.INFO)

class CHolterExchanger(QtCore.QCoreApplication):
    
    mapStatusCodeToName = {0: u'Заявка без вложений', 1: u'Заявка подана', 2: u'Заявка взята в работу', 3: u'Заявка выполнена', 4: u'Заявка аннулирована'}
    
    
    def __init__(self, args):
        QtCore.QCoreApplication.__init__(self, args)
        self.db = None
        self.preferences = None
        self.connectionName = 'HolterDB'
        self.iniFileName = '/root/.config/samson-vista/HolterExchanger.ini'
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
            self.SOAP = Client(url, timeout=180)
        except WebFault as e:
            print anyToUnicode(e)
        except Exception as e:
            print(anyToUnicode(e))
        self.auth = self.SOAP.factory.create('authInfo')
        self.auth._userName = user
        self.auth._pass = password
        
        
    def createRequestInfo(self, record):
        requestInfo = self.SOAP.factory.create('requestInfo')
        requestInfo.datR = forceDate(record.value('birthDate')).toString('yyyy-MM-dd')
        requestInfo.omsCode = forceString(record.value('omsCode'))
        requestInfo.fam = forceString(record.value('lastName'))
        requestInfo.im = forceString(record.value('firstName'))
        requestInfo.otch = forceString(record.value('patrName'))
        requestInfo.pol = forceString(record.value('sex'))
        dt = forceString(record.value('docTypeId'))
        pn = forceString(record.value('pN'))
        ps = forceString(record.value('pS'))
        snils = forceString(record.value('snils'))
        polisTypeId = forceString(record.value('polisTypeId'))
        polisS = forceString(record.value('polisS'))
        polisN = forceString(record.value('polisN'))
        if dt:
            requestInfo.docTypeId = dt
        if ps:
            requestInfo.pS = ps
        if pn:
            requestInfo.pN = pn
        if snils:
            requestInfo.snils = snils
        if polisTypeId:
            requestInfo.polisTypeId = polisTypeId
        if polisS:
            requestInfo.polisS = polisS
        if polisN:
            requestInfo.polisN = polisN
        requestInfo.dInput = forceDate(record.value('begDate')).toString('yyyy-MM-dd')
        requestInfo.prRab = 0
        requestInfo.registrId = forceInt(record.value('id'))
        return requestInfo


    def main(self):
        self.loadPreferences()
        if self.preferences:
            self.openDatabase()
            if self.db:
                self.connectService()
                if self.SOAP:
                    self.uploadReguests()
        self.closeDatabase()
        
        
    def getData(self):
        stmt = u"""
SELECT c.id, c.lastName, c.firstName, c.patrName, case c.sex when 1 then 'М' when 2 then 'Ж' end as sex, c.birthDate, a.begDate, 
  if(ifnull(c.snils, '') <> '', concat(substr(c.snils,1,3), '-', substr(c.snils,4,3), '-', substr(c.snils,7,3), ' ', substr(c.snils,10,2)), null) as snils,
  dt.regionalCode AS docTypeId, cd.serial as pS, cd.number AS pN,
  pk.regionalCode AS polisTypeId, cp.serial AS polisS, cp.number AS polisN,
  IF(length(trim(o.bookkeeperCode))=5, o.bookkeeperCode,
                    IF(length(trim(Parent1.bookkeeperCode))=5, Parent1.bookkeeperCode,
                      IF(length(trim(Parent2.bookkeeperCode))=5, Parent2.bookkeeperCode,
                        IF(length(trim(Parent3.bookkeeperCode))=5, Parent3.bookkeeperCode,
                          IF(length(trim(Parent4.bookkeeperCode))=5, Parent4.bookkeeperCode, Parent5.bookkeeperCode))))) AS omsCode,
  apNumber.id AS apNumber, aptNumber.id AS aptNumber,
  apStatus.id AS apStatus, aptStatus.id AS aptStatus,
  apExecutive.id AS apExecutive, aptExecutive.id AS aptExecutive,
  apResult.id AS apResult, aptResult.id AS aptResult,
  Number.value as Number,
  status.value as status,
  a.id as actionId
  FROM Action a
  left JOIN ActionType at on at.id = a.actionType_id
  LEFT JOIN ActionPropertyType aptNumber ON aptNumber.actionType_id = at.id AND aptNumber.deleted = 0 AND aptNumber.name = 'Номер заявки'
  LEFT JOIN ActionPropertyType aptStatus ON aptStatus.actionType_id = at.id AND aptStatus.deleted = 0 AND aptStatus.name = 'Статус заявки'
  LEFT JOIN ActionPropertyType aptExecutive ON aptExecutive.actionType_id = at.id AND aptExecutive.deleted = 0 AND aptExecutive.name = 'Исполнитель'
  LEFT JOIN ActionPropertyType aptResult ON aptResult.actionType_id = at.id AND aptResult.deleted = 0 AND aptResult.name = 'Результат заявки'
  left JOIN ActionProperty apNumber ON apNumber.action_id = a.id AND apNumber.type_id = aptNumber.id AND apNumber.deleted = 0
  left JOIN ActionProperty apStatus ON apStatus.action_id = a.id AND apStatus.type_id = aptStatus.id AND apStatus.deleted = 0
  left JOIN ActionProperty apExecutive ON apExecutive.action_id = a.id AND apExecutive.type_id = aptExecutive.id AND apExecutive.deleted = 0
  left JOIN ActionProperty apResult ON apResult.action_id = a.id AND apResult.type_id = aptResult.id AND apResult.deleted = 0
  left JOIN ActionProperty_Integer Number ON Number.id = apNumber.id
  left JOIN ActionProperty_String status ON status.id = apStatus.id
  left JOIN ActionProperty_String aps_res ON aps_res.id = apResult.id
  left JOIN Event e on e.id = a.event_id
  left JOIN Person p ON p.id = COALESCE(a.person_id, a.setPerson_id, e.execPerson_id)
  LEFT JOIN OrgStructure o ON o.id = p.orgStructure_id
  left join OrgStructure as Parent1 on Parent1.id = o.parent_id
  left join OrgStructure as Parent2 on Parent2.id = Parent1.parent_id
  left join OrgStructure as Parent3 on Parent3.id = Parent2.parent_id
  left join OrgStructure as Parent4 on Parent4.id = Parent3.parent_id
  left join OrgStructure as Parent5 on Parent5.id = Parent4.parent_id
  left JOIN Client c ON c.id = e.client_id
  left JOIN ClientPolicy cp ON cp.id = getClientPolicyIdForDate(c.id, 1, a.begDate, e.id)
  LEFT JOIN rbPolicyKind pk ON pk.id = cp.policyKind_id
  left JOIN ClientDocument cd ON cd.id = getClientDocumentId(c.id)
  LEFT JOIN rbDocumentType dt ON dt.id = cd.documentType_id
  WHERE at.flatCode = 'holter' and IFNULL(aps_res.value, '') = '' AND IFNULL(status.value, '') != 'Заявка аннулирована' and length(trim(c.snils)) > 0;
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


    def uploadReguests(self):
        query = self.getData()
        print('count requests: {0:d}'.format(query.size()))
        if query.size() > 0:
            db = self.db
            cntNewRequests = 0
            cntNoChange = 0
            cntUpdateStatus = 0
            cntResults = 0
            self.tableActionProperty = db.table(u'ActionProperty')
            tableActionProperty_Integer = db.table('ActionProperty_Integer')
            tableActionProperty_String = db.table('ActionProperty_String')
            print(u'{0:s}: start exchange'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
            while query.next():
                record = query.record()
                actionId = forceRef(record.value('actionId'))
                try:
                    Number = forceInt(record.value('Number'))
                    if Number:
                        # если уже есть номер заявки, то запрашиваем ее статус
                        res = self.SOAP.service.getRequestsCustomer(self.auth, Number)
                        if res:
                            oldStatus = forceString(record.value('status'))
                            status = self.mapStatusCodeToName[res[0].status]
                            # если статуст изменился
                            if status != oldStatus:
                                aptStatus = forceRef(record.value('aptStatus'))
                                apStatus = forceRef(record.value('apStatus'))
                                self.fillActionProperty(apStatus, aptStatus, tableActionProperty_String, actionId, status)
                                
                                if 'executive' in res[0]:
                                    executive = unicode(res[0].executive)
                                    aptExecutive = forceRef(record.value('aptExecutive'))
                                    apExecutive = forceRef(record.value('apExecutive'))
                                    self.fillActionProperty(apExecutive, aptExecutive, tableActionProperty_String, actionId, executive)

                                
                                if res[0].status == 3:
                                    # если статус заявки 'Заявка выполнена' - то склеиваем урл к пдф результата
                                    cntResults += 1
                                    aptResult = forceRef(record.value('aptResult'))
                                    apResult = forceRef(record.value('apResult'))
                                    param = u'mis?user={0:s}&pass={1:s}&request={2:d}'.format(self.auth._userName, self.auth._pass, Number)
                                    url = forceString(self.preferences.appPrefs.get('url', ''))
                                    result = url.replace(u'soap?wsdl', param)
                                    self.fillActionProperty(apResult, aptResult, tableActionProperty_String, actionId, result)
                                    actionRecord = db.getRecord('Action', '*', actionId)
                                    actionRecord.setValue('status', toVariant(2))
                                    curDateTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                    actionRecord.setValue('endDate', toVariant(curDateTime))
                                    actionRecord.setValue('modifyDatetime', toVariant(curDateTime))
                                    db.updateRecord('Action', actionRecord)
                                else:
                                    # иначе обновлем статус заявки
                                    cntUpdateStatus += 1
                                                                        
                                    if res[0].status == 2:
                                        actionRecord = db.getRecord('Action', '*', actionId)
                                        actionRecord.setValue('status', toVariant(1))
                                        actionRecord.setValue('modifyDatetime', toVariant(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
                                        db.updateRecord('Action', actionRecord)  
                            else:
                                cntNoChange += 1
                    else:
                        # номера заявки нет - создаем заявку
                        res = self.SOAP.service.createRequest(self.auth, self.createRequestInfo(record))
                        if res:
                            cntNewRequests += 1
                            apNumber = forceRef(record.value('apNumber'))
                            aptNumber = forceRef(record.value('aptNumber'))
                            self.fillActionProperty(apNumber, aptNumber, tableActionProperty_Integer, actionId, res)
                            
                            aptStatus = forceRef(record.value('aptStatus'))
                            apStatus = forceRef(record.value('apStatus'))
                            status = self.mapStatusCodeToName[0]
                            self.fillActionProperty(apStatus, aptStatus, tableActionProperty_String, actionId, status)
                except WebFault as e:
                    print anyToUnicode(e)
                except Exception as e:
                    print(anyToUnicode(e))
            print(u'created: {0:d}\nupdated: {1:d}\ncompleted: {2:d}\nwithout changes: {3:d}'.format(
                 cntNewRequests, cntUpdateStatus, cntResults, cntNoChange))
            print(u'{0:s}: exchange completed'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))


if __name__ == '__main__':
    app = CHolterExchanger(sys.argv)
    app.main()
