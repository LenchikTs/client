# -*- coding: utf-8 -*-
'''
Created on 04.09.2012

@author: Alex Parfentjev
'''

#from PyQt4.QtXml import *
from PyQt4 import QtGui
from PyQt4.QtCore import Qt


from library.Utils     import forceDate, forceInt, forceRef, forceString, forceDouble

class Export29XMLCommon(object):
    u'''
    здесь будут храниться методы общего назначения для подушевого и простого экспортов
    это необходимо чтобы гарантировать одновременность правок (избегать двойного кода),
    а также собрать воедино в статические методы те вещи, которые имеют общее назначение
    '''

#unused yet
    def __init__(self):
        pass


    @staticmethod
    def isPatientAttached(db, clientId):
        stmt = """SELECT `rbAttachType`.`code` as CODE
                  FROM
                  `ClientAttach`
                  LEFT JOIN `rbAttachType` ON `rbAttachType`.`id` = `ClientAttach`.`AttachType_id`
                  WHERE `client_id` =%d"""%clientId
        query = db.query(stmt)
        if query.next():
            return forceInt(query.record().value('CODE')) == 1


    @staticmethod
    def getDatesForAction(db, eventId, actionId = None, serviceNote = None):
        if  'isDateByAction' in serviceNote:
            stmt = """SELECT `begDate` AS `begDate`, `endDate` AS `endDate`
                    FROM `Action`
                    WHERE `Action`.`id` = %d """%(actionId)
        else:
            stmt = """SELECT MIN(`begDate`) AS `begDate`, MAX(`endDate`) AS `endDate`
                  FROM
                  `Action`
                  LEFT JOIN `ActionType` ON `ActionType`.`id` = `Action`.`ActionType_id`
                  WHERE `Action`.`Event_Id` = %d """%(eventId)

        query = db.query(stmt)

        if query.next():
            #возвращаем первый actionId, т.е. самый новый
            begDate = forceDate(query.record().value('begDate'))
            endDate = forceDate(query.record().value('endDate'))

        try:
            begDate
        except:
            begDate = None

        try:
            endDate
        except:
            endDate = None

        return (begDate, endDate)


    @staticmethod
    def getDatesForEvent(db, eventId):
        stmt = """SELECT  `setDate`  as begDate,  `execDate` as endDate
                  FROM  `Event`
                  WHERE  `id` = %d """%eventId
        query = db.query(stmt)
        if query.next():
            return (forceDate(query.record().value('begDate')),
                    forceDate(query.record().value('endDate')))
        else:
            return None, None


    @staticmethod
    def getPcode(db, record, visitId = None, actionId1 = None):
        actionId = forceInt(record.value('action_id')) if not actionId1 else actionId1
        if not visitId: visitId= forceInt(record.value('visit_id'))
        eventId = forceInt(record.value('event_id'))
        stmt = """SELECT CONCAT_WS('-',SUBSTRING(Person.`SNILS`, 1, 3), SUBSTRING(Person.`SNILS`, 4, 3), SUBSTRING(Person.`SNILS`, 7, 3), SUBSTRING(Person.`SNILS`, 10, 2)) as code, `Person`.`id` as `personId`
                        FROM `Person`
                        LEFT JOIN `TableName` ON `TableName`.`person_id` = `Person`.`id`
                        WHERE
                        `TableName`.`id` = %d"""

        if (not actionId and not visitId):
            if eventId:
                stmt = stmt.replace('TableName', 'Event').replace('person_id', 'execPerson_id') %eventId
            else:
                return None, None
        else:
            if actionId:
                stmt = stmt.replace('TableName', 'Action')%actionId
            elif visitId:
                stmt = stmt.replace('TableName', 'Visit')%visitId
        query = db.query(stmt)
        if query.next():
            return forceString(query.record().value('personId')), forceString(query.record().value('code'))
        else:
            return None, None
        
    
        

    
    @staticmethod
    def getDirectionEIRNumber(db, eventId):
        str = u"DS_ONK"
        str1 = u"Да"
        stmt1 = """SELECT 1 as flag
                    FROM Action
                    LEFT JOIN ActionType ON ActionType.id = actionType_id
                    WHERE ActionType.flatCode IN ('received', 'hospitalDirection', 'hospitalDirection2018',
                     'planning') AND `Action`.event_id =%d AND Action.deleted = 0
                     """%( eventId)
                     
        stmt2 = """SELECT 1 as flag
                    FROM Action
                    LEFT JOIN ActionType ON ActionType.id = actionType_id
                    WHERE ActionType.flatCode IN ('expertiseDirection', 'expertiseDirection2018') AND `Action`.event_id =%d AND Action.deleted = 0
                     """%( eventId)
        
        stmt = """SELECT ActionProperty_String.value as code, 1 as flag 
                FROM `ActionProperty_String`
                LEFT JOIN `ActionProperty` On `ActionProperty_String`.id = `ActionProperty`.`id`
                LEFT JOIN Action ON Action.id = ActionProperty.action_id
                LEFT JOIN ActionPropertyType ON ActionPropertyType.id = ActionProperty.type_id
                WHERE Action.deleted = 0 AND `Action`.event_id =%d 
                AND ActionPropertyType.`descr` LIKE 'EIR'"""%( eventId)
                
        stmt3 = """select 1 as flag from Action
                        left join ActionType on ActionType.id=Action.actionType_id
                        left join ActionPropertyType on ActionPropertyType.actionType_id=ActionType.id
                        left join ActionProperty on ActionProperty.action_id=Action.id and ActionPropertyType.id = ActionProperty.type_id
                        left join ActionProperty_String on ActionProperty_String.id=ActionProperty.id
                    where ActionType.flatCode in ('consultationDirection', 'inspectionDirection',
                            'consultationDirection2018', 'researchDirection2018',
                            'inspectionDirection2018', 'consultationDirection_tm') and ActionType.id=Action.actionType_id and
                                ActionPropertyType.actionType_id=ActionType.id and
                                ActionPropertyType.descr like '%s' AND Action.status!=3
                            and ActionProperty.action_id=Action.id
                    and ActionProperty_String.value='%s' and Action.event_id = %s """%(str, str1, eventId)
                
        query = db.query(stmt)
        query1 = db.query(stmt1)
        query2 = db.query(stmt2)
        query3 = db.query(stmt3)
        code = None
        flag = 0
        flag2= 0
        flag3= 0
        if query.next():
           code = forceString(query.record().value('code'))
        if query1.next():
           flag = forceInt(query1.record().value('flag'))
        if query2.next():
           flag2 = forceInt(query2.record().value('flag'))
        if query3.next():
           flag3 = forceInt(query3.record().value('flag'))
        return code, flag, flag2, flag3
    
    @staticmethod
    def getOperationCase(self, eventId):
        stmt = """SELECT `ActionProperty_String`.value as val, rbService.infis as code
                    FROM `ActionProperty_String`
                    LEFT JOIN  ActionProperty ON `ActionProperty_String`.id = ActionProperty.id
                    LEFT JOIN ActionPropertyType ON ActionPropertyType.id =  ActionProperty.type_id
                    LEFT JOIN Action ON Action.id = ActionProperty.action_id
                    LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
                    LEFT JOIN rbService On rbService.id = nomenclativeService_id
                    WHERE ActionPropertyType.descr IN ('isOperativeTogether', 'isOperativeTogetherOne') AND `Action`.event_id =%d AND Action.deleted = 0
                     """%( eventId)
        query = QtGui.qApp.db.query(stmt)
        codeM = []
        if query:
            while query.next():
                record = query.record()
                if forceString(record.value('val')) == u'да':
                    code = forceString(record.value('code'))
                    codeM.append(code)
        return codeM 
    
    @staticmethod
    def getCanses(self, eventId):
        stmt = """SELECT ActionType.code
                    FROM Action
                    LEFT JOIN ActionType ON ActionType.id = actionType_id
                    WHERE ActionType.flatCode IN ('dnv.otk') AND `Action`.event_id =%d AND Action.deleted = 0
                     """%( eventId)
        query = QtGui.qApp.db.query(stmt)
        if query.next():
            return 1 
        return 0  
    
    @staticmethod
    def getDiagnosis(self, eventId, eventPersonId, eventExecPersonId, contractBegDate):
        def getTNMS( recordMain):
            onk = ['STAD', 'ONK_T', 'ONK_N', 'ONK_M']
            TNMS= {}
            translate = {'STAD':'rbTNMphase', 'ONK_T':'rbTumor', 'ONK_N':'rbNodus', 'ONK_M':'rbMetastasis'}
            for x in onk:
                table = QtGui.qApp.db.table(translate[x])
                tableIdentification = QtGui.qApp.db.table(translate[x] + '_Identification')
                tableSystem = QtGui.qApp.db.table('`rbAccountingSystem`')
                table = table.leftJoin(tableIdentification, tableIdentification['master_id'].eq(table['id']))
                table = table.leftJoin(tableSystem, tableSystem['id'].eq(tableIdentification['system_id']))
        #                addCondLike(cond, table['MKB'], MKB)
              #  cond = [ table['MKB'].eq(MKB), table['code'].eq(a)]
                cond = [table['id'].eq(forceRef(recordMain.value(x)))]
                cond.append(QtGui.qApp.db.joinOr([table['endDate'].lt(contractBegDate), table['endDate'].isNull()]))
               # cond.append(tableSystem['code'].eq(translate[s[0:2]][2:]))
                
                stmt = QtGui.qApp.db.selectStmt(table, ['value'], where=cond)
             #   MKB1 = MKB.split('.')[0]
                query = QtGui.qApp.db.query(stmt)
             #   cond.append(table['MKB'].eq(MKB1) )
             #   cond.append(table['code'].eq(a))
            #    stmt1 = QtGui.qApp.db.selectStmt(table, ['value'], where=cond)
            #    query1 = QtGui.qApp.db.query(stmt1)
                if query.next():
                    TNMS[x] =  forceString(query.record().value('value'))
               # elif query1.next():
               #     TNMS[x] =  forceString(query1.record().value('value'))
            return TNMS
 
        def getDiag(eventId, eventPersonId):
           resultMKB = ''
           AccMKB = []
           CompMKB = ''
           PreMKB = ''
           traumaCode = ''
           resultFederalCode = ''
           diagnosisTypeCode = ''
           TNMS = ''
           diseaseCharacter = ''
           diseasePhase = ''
           dispanserStatus =''
           onk ={}
           stmt = """SELECT    Diagnosis.MKB, 
                                Diagnostic.TNMS as TNMS,
                            rbDiagnosticResult.federalCode as resultFederalCode, 
                            rbTraumaType.code traumaCode, 
                            rbDiagnosisType.code as diagnosisTypeCode,
                            rbDiseaseCharacter_Identification.value as diseaseCharacter, 
                            rbDiseasePhases.code as diseasePhase,
                            IF(Diagnostic.cTNMphase_id != '', cTNMphase_id, pTNMphase_id) as STAD,
                            IF(Diagnostic.cTumor_id != '', cTumor_id, pTumor_id) as ONK_T,
                            IF(Diagnostic.cNodus_id != '', cNodus_id, pNodus_id) as ONK_N,
                            IF(Diagnostic.cMetastasis_id != '', cMetastasis_id, pMetastasis_id) as ONK_M,
                            if(`rbDispanser`.code IN (1, 2, 3, 4, 5, 6), 
                                IF(`rbDispanser`.code = 6, 2,     
                                    IF(`rbDispanser`.code iN (3, 5), 6, `rbDispanser`.code)), 0) as dispanserStatus
                FROM `Diagnostic`
                LEFT JOIN `Diagnosis` ON `Diagnosis`.id = `Diagnostic`.diagnosis_id
                LEFT JOIN `rbDiseaseCharacter` ON `rbDiseaseCharacter`.id = `Diagnostic`.character_id
                LEFT JOIN `rbDiseaseCharacter_Identification` ON `rbDiseaseCharacter`.id = `rbDiseaseCharacter_Identification`.master_id 
                            AND (Diagnostic.endDate > rbDiseaseCharacter_Identification.checkDate or 
                                    (Diagnostic.endDate iS NULL AND Diagnostic.setDate > rbDiseaseCharacter_Identification.checkDate))
                LEFT JOIN `rbDiagnosticResult` ON `rbDiagnosticResult`.id = `Diagnostic`.result_id
                LEFT JOIN `rbTraumaType` ON `rbTraumaType`.id = `Diagnostic`.traumaType_id
                LEFT JOIN `rbDiagnosisType` ON `rbDiagnosisType`.id = `Diagnostic`.diagnosisType_id
                LEFT JOIN rbDiseasePhases ON Diagnostic.phase_id = rbDiseasePhases.id
                LEFT JOIN rbTNMphase     as cPhase ON cPhase.id = Diagnostic.cTNMphase_id 
                LEFT JOIN rbDispanser ON rbDispanser.id = Diagnostic.dispanser_id
                LEFT JOIN rbTumor        as cTumor ON cTumor.id = Diagnostic.cTumor_id 
                LEFT JOIN rbNodus        as cNodus  ON cNodus.id = Diagnostic.cNodus_id 
                LEFT JOIN rbMetastasis   as cMetastasis ON cMetastasis.id = Diagnostic.cMetastasis_id 
                LEFT JOIN rbTNMphase     as pPhase ON pPhase.id = Diagnostic.pTNMphase_id 
                LEFT JOIN rbTumor        as pTumor ON pTumor.id = Diagnostic.pTumor_id 
                LEFT JOIN rbNodus        as pNodus ON pNodus.id = Diagnostic.pNodus_id 
                LEFT JOIN rbMetastasis   as pMetastasis ON pMetastasis.id = Diagnostic.pMetastasis_id 
                WHERE `Diagnostic`.event_id = %s and `Diagnostic`.person_id = %s and `Diagnostic`.deleted =0""" % (eventId, eventPersonId)
           query = QtGui.qApp.db.query(stmt)
           if query:
                while query.next():
                    record = query.record()
                    diagnosisTypeCode = forceInt(record.value('diagnosisTypeCode'))
                    if diagnosisTypeCode == 1 or diagnosisTypeCode == 4:
                        resultMKB = forceString(record.value('MKB')).replace(' ', '')
                        resultFederalCode = forceString(record.value('resultFederalCode'))
                        traumaCode = forceInt(record.value('traumaCode'))
                        TNMS = forceString(record.value('TNMS'))
                        onk = getTNMS(record)
                        diseaseCharacter = forceString(record.value('diseaseCharacter'))
                        dispanserStatus = forceString(record.value('dispanserStatus'))
                        diseasePhase = 1 if forceString(record.value('diseasePhase')) == '10' else 0
                    elif diagnosisTypeCode == 2 and resultMKB == '':
                        resultMKB = forceString(record.value('MKB')).replace(' ', '')
                        resultFederalCode = forceString(record.value('resultFederalCode'))
                        traumaCode = forceInt(record.value('traumaCode'))
                        TNMS = forceString(record.value('TNMS'))
                        onk = getTNMS(record)
                        diseaseCharacter = forceString(record.value('diseaseCharacter'))
                        dispanserStatus = forceString(record.value('dispanserStatus'))
                        diseasePhase = 1 if forceString(record.value('diseasePhase')) == '10' and diseasePhase != 1 else 0
                    elif diagnosisTypeCode == 9:
                        AccMKB.append(forceString(record.value('MKB')).replace(' ', ''))
                      #  TNMS = forceString(record.value('TNMS'))
                      #  diseasePhase = 1 if forceString(record.value('diseasePhase')) == '10' and diseasePhase != 1 else 0
                    elif diagnosisTypeCode == 3:
                        CompMKB = forceString(record.value('MKB')).replace(' ', '')
                      #  TNMS = forceString(record.value('TNMS'))
                      #  diseasePhase = 1 if forceString(record.value('diseasePhase')) == '10' and diseasePhase != 1 else 0
                    elif diagnosisTypeCode == 7:
                        PreMKB = forceString(record.value('MKB')).replace(' ', '')
                        if u'isMainDiagnosis' in self.serviceNote:
                            TNMS = forceString(record.value('TNMS'))
                            traumaCode = forceInt(record.value('traumaCode'))
                            diseaseCharacter = forceString(record.value('diseaseCharacter'))
                            dispanserStatus = forceString(record.value('dispanserStatus'))
                            diseasePhase = 1 if forceString(record.value('diseasePhase')) == '10' and diseasePhase != 1 else 0
                            onk = getTNMS(record)
                            if not resultFederalCode:
                               resultFederalCode = forceString(record.value('resultFederalCode'))
                            resultMKB = PreMKB
           if resultMKB:
                return resultMKB.replace(' ', ''), resultFederalCode, traumaCode, AccMKB, CompMKB, PreMKB, TNMS, diseaseCharacter,diseasePhase, onk, dispanserStatus
           else:
               return None, None, None, None, None, None, None, None, None, None, None
        if  eventPersonId: 
            (resultMKB,  resultFederalCode, traumaCode, AccMKB, 
             CompMKB, PreMKB, TNMS, diseaseCharacter,diseasePhase, onk, dispanserStatus) = getDiag(eventId, eventPersonId)
        if not resultMKB and eventExecPersonId:
            (resultMKB,  resultFederalCode, traumaCode, AccMKB, 
             CompMKB, PreMKB, TNMS, diseaseCharacter,
             diseasePhase, onk, dispanserStatus) = getDiag(eventId, eventExecPersonId)
        if resultMKB:
            return resultMKB,  resultFederalCode, traumaCode, AccMKB, CompMKB, PreMKB, TNMS, diseaseCharacter,diseasePhase, onk, dispanserStatus
        else:
           return None, None, None, None, None, None, None, None, None, None, None
    
    @staticmethod
    def writeOncology1(self, eventId, tmns, tnms1, schema, flag, onk = {}):
        stmt = """SELECT ActionType.flatCode as flatCode, ActionPropertyType.descr as descr, ActionPropertyType.shortName as name, ActionProperty.id,  
                        ActionProperty_Double.value as v1, 
                        ActionProperty_String.value as v2, 
                        ActionProperty_Date.value as v3,
                        ActionProperty_Integer.value as v4,
                        Action.ID AS actionId
                        FROM Action 
                        LEFT JOIn ActionProperty ON ActionProperty.action_id = Action.id 
                        LEFT JOIN ActionPropertyType ON ActionPropertyType.id = ActionProperty.type_id 
                        LEFT JOIN ActionType ON ActionType.id = Action.actionType_id 
                        LEFT JOIN ActionProperty_Double ON ActionProperty_Double.id = ActionProperty.id
                        LEFT JOIN ActionProperty_Integer ON ActionProperty_Integer.id = ActionProperty.id
                        LEFT JOIN ActionProperty_String ON ActionProperty_String.id = ActionProperty.id
                        LEFT JOIN ActionProperty_Date ON ActionProperty_Date.id = ActionProperty.id
                        WHERE ActionProperty.deleted =0 AND Action.status != 3
                        AND flatCode IN ('ControlListOnko', 'Gistologia', 'Immunohistochemistry') 
                        and Action.event_id = %d""" %eventId
                        
        stmt1 = """SELECT 
                    Action.begDate as dateInj
                    , rbNomenclature_Identification.value as code
                    , Action.id as actionId
                    FROM Action
                    LEFT JOIn ActionProperty ON ActionProperty.action_id = Action.id 
                    LEFT JOIN ActionPropertyType ON ActionPropertyType.id = ActionProperty.type_id 
                    LEFT JOIN ActionProperty_rbNomenclature ON ActionProperty_rbNomenclature.id = ActionProperty.id
                    LEFT JOIN rbNomenclature ON ActionProperty_rbNomenclature.value = rbNomenclature.id
                    LEFT JOIN rbNomenclature_Identification ON rbNomenclature_Identification.master_id = rbNomenclature.id
                    LEFT JOIN rbAccountingSystem ON rbNomenclature_Identification.system_id = rbAccountingSystem.id
                    LEFT JOIN ActionType ON ActionType.id = Action.actionType_id 
                    WHERE ActionType.isNomenclatureExpense = 1 AND Action.note = '1'  AND
                    Action.status != 3 AND ActionProperty.deleted =0 AND Action.deleted =0
                    AND rbAccountingSystem.code = 'N020' 
                    AND Action.begDate > rbNomenclature_Identification.checkDate and Action.event_id = %d""" %eventId

        query = QtGui.qApp.db.query(stmt)
        query1= QtGui.qApp.db.query(stmt1)
        mass= {}
        mass['B_DIAG'] = {}
        mass['B_PROT'] = {}
        mass['ONK_USL'] = {}
        if flag == 1:
            order = [ 'ONK_USL']
        else:
            order = ['DS1_T', 'STAD', 'ONK_T', 'ONK_N', 'ONK_M', 'MTSTZ', 'SOD', 'K_FR', 'WEI', 'HEI', 'BSA', 'B_DIAG', 'B_PROT', 'ONK_USL']
        order2 = ['DIAG_DATE','DIAG_TIP', 'DIAG_CODE', 'DIAG_RSLT', 'REC_RSLT','PROT', 'D_PROT',  'USL_TIP', 'HIR_TIP', 'LEK_TIP_L', 'LEK_TIP_V', 'LEK_PR','PPTR','LUCH_TIP']
        translate1= { 'typeUsl':'USL_TIP', 'type1':'HIR_TIP', 'Ltype2':'LEK_TIP_L', 'Ztype2':'LEK_TIP_V', 'type3':'LUCH_TIP', 'PPTR':'PPTR' }
        actionId= None
        while query.next(): 
            diagrslt = None
            flatCode = (forceString(query.record().value('flatCode')))
            name = forceString(query.record().value('name'))
            
            type2 = forceString(query.record().value('v2')).split('.')[0] if forceString(query.record().value('v2')) != '' and forceString(query.record().value('v2')) != ' ' else ''
            type1 =forceDouble(query.record().value('v1')) if forceInt(query.record().value('v1')) > 0 else ''
            type4 =forceString(query.record().value('v4')) if forceInt(query.record().value('v4')) > 0 else ''
            descr = forceString(query.record().value('descr'))
            actionId = forceString(query.record().value('actionId'))
            date = (forceDate(query.record().value('v3'))).toString(Qt.ISODate)
            if  flatCode == u'ControlListOnko':
                if (name == u'povod' and forceString(query.record().value('v2')) != ''):
                    mass['DS1_T'] =  type2

                  #  mass['MTSTZ'] =  '1'
                elif name == u'sumOZ' and type1 != '':
                    mass['SOD'] =  type1
                elif name in translate1.keys() and type2 != '' and type2 != ' ':
                    if actionId not in mass['ONK_USL'].keys():
                        mass['ONK_USL'][actionId]= {}
                    mass['ONK_USL'][actionId][translate1[name]] = type2
                elif name == u'OnkPrOt' and date != '':
                    mass['B_PROT'][actionId]  = { 'PROT':descr,  
                                                 'D_PROT':date}
                elif (name == u'K_FR' or name == u'HEI')and  type4 != '':
                    mass[name] = type4
                    
                elif name in order and  type1 != '':
                    mass[name] = type1

            elif  flatCode == u'Gistologia' or u'Immunohistochemistry':

                if actionId not in mass['B_DIAG'].keys():
                    mass['B_DIAG'][actionId] = {} 
                    mass['B_DIAG'][actionId]['DIAG'] = {} 
                mass['B_DIAG'][actionId]['DIAG_TIP'] = '1' if flatCode == u'Gistologia' else '2'
                if name == u'DIAG_DATE' and date != '': 
                    mass['B_DIAG'][actionId]['DIAG_DATE'] = forceDate(query.record().value('v3')).toString(Qt.ISODate) 
                if name == u'REC_RSLT' and type2 != '':
                    mass['B_DIAG'][actionId]['REC_RSLT'] = type2
                if type2 != '' and type2 != ' ' and descr != '':
                   mass['B_DIAG'][actionId]['DIAG'][type2] = descr
        massLek = {}

        while query1.next():    
            massNomenclature = {}
            if forceString(query1.record().value('code')) not in massLek.keys():
                massNomenclature['REGNUM'] =  forceString(query1.record().value('code'))
                massNomenclature['DATE_INJ'] = []
                massNomenclature['DATE_INJ'].append(forceDate(query1.record().value('dateInj')).toString(Qt.ISODate) )
                massLek[forceString(query1.record().value('code'))]= massNomenclature
            else:
                massLek[forceString(query1.record().value('code'))]['DATE_INJ'].append(forceDate(query1.record().value('dateInj')).toString(Qt.ISODate) ) 
            
        translate= {'S':'STAD', 'T':'ONK_T', 'N':'ONK_N', 'M':'ONK_M'} #{'STAD':'S', 'ONK_T':'T', 'ONK_N':'N', 'ONK_M':'M'} # {'cS':'STAD', 'cT':'ONK_T', 'cN':'ONK_N', 'cM':'ONK_M'} #{'STAD':'S', 'ONK_T':'T', 'ONK_N':'N', 'ONK_M':'M'} #'S':'STAD', 'T':'ONK_T', 'N':'ONK_N', 'M':'ONK_M'
        if mass != {'B_PROT': {}, 'ONK_USL': {}, 'B_DIAG': {}}:
            if flag == 0: 
                self.writeStartElement('ONK_SL')
            if tnms1:
                for s in tnms1.split(' '):
                    if s[1:2] in translate.keys() and (s[2:]!='x' and  s[2:]!='0'):
                        if s[1:2] == 'M' and 'DS1_T' in mass:
                            if int(mass['DS1_T'])  in [1,2]:
                                mass['MTSTZ'] = '1'
        #    for s in tmns.split(' '):
        #        if s[1:2] in translate.keys():
        #            trans[translate[s[1:2]]] = s[2:]
            for el in order:
             #   if trans != {}:
              #      if onk == None:
                    #    pass
                #    print onk
                    if el in onk.keys():
                         self.writeTextElement(el, onk[el])
                  #      elif el in translate.values() and el in trans.keys(): #['STAD', 'ONK_T', 'ONK_N', 'ONK_M']:
                  #              self.writeTextElement(el, trans[el])
                    elif el in  mass.keys():
                        if el in ['B_PROT', 'ONK_USL']:
                            for re in mass[el]:
                              #  for de in mass[el][re]:
                                    self.writeStartElement(el)
                                    for element in order2:
                                        if element == 'LEK_PR' and massLek !=[] and el == 'ONK_USL':
                                            for le in massLek.values():  
                                                self.writeStartElement(element)
                                                self.writeTextElement('REGNUM', le['REGNUM'])
                                                if schema != []:
                                                    self.writeTextElement('CODE_SH', schema[0])
                                                    for dt in le['DATE_INJ']:
                                                        self.writeTextElement('DATE_INJ', dt)
                                                self.writeEndElement() #LEK_PR 
    
                                        elif element in mass[el][re].keys():
                                            self.writeTextElement(element, mass[el][re][element])
                                    self.writeEndElement() #
                        elif el in ['B_DIAG']:
                            for re in mass[el]:
                                
                                for element in  mass[el][re]:
                                    if element == 'DIAG':
                                        if 'DIAG' in  mass[el][re]:
                                            for diag, res in mass[el][re][element].items():
                                                self.writeStartElement(el)
                                                if 'DIAG_DATE' in mass[el][re].keys():
                                                    self.writeTextElement('DIAG_DATE', mass[el][re]['DIAG_DATE'])
                                                if 'DIAG_TIP' in mass[el][re].keys():
                                                    self.writeTextElement('DIAG_TIP', mass[el][re]['DIAG_TIP'])
                                                self.writeTextElement('DIAG_CODE', res)
                                                self.writeTextElement('DIAG_RSLT', diag)
                                                if 'REC_RSLT' in mass[el][re].keys():
                                                    self.writeTextElement('REC_RSLT', mass[el][re]['REC_RSLT'])
                                                self.writeEndElement() #
                                  #  else:
                                  #      self.writeTextElement(element, mass[el][re][element])
                              #  self.writeEndElement() #
                            
                            
                        elif el in mass.keys():
                            self.writeTextElement(el, forceString(mass[el]))
            if flag == 0:
                self.writeEndElement() #ONK_SL  
                
    @staticmethod
    def getOss(self, eventId, type):
        stmt = """SELECT ActionType.code
                    FROM Action
                    LEFT JOIN ActionType ON ActionType.id = actionType_id
                    WHERE ActionType.flatCode IN (%s) AND `Action`.event_id =%d AND Action.deleted = 0
                     """%( type, eventId)
        query = QtGui.qApp.db.query(stmt)
        codeM = []
        if query:
            while query.next():
                record = query.record()
                code = forceString(record.value('code'))
                codeM.append(code)
        return codeM   
    
    @staticmethod
    def getOss(self, eventId, type):
        stmt = """SELECT ActionType.code
                    FROM Action
                    LEFT JOIN ActionType ON ActionType.id = actionType_id
                    WHERE ActionType.flatCode IN (%s) AND `Action`.event_id =%d AND Action.deleted = 0
                     """%( type, eventId)
        query = QtGui.qApp.db.query(stmt)
        codeM = []
        if query:
            while query.next():
                record = query.record()
                code = forceString(record.value('code'))
                codeM.append(code)
        return codeM   
    
    
    @staticmethod
    def getBenefitsType(self, clientId):
        if not clientId:
                        QtGui.QMessageBox.warning( self.parent,
                                       u'Внимание!',
                                       u'Для экспорта счета необходимо снять подверждение оплаты',
                                       QtGui.QMessageBox.Close)
                        return
        else:
            stmt = """SELECT rbSocStatusType.code as code
                            FROM `ClientSocStatus`
                            LEFT JOIN rbSocStatusType ON rbSocStatusType.id = `ClientSocStatus`.`socStatusType_id`
                            WHERE `client_id` =  %s""" % clientId
            query = QtGui.qApp.db.query(stmt)
            codeM = []
            if query:
                
                while query.next():
                    codeR = 0
                    record = query.record()
                    code = forceString(record.value('code'))
                    if code == u'010' or code == u'011':
                        codeR = 1
                    elif code == u'050':
                        codeR = 2
                    elif code == u'140':
                         codeR = 3
                    elif code == u'1501' or code == u'1502':
                         codeR = 4
                    if codeR > 0:
                        codeM.append(codeR)
            return codeM    

    @staticmethod
    def getHelpForm(db, eventId, order):
        helpForm = 0
        if order in ('2'):
            helpForm = 1
        elif order == '6':
            helpForm = 2
        else:
            helpForm = 3
        stmt = """SELECT rbMedicalAidKind.code as code FROM `Event`
                LEFT JOIN `EventType` On `EventType`.id = `Event`.`eventType_id`
                LEFT JOIN rbMedicalAidKind ON rbMedicalAidKind.id = EventType.medicalAidKind_id
                WHERE `Event`.id =%d"""%( eventId)
        query = db.query(stmt)
        if query.next():
            if forceString(query.record().value('code')) == '12':
                helpForm = 2
        return helpForm


    @staticmethod
    def getLatestActionMove(db, masterId, eventId):
        u'Возвращает самое последнее движение'
        stmt = """SELECT `Account_Item`.`service_id` AS serviceId,
                         `Account_Item`.`id` AS Id,  rbService.code AS code
                FROM
                    `Account_Item`
                    LEFT JOIN `Action` ON `Account_Item`.`action_id` = `Action`.`id`
                    LEFT JOIN `ActionType` ON `ActionType`.`id` = `Action`.`actionType_id`
                    LEFT JOIN rbService ON Account_Item.`service_id` = rbService.id
                    WHERE Master_id = %d AND `Account_Item`.`event_id` = %d
                    AND `ActionType`.`flatCode` = 'moving'
                ORDER BY `Action`.`begDate` DESC
                LIMIT 1
                """%(masterId, eventId)
        query = db.query(stmt)
        if query.next():
                if forceString(query.record().value('code')) == '5.20' or forceString(query.record().value('code')) == '5.19':
                    return None, None
                else:
                    return (forceInt(query.record().value('serviceId')),
                            forceInt(query.record().value('Id')))
        else:
            return None, None


    @staticmethod
    def getSpecialCaseCode(db, clientId, contractBegDate = None, socStatusClassCode = None):
        if not socStatusClassCode:
            socStatusClassCode = 10
        stmStr = "and (ClientSocStatus.endDate >= '%s' or ClientSocStatus.endDate IS NULL)"% contractBegDate.toString(Qt.ISODate) if contractBegDate else ''

        stmt = """SELECT rbSocStatusType.code as code, rbSocStatusType.regionalCode as regionalCode, ClientSocStatus.endDate
                    FROM `ClientSocStatus`
                    LEFT JOIN rbSocStatusType ON rbSocStatusType.id = `ClientSocStatus`.`socStatusType_id`
                    LEFT JOIN rbSocStatusClass ON rbSocStatusClass.id = `ClientSocStatus`.`socStatusClass_id`
                     WHERE `client_id` = %d and rbSocStatusClass.code = %s
                     and ClientSocStatus.deleted =0 %s
                     """%(clientId, socStatusClassCode, stmStr)
        query = db.query(stmt)
        code = []
        while query.next():
            if socStatusClassCode == 10:
                code.append(forceString(query.record().value('code')))
            else:
                code.append(forceString(query.record().value('regionalCode')))
        return code
        
    @staticmethod
    def getIncompleteReason(db, eventId):
        stmt = """SELECT rbMesSpecification.regionalCode as number
                    FROM `Event` 
                    LEFT JOIN rbMesSpecification ON rbMesSpecification.id = mesSpecification_id 
                     
                    WHERE `Event`.`id` = %s AND regionalCode != ''
                     """%(eventId)
        query = db.query(stmt)
        if query.next():
            return forceString(query.record().value('number'))
        stmt = """SELECT value as code
                    FROM `ActionProperty_String`
                    LEFT JOIN ActionProperty ON ActionProperty.id = `ActionProperty_String`.id
                    LEFT JOIN ActionPropertyType ON ActionPropertyType.id = type_id
                    LEFT JOIN ActionType On ActionType.id = ActionPropertyType.actionType_id
                    LEFT JOIN Action ON Action.id = ActionProperty.action_id
                      WHERE Action.deleted =0  AND flatCode = 'NPL' AND event_id = %s AND ActionPropertyType.descr = 'NPL'
                  """
        query = db.query(stmt %  eventId)
        code = None
        if query.next():
            record = query.record()
            code = forceString(record.value('code')).split(".")[0]
        return code
       # else:
        #    return 0
        
    @staticmethod
    def getAccountNumber(db, accountId):
        str = '''IF((rbService.note LIKE "%isSelfCase%"), COUNT(DISTINCT(event_id))+COUNT(rbService.note LIKE "%isSelfCase%"), COUNT(DISTINCT(event_id)) )'''
        stmt = """SELECT SUM(IF(%s, 0, 1 )) as number
                    FROM `Account_Item` 
                    LEFT JOIN rbService ON rbService.id = service_id 
                    WHERE `master_id` = %s
                     """%(str, accountId)
        query = db.query(stmt)
        if query.next():
            return forceString(query.record().value('number'))
        else:
            return 0
        
    @staticmethod    
    def getTransferName(db, eventId):
        stmt = """SELECT `ActionProperty_String`.value AS str
                            FROM  `ActionProperty_String`
                            lEFT JOIN ActionProperty ON ActionProperty.id = `ActionProperty_String`.id
                            LEFT JOIN ActionPropertyType ON ActionPropertyType.id = type_id
                            LEFT JOIN `Action` ON    ActionProperty.action_id =  Action.id
                            LEFT JOIN  `ActionType` ON `Action`.`ActionType_id` =  `ActionType`.`id` 
                            WHERE  `ActionType`.`flatCode` IN ("received", 'moving') AND ActionPropertyType.descr = "perevod"
                            AND  `Action`.`event_id` =%d
                            AND Action.deleted !=1""" %(eventId)
        query =  db.query(stmt)
        if query.next():
            return (forceString(query.record().value('str'))).split('.')[0]
        else:
            return None
    
    @staticmethod
    def getLatestDateOfVisitOrAction(db, masterId, eventId):
        u'Возвращает дату последнего джвижения'
        stmtAction = """SELECT `Action`.`endDate` as EndDate
                    FROM  `Account_Item`
                    LEFT JOIN `Action` ON `Account_Item`.`action_id` = `Action`.`id`
                    LEFT JOIN `ActionType` ON `ActionType`.`id` = `Action`.`actionType_id`
                    WHERE Master_id = %d AND `Account_Item`.`event_id` = %d
                    AND `ActionType`.`flatCode` = 'moving'
               ORDER BY `Action`.`begDate` DESC
                """%(masterId, eventId)

        u'Возвращает дату последнего визита'
        stmtVisit = """ SELECT  `Visit`.`date` AS EndDate
                    FROM  `Account_Item`
                    LEFT JOIN  `Visit` ON  `Account_Item`.`visit_id` =  `Visit`.`id`
                    WHERE Master_id = %d AND `Account_Item`.`event_id` = %d
                    ORDER BY  `Visit`.`date` DESC
                    """%(masterId, eventId)
        query = db.query(stmtAction)
        if query.next():
            return (forceDate(query.record().value('EndDate')))
        else:
            queryH = db.query(stmtVisit)
            if queryH.next():
                return (forceDate(queryH.record().value('EndDate')))
            else:
                return None
    

    @staticmethod
    def getVisit(db, masterId, eventId, serviceId):
        stmt = """SELECT  `Visit`.`id` AS visitId
                    FROM  `Account_Item`
                    LEFT JOIN  `Visit` ON  `Account_Item`.`visit_id` =  `Visit`.`id`
                    WHERE Master_id = %d AND `Account_Item`.`event_id` = %d AND Visit.service_id=%d
                    ORDER BY  `Visit`.`visitType_id` DESC
                    """%(masterId, eventId, serviceId)
        query = db.query(stmt)
        if query.next():
            return (forceRef(query.record().value('visitId')))
        else:
            return None

#    @staticmethod
#    def getVisit(db, eventId, serviceId):
#        stmt = """SELECT  `Visit`.`id` AS visitId
#                    FROM  `Visit`
#                    WHERE `event_id` = %d AND Visit.service_id!=%d
#                    ORDER BY  `Visit`.`visitType_id` DESC
#                    """%( eventId, serviceId)
#        query = db.query(stmt)
#        visits = []
#        while query.next():
#            visits.append(forceRef(query.record().value('visitId')))
#        return (visits)

    @staticmethod
    def getDatesForConsultVisit(db, visitId):
        stmt = """SELECT  `date` as dateVisit
                    FROM  `Visit`
                    WHERE  `id` =%d"""%(visitId)
        query = db.query(stmt)
        if query.next():
            return (forceDate(query.record().value('dateVisit')))
        else:
            return None


    @staticmethod
    def getPersonRegionalCodeForConsultVisit(db, visitId):
        stmt = """SELECT  CONCAT_WS('-',SUBSTRING(Person.`SNILS`, 1, 3), SUBSTRING(Person.`SNILS`, 4, 3), SUBSTRING(Person.`SNILS`, 7, 3), SUBSTRING(Person.`SNILS`, 10, 2))  as regionalCode
                    FROM  `Person`
                    LEFT JOIN  `Visit` ON  `Person`.`id` =  `Visit`.`person_id`
                    WHERE  `Visit`.`id` =%d"""%(visitId)
        query = db.query(stmt)
        if query.next():
            return (forceString(query.record().value('regionalCode')))
        else:
            return None


    @staticmethod
    def doubleToStrRounded(f):
        slen = len('%.*f' % (2, f))
        if int(str(f)[-1]) >= 5:
            return float(str(f + 0.006)[:slen])
        else: 
            return round(f, 2)
        
    @staticmethod
    def rd(x,y=0):
        m = int('1'+'0'*y) # multiplier - how many positions to the right
        q = x*m # shift to the right by multiplier
        c = int(q) # new number
        i = int( (q-c)*10 ) # indicator number on the right
        if i >= 5:
            c += 1
        return c/m


    @staticmethod
    def doubleToStrCut(f):
        slen = len('%.*f' % (2, f))
        return float(str(f)[:slen])


    #WFT? есть же db.translate('Organisation', 'infisCode', miacCode, 'notes')
    @staticmethod
    def getMobileModule(db, miacCode):
        stmt = """SELECT  `notes` as MobileModule
                  FROM  `Organisation`
                  WHERE  `infisCode` =  %d
                  """%(miacCode)
        query = db.query(stmt)
        if query.next():
            return (forceString(query.record().value('MobileModule')))
        else:
            return None
        
    @staticmethod
    def isOncology(db, eventId):
        stmt = """SELECT IF(ActionProperty_String.value = '%s', 1, 0) as v2
                    FROM Action
                        LEFT JOIn ActionProperty ON ActionProperty.action_id = Action.id 
                        LEFT JOIN ActionPropertyType ON ActionPropertyType.id = ActionProperty.type_id 
                        LEFT JOIN ActionType ON ActionType.id = Action.actionType_id 
                        LEFT JOIN ActionProperty_String ON ActionProperty_String.id = ActionProperty.id
                    WHERE (`flatCode` LIKE 'inspectionDirection' or 
                            `flatCode` LIKE 'inspectionDirection2018' or
                            `flatCode` LIKE 'consultationDirection' or 
                            `flatCode` LIKE 'consultationDirection2018' or 
                            `flatCode` LIKE 'consultationDirection_tm') 
                            and Action.event_id = %d
                             AND ActionPropertyType.descr like 'DS_ONK'
                             AND Action.deleted = 0
                    """%(u'да',eventId)
        query = db.query(stmt)
        if query.next():
            return  forceInt(query.record().value('v2'))
        else:
            return 0

    @staticmethod
    def getRefernceType(db, eventId, eventMedicalAidProfileCode):
        stmt = """SELECT Action.id, status FROM Action
                    LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
                    WHERE flatCode = 'fz108' and Action.event_id = %d
                    """%(eventId)
        query = db.query(stmt)
        if query.next():
            code = 1
            if eventMedicalAidProfileCode == '6' or eventMedicalAidProfileCode == '8':
                code = 3
            if forceString(query.record().value('status')) == '3':
                code = 2
            return code
        else:
            return None
        
    
    
    @staticmethod
    def getConnection(db, clientId):
        stmt = """SELECT lastName, firstName, patrName, birthDate, sex
                    FROM Client
                    WHERE Client.id = (
                    SELECT  `ClientRelation`.`client_id`
                    FROM  `ClientRelation`
                    WHERE  `relative_id` =%d and ClientRelation.deleted = 0
                    LIMIT 1 )
                  """%(clientId)
        query = db.query(stmt)
        if query.next():
            return ((forceString(query.record().value('lastName'))) ,
                    (forceString(query.record().value('firstName'))),
                    (forceString(query.record().value('patrName'))),
                    (forceDate(query.record().value('birthDate'))),
                    (forceString(query.record().value('sex'))))
        else:
            return None, None, None, None, None


    @staticmethod
    def diagnosisHasSpecification(db, mkb):
        stmt = """ SELECT LEFT(`DiagID`, 3) FROM `MKB`
        WHERE LENGTH(`DiagID`) >3 AND LEFT(`DiagID`, 3) = '%s' """%(mkb)
        query = db.query(stmt)
        if query.next():
            return True
        else:
            return False


    @staticmethod
    def changeOkato(okato):
        i=3
        g=len(okato)
        okatoH =okato
        while okatoH[-3:] == '000' and i<7:
            okatoH =okato[0:g-i]
            i=i+3
        else:
            return okatoH


    @staticmethod
    def isOverHospitalLimit(db, eventId):
        stmt = """SELECT `Contract_Tariff`.`frag2Start` as `limit`, `Contract_Tariff`.`amount` as `contractTariffAmount`, `Account_Item`.`amount` as accountAmount
                FROM  `Account_Item`
                LEFT JOIN `Contract_Tariff` ON `Contract_Tariff`.`id` =  `Account_Item`.`tariff_id`
                LEFT JOIN `Action` ON `Action`.`id` =  `Account_Item`.`action_id`
                LEFT JOIN  `ActionType` ON  `Action`.`actionType_id` =  `ActionType`.`id`
                WHERE  `Account_Item`.`event_id` =%d
                AND Contract_Tariff.amount <  `Account_Item`.`amount`
                AND (`Account_Item`.`amount` - Contract_Tariff.frag2Start) !=  `Account_Item`.`amount`
                """%(eventId)
        query = db.query(stmt)
        difference = 0
        amount = 0
        limit = 0
        contractTariffAmount = 0
        accountAmount = 0
        if query.next():
            limit = (forceInt(query.record().value('limit')))
        stmt1 = """    SELECT SUM(`Action`.AmoUnt) as sumAmount
                        FROM  `Action`
                        LEFT JOIN  `ActionType` ON  `Action`.`actionType_id` =  `ActionType`.`id`
                        WHERE Action.deleted =0 AND `Action`.event_id =%d AND `ActionType`.`flatCode` =  'moving'"""%(eventId)
        query = db.query(stmt1)
        if query.next():
            amount = (forceInt(query.record().value('sumAmount')))
        if limit < amount and difference != amount:
            difference =  (amount - limit)
        return difference


    @staticmethod
    def getExtr(self, eventId):
        stmt = """SELECT IF(`ActionProperty_String`.`value` LIKE %s,1,2) as isExtr
                        FROM `ActionProperty_String`
                        WHERE `id` IN (SELECT `ActionProperty`.`id`
                                        FROM  `ActionProperty`
                                        LEFT JOIN `ActionPropertyType` ON `ActionPropertyType`.`id` = `ActionProperty`.`type_id`
                                        -- LEFT JOIN ActionType ON ActionType.id = `ActionPropertyType`.actionType_id
                                        LEFT JOIN `Action` ON `ActionProperty`.`action_id` = `Action`.id
                                        WHERE   `ActionPropertyType`.actionType_id =4076
                                        AND  `Action`.event_id =%d
                                        AND Action.deletd= 0
                                        AND `ActionPropertyType`.`name` LIKE %s)"""%(u"""'плановым показаниям'""", eventId, u"""'Доставлен по'""")
        query =  QtGui.qApp.db.query(stmt)
        if query.next():
            return (forceString(query.record().value('Extr')))
        else:
            return None


    @staticmethod
    def getDiagnosForAction(db, actionId):
        stmt = """SELECT  `MKB` as ds
                    FROM  `Action`
                    WHERE  `id` = %s"""%(actionId)
        query = db.query(stmt)
        if query.next():
            return  (forceString(query.record().value('ds')))
        else:
            return None


    @staticmethod
    def isRegionalAdditionalPay(db, serviceCode):
        regionalAdditionalCode = ['3.14.1',
                                  '3.4.1',
                                  '4.3.1',
                                  '2.13.1',
                                  '1.4.1',
                                  '3.15.1',
                                  '1.3.1',
                                  '1.4.1',
                                  '1.4.1',
                                  '3.13.1',
                                  '2.10.1',
                                  '2.10.3',
                                  '2.23.2',
                                  '2.13.1',
                                  '2.3.1',
                                  '3.15.1']
        return True if serviceCode in regionalAdditionalCode else False


    @staticmethod
    def isNotUniqueEmergencyDayVisit(db, accountId, clientId, endDate):
        stmt = """SELECT MAX(Event.id) as eventId
                    FROM `Account_Item`
                    LEFT JOIN Event ON Event.id = `Account_Item`.`event_id`
                    WHERE `Account_Item`.master_id = %s AND Event.client_Id = %s  AND LEFT(Event.execDate,10) LIKE '%s'
                   --  GROUP BY date

                    HAVING COUNT(Event.id) > 1 -- AND MAX(Event.execDate)
                 --   ORDER BY Event.execDate
                --   LIMIT 1
                    """%(accountId, clientId, endDate.toString(Qt.ISODate))
        query = db.query(stmt)
        if query.next():
            return (forceRef(query.record().value('eventId')))
        else:
            return None


    @staticmethod
    def getActionForHealthCentr(db, accountId, eventId):
        stmt = """SELECT action_id  as actionId
                FROM  `Account_Item`
                    WHERE  `event_id` =%s AND master_id=%s"""%(eventId,accountId)
        query = db.query(stmt)
        buffer = []
        while query.next():
          #  print forceRef(query.record().value('actionId'))
            buffer.append(forceRef(query.record().value('actionId')))
        return buffer


    @staticmethod
    def getClientPolicy(db, clientId, eventBegDate, eventSetDate):
        stmt = """SELECT    ClientPolicy.serial AS policySerial,
                            ClientPolicy.number AS policyNumber,
                            rbPolicyKind.regionalCode AS policyKindCode,
                            Insurer.id as insurerId,
                            Insurer.miacCode as insurerMiac,
                            Insurer.OGRN AS insurerOGRN,
                            Insurer.OKATO AS insurerOKATO
                FROM  `ClientPolicy`
                LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
                LEFT JOIN rbPolicyKind ON ClientPolicy.policyKind_id = rbPolicyKind.id
                LEFT JOIN rbPolicyType AS CPT ON CPT.id = ClientPolicy.policyType_id
                WHERE  `client_id` =%s AND
                        ( `endDate` >=  '%s'
                            OR ClientPolicy.endDate IS NULL
                            OR ClientPolicy.endDate =  '0000-00-00')
                        AND  ClientPolicy.`deleted` =0
                        AND  '%s' >= ClientPolicy.begDate
                        AND ClientPolicy.insurer_id IS NOT NULL

                        AND CPT.code IN ('1','2') ORDER BY ClientPolicy.id DESC"""%(clientId, eventSetDate.toString(Qt.ISODate) if (eventSetDate.toString(Qt.ISODate)) else eventBegDate.toString(Qt.ISODate),
                                                                                     eventSetDate.toString(Qt.ISODate) if (eventSetDate.toString(Qt.ISODate)) else eventBegDate.toString(Qt.ISODate))

        query = db.query(stmt)
        policyNumber = None
        policySerial = None 
        policyKindCode = None
        insurerOGRN = None
        insurerOKATO = None
        insurerMiac = None
        insurerName = None
        insurerId = None
        if query.next():
            policyNumber = forceString(query.record().value(u'policyNumber'))[:20]
            policySerial = forceString(query.record().value(u'policySerial'))[:10]
            policyKindCode = forceString(query.record().value('policyKindCode'))[:1]
            insurerOGRN =  forceString(query.record().value('insurerOGRN'))[:15]
            insurerOKATO =  forceString(query.record().value('insurerOKATO'))[:5]
            insurerName = forceString(query.record().value('insurerName'))[:100],
            insurerMiac = forceString(query.record().value('insurerMiac'))[:5]
            insurerId =  forceString(query.record().value('insurerId'))
        return policyNumber, policySerial, policyKindCode, insurerOGRN, insurerOKATO, insurerName, insurerMiac, insurerId
    
    @staticmethod
    def getClientPolicy1(db, clientId, eventBegDate, eventSetDate):
        stmt = """SELECT    ClientPolicy.serial AS policySerial,
                            ClientPolicy.number AS policyNumber,
                            rbPolicyKind.regionalCode AS policyKindCode,
                            Insurer.id as insurerId,
                            Insurer.miacCode as insurerMiac,
                            Insurer.OGRN AS insurerOGRN,
                            Insurer.OKATO AS insurerOKATO
                FROM  `ClientPolicy`
                LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
                LEFT JOIN rbPolicyKind ON ClientPolicy.policyKind_id = rbPolicyKind.id
                LEFT JOIN rbPolicyType AS CPT ON CPT.id = ClientPolicy.policyType_id
                WHERE  `client_id` =%s AND
                        ( `endDate` >=  '%s'
                            OR ClientPolicy.endDate IS NULL
                            OR ClientPolicy.endDate =  '0000-00-00')
                        AND  ClientPolicy.`deleted` =0
                        AND   ClientPolicy.begDate <= '%s'
                        AND ClientPolicy.insurer_id IS NOT NULL
                        AND CPT.code IN ('1','2') ORDER BY ClientPolicy.id DESC"""%(clientId, eventBegDate.toString(Qt.ISODate) if (eventBegDate.toString(Qt.ISODate) ) else eventSetDate.toString(Qt.ISODate), 
                                                                                    eventBegDate.toString(Qt.ISODate) if (eventBegDate.toString(Qt.ISODate) ) else eventSetDate.toString(Qt.ISODate))
        query = db.query(stmt)
   #     print stmt
        policyNumber = None
        policySerial = None 
        policyKindCode = None
        insurerOGRN = None
        insurerOKATO = None
        insurerMiac = None
        insurerName = None
        insurerId = None
        while query.next():
            policyNumber = forceString(query.record().value(u'policyNumber'))[:20]
            policySerial = forceString(query.record().value(u'policySerial'))[:10]
            policyKindCode = forceString(query.record().value('policyKindCode'))[:1]
            insurerOGRN =  forceString(query.record().value('insurerOGRN'))[:15]
            insurerOKATO =  forceString(query.record().value('insurerOKATO'))[:5]
            insurerName = forceString(query.record().value('insurerName'))[:100],
            insurerMiac = forceString(query.record().value('insurerMiac'))[:5]
            insurerId =  forceString(query.record().value('insurerId'))
        return policyNumber, policySerial, policyKindCode, insurerOGRN, insurerOKATO, insurerName, insurerMiac, insurerId

class PriceType:
    basePrice = 0
    federalPrice = 1
    regionalPrice = 2


class SummSingleton(object):
    _instance = None

    summTotal = 0.0
    summCaseTotal = 0
    dictSums = {1: 0.0}
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SummSingleton, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

