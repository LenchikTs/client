# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################


# поддержка получения полиса пациента по протоколу СПб ТФОМС

import uuid
from PyQt4               import QtCore, QtGui
from library.Utils       import *
from IdentService_client import *


class CTF78IdentService:
    def __init__(self, url, login, password):
        self.port = None
        self.url = url
        self.login = login
        self.password = password
        self.smoList = None
        self.geonimNameList = None
        self.geonimTypeList = None
        self.TAreaList = None


    def getPort(self):
        if self.port is None:
            loc = IdentServiceLocator()
            self.port = loc.getIdentPort(self.url)
        return self.port


    def getSmoList(self):
        if self.smoList is None:
            req = getIdSmo()
            req._arg0 = self.login
            req._arg1 = self.password
            resp = self.getPort().getIdSmo(req)
            self.smoList = self.parseList(resp)
        return self.smoList


    def getGeonimNameList(self):
        if self.geonimNameList is None:
            req = getIdGeonimName()
            req._arg0 = self.login
            req._arg1 = self.password
            resp = self.getPort().getIdGeonimName(req)
            self.geonimNameList = self.parseList(resp)
        return self.geonimNameList


    def getGeonimTypeList(self):
        if self.geonimTypeList is None:
            req = getIdGeonimType()
            req._arg0 = self.login
            req._arg1 = self.password
            resp = self.getPort().getIdGeonimType(req)
            self.geonimTypeList = self.parseList(resp)
        return self.geonimTypeList


    def getTAreaList(self):
        if self.TAreaList is None:
            req = getIdTArea()
            req._arg0 = self.login
            req._arg1 = self.password
            resp = self.getPort().getIdTArea(req)
            self.TAreaList = self.parseList(resp)
        return self.TAreaList


    def getPolicy(self, firstName, lastName, patrName, sex, birthDate, snils, policySerial, policyNumber, docSerial, docNumber):
        identTO = ns0.identTO_Def('identTO')
        identTO._idCase = str(uuid.uuid1())
        today = QtCore.QDate.currentDate()
        identTO._dateBegin  = unicode(today.toString(QtCore.Qt.ISODate))
        identTO._surname    = lastName
        identTO._name       = firstName
        identTO._secondName = patrName
        identTO._birthday = unicode(birthDate.toString(QtCore.Qt.ISODate))
        identTO._idTArea      = 0   # fake value
        identTO._idGeonimName = 0   # fake value
        identTO._idGeonimType = 0   # fake value
        identTO._house        = '-' # fake value
        identTO._polisS = policySerial
        identTO._polisN = policyNumber
        identTO._docNumber = docNumber
        req = doIdentification()
        req._arg0 = self.login
        req._arg1 = self.password
        req._arg2 = identTO
        resp = self.getPort().doIdentification(req)
        if resp._return._numTest>0:
            result = smartDict()
            result.hicId, result.hicName = self.getHicId(resp._return._idSmo)
            result.policySerial = resp._return._polisS.decode('utf8')
            result.policyNumber = resp._return._polisN.decode('utf8')
            result.typeCode     = self.getPolicyTypeCode(resp._return._agrType)
            result.kindCode     = None
#            result.begDate      = self.tupleToQDate(resp._return._dateBegin)
#            result.endDate      = self.tupleToQDate(resp._return._dateEnd)
            result.begDate      = QtCore.QDate.fromString(resp._return._dateBegin, QtCore.Qt.ISODate)
            result.endDate      = QtCore.QDate.fromString(resp._return._dateEnd, QtCore.Qt.ISODate)
            return result
        else:
            return None


    def getPolicyAndAttach(self, firstName, lastName, patrName, sex, birthDate, snils, policySerial, policyNumber, docSerial, docNumber):
        policy = self.getPolicy(firstName, lastName, patrName, sex, birthDate, snils, policySerial, policyNumber, docSerial, docNumber)
        return policy, None, None



    @staticmethod
    def parseList(resp):
        result = []
        for items in resp._return:
            code = int(items._item[0])
            name = items._item[1].decode('utf8')
            result.append((code, name))
        return result


    @staticmethod
    def tupleToQDate(t):
        if t and len(t)>=3:
            return QtCore.QDate(t[0], t[1], t[2])


    def getHicId(self, smoCode):
        name = trim(dict(self.getSmoList()).get(smoCode,''))
        if name:
            db = QtGui.qApp.db
            table = db.table('Organisation')
            record = db.getRecordEx(table, 'id', [ table['deleted'].eq(0), table['isInsurer'].eq(1), table['fullName'].eq(name) ])
            if record:
                return forceRef(record.value(0)), name
        return None, name


    def getPolicyTypeCode(self, agrType):
        if agrType == 1: # произв.
            code = '2'
        elif agrType == 2: # терр.
            code = '1'
        else:
            code = None
        return code


