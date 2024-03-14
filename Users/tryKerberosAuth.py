# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2015-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Аутентификация пользователя средствами gssapi/kerberos
## с благодарностью к проектам:
## 1) модуль kerberos для python:
##      https://pypi.python.org/pypi/kerberos
##      http://www.calendarserver.org/
##    - за хорошую стартовую точку,
##    - и за хорошее основание для серверной части
##
## 2) модуль mod_auth_kerb для apache:
##      http://modauthkerb.sourceforge.net/
##      http://sourceforge.net/projects/modauthkerb/
##    - за идеи для серверной части
##
## 3) модуль kerberos-sspi для python:
##      https://pypi.python.org/pypi/kerberos-sspi
##      https://github.com/may-day/kerberos-sspi
##    - за подсказку как это повторить в windows
##
## 4) модуль python-tds для python:
##      https://pypi.python.org/pypi/kerberos-sspi
##      https://github.com/denisenkom/pytds
##    - за код, который позволил отказаться от нескольких dll в пользу ctypes
##
#############################################################################

import os
from PyQt4 import QtGui
from library.database import decorateString
from library.Utils import forceInt, forceString

kerberosAuthPosible = True

try:
    if os.name in ('posix', 'mac'):
        import kerberos as gss
    elif os.name == 'nt':
        import library.auth.tinysspigss as gss
    else:
        kerberosAuthPosible = False
except:
    kerberosAuthPosible = False


# попытаться авторизоваться средствами gssapi/kerberos
# возвращает id пользователя или None
def tryKerberosAuth():
    def callDb(db, stmt, raiseOnEmptyResult=True):
        query = db.query(stmt)
        if query.first():
            return query.record().value(0)
        elif raiseOnEmptyResult:
            raise Exception('Kerberos gss api auth error')
        else:
            return None

    if not kerberosAuthPosible:
        return None

    client = None
    cleanServ = False
    logException = False
    try:
        db = QtGui.qApp.db
        ok = forceString(callDb(db, 'SHOW GLOBAL VARIABLES LIKE \'krb5gss_service\'', False))
        if not ok:
            return None
        service = forceString(callDb(db,'SELECT @@GLOBAL.krb5gss_service AS S'))
        rc = forceInt(callDb(db,'SELECT krb5gss_init() AS S'))
        if rc != 1:
            return None

        cleanServ = True
        # надо сказать, что я подошёл к флагам некритично, просто "срисовав" их из примера.
        flags=gss.GSS_C_CONF_FLAG|gss.GSS_C_INTEG_FLAG|gss.GSS_C_MUTUAL_FLAG|gss.GSS_C_SEQUENCE_FLAG
        errc, client = gss.authGSSClientInit(service, gssflags=flags)
        if errc != 1:
            return None
        logException = True
        cres = sres = gss.AUTH_GSS_CONTINUE
        response = ''
        while sres == gss.AUTH_GSS_CONTINUE or cres == gss.AUTH_GSS_CONTINUE:
            if cres == gss.AUTH_GSS_CONTINUE:
                cres = gss.authGSSClientStep(client, response)
                if cres not in (gss.AUTH_GSS_COMPLETE, gss.AUTH_GSS_CONTINUE):
                    break
                response = gss.authGSSClientResponse(client)

            if sres == gss.AUTH_GSS_CONTINUE:
                sres = forceInt(callDb(db,'SELECT krb5gss_step(%s) AS S' % decorateString(response)))
                if cres not in ( gss.AUTH_GSS_COMPLETE, gss.AUTH_GSS_CONTINUE):
                    break
                response = forceString(callDb(db, 'SELECT krb5gss_response()'))

        if sres == gss.AUTH_GSS_COMPLETE and cres == gss.AUTH_GSS_COMPLETE:
#            userName = forceString(callDb(db, 'SELECT krb5gss_username()'))
            tablePerson = QtGui.qApp.db.table('Person')
            cond = [ 'BINARY login = SUBSTRING_INDEX(krb5gss_username(),\'@\',1)',
                     tablePerson['login'].ne(''),
                     tablePerson['retired'].eq(False),
                     tablePerson['deleted'].eq(False),
                     '(Person.retireDate IS NULL OR Person.retireDate > CURDATE())'

                   ]
            userIdList = db.getIdList(tablePerson, 'id', cond, ['id'])
            if len(userIdList) == 1:
                return userIdList[0]
        return None
    except:
        if logException:
            QtGui.qApp.logCurrentException()

    finally:
        if cleanServ:
            callDb(db, 'SELECT krb5gss_clean()')
        if client:
            gss.authGSSClientClean(client)

