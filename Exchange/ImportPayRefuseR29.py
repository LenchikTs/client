# -*- coding: utf-8 -*-
import os

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate, QDir, QFile, pyqtSignature


from library.Utils import forceDate, forceInt, forceRef, forceString, forceStringEx, nameCase, toVariant

from Accounting.Utils import updateAccounts, updateDocsPayStatus
from Events.Utils import CPayStatus, getPayStatusMask
from Exchange.Cimport import CDBFimport, CXMLimport

from Exchange.Export29XMLCommon import Export29XMLCommon
from Exchange.Utils import tbl

from Exchange.Ui_ImportPayRefuseR29 import Ui_Dialog


def ImportPayRefuseR29Native(widget, accountId, accountItemIdList):
    dlg = CImportPayRefuseR29Native(accountId, accountItemIdList)
    dlg.edtFileName.setText(forceString(QtGui.qApp.preferences.appPrefs.get('ImportPayRefuseR29FileName', '')))
    dlg.exec_()
    QtGui.qApp.preferences.appPrefs['ImportPayRefuseR29FileName'] = toVariant(dlg.edtFileName.text())


class CImportPayRefuseR29Native(QtGui.QDialog, Ui_Dialog, CDBFimport, CXMLimport):
    sexMap = {u'Ж':2, u'ж':2, u'М':1, u'м':1}
    zglvFields = ('VERSION', 'DATA', 'FILENAME')
    pacientFields = ('ID_PAC','VPOLIS', 'SPOLIS', 'NPOLIS', 'SMO', 'SMO_OGRN', 'SMO_OK', 'SMO_NAM', 'NOVOR')
    sluchFields = ('IDCASE','USL_OK', 'VIDPOM', 'NPR_MO', 'EXTR', 'PODR','LPU','PROFIL', 'DET','NHISTORY',
                        'DATE_1', 'DATE_2', 'DS1', 'DS2', 'RSLT', 'ISHOD', 'PRVS', 'IDSP','ED_COL', 'TARIF',
                        'SUMV', 'REFREASON', 'COMENTSL')
    sankFields = ('S_CODE', 'S_SUM', 'S_TIP', 'S_OSN', 'S_COM', 'S_IST')
    sankGroup = {'SANK': (sankFields, {})}
    def __init__(self, accountId, accountItemIdList):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        CDBFimport.__init__(self, self.log)
        CXMLimport.__init__(self)
        self.accountId=accountId
        self.accountItemIdList=accountItemIdList
        self.progressBar.setFormat('%p%')
        self.checkName()
        self.errorPrefix = ''
        self.nProcessed = 0
        self.nPayed = 0
        self.nRefused = 0
        self.nNotFound = 0
        self.tableAccountItem = tbl('Account_Item')
        self.tableEvent = tbl('Event')
        self.tableAccount = tbl('Account')
        self.tableAcc=self.db.join(self.tableAccountItem, self.tableAccount,
            'Account_Item.master_id=Account.id')
        self.prevContractId = None
        self.financeTypeOMS = forceRef(self.db.translate('rbFinance',
            'code', '2', 'id'))
        self.refuseTypeIdCache = {}
        self.insurerCache = {}
        self.policyKindIdCache = {}
        self.policyTypeTerritorial = forceRef(self.db.translate('rbPolicyType',
            'code', '1', 'id'))
        self.policyTypeIndustrial = forceRef(self.db.translate('rbPolicyType',
            'code', '2', 'id'))
        self.confirmation = ''



    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
        fileName = QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите файл с данными', self.edtFileName.text(), u'Файлы ELU, XML (*.elu *.xml)')
        if fileName != '':
            self.edtFileName.setText(QDir.toNativeSeparators(fileName))
            self.btnImport.setEnabled(True)


    def err2log(self, e):
        self.log.append(self.errorPrefix+e)


    def checkHeader(self, txtStream):
        if txtStream.atEnd():
            return False

        header = forceString(txtStream.readLine())

        if len(header)<4:
            return False

        fields = header[4:].split(',')

        if len(fields)<5:
            return False

        if fields[3] == '1':
            txtStream.setCodec('CP866')
        elif fields[3] == '2':
            txtStream.setCodec('CP1251')

        if forceString(txtStream.readLine()) != '@@@':
            return False

        return True


    def readRecord(self, txtStream):
        result = {}
        s = ''

        while not txtStream.atEnd():
            s = forceString(txtStream.readLine())

            if s == '@@@':
                break

            list = s.split(':')

            if len(list)>1:
                result[list[0].strip()] = list[1].strip()

        return result


    def startImport(self):
        self.insurerCache = {}
        fileName = forceStringEx(self.edtFileName.text())
        self.confirmation = forceStringEx(self.edtConfirmation.text())
        (name,  fileExt) = os.path.splitext(fileName)
        isXML = (fileExt.lower() == '.xml')

#        currentAccountOnly = self.chkOnlyCurrentAccount.isChecked()
#        importPayed =self.chkImportPayed.isChecked()
#        importRefused = self.chkImportRefused.isChecked()
        confirmation = self.edtConfirmation.text()
        if not confirmation:
            self.log.append(u'нет подтверждения')
            return

        self.prevContractId = None
        accountIdSet = set()

        self.nProcessed = 0
        self.nPayed = 0
        self.nRefused = 0
        self.nNotFound = 0

        fileName = unicode(self.edtFileName.text())
        txtFile = QFile(fileName)
        txtFile.open(QFile.ReadOnly | QFile.Text)

        self.labelNum.setText(u'размер источника: '+str(txtFile.size()))
        self.progressBar.setFormat('%p%')
        self.progressBar.setMaximum(txtFile.size()-1)

        if isXML:
            self.readFile(txtFile, accountIdSet)
#===============================================================================
#        else:
#            txtStream =  QTextStream(txtFile)
#            if not self.checkHeader(txtStream):
#                self.log.append(u'заголовок повреждён.')
#                return
#
#            while not txtStream.atEnd():
#                row = self.readRecord(txtStream)
#                QtGui.qApp.processEvents()
#                if self.abort or row.get(u'КОН'):
#                    break
#                self.progressBar.setValue(txtStream.pos())
#                self.stat.setText(
#                    u'обработано: %d; оплаченых: %d; отказаных: %d; не найдено: %d' % \
#                    (self.nProcessed, self.nPayed, self.nRefused, self.nNotFound))
#                self.processRow(row, currentAccountOnly, importPayed, importRefused, confirmation, accountIdSet)
#===============================================================================

        self.stat.setText(
            u'обработано: %d; оплаченых: %d; отказаных: %d; не найдено: %d' % \
            (self.nProcessed, self.nPayed, self.nRefused, self.nNotFound))

        updateAccounts(self.accountIdSet)

        txtFile.close()


    def processRow(self,  row, currentAccountOnly, importPayed, importRefused, confirmation,  accountIdSet):
        lastName = nameCase(row.get(u'ФАМ', ''))
        firstName = nameCase(row.get(u'ИМЯ', ''))
        patrName = nameCase(row.get(u'ОТЧ', ''))
        refuseReasonCodeList =  forceString(row.get(u'ОШЛ', '')).split(',')
        refuseDate = QDate.currentDate() if refuseReasonCodeList != [u''] else None
        refuseComment = row.get(u'ЗАМ', '')
        accountItemId = forceInt(row.get(u'УКЛ'))/100
        recNum = accountItemId if accountItemId else 0
        payStatusMask = 0

        self.errorPrefix = u'Элемент №%d (%s %s %s): ' % (recNum, lastName,  firstName,  patrName)

        if not accountItemId:
            self.err2log(u'не найден в реестре.')
            self.nNotFound += 1
            return

        cond=[]
        cond.append(self.tableAccountItem['id'].eq(accountItemId))

        if currentAccountOnly:
            cond.append(self.tableAccount['id'].eq(toVariant(self.accountId)))

        fields = 'Account_Item.id, Account.date as Account_date, Account_Item.date as Account_Item_date, Account_Item.master_id as Account_id, Account.contract_id as contract_id'
        recordList = self.db.getRecordList(self.tableAcc, fields, where=cond)

        for record in recordList:
            accountIdSet.add(forceRef(record.value('Account_id')))
            contractId = forceRef(record.value('contract_id'))

            if self.prevContractId != contractId:
                self.prevContractId = contractId
                financeId = forceRef(self.db.translate('Contract', 'id', contractId, 'finance_id'))
                payStatusMask = getPayStatusMask(financeId)

            accDate = forceDate(record.value('Account_date'))
            accItemDate = forceDate(record.value('Account_Item_date'))

            if accItemDate or (refuseDate and (accDate > refuseDate)):
                self.err2log(u'счёт уже отказан')
                return

            self.nProcessed += 1

            accItem = self.db.getRecord(self.tableAccountItem, '*', accountItemId)
            accItem.setValue('date', toVariant(refuseDate if refuseDate else QDate.currentDate()))
            refuseTypeId = None

            if refuseDate:
                self.nRefused += 1
                refuseTypeId= self.getRefuseTypeId(refuseReasonCodeList[0])

                if not refuseTypeId:
                    refuseTypeId = self.addRefuseTypeId(refuseReasonCodeList[0], refuseComment, self.financeTypeOMS)
                    self.refuseTypeIdCache[refuseReasonCodeList[0]] = refuseTypeId

                accItem.setValue('refuseType_id', toVariant(refuseTypeId))
                updateDocsPayStatus(accItem, payStatusMask, CPayStatus.refusedBits)
                self.err2log(u'отказан, код `%s`:`%s`' % (refuseReasonCodeList[0], refuseComment))
            else:
                self.err2log(u'подтверждён')
                self.nPayed += 1

            accItem.setValue('number', toVariant(confirmation))
            self.db.updateRecord(self.tableAccountItem, accItem)

        if recordList == []:
            self.nNotFound += 1
            self.err2log(u'счёт не найден')

# ****************************************************************************************
#  XML
# *****************************************************************************************

    def readFile(self, device, accountIdSet):
        self.setDevice(device)
        self.accountIdSet = accountIdSet

        while (not self.atEnd()):
            self.readNext()

            if self.isStartElement():
                if self.name() == 'ZL_LIST':
                    self.readList()
                else:
                    self.raiseError(u'Неверный формат данных.')

            if self.hasError():
                return False

        return True


    def readList(self):
        assert self.isStartElement() and self.name() == 'ZL_LIST'

        while (not self.atEnd()):
            self.readNext()

            if self.isEndElement():
                break

            if self.isStartElement():
                if self.name() == 'ZGLV':
                    self.readGroup('ZGLV', self.zglvFields)
                elif self.name() == 'ZAP':
                    self.readZap()
                else:
                    self.readUnknownElement(True)

            if self.hasError():
                break


    def readZap(self):
        assert self.isStartElement() and self.name() == 'ZAP'
        result = {}

        while (not self.atEnd()):
            self.readNext()
#            print self.name().toString()
            if self.isEndElement():
                break

            if self.isStartElement():
                if self.name() == 'N_ZAP':
                    result['N_ZAP'] = forceString(self.readElementText())
                elif self.name() == 'PACIENT':
                    result = self.readGroup('PACIENT', self.pacientFields,  True, {}, result)
                elif self.name() == 'SLUCH':
                    result = self.readGroup('SLUCH', self.sluchFields, True, self.sankGroup, result)
#                    result = CXMLimport.readGroup(self, 'SLUCH', self.sluchFields,  True, self.sankGroup)

                    if not self.hasError():
                        self.processXMLImport(result)
                        result['SANK'] = ''
                else:
                    self.readUnknownElement(True)

            if self.hasError():
                break

    def readSluch(self, result):
        assert self.isStartElement() and self.name() == 'SLUCH'
#        result = {}
        while (not self.atEnd()):
            self.readNext()

            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'SLUCH':
                    result = self.readGroup('SLUCH', self.sluchFields, True, {}, result)
                    if not self.hasError():
                        self.processXMLImport(result)
            if self.hasError():
                break

    def getRefuseReasonText(self, refReasonCode):
        stmt = "SELECT `name` FROM `rbPayRefuseType` WHERE `code` = %s"
        query = self.db.query(stmt%refReasonCode)
        if query.next():
            return forceString(query.record().value(0))
        else:
            return ''

    def processXMLImport(self, row):
        refuseCode = 0
        sank = 0
        note = ''
        clientId = forceInt(row.get('ID_PAC', None))
        eventId = forceInt(row.get('NHISTORY', None))
        refuseCode = forceInt(row.get('REFREASON', None))
        sank = row.get('SANK')
        if sank:
            refuseCode = sank.get('S_OSN')
        if refuseCode:
            refuseCode = int(refuseCode)
        else:
            refuseCode = 0
        if not clientId:
            self.err2log(u'Поле ID_PAC не заполнено!')
            return


        if not eventId:
            self.err2log(u'Поле NHISTORY не заполнено!')
            return

        if not self.db.getRecord('Client', 'id', clientId):
            self.err2log(u'Пациент с id=%d не найден в БД.' % clientId)
            return

        self.errorPrefix = u'Элемент ID_PAC=%d: ' % clientId
        policyNumber = forceString(row.get('NPOLIS',  None))
        policySerial = forceString(row.get('SPOLIS', None))

        policyKindId = self.getPolicyKindId(forceString(row.get('VPOLIS', None)))
        dateStr = forceString(row.get('DATE_1'))
        policyBegDate = QDate.fromString(dateStr, Qt.ISODate) if dateStr else QDate.currentDate()

        if not policySerial and not policyNumber:
            self.err2log(u'Отсутствуют данные о полисе, ID_PAC=%d' % clientId)
            note = note + u'Отсутствуют данные о полисе, ID_PAC=%d;' % clientId
          #  refuseCode = 401
        note= forceString(row.get('COMENTSL'))
        insurerOGRN = forceString(row.get('SMO_OGRN'))
        insurerOKATO = forceString(row.get('SMO_OK'))
        insurerId = None
        smo = forceString(row.get('SMO'))
        eventInfo = self.db.getRecord(self.tableEvent, '*', eventId)
        if smo:
            insurerId = forceString(QtGui.qApp.db.translate('Organisation', 'miacCode', smo, 'id'))
        elif not insurerOGRN and not insurerOKATO:
            self.err2log(u"""Не указано ОГРН и ОКАТО """)
            note = note + u""" Не указано ОГРН и ОКАТО;"""
        else:
            insurerId = self.findInsurerByOGRNandOKATO(insurerOGRN, insurerOKATO)
        if insurerId:
                if eventInfo:
                    self.updateClientPolicy(clientId, insurerId, policySerial,
                                            policyNumber, policyBegDate,
                                            insurerOGRN,
                                            policyKindId, eventInfo)
                    self.closeOpenedPolicy(clientId)
        else:
            self.err2log(u"""СМО с ОГРН %s и ОКАТО %s не найдена""" %(insurerOGRN, insurerOKATO))
            note = note + u""" СМО с ОГРН %s и ОКАТО %s не найдена;""" %(insurerOGRN, insurerOKATO)
            #    refuseCode = 401
        contractId, oldContractId, k, isAmbiguitous, contractName = self.getContract(eventId)
        accountItemIdList = self.getAccountItemIdListByClientAndEvent(clientId, eventId)
        refuseText = self.getRefuseReasonText(refuseCode)

        if contractId == 'flag':
            note =note +u' Не удалось подобрать договор;'

        if oldContractId != contractId:
           #  eventInfo = self.db.getRecord(self.tableEvent, '*', eventId)
             if eventInfo:
                 eventInfo.setValue('contract_id', toVariant(contractId))
                 self.db.updateRecord(self.tableEvent, eventInfo)
                 note =u' Произошла смена договора;'
        if k >1:
            note =note + u' Попадает под действие нескольких договоров %s;'% u', '.join(contractName)
        if isAmbiguitous > 1:
            note =note + u' В рег. карте имеются несколько открытых прикреплений/полисов;'
        self.processAccountItemIdList(accountItemIdList, refuseCode, refuseText, note, eventId)


    def getAccountItemIdListByClientAndEvent(self, clientId, eventId):
        s = 'AND Account_Item.master_id=%d'  % self.accountId  if self.chkOnlyCurrentAccount.isChecked() else ''

        stmt = """SELECT  Account_Item.id,
            Account.date as Account_date,
            Account_Item.date as Account_Item_date,
            Account_Item.master_id as Account_id,
            Account.contract_id as contract_id
        FROM Account_Item
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN Account ON Account_Item.master_id = Account.id
        WHERE Event.client_id = %d AND Event.id = %d %s""" % (clientId, eventId,  s)

        res = []
        query = self.db.query(stmt)
        while query.next():
            res.append(query.record())

        return res


    def findInsurerByOGRNandOKATO(self, OGRN, OKATO):
        u"""Поиск по ОГРН и ОКАТО"""

        key = (OGRN,  OKATO)
        result = self.insurerCache.get(key, -1)


        if result == -1:
            record = self.db.getRecordEx(self.tableOrganisation, 'id',
                                      [self.tableOrganisation['OGRN'].eq(OGRN),
                                      self.tableOrganisation['OKATO'].eq(OKATO),
                                      self.tableOrganisation['isInsurer'].eq(1)],
                                         )
            if record:
                self.insurerCache[key] = result
                result = forceRef(record.value(0)) # if record else self.OGRN2orgId(OGRN)


        return result


    def getPolicyKindId(self, code):
        result = self.policyKindIdCache.get(code, -1)

        if result == -1:
            result =forceRef(self.db.translate(
                'rbPolicyKind', 'regionalCode', code, 'id'))
            self.policyKindIdCache[code] = result

        return result


    def updateClientPolicy(self, clientId, insurerId, serial, number, begDate,  newInsurerOGRN, policyKindId, eventInfo):
#        record = selectLatestRecord('ClientPolicy', clientId,
#            '(Tmp.`policyType_id` IN (%d,%d))' % \
#              (self.policyTypeIndustrial, self.policyTypeTerritorial))
        begDate = forceDate(eventInfo.value('setDate'))
        endDate = forceDate(eventInfo.value('execDate'))
        oldNpolis, oldSpolis, oldVpolis, oldInsurerOGRN, oldInsurerOKATO, oldInsurerName, oldSmo, oldInsurerId = Export29XMLCommon.getClientPolicy(self.db, clientId, begDate, endDate)
#если полиса нет то добавляем и все
 #       if not record:
        if not oldNpolis:
            self.addClientPolicy(clientId, insurerId, serial, number, begDate, self.policyTypeTerritorial, policyKindId)
            self.err2log(u'добавлен полис: `%s№%s (%s)`' % (
                          serial, number, insurerId if insurerId else 0))
            return True

#        oldInsurerId = forceRef(record.value('insurer_id'))
#        oldInsurerOGRN = forceString(self.db.translate('Organisation', 'id', oldInsurerId, 'OGRN'))
        if not newInsurerOGRN:
            newInsurerOGRN = forceString(self.db.translate('Organisation', 'id', insurerId, 'OGRN'))
        if ((insurerId and (oldInsurerId != insurerId)
                    and (oldInsurerOGRN != newInsurerOGRN)) or
                ( oldSpolis!= serial) or
                ( oldNpolis != number)):
            newInsurer = insurerId
            newSerial = serial
            newNumber = number
            self.addClientPolicy(clientId, insurerId, serial, number, begDate, self.policyTypeTerritorial, policyKindId)


            self.err2log(u'обновлен полис: `%s№%s (%s)` на `%s№%s (%s)`' % (
                         newSerial if newSerial else '', newNumber if newNumber else '',
                         newInsurer if newInsurer else 0, serial if serial else '', number if number else '', insurerId if insurerId else 0))
            return True

        return False

    def closeOpenedPolicy(self, clientId):
       recordList = self.db.getRecordList('ClientPolicy', '*', "client_id = %s AND (endDate IS NULL or endDate  = '0000-00-00') AND deleted = 0 "%clientId, '', 'begDate')
       acc = []
       for record in recordList:
           count = {}
           count['policyId'] = forceRef(record.value('id'))
           count['begDate'] = forceDate(record.value('begDate'))
           acc.append(count)
       if acc:
           maxCP = max(acc)
           while min(acc) != maxCP:
                record = acc.pop(acc.index(min(acc)))
                clientPolicy = self.db.getRecord(self.db.table('ClientPolicy'), '*', record['policyId'])
                clientPolicy.setValue('endDate', toVariant(min(acc)['begDate'].addDays(-1)))
                self.db.updateRecord(self.db.table('ClientPolicy'), clientPolicy)
                self.err2log(u'закрыты полиса у пациента %s'%clientId)
           if maxCP['policyId'] != self.db.getRecord(self.db.table('ClientPolicy'), '*', 'max(id)'):
               clientPolicy = self.db.getRecord(self.db.table('ClientPolicy'), '*', maxCP['policyId'])
               clientPolicy.setValue('deleted', toVariant(1))
               self.db.updateRecord(self.db.table('ClientPolicy'), clientPolicy)
               clientPolicy.setValue('id', toVariant('Null'))
               clientPolicy.setValue('deleted', toVariant(0))
               self.db.insertRecord(self.db.table('ClientPolicy'), clientPolicy)


    def getContract(self, eventId):
        (eventType, oldContractId, clientId, eventBegDate,
          eventEndDate, clientInsurerId, policyType,
            clientAge, clientSex,
           clientAttachType, organizationArea, socStatus, clientWork, isAmbiguitous) = self.getInfromationForContract(eventId)
        cond = []
        if eventEndDate:
            cond.append(u"Contract.begDate <='%s'"% eventEndDate.toString(Qt.ISODate))
            cond.append(u"Contract.endDate >='%s'"% eventEndDate.toString(Qt.ISODate))
        if eventType:
            cond.append(u'Contract_Specification.eventType_id =%s'%eventType)
        if clientInsurerId:
#            cond.append(u'IF(Contract_Contingent.insurer_id IS NULL, 1 =1, Contract_Contingent.insurer_id =%d)'% clientInsurerId)
            if organizationArea == 29:
                cond.append(u'Contract_Contingent.insurer_id =%d'% clientInsurerId)
            else:
               cond.append(u'IF(Contract_Contingent.insurer_id IS NULL, 1 =1, Contract_Contingent.insurer_id =%d)'% clientInsurerId)
        if clientAttachType:
            cond.append(u'IF( Contract_Contingent.attachType_id IS NULL , 1 =1, Contract_Contingent.attachType_id =%d)'%clientAttachType)
        if policyType:
            cond.append(u'IF( Contract_Contingent.policyType_id IS NULL , 1 =1, Contract_Contingent.policyType_id =%d)'%policyType)
        if clientSex:
            cond.append(u'IF( Contract_Contingent.sex =0, 1 =1,Contract_Contingent.sex=%d)'%clientSex)
        if socStatus:
            cond.append(u'IF( Contract_Contingent.socStatusType_id IS NULL, 1 =1,Contract_Contingent.socStatusType_id=%d)'%socStatus)
        if clientWork:
            cond.append(u'IF( Contract_Contingent.org_id IS NULL, 1 =1,Contract_Contingent.org_id=%d)'%clientWork)

        cond.append(u'IF( Contract.finance_id IS NULL, 1 =1,Contract.finance_id=2)')
        if not cond:
            return 'flag', 'flag', 0, 0
        stmtContract = """SELECT  DISTINCT(`Contract`.id) as contractId, Contract.number as contractName
                                FROM  `Contract`
                                LEFT JOIN Contract_Contingent ON Contract_Contingent.master_id = Contract.id
                                LEFT JOIN Contract_Specification ON Contract_Specification.master_id = Contract.id
                                LEFT JOIN Organisation ON Contract_Contingent.insurer_id = Organisation.id
                                WHERE `Contract_Specification`.deleted =0 AND Contract_Contingent.deleted =0 AND %s"""%(QtGui.qApp.db.joinAnd(cond))
        queryC = self.db.query(stmtContract)

        k =0
        contractId = None
        contractName = []
        while queryC.next():
            k+=1
            contractId= forceInt(queryC.record().value('contractId'))
            contractName.append(forceString(queryC.record().value('contractName')))
        if contractId:
            return  contractId, oldContractId, k, isAmbiguitous, contractName
        else:
             return None, None, k, 0, contractName

    def getInfromationForContract(self,eventId):
        stmt = """SELECT
                        Event.contract_id as oldContract,
                        Event.eventType_id as eventType,
                        Event.client_id as clientId,
                        Event.setDate as eventBegDate,
                        Event.execDate as eventEndDate,
                        ClientPolicy.insurer_id as clientInsurerId,
                        ClientPolicy.policyType_id as policyType,
                        ClientAttach.attachType_id as clientAttachType,
                        -- SUBSTRING(AddressHouse.KLADRCode,1,2) as addressArea,
                        ((YEAR(Event.setDate) - YEAR(Client.birthDate)) -
                        (RIGHT(Event.setDate, 5) < RIGHT(Client.birthDate, 5))) as clientAge,
                        Client.sex as clientSex,
                        SUBSTRING( Organisation.area, 1, 2 ) as organizationArea,
                        ClientSocStatus.socStatusType_id as socStatus,
                        ClientWork.org_id as clientWork
                FROM  `Event`
                LEFT JOIN Client ON Client.id = Event.client_id
                LEFT JOIN ClientAttach ON (ClientAttach.client_id = Client.id AND ClientAttach.begDate < Event.setDate
                            AND (ClientAttach.endDate IS NULL or ClientAttach.endDate>Event.execDate or ClientAttach.endDate='0000-00-00') AND ClientAttach.deleted =0)
                LEFT JOIN ClientPolicy ON (ClientPolicy.client_id = Client.id AND
                            ClientPolicy.begDate <= Event.setDate AND
                            (ClientPolicy.endDate is NULL or ClientPolicy.endDate >= Event.setDate or ClientPolicy.endDate='0000-00-00') and ClientPolicy.insurer_id IS NOT NULL AND ClientPolicy.deleted =0)
                LEFT JOIN Organisation ON ClientPolicy.insurer_id = Organisation.id
                LEFT JOIN ClientAddress ON ClientAddress.client_id = Client.id
                            and ClientAddress.type = 0 AND ClientAddress.address_id IS NOT NULL
                -- LEFT JOIN Address ON Address.id = ClientAddress.address_id
                -- LEFT JOIN AddressHouse ON AddressHouse.id = Address.house_id
                LEFT JOIN ClientSocStatus ON Client.id = ClientSocStatus.client_id
                LEFT JOIN ClientWork ON Client.id = ClientWork.client_id
                WHERE Event.id =%d
                GROUP BY ClientPolicy.id, ClientAttach.id
                HAVING MAX(ClientAddress.id)
                """ % (eventId)
        query = self.db.query(stmt)
#        cond = []
        eventType = None
        oldContract = None
        clientId = None
        eventBegDate= None
        eventEndDate = None
        clientInsurerId = None
        policyType = None
        clientAge = None
        clientSex = None
        clientAttachType = None
        organizationArea = None
        socStatus = None
        clientWork = None
        i=0

        while query.next():
            i=i+1
            eventType = forceRef(query.record().value('eventType'))
            oldContract = forceRef(query.record().value('oldContract'))
            clientId = forceRef(query.record().value('clientId'))
            eventBegDate = forceDate(query.record().value('eventBegDate'))
            eventEndDate = forceDate(query.record().value('eventEndDate'))
            clientInsurerId = forceRef(query.record().value('clientInsurerId'))
            policyType = forceRef(query.record().value('policyType'))
#            addressArea = forceInt(query.record().value('addressArea'))
            clientAge = forceInt(query.record().value('clientAge'))
            clientSex = forceInt(query.record().value('clientSex'))
            clientAttachType= forceRef(query.record().value('clientAttachType'))
            organizationArea = forceInt(query.record().value('organizationArea'))
            socStatus = forceRef(query.record().value('socStatus'))
            clientWork = forceRef(query.record().value('clientWork'))
        return  eventType, oldContract, clientId, eventBegDate, \
                eventEndDate, clientInsurerId, policyType,   \
                clientAge, clientSex, clientAttachType, organizationArea, \
                socStatus, clientWork, i




    def addClientPolicy(self, clientId, insurerId, serial, number, begDate, policyTypeId, policyKindId):
        table = self.db.table('ClientPolicy')
        record = table.newRecord()
        record.setValue('client_id', toVariant(clientId))
        record.setValue('insurer_id', toVariant(insurerId))

        if policyTypeId:
            record.setValue('policyType_id', toVariant(policyTypeId))

        if policyKindId:
            record.setValue('policyKind_id', toVariant(policyKindId))

        record.setValue('serial', toVariant(serial))
        record.setValue('number', toVariant(number))
        record.setValue('begDate', toVariant(begDate))
        self.db.insertRecord(table, record)

# , refuseTypeId
    def processAccountItemIdList(self, recordList, refuseCode, refuseText, note, eventId):
        payStatusMask = 0

        for record in recordList:
            QtGui.qApp.processEvents()
            self.accountIdSet.add(forceRef(record.value('Account_id')))
            contractId = forceRef(record.value('contract_id'))

            if self.prevContractId != contractId:
                self.prevContractId = contractId
                financeId = forceRef(self.db.translate('Contract', 'id', contractId, 'finance_id'))
                payStatusMask = getPayStatusMask(financeId)

            accountItemId = forceRef(record.value('id'))

#            accDate = forceDate(record.value('Account_date'))
#            accItemDate = forceDate(record.value('Account_Item_date'))
#            if accItemDate or (refuseDate and (accDate > refuseDate)):
#                self.err2log(u'счёт уже отказан')
#                return

            self.nProcessed += 1

            accItem = self.db.getRecord(self.tableAccountItem, '*', accountItemId)
#            accItem.setValue('date', toVariant(refuseDate if refuseDate else QDate.currentDate()))


            if ((refuseCode <> 0) and (refuseCode <> 53)) :
                refuseTypeId = self.getRefuseTypeId(refuseCode)
                self.nRefused += 1
                accItem.setValue('refuseType_id', toVariant(refuseTypeId))
                updateDocsPayStatus(accItem, payStatusMask, CPayStatus.refusedBits)
#                accItem.setValue('note', toVariant(refuseTypeId))
                self.err2log(u'отказан, код: ' + str(refuseCode)+' '+ refuseText)
                accItem.setValue('date', toVariant(QDate.currentDate()))

            else:
                if (refuseCode == 53):
                    refuseTypeId = self.getRefuseTypeId(refuseCode)
                    accItem.setValue('refuseType_id', toVariant(refuseTypeId))
                    updateDocsPayStatus(accItem, payStatusMask, CPayStatus.payedBits)
                    self.err2log(u'подтвержден, код: 53 '+ refuseText)
                    self.nPayed += 1
                    accItem.setValue('date', toVariant(QDate.currentDate()))
                else:
                    updateDocsPayStatus(accItem, payStatusMask, CPayStatus.payedBits)
                    accItem.setValue('date', toVariant(QDate.currentDate()))
                    self.err2log(u'подтверждён')
                    self.nPayed += 1

            accItem.setValue('number', toVariant(self.confirmation))
            accItem.setValue('note', toVariant(note))
            self.db.updateRecord(self.tableAccountItem, accItem)

        if recordList == []:
            self.nNotFound += 1
            self.err2log(u'счёт не найден')


    def readGroup(self,  name,  fields, silent = False, subGroupDict= {}, result = {}):
        r = CXMLimport.readGroup(self, name, fields, silent, subGroupDict)
        for key, val in r.iteritems():
            result[key] = val
#        print result
        return result
