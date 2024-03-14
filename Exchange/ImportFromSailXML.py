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

import time
import datetime
# WTF? DOM для массированной загрузки использовать нельзя. нужно использовать SAX
from xml.dom.minidom import parse

from PyQt4 import QtGui
from PyQt4.QtCore import QString, pyqtSignature


from library.Utils import forceInt, forceRef, forceString, toVariant

from Exchange.Cimport import Cimport
from Exchange.Ui_ImportFromSailXMLDialog import Ui_ImportFromSailXMLDialog

#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
class CImportFromSailXML(Cimport, QtGui.QDialog, Ui_ImportFromSailXMLDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        Cimport.__init__(self, self.log)
        self.departsAdded=0
        self.departsUpdated=0
        self.personsAdded=0
        self.personsUpdated=0

        self.abort = False
        self.setFixedSize(500,380)
        self.prbImport.setValue(0)
        self.cbNet.insertItem(0,QString(u'Не задана'),0)
        self.orgId = QtGui.qApp.currentOrgId()
        self.db = QtGui.qApp.db
        tableNet = self.db.table('rbNet')
        for record in  self.db.getRecordList(tableNet,'id,name'):
            self.cbNet.insertItem(forceInt(record.value('id')),QString(forceString(record.value('name'))),record.value('id'))

    def __addPersonToDB(self,surname,firstname,secondname,snils,db_departid,staffname):
        snils=snils.replace('-','').replace(' ','')
        postId = forceRef(self.db.translate('rbPost', 'name', staffname, 'id'))
        #Ищем сотрудника в базе. Если есть-заменяем. Если нету-добавляем
        #WTF?
        # 1) UPPER - не нужно, так как поиск у нас везде ci
        # 2) Что произойдёт, если в источнике фамилия будет '); delete * from Client; -- '?
        record = self.db.getRecordEx(self.tablePerson, '*', "UPPER(firstName)=UPPER('%s') and UPPER(lastName)=UPPER('%s') and UPPER(patrName)=UPPER('%s') and SNILS='%s' and org_id=%s" % (firstname,surname,secondname,snils,self.orgId))
        if record:
            record.setValue('orgStructure_id',toVariant(db_departid))
            if postId<>-1:
                record.setValue('post_id',toVariant(postId))
            recid = self.db.updateRecord(self.tablePerson, record)
            if not recid:
                self.log.append(u'<font color="red">Ошибка обновления сотрудника<font> %s %s %s %s'%(surname,firstname,secondname,snils))
            else:
                self.log.append(u'<font color="blue">Обновляем</font>  %s %s %s %s'%(surname,firstname,secondname,snils))
                self.personsUpdated+=1
        else:
            row = QtGui.qApp.db.record('Person')
            row.setValue('firstName', toVariant(firstname))
            row.setValue('lastName', toVariant(surname))
            row.setValue('patrName', toVariant(secondname))
            row.setValue('SNILS', toVariant(snils))
            row.setValue('org_id', toVariant(self.orgId))
            row.setValue('orgStructure_id',toVariant(db_departid))
            row.setValue('post_id',toVariant(postId))
            self.log.append(u'<font color="green">Добавляем</font> %s %s %s %s'%(surname,firstname,secondname,snils))
            QtGui.qApp.processEvents()
            self.personsAdded+=1
            return self.db.insertRecord(self.tablePerson,row)

    def __addDepartToDB(self,depart,sname,parentID=None):
        QtGui.qApp.processEvents()
        if not len(sname):
            sname = depart;
        record = self.db.getRecordEx(self.tableOrgStructure, '*', '%s = \'%s\' and organisation_id=%s'%('name', depart,self.orgId))
        if record:
            record.setValue('code', toVariant(sname))
            if self.cbType.currentIndex() >0:
                record.setValue('type', toVariant(self.cbType.currentIndex()-1))
            if self.cbNet.itemData(self.cbNet.currentIndex()).toInt()<>(0,True):
                record.setValue('net_id', self.cbNet.itemData(self.cbNet.currentIndex()))
            if parentID:
                record.setValue('parent_id', toVariant(parentID))
            orgStructureId = self.db.updateRecord(self.tableOrgStructure, record)
            if not orgStructureId:
                self.log.append(u'<font color="red">Ошибка обновления отдела<font> %s'%depart)
            else:
                self.log.append(u'<font color="blue">Обновляем</font>  %s'%depart)
                self.departsUpdated+=1
                return orgStructureId
        else:
            row = QtGui.qApp.db.record('OrgStructure')
            row.setValue('name', toVariant(depart))
            row.setValue('code', toVariant(sname))
            row.setValue('organisation_id', toVariant(self.orgId))
            if self.cbType.currentIndex() >0:
                row.setValue('type', toVariant(self.cbType.currentIndex()-1))
            if self.cbNet.itemData(self.cbNet.currentIndex()).toInt()<>(0,True):
                row.setValue('net_id', self.cbNet.itemData(self.cbNet.currentIndex()))
            if parentID:
                row.setValue('parent_id', toVariant(parentID))
            self.log.append(u'<font color="green">Добавляем</font> %s'%depart)
            self.departsAdded+=1
            return self.db.insertRecord(self.tableOrgStructure,row)


    def __dateFromStr(self,str):
        if '-' in str:
            delimiter='-'
        elif '/' in str:
            delimiter='/'
        else:
            delimiter='.'
        yeartype='%Y' if len(str)==10 else '%y'
        return time.strptime(str,'%d'+delimiter+'%m'+delimiter+yeartype)


    #Возвращает работника по коду
    def __getWorkertNodeByID(self,xml,id):
        subdivisions = xml.getElementsByTagName('Workers')
        for subdivision in subdivisions:
            for subnode in subdivision.childNodes:
                if subnode.nodeName =='Worker':
                    if subnode.getAttribute('Id')==id: return subnode;

    #Возвращает ставки
    def __getEploymentAccounts(self,xml,staffid,staffname,db_departid):
        staffposts = xml.getElementsByTagName('EploymentAccounts')
        for staffpost in staffposts:
            for staffnode in staffpost.childNodes:
                if (staffnode.nodeName =='EploymentAccount') or (staffnode.nodeName == 'EmploymentAccount'):
                    if self.__isActual(staffnode):
                        for cnodes in  staffnode.getElementsByTagName('StaffPost'):
                            if cnodes.childNodes[0].nodeValue == staffid:
                                for workerid in  staffnode.getElementsByTagName('Worker'):
                                    worker = self.__getWorkertNodeByID(xml,workerid.childNodes[0].nodeValue)
                                    for wsurname in  worker.getElementsByTagName('Surname'):
                                        surname=wsurname.childNodes[0].nodeValue if len(wsurname.childNodes) else ''
                                    for wfirstname in  worker.getElementsByTagName('Firstname'):
                                        firstname=wfirstname.childNodes[0].nodeValue   if len(wfirstname.childNodes) else ''
                                    for wsecondname in  worker.getElementsByTagName('Secondname'):
                                        secondname=wsecondname.childNodes[0].nodeValue if len(wsecondname.childNodes) else ''
                                    for wsnils in  worker.getElementsByTagName('SNILS'):
                                        snils=wsnils.childNodes[0].nodeValue if len(wsnils.childNodes) else ''
                                    self.__addPersonToDB(surname,firstname,secondname,snils,db_departid,staffname)


    #Возвращает должности в отделе
    def __getSraffPosts(self,xml,departid,db_departid):
        staffposts = xml.getElementsByTagName('StaffPosts')
        for staffpost in staffposts:
            for staffnode in staffpost.childNodes:
                if staffnode.nodeName =='StaffPost':
                    if self.__isActual(staffnode):
                        for cnodes in  staffnode.getElementsByTagName('Subdivision'):
                            if cnodes.childNodes[0].nodeValue == departid:
                                self.__getEploymentAccounts(xml,staffnode.getAttribute('Id'),self.__getLastStaffPostName(staffnode),db_departid)

    #Возвращает последнее актуальное название отдела
    def __getLastStaffPostName(self,staffpost):
        dateFrom = None
        staffpostName = ''
        for staffpostHistory in staffpost.getElementsByTagName('StaffPostHistorys'):
            for hisNode in staffpostHistory.childNodes:
                if hisNode.nodeName =='StaffPostHistory':
                    for dt in  hisNode.getElementsByTagName('DateChange'):
                        if (not dateFrom) or (dateFrom<self.__dateFromStr(dt.childNodes[0].nodeValue)):
                            for nm in hisNode.getElementsByTagName('Name'):
                                if len(nm.childNodes):
                                    staffpostName = nm.childNodes[0].nodeValue
                                else: staffpostName = ''
        return staffpostName

    def __getLastDepartName(self,depart):
        dateFrom = None
        departName = ''
        for departHistory in depart.getElementsByTagName('SubdivisionHistorys'):
            for hisNode in departHistory.childNodes:
                if hisNode.nodeName =='SubdivisionHistory':
                    for dt in  hisNode.getElementsByTagName('DateChange'):
                        if (not dateFrom) or (dateFrom<self.__dateFromStr(dt.childNodes[0].nodeValue)):
                            for nm in hisNode.getElementsByTagName('Name'):
                                if len(nm.childNodes):
                                    departName = nm.childNodes[0].nodeValue
                                else: departName=''
        return departName

    #Проверяет у узла тег DateTo на актукльность
    def __isActual(self,node):
        for dateto in node.getElementsByTagName('DateTo'):
            if not dateto.childNodes: return True;
            if  datetime.datetime(*self.__dateFromStr(dateto.childNodes[0].nodeValue)[:6])> datetime.datetime.now(): return True
        return False;

    #Возвращает ноду отдела по ID
    def __getDepartNodeByID(self,xml,id):
        subdivisions = xml.getElementsByTagName('Subdivisions')
        for subdivision in subdivisions:
            for subnode in subdivision.childNodes:
                if subnode.nodeName =='Subdivision':
                    if subnode.getAttribute('Id')==id: return subnode;

    #Функуия добавляет отделы от указанного, пока не дойдет до парента
    #На входе список отделов, которые уже добавлены
    def __addDepart(self,xml,depart,departs):
        if depart.getAttribute('Id') in departs.keys(): return
        #departs[depart.getAttribute('Id')]='0'
        sname=''
        shortnames = depart.getElementsByTagName('Mnemo')
        for shortname in shortnames:
            if shortname.childNodes:
                sname=shortname.childNodes[0].nodeValue


        parents = depart.getElementsByTagName('Parent')
        for parent in parents:
            if not parent.childNodes:
                #Обрабатываем тех, у кого Parent пустой
                if self.__isActual(depart):
                    #self.__getLastDepartName(depart)
                    #self.log.append('>D '+ depart.getAttribute('Id')+' '+self.__getLastDepartName(depart))
                    departs[depart.getAttribute('Id')]=self.__addDepartToDB(self.__getLastDepartName(depart),sname)
                    if self.chkPersonImport.isChecked():
                        self.__getSraffPosts(xml,depart.getAttribute('Id'),departs[depart.getAttribute('Id')])
            else:
                dpt = self.__getDepartNodeByID(xml,parent.childNodes[0].nodeValue)
                self.__addDepart(xml,dpt,departs)
                if self.__isActual(depart):
                    departs[depart.getAttribute('Id')]=self.__addDepartToDB(self.__getLastDepartName(depart),sname,departs[dpt.getAttribute('Id')])
                    if self.chkPersonImport.isChecked():
                        self.__getSraffPosts(xml,depart.getAttribute('Id'),departs[depart.getAttribute('Id')])

    def __loadFromSailXMLFile(self,filename):
        self.departsAdded=0
        self.departsUpdated=0
        self.personsAdded=0
        self.personsUpdated=0

        self.log.clear()
        self.abort=False
        file = open(filename)
        xml = parse(file)
        subdivisions = xml.getElementsByTagName('Subdivisions')
        cnt=0;
        Departs = dict()
        #Разбиваем элементы на корневые и нет
        for subdivision in subdivisions:
            for subnode in subdivision.childNodes:
                if subnode.nodeName =='Subdivision':
                    cnt+=1

        self.prbImport.setMaximum(cnt)
        for subnode in subdivision.childNodes:
            if subnode.nodeName =='Subdivision':
                if self.abort:
                    self.log.append(u'<font color="red">Прервано пользователем</font>')
                    self.db.rollback()
                    break
                self.__addDepart(xml,subnode,Departs)
                self.n += 1
                self.prbImport.setValue(self.n)
                self.stat.setText(u'обработано: '+str(self.n))
        if not  self.abort:
            self.log.append(u'<font color="green"><b>Готово</b><br/>Отделений: добавлено %s обновлено %s<br>Сотрудников добавлено %s обновлено %s</font>'%(self.departsAdded,self.departsUpdated,self.personsAdded,self.personsUpdated))



    @pyqtSignature('')
    def on_btnSelectFileXML_clicked(self):
        fileName = QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите файл с данными', self.edtFileNameXML.text(), u'Файлы XML (*.xml)')
        if fileName != '':
            self.edtFileNameXML.setText(fileName)
            self.btnImport.setEnabled(True)

    def startImport(self):
        self.n = 0
        #Грузим и парсим XML

        self.tableOrgStructure = self.db.table('OrgStructure')
        self.tablePerson =self.db.table('Person')
        self.db.transaction()
        try:
            self.btnImport.setEnabled(False)
            self.wControl.setEnabled(False)
            self.__loadFromSailXMLFile(unicode(self.edtFileNameXML.text()))

            self.db.commit()
            self.btnImport.setEnabled(True)
            self.wControl.setEnabled(True)
        except:
            self.db.rollback()
            self.btnImport.setEnabled(True)
            self.wControl.setEnabled(True)
            QtGui.qApp.logCurrentException()
            raise

def ImportFromSailXML():
    dlg = CImportFromSailXML()
    dlg.edtFileNameXML.setText(forceString(QtGui.qApp.preferences.appPrefs.get('ImportFromSailXML', '')))
    dlg.exec_()
    QtGui.qApp.preferences.appPrefs['ImportFromSailXML'] = toVariant(dlg.edtFileNameXML.text())
