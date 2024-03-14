# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Кое-что, имеющее отношение к XML signature
## Это не специфично для криптопровайдера и MSCAPI,
## но поскольку мы ориентируемся на MSCAPI, пусть лежит здесь.
##
#############################################################################


from oids import (
                    oidHashGostR3411_94,
                    oidHashGostR3411_2012_256,
                    oidHashGostR3411_2012_512,
                    oidSignGostR3410_2001,
                    oidSignGostR3410_2012_256,
                    oidSignGostR3410_2012_512,
                 )

# по https://tools.ietf.org/html/draft-chudov-cryptopro-cpxmldsig-00
uriHashGostR3411_94_v0   = 'http://www.w3.org/2001/04/xmldsig-more#gostr3411'
uriSignGostR3410_2001_v0 = 'http://www.w3.org/2001/04/xmldsig-more#gostr34102001-gostr3411'

# по https://tools.ietf.org/html/draft-chudov-cryptopro-cpxmldsig-01
# этот вариант в "дикой природе" скорее всего не встречается, поэтому я помяну его - но в комментариях
#uriHashGostR3411_94_v1   = 'http://www.w3.org/2006/10/xmldsig-gost#gostr3411'
#uriSignGostR3410_2001_v1 = 'http://www.w3.org/2006/10/xmldsig-gost#gostr34102001-gostr3411'

## по https://tools.ietf.org/html/draft-chudov-cryptopro-cpxmldsig-02
# этот вариант в "дикой природе" скорее всего не встречается, поэтому я помяну его - но в комментариях
#uriHashGostR3411_94_v2   = 'urn:ietf:params:xml:ns:xmlsec-gost:algorithms:gostr3411'
#uriSignGostR3410_2001_v2 = 'urn:ietf:params:xml:ns:xmlsec-gost:algorithms:gostr34102001-gostr3411'

# по https://tools.ietf.org/html/draft-chudov-cryptopro-cpxmldsig-03
uriHashGostR3411_94_v3   = 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr3411'
uriSignGostR3410_2001_v3 = 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102001-gostr3411'

## по https://tools.ietf.org/html/draft-chudov-cryptopro-cpxmldsig-04
#uriHashGostR3411_94_v4   = 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr3411'
#uriSignGostR3410_2001_v4 = 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102001-gostr3411'

## по https://tools.ietf.org/html/draft-chudov-cryptopro-cpxmldsig-05
#uriHashGostR3411_94_v5   = 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr3411'
#uriSignGostR3410_2001_v5 = 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102001-gostr3411'

## по https://tools.ietf.org/html/draft-chudov-cryptopro-cpxmldsig-06
#The identifier for the GOST R 34.11-94 digest algorithm is:
#uriHashGostR3411_94_v6   = 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr3411'
#uriSignGostR3410_2001_v6 = 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102001-gostr3411'

## по https://tools.ietf.org/html/draft-chudov-cryptopro-cpxmldsig-07
#uriHashGostR3411_94_v7   = 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr3411'
#uriSignGostR3410_2001_v7 = 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102001-gostr3411'

# по https://tools.ietf.org/html/draft-chudov-cryptopro-cpxmldsig-09
#uriHashGostR3411_94_v9        = 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr3411'
uriHashGostR3411_2012_256_v9  = 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-256'
uriHashGostR3411_2012_512_v9  = 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34112012-512'
#uriSignGostR3410_2001_v9      = 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102001-gostr3411'
uriSignGostR3410_2012_256_v9  = 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-256'
uriSignGostR3410_2012_512_v9  = 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr34102012-gostr34112012-512'

####

def getHashUriByOid(hashOid):
    if hashOid == oidHashGostR3411_94:
        return uriHashGostR3411_94_v0
    if hashOid == oidHashGostR3411_2012_256:
        return uriHashGostR3411_2012_256_v9
    if hashOid == oidHashGostR3411_2012_512:
        return uriHashGostR3411_2012_512_v9
    raise Exception(u'Невозможно определить URI алгоритма хеширования по OID «%s»' % hashOid)


def getHashOidByUri(hashUri):
    if hashUri in ( uriHashGostR3411_94_v0, uriHashGostR3411_94_v3 ):
        return oidHashGostR3411_94
    if hashUri == uriHashGostR3411_2012_256_v9:
        return oidHashGostR3411_2012_256
    if hashUri == uriHashGostR3411_2012_512_v9:
        return oidHashGostR3411_2012_512
    raise Exception(u'Невозможно определить OID алгоритма хеширования по URI «%s»' % hashUri)


def getSignUriByOid(signOid):
    if signOid == oidSignGostR3410_2001:
        return uriSignGostR3410_2001_v0
    if signOid == oidSignGostR3410_2012_256:
        return uriSignGostR3410_2012_256_v9
    if signOid == oidSignGostR3410_2012_512:
        return uriSignGostR3410_2012_512_v9
    raise Exception(u'Невозможно определить URI алгоритма подписи по OID «%s»' % signOid)


def getSignOidByUri(signUri):
    if signUri in (uriSignGostR3410_2001_v0, uriSignGostR3410_2001_v3):
        return oidSignGostR3410_2001
    if signUri == uriSignGostR3410_2012_256_v9:
        return oidSignGostR3410_2012_256
    if signUri == uriSignGostR3410_2012_512_v9:
        return oidSignGostR3410_2012_512
    raise Exception(u'Невозможно определить OID алгоритма подписи по URI «%s»' % signUri)

