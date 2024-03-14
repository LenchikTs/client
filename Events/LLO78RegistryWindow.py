# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4                   import QtGui, QtCore
from PyQt4.QtCore            import pyqtSignature, SIGNAL, QObject, QDateTime

from library.DialogBase      import CDialogBase
from library.TableModel      import CTableModel
from library.TableModel      import CTextCol
from library.Identification  import findByIdentification, getIdentification
from library.Utils           import forceString, exceptionToUnicode, toVariant
from library.MSCAPI          import MSCApi

from RefBooks.Tables               import rbCode, rbName, rbSocStatusType
from Ui_LLO78RegistryWindow        import Ui_LLO78RegistryDialog
from Events.LLO78MkbSearchDialog   import CLLO78MkbSearchDialog

from Exchange.FSS.signatureHandler import CSignatureHandler

import requests
import base64
import xml.etree.ElementTree as ET


class CLLO78RecipeRegistryDialog(CDialogBase, Ui_LLO78RegistryDialog):
    idFieldName = 'id'
    def __init__(self, parent, ckatlList, servCode, login, password, clientInfo, NPPCode):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.setup([CTextCol(u'Код',          [rbCode], 20),
                    CTextCol(u'Наименование', [rbName], 40)
                   ], rbSocStatusType, [rbCode, rbName])
        self.ckatlList = ckatlList
        self.servCode = servCode
        self.login = login
        self.password = password
        self.clientInfo = clientInfo
        self.NPPCode = NPPCode
        self.actionProps = []
        self.currentCkatlForMkbSearch = None
        if not QtGui.qApp.lloTestMode():
            QtGui.QMessageBox.critical( self, u'', u'Внимание! Тестовый режим ЛЛО выключен.', QtGui.QMessageBox.Close)
        self.btnMkbSearch.setEnabled(False)
        self.cmbRecipeExpirationDate.setCurrentIndex(3)


    def setup(self, cols, tableName, order):
        self.props = {}
        self.order = order
        self.addModels('SocStatusTypes', CTableModel(self, cols))
        self.modelSocStatusTypes.idFieldName = self.idFieldName
        self.modelSocStatusTypes.setTable(tableName)
        self.setModels(self.tblSocStatusTypes, self.modelSocStatusTypes, self.selectionModelSocStatusTypes)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinMaxButtonsHint)


    def accept(self):
        QtGui.QDialog.accept(self)
        return


    def exec_(self):
        idList = self.select(self.props)
        self.modelSocStatusTypes.setIdList(idList)
        return CDialogBase.exec_(self)


    def generateFilterByProps(self, props):
        cond = []
        table = self.modelSocStatusTypes.table()
#        for key, value in props.iteritems():
#            if table.hasField(key):
#                cond.append(table['key'].eq(value))
        if table.hasField('deleted'):
            cond.append(table['deleted'].eq(0))
        socStatusCodes = []
        missedTypesInfo = u''
        for ckatl in self.ckatlList:
            socStatusId = findByIdentification('rbSocStatusType', 'urn:socStatusTypeLLO78', ckatl, False)
            if not socStatusId:
                missedTypesInfo += u'%s, ' % ckatl
                continue
            socStatusCode = QtGui.qApp.db.translate(table, 'id', socStatusId, 'code').toString()
            socStatusCodes.append(socStatusCode)
        if missedTypesInfo:
            self.lblMissedTypesInfo.setText(u'В справочнике МИС нет указанных кодов льгот: %s' % missedTypesInfo[:-2])
            self.lblMissedTypesInfo.setStyleSheet('color: red')
        else:
            self.lblMissedTypesInfo.setText(u'В справочнике МИС найдены все льготы, полученные из сервиса ЛЛО')
        cond.append(table['code'].inlist(socStatusCodes))
        return cond


    def select(self, props={}):
        db = QtGui.qApp.db
        table = self.modelSocStatusTypes.table()
        return db.getIdList(table,
                            self.idFieldName,
                            self.generateFilterByProps(props),
                            self.order)


    def setCurrentItemSocStatusTypeId(self, itemId):
        self.tblSocStatusTypes.setCurrentItemId(itemId)


    def currentItemSocStatusTypeId(self):
        return self.tblSocStatusTypes.currentItemId()


    def currentData(self, col):
        row = self.tblSocStatusTypes.currentRow()
        index = self.modelSocStatusTypes.createIndex(row, col)
        return self.modelSocStatusTypes.data(index)


    @pyqtSignature('QModelIndex')
    def on_tblSocStatusTypes_clicked(self, index):
        ckatlId = self.currentItemSocStatusTypeId()
        if not ckatlId:
            QtGui.QMessageBox.critical( self, u'', u'Льгота не выбрана', QtGui.QMessageBox.Close)
            return
        self.currentCkatlForMkbSearch = getIdentification('rbSocStatusType', ckatlId, 'urn:socStatusTypeLLO78')
        if self.currentCkatlForMkbSearch:
            self.btnMkbSearch.setEnabled(True)


    @pyqtSignature('')
    def on_btnFindLPs_clicked(self):
        try:
            ckatlId = self.currentItemSocStatusTypeId()
            if not ckatlId:
                raise Exception(u'Льгота не выбрана. Необходимо выбрать льготу.')
            self.ckatl = getIdentification('rbSocStatusType', ckatlId, 'urn:socStatusTypeLLO78')
            self.getMkbFromLLO()
            nameMed = self.edtRequestedLP.text()
            xmlGetLP = """<?xml version="1.0" encoding="utf-8"?>
                            <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                              <soap:Body>
                                <GetLp xmlns="http://tempuri.org/">
                                  <name_med>%s</name_med>
                                  <Kodlg>%s</Kodlg>
                                  <user>%s</user>
                                  <pass>%s</pass>
                                  <serv>%s</serv>
                                </GetLp>
                              </soap:Body>
                            </soap:Envelope>
                            """ % (nameMed, self.ckatl, self.login, self.password, self.servCode)
            body = xmlGetLP.encode('utf-8')
            #print(body.decode('utf-8'))
            headers = {'Content-Type': 'text/xml; charset=utf-8', 'Content-Length': str(len(body))}
            serviceUrl = QtGui.qApp.lloServiceUrl()
            response = requests.post(serviceUrl, data=body, headers=headers)
            content = response.content
            status = response.status_code
            #print(content.decode('utf-8'))
            QtGui.qApp.log('================================================================================\nLLO78Service', 'ResponseStatus ' + str(status) + ' ResponseContent:\n' + content.decode('utf-8'))
            lpData = []
            root = ET.fromstring(content)
            hasTagsWithData = False
            for NewDataSet in root.getiterator('NewDataSet'):
                for tableTag in NewDataSet.getiterator('Table'):
                    hasTagsWithData = True
                    lpData.append([])
                    lpData[-1].append(tableTag.find('nomk_ls').text)
                    lpData[-1].append(tableTag.find('mnn').text)
                    lpData[-1].append(tableTag.find('asmnn_l').text)

                    flagDoctorsComission = tableTag.find('flag_kek').text
                    if flagDoctorsComission == 'false':
                        lpData[-1].append(u'нет')
                    elif flagDoctorsComission == 'true':
                        lpData[-1].append(u'да')
                    else:
                        lpData[-1].append(flagDoctorsComission)

                    #lpData[-1].append(tableTag.find('ko_ost').text)
                    tagKo_ost = tableTag.find('ko_ost')
                    if tagKo_ost is not None:
                        lpData[-1].append(tagKo_ost.text)
                    else:
                        lpData[-1].append(u'0 - Остатки ЛП и МИ на хранении отсутствуют')
                    lpData[-1].append(tableTag.find('name_med').text)

                    tagName_fct = tableTag.find('name_fct')
                    if tagName_fct is not None:
                        lpData[-1].append(tagName_fct.text)
                    else:
                        lpData[-1].append(u'Производитель не указан в сервисе ЛЛО')

                    lpData[-1].append(tableTag.find('NAME_LF_R').text)

                    tagD_LS_doc = tableTag.find('D_LS_doc')
                    if tagD_LS_doc is not None:
                        lpData[-1].append(tagD_LS_doc.text)
                    else:
                        lpData[-1].append(u'')
            if not hasTagsWithData:
                QtGui.QMessageBox.critical( self, u'', u'Препарат не найден в сервисе ЛЛО', QtGui.QMessageBox.Close)
                return
            self.tblRequestedLPs.setRowCount(len(lpData))
            self.tblRequestedLPs.setColumnCount(9)
            self.tblRequestedLPs.setColumnHidden(6, True)
            self.tblRequestedLPs.setColumnHidden(7, True)
            for i, lp in enumerate(lpData):
                for j, item in enumerate(lp):
                    self.tblRequestedLPs.setItem(i, j, QtGui.QTableWidgetItem(item))
            self.tblRequestedLPs.setHorizontalHeaderLabels([u'Код ЛЛО', u'МНН на русском', u'МНН на латинском', u'ВК', u'Остаток', u'Название', u'Производитель', u'Тип упаковки', u'Дозировка ЛП'])
            self.tblRequestedLPs.resizeColumnsToContents()
            self.tblRequestedLPs.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            self.tblRequestedLPs.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
            self.tblRequestedLPs.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
            QObject.connect(self.tblRequestedLPs, SIGNAL('clicked(QModelIndex)'), self.on_tblRequestedLPs_clicked)
        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical( self,
                                        u'',
                                        exceptionToUnicode(e),
                                        QtGui.QMessageBox.Close)


    @pyqtSignature('')
    def on_tblRequestedLPs_clicked(self):
        index = self.tblRequestedLPs.currentIndex()
        if index.isValid():
            row = index.row()
        self.tblRequestedLPs.setCurrentCell(row, 0)
        itemCode = self.tblRequestedLPs.currentItem()
        self.codLP = itemCode.data(0).toString()

        self.tblRequestedLPs.setCurrentCell(row, 5)
        itemName = self.tblRequestedLPs.currentItem()
        self.nameLP = itemName.data(0).toString()

        self.tblRequestedLPs.setCurrentCell(row, 4)
        itemKo_ost = self.tblRequestedLPs.currentItem()
        self.ko_ost = itemKo_ost.data(0).toString()

        self.tblRequestedLPs.setCurrentCell(row, 1)
        itemMnn = self.tblRequestedLPs.currentItem()
        self.mnn = itemMnn.data(0).toString()

        self.tblRequestedLPs.setCurrentCell(row, 2)
        itemAmnn_l = self.tblRequestedLPs.currentItem()
        self.amnn_l = itemAmnn_l.data(0).toString()
        
        self.tblRequestedLPs.setCurrentCell(row, 6)
        itemName_fct = self.tblRequestedLPs.currentItem()
        self.name_fct = itemName_fct.data(0).toString()
        
        self.tblRequestedLPs.setCurrentCell(row, 7)
        itemNameLfR = self.tblRequestedLPs.currentItem()
        self.nameLfR = itemNameLfR.data(0).toString()

        self.tblRequestedLPs.setCurrentCell(row, 8)
        itemD_LS_doc = self.tblRequestedLPs.currentItem()
        self.D_LS_doc = itemD_LS_doc.data(0).toString()


    @pyqtSignature('')
    def on_btnMkbSearch_clicked(self):
        LLO78MkbSearchDialog = CLLO78MkbSearchDialog(self, self.currentCkatlForMkbSearch, self.login, self.password, self.servCode)
        if LLO78MkbSearchDialog.exec_():
            self.cmbMKB.setText(LLO78MkbSearchDialog.currentMkbCode)


    @pyqtSignature('')
    def on_btnCancelRecipeRegistration_clicked(self):
        QtGui.QDialog.reject(self)
        return


    @pyqtSignature('')
    def on_btnSignAndRegistrateRecipe_clicked(self):
        try:
            if self.tblRequestedLPs.currentRow() == -1:
                QtGui.QMessageBox.critical( self, u'', u'Необходимо выбрать препарат', QtGui.QMessageBox.Close)
                return
            if self.ko_ost == u'0 - Остатки ЛП и МИ на хранении отсутствуют':
                QtGui.QMessageBox.critical( self, u'', u'Остатки ЛП и МИ на хранении отсутствуют', QtGui.QMessageBox.Close)
                return
            serviceUrl = QtGui.qApp.lloServiceUrl()
            lloRecipientCode = QtGui.qApp.lloRecipientCode()
            lloRecipientName = QtGui.qApp.lloRecipientName()
            db = QtGui.qApp.db
            codDoc = getIdentification('Person', QtGui.qApp.userId, 'urn:personLLO78')
            currentOrgId = QtGui.qApp.currentOrgId()
            orgCode = getIdentification('Organisation', currentOrgId, 'urn:organisationLLO78')
            orgName = forceString(db.translate('Organisation', 'id', currentOrgId, 'shortName').toString())
            fam, im, ot, ss, dr, policySeria, policyNumber, clientId, sex = self.clientInfo
            
            if sex == '1':
                fSex = '0'
            elif sex == '2':
                fSex = '1'
            else:
                raise Exception(u'Пол пациента не указан')
            
            if self.cmbDischargeType.currentText() == u'Упаковка':
                dischargeType = '0'
            elif self.cmbDischargeType.currentText() == u'Единицы ЛП и МИ':
                dischargeType = '1'
            
            if self.cmbRecipeExpirationDate.currentText() == u'5 дней':
                expirationDate = '4'
            elif self.cmbRecipeExpirationDate.currentText() == u'10 дней':
                expirationDate = '1'
            elif self.cmbRecipeExpirationDate.currentText() == u'1 месяц':
                expirationDate = '2'
            elif self.cmbRecipeExpirationDate.currentText() == u'3 месяца':
                expirationDate = '3'
            
            typeOfProtocol = '0' if self.chkTypeOfProtocol.isChecked() else '1'
            
            if self.cmbDischargeAttribute.currentText() == u'МНН':
                dischargeAttributeCode = '2'
            elif self.cmbDischargeAttribute.currentText() == u'ТРН':
                dischargeAttributeCode = '1'
            
            testMsg = u'TestMessage' if QtGui.qApp.lloTestMode() else u''
            currDate = forceString(QDateTime.currentDateTime().toString('yyyy-MM-ddThh:mm:ss'))
            lpQuantity = self.dsbLPQuantity.value()
            lpQuantityFinal = ('%10.3f' % lpQuantity).strip()
            if lpQuantityFinal == u'0.000':
                QtGui.QMessageBox.critical( self, u'', u'Необходимо указать ненулевое количество', QtGui.QMessageBox.Close)
                return
            nomenclatureId = findByIdentification('rbNomenclature', 'urn:nomenclatureLLO78', self.codLP, False)
            nomenclatureId = self.storeLPInNomenclature() if not nomenclatureId else nomenclatureId
            
            rawXmlSetRecipeNumberHeaderPart1 = u"""<?xml version="1.0" encoding="utf-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/"><soapenv:Header></soapenv:Header><soapenv:Body><tem:SetRecipeNumber><tem:RequestDaraRecipe><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Header><wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" soapenv:actor="http://smev.gosuslugi.ru/actors/smev"><wsse:BinarySecurityToken xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary" ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3" wsu:Id="http://smev.gosuslugi.ru/actors/smev" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">%s</wsse:BinarySecurityToken><ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">"""

            rawXmlSetRecipeNumberHeaderPart2 = u"""<ds:SignatureValue>%s</ds:SignatureValue><ds:KeyInfo><wsse:SecurityTokenReference xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"><wsse:Reference URI="#http://smev.gosuslugi.ru/actors/smev" ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"></wsse:Reference></wsse:SecurityTokenReference></ds:KeyInfo></ds:Signature></wsse:Security></soapenv:Header>"""

            signedInfo = u"""<ds:SignedInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#"><ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"></ds:CanonicalizationMethod><ds:SignatureMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256"></ds:SignatureMethod><ds:Reference URI="#DataOfRicipe"><ds:Transforms><ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"></ds:Transform></ds:Transforms><ds:DigestMethod Algorithm="urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256"></ds:DigestMethod><ds:DigestValue>%s</ds:DigestValue></ds:Reference></ds:SignedInfo>"""

            rawXmlSetRecipeNumberBody = u"""<soapenv:Body xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" wsu:Id="DataOfRicipe"><Recipe:DataRequest xmlns:Recipe="http://Recipe-by-data.skmv.rstyle.com"><rev:Message xmlns:rev="http://smev.gosuslugi.ru/rev120315"><rev:Sender><rev:Code>%s</rev:Code><rev:Name>%s</rev:Name></rev:Sender><rev:Recipient><rev:Code>%s</rev:Code><rev:Name>%s</rev:Name></rev:Recipient><rev:Service><rev:Mnemonic>Get_Recope_Number</rev:Mnemonic><rev:Version>1.02</rev:Version></rev:Service><rev:TypeCode>OTHR</rev:TypeCode><rev:Status>REQUEST</rev:Status><rev:Date>%s</rev:Date><rev:ExchangeType>%s</rev:ExchangeType><rev:ServiceCode>%s</rev:ServiceCode><rev:TestMsg>%s</rev:TestMsg></rev:Message><rev:MessageData xmlns:rev="http://smev.gosuslugi.ru/rev120315"><rev:AppData><rev:request><Recipe:fio><fio:FirstName xmlns:fio="http://fio.skmv.rstyle.com">%s</fio:FirstName><fio:LastName xmlns:fio="http://fio.skmv.rstyle.com">%s</fio:LastName><fio:Patronymic xmlns:fio="http://fio.skmv.rstyle.com">%s</fio:Patronymic><fio:gender xmlns:fio="http://fio.skmv.rstyle.com">%s</fio:gender><fio:birthDate xmlns:fio="http://fio.skmv.rstyle.com">%s</fio:birthDate><fio:Snils xmlns:fio="http://fio.skmv.rstyle.com">%s</fio:Snils></Recipe:fio><Recipe:LGCOD>%s</Recipe:LGCOD><Recipe:MKBCod>%s</Recipe:MKBCod><Recipe:CodLP>%s</Recipe:CodLP><Recipe:ViewPacking>%s</Recipe:ViewPacking><Recipe:validity>%s</Recipe:validity><Recipe:TypeOfProtocol>%s</Recipe:TypeOfProtocol><Recipe:PolisSer>%s</Recipe:PolisSer><Recipe:polisNum>%s</Recipe:polisNum><Recipe:OutpatientCard>%s</Recipe:OutpatientCard><Recipe:Signature>%s</Recipe:Signature><Recipe:UserCode>%s</Recipe:UserCode><Recipe:CodDoc>%s</Recipe:CodDoc><Recipe:NPP>%s</Recipe:NPP><Recipe:Quantit>%s</Recipe:Quantit><Recipe:MNN>%s</Recipe:MNN></rev:request></rev:AppData></rev:MessageData></Recipe:DataRequest></soapenv:Body>"""
            
            rawXmlSetRecipeNumberTail = u"""</soapenv:Envelope></tem:RequestDaraRecipe></tem:SetRecipeNumber></soapenv:Body></soapenv:Envelope>"""

            xmlSetRecipeNumberBody = rawXmlSetRecipeNumberBody.decode('utf-8') % (orgCode,
                                                                                  orgName,
                                                                                  lloRecipientCode,
                                                                                  lloRecipientName, 
                                                                                  currDate,
                                                                                  '1',
                                                                                  self.servCode,
                                                                                  testMsg,
                                                                                  fam,
                                                                                  im,
                                                                                  ot,
                                                                                  unicode(fSex),
                                                                                  dr,
                                                                                  ss,
                                                                                  self.ckatl,
                                                                                  self.cmbMKB.text(),
                                                                                  self.codLP,
                                                                                  unicode(dischargeType),
                                                                                  unicode(expirationDate),
                                                                                  unicode(typeOfProtocol),
                                                                                  policySeria,
                                                                                  policyNumber,
                                                                                  clientId,    
                                                                                  unicode(self.edtUseMethod.text()),
                                                                                  u'',
                                                                                  codDoc,
                                                                                  self.NPPCode,
                                                                                  lpQuantityFinal,
                                                                                  unicode(dischargeAttributeCode)
                                                                                 )
            api = MSCApi(QtGui.qApp.getCsp())
            userCert = QtGui.qApp.getUserCert(api)
            handler = CSignatureHandler(api, userCert)
            with userCert.provider() as provider:
                userCertBytes = handler._getCertBytes(provider)
                cert = base64.b64encode(userCertBytes)
                rawXmlSetRecipeNumberHeaderPart1Final = rawXmlSetRecipeNumberHeaderPart1 % (cert)

                bodyBeforeSign = xmlSetRecipeNumberBody.encode('utf-8')
                digest = handler._hash(provider, bodyBeforeSign)
                digestValue = base64.b64encode(digest)

                signedInfoFinal = signedInfo % digestValue
                signatureValue = handler._sign(provider, signedInfoFinal.encode('utf-8'))
                signatureValueFinal = base64.b64encode(signatureValue)

            rawXmlSetRecipeNumberHeaderPart2Final = rawXmlSetRecipeNumberHeaderPart2 % (signatureValueFinal)

            xmlSetRecipeNumberHeader = rawXmlSetRecipeNumberHeaderPart1Final.encode('utf-8') + signedInfoFinal.encode('utf-8') + rawXmlSetRecipeNumberHeaderPart2Final.encode('utf-8')

            body = xmlSetRecipeNumberHeader + bodyBeforeSign + rawXmlSetRecipeNumberTail.encode('utf-8')
            #print(body.decode('utf-8'))
            headers = {'Content-Type': 'text/xml; charset=utf-8', 'Content-Length': str(len(body)), 'SOAPAction': 'http://tempuri.org/SetRecipeNumber'}
            QtGui.qApp.log('================================================================================\nLLO78Service', 'Location: ' + serviceUrl + '\nAction: SetRecipeNumber\nRequestContent:\n' + body.decode('utf-8'))
            response = requests.post(serviceUrl, data=body, headers=headers)

            content = response.content
            status = response.status_code
            QtGui.qApp.log('================================================================================\nLLO78Service', 'ResponseStatus ' + str(status) + ' ResponseContent:\n' + content.decode('utf-8'))
            #print(status)
            #print(content.decode('utf-8'))
            recipeData = self.getRecipeData(content)
            if not recipeData:
                QtGui.QMessageBox.critical( self, u'', u'Данные по рецепту не получены', QtGui.QMessageBox.Close)
                return
            # порядок добавления в список self.actionProps важен !!!
            self.actionProps.extend(recipeData)
            self.actionProps.append(self.cmbDischargeAttribute.currentText())
            self.actionProps.append(self.cmbDischargeType.currentText())
            self.actionProps.append(self.dsbLPQuantity.value())
            self.actionProps.append(self.edtUseMethod.text())
            self.actionProps.append(self.cmbRecipeExpirationDate.currentText())
            self.actionProps.append(self.chkTypeOfProtocol.isChecked())
            self.actionProps.append(self.currentItemSocStatusTypeId())
            self.actionProps.append(nomenclatureId)
            self.actionProps.append(self.D_LS_doc)
            self.actionProps.append(self.cmbMKB.currentText())
            QtGui.QDialog.accept(self)
            return
        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical( self,
                                        u'',
                                        exceptionToUnicode(e),
                                        QtGui.QMessageBox.Close)


    def getRecipeData(self, content):
        start1 = content.find('DateField:RecipeBarCod')
        end1 = content.rfind('DateField:RecipeBarCod')

        start2 = content.find('DateField:RecipeSeriesr')
        end2 = content.rfind('DateField:RecipeSeriesr')

        start3 = content.find('DateField:RecipeNumber')
        end3 = content.rfind('DateField:RecipeNumber')

        if any(x == -1 for x in [start1, start2, start3, end1, end2, end3]):
            QtGui.qApp.log('================================================================================\nLLO78Service', u'В ответе нет ожидаемого тега RecipeBarCod/RecipeSeriesr/RecipeNumber\n')
            return None
            #raise Exception(u'Полученный ответ не содержит данных по рецепту')
        if start1 == -1 or start2 == -1 or start3 == -1 or end1 == -1 or end2 == -1 or end3 == -1:
            QtGui.qApp.log('================================================================================\nLLO78Service', u'В ответе нет ожидаемого тега RecipeBarCod/RecipeSeriesr/RecipeNumber\n')
            return None

        recipeSeria = content[start2 + 24:end2 - 2]
        recipeBarCodeReference = content[start1 + 23:end1 - 2]
        recipeNumber = content[start3 + 23:end3 - 2]
        return (recipeBarCodeReference, recipeSeria, recipeNumber)


    def getMkbFromLLO(self):
        nameds = self.cmbMKB.text()
        xmlGetMkb = """<?xml version="1.0" encoding="utf-8"?>
                         <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                         xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                         xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                          <soap:Body>
                           <GetMkb xmlns="http://tempuri.org/">
                            <nameds>%s</nameds>
                            <ckatl>%s</ckatl>
                            <user>%s</user>
                            <pass>%s</pass>
                            <serv>%s</serv>
                           </GetMkb>
                          </soap:Body>
                         </soap:Envelope>
                      """ % (nameds, self.ckatl, self.login, self.password, self.servCode)
        body = xmlGetMkb.encode('utf-8')
        headers = {'Content-Type': 'text/xml; charset=utf-8', 'Content-Length': str(len(body))}
        serviceUrl = QtGui.qApp.lloServiceUrl()
        response = requests.post(serviceUrl, data=body, headers=headers)
        content = response.content
        status = response.status_code
        #print(content.decode('utf-8'))
        QtGui.qApp.log('================================================================================\nLLO78Service', 'ResponseStatus ' + str(status) + ' ResponseContent:\n' + content.decode('utf-8'))


    def storeLPInNomenclature(self):
        db = QtGui.qApp.db
        db.transaction()
        try:
            tableNomenclature = db.table('rbNomenclature')
            newNomenclatureRecord = tableNomenclature.newRecord()
            newNomenclatureRecord.setValue('name', toVariant(self.nameLP))
            newNomenclatureRecord.setValue('mnnLatin', toVariant(self.amnn_l))
            newNomenclatureRecord.setValue('code', toVariant(self.codLP))
            newNomenclatureRecord.setValue('internationalNonproprietaryName', toVariant(self.mnn))
            newNomenclatureRecord.setValue('producer', toVariant(self.name_fct))
            newNomenclatureRecord.setValue('note', toVariant(u'Тип упаковки: ' + self.nameLfR))
            nomenclatureId = db.insertRecord(tableNomenclature, newNomenclatureRecord)

            tableNomenclatureIdentification = db.table('rbNomenclature_Identification')
            newNomenclatureIdentificationRecord = tableNomenclatureIdentification.newRecord()
            newNomenclatureIdentificationRecord.setValue('value', self.codLP)
            newNomenclatureIdentificationRecord.setValue('master_id', nomenclatureId)
            systemId = db.translate('rbAccountingSystem', 'urn', 'urn:nomenclatureLLO78', 'id')
            newNomenclatureIdentificationRecord.setValue('system_id', systemId)
            db.insertRecord(tableNomenclatureIdentification, newNomenclatureIdentificationRecord)

            db.commit()
            return nomenclatureId
        except:
            db.rollback()
            raise
