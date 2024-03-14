# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2017-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Handler зашифровывающий и расшифровывающий сообщение по спецификации
##
#############################################################################

import logging
from ZSI.wstools.Namespaces import SOAP, DSIG, ENCRYPTION

from library.MSCAPI.tinyAsn1               import Asn1Base, Asn1OctetString, Asn1Oid, Asn1Sequence
from library.MSCAPI.gostR3410_KeyTransport import GostR3410_KeyTransport
from library.Utils                         import anyToUnicode

from domUtils import getElement, verifyAttributeValue, getDecodedText


class CEncryptionHandler(object):
    ENCRYPTED_DATA_TYPE = 'http://www.w3.org/2001/04/xmlenc#Element'
    ENCRYPTION_ALGORITM = 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gost28147'
    KEY_TRANSPORT       = 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:transport-gost2001'

    def __init__(self, api, userCert=None, receiverCert=None, receiverCertBytes=None):
        assert userCert is not None, u'Должно быть задано userCert'
        assert (receiverCert is not None) != bool(receiverCertBytes), u'Должно быть задано одно и только одно receiverCert или receiverCertBytes'
        assert isinstance(receiverCertBytes, basestring) or receiverCertBytes is None, u'receiverCertBytes должно быть строкой или None'

        self.api = api
        self.userCert          = userCert
        self.receiverCert      = receiverCert
        self.receiverCertBytes = receiverCertBytes


    def sign(self, sw):
        envelope = sw.dom
        envelope, header, body = self._encrypt(envelope)
        sw.dom, sw._header, sw.body = envelope, header, body


    def verify(self, ps):
        decryptedMessage = self._decrypt(ps.body)
        # Да, очень некрасиво.
        # Но я не знаю как "по простому" перечитать документ, когда у нас уже есть готовый ParsedSoap
        ps.__init__(decryptedMessage, ps.readerclass, ps.keepdom, ps.trailers, ps.resolver, ps.envelope)
        return


    #########################################################################
    # for sign ##############################################################
    #########################################################################

    def _getReceiverCertBytes(self):
        if self.receiverCert:
            return self.receiverCert.encoded()
        if self.receiverCertBytes:
            return self.receiverCertBytes
        assert False


    def _getSenderCertBytes(self):
        if self.userCert:
            return self.userCert.encoded()
        assert False


    def _encrypt(self, envelope):
        xmlText = str(envelope)
        logger = logging.getLogger()
        logger.info(u'before encryption: %s' % anyToUnicode(xmlText))

        api = self.api
        receiverCertBytes = self._getReceiverCertBytes()
        senderCertBytes   = self._getSenderCertBytes()

        keyOid = self.userCert.keyOid()
        with api.provider(flags=api.CRYPT_VERIFYCONTEXT,
                          providerType=api.getProviderTypeByKeyOid(keyOid)
                         ) as provider:
            with api.cert(receiverCertBytes) as receiverCert:
                with provider.importPubKeyfromCert(receiverCert) as receiverPubKey:
                    receiverPubKeyBlobBytes = receiverPubKey.export(api.PUBLICKEYBLOB)
                    pkb = api.PublicKeyBlob()
                    pkb.decode(receiverPubKeyBlobBytes)
#                    print 'receiverPubKey',  receiverPubKeyBlobBytes.encode('hex'), len(receiverPubKeyBlobBytes)
#                    print 'pkb.keyAlgId       = ', hex(pkb.keyAlgId)
#                    print 'pkb.bitLen         = ', pkb.bitLen
#                    print 'pkb.paramSetBytes  = ', pkb.paramSetBytes.encode('hex'), len(pkb.paramSetBytes)
#                    print 'pkb.publicKeyBytes = ', pkb.publicKeyBytes.encode('hex'), len(pkb.publicKeyBytes)

                    paramSet = Asn1Base.decode(pkb.paramSetBytes)
                    assert isinstance(paramSet, Asn1Sequence)
                    assert len(paramSet.value) == 2
                    assert isinstance(paramSet.value[0], Asn1Oid)
                    assert isinstance(paramSet.value[1], Asn1Oid)

                    publicKeyParamSet = paramSet.value[0].value
#                    digestParamSet    = paramSet.value[1].value

#                   print 'publicKeyParamSet =', publicKeyParamSet
#                   print 'digestParamSet    =', digestParamSet
                    with provider.genKey(api.CALG_CRYPT_GR28147, api.CRYPT_EXPORTABLE) as sessionKey:
                        with provider.genKey(api.getDhElEphemAlgIdByKeyOid(keyOid), api.CRYPT_EXPORTABLE|api.CRYPT_PREGEN) as ephemeralKey:
# назначение ephemeralKey.setParam(api.KP_HASHOID, digestParamSet ) не понятно.
# на первый взгляд и без этого работает...
#                            ephemeralKey.setParam(api.KP_HASHOID, digestParamSet )
                            ephemeralKey.setParam(api.KP_DHOID, publicKeyParamSet )
                            ephemeralKey.setParam(api.KP_X, None)

#                            ephemeralKeyBlobBytes = ephemeralKey.export(api.PUBLICKEYBLOB)
#                            epkb = api.PublicKeyBlob()
#                            epkb.decode(ephemeralKeyBlobBytes)
                            epkb = ephemeralKey.exportPublicKeyBlob()

                            with provider.importKey(receiverPubKeyBlobBytes, ephemeralKey, flags=api.CRYPT_EXPORTABLE) as exchangeKey:
# этот код «правильный»:
#                                exchangeKey.setParam(api.KP_EXPORT_ALGID, api.getProtectedKeyExportAlgIdByKeyOid(keyOid))
# а этот работает с ФСС:
                                exchangeKey.setParam(api.KP_EXPORT_ALGID, api.CALG_PRO_EXPORT)
                                sb = sessionKey.exportSimpleBlob(expKey=exchangeKey)
#                        print 'sb.keyAlgId          ', hex(sb.keyAlgId)
#                        print 'sb.encryptKeyAlgId   ', hex(sb.encryptKeyAlgId)
#                        print 'sb.sv                ', sb.sv.encode('hex')
#                        print 'sb.encryptedKey      ', sb.encryptedKey.encode('hex')
#                        print 'sb.macKey            ', sb.macKey.encode('hex')
#                        print 'sb.encryptionParamSet', sb.encryptionParamSet.encode('hex')
##                        print 'cons: ',  sb.encode().encode('hex')

                                # Формирование GOSTR3410-KeyTransport
                                eps = Asn1Base.decode(sb.encryptionParamSet)
#                                print repr(eps)
#                                assert isinstance(eps, Asn1Sequence) and len(eps.value) == 1 and isinstance(eps.value[0], Asn1Oid) and eps.value[0].value

                                kt = GostR3410_KeyTransport()
                                kt.sessionEncryptedKey.encryptedKey = sb.encryptedKey
                                kt.sessionEncryptedKey.macKey       = sb.macKey
                                kt.transportParameters.encryptionParamSet = eps.value[0].value

                                kt.transportParameters.ephemeralPublicKey.algorithm.algorithm = api.findOidByAlgId(pkb.keyAlgId)
                                kt.transportParameters.ephemeralPublicKey.algorithm.parameters = Asn1Base.decode(pkb.paramSetBytes).value
                                pkbAsOs = Asn1OctetString(epkb.publicKeyBytes).encode()
                                kt.transportParameters.ephemeralPublicKey.subjectPublicKey = (0, pkbAsOs)

                                kt.transportParameters.ukm = sb.sv
                                ktBytes = bytes(kt.encode())
#                                print 'keyTransport', ktBytes.encode('hex')

                        iv = provider.genRandom(8)
#                        print 'iv:', iv.encode('hex')
                        sessionKey.setParam(api.KP_MODE, api.CRYPT_MODE_CBC)
#                        sessionKey.setParam(api.KP_PADDING, api.ISO10126_PADDING)
                        sessionKey.setParam(api.KP_IV, iv)

                        padLen = ( 8 - len(xmlText) % 8 )
                        pad = chr(padLen)*padLen

#                        print padLen, repr(pad)
                        enc = sessionKey.encrypt2(xmlText + pad, final=False)
#                        enc = sessionKey.encrypt2(doc)
#                        print len(enc)

#                    ciphertext = iv + encKey.encrypt2(srcDoc + pad)
                        ciphertext = iv + enc

#                    print 'ciphertext', ciphertext.encode('hex')
#                file(fnEncDoc,'wb').write( ciphertext )


        envelope.createDocument(SOAP.ENV, 'Envelope')
        envelope.setNamespaceAttribute('soapenv', SOAP.ENV)
#        envelope.setNamespaceAttribute('ds',      DSIG.BASE)
#        envelope.setNamespaceAttribute('xenc',    ENCRYPTION.BASE)

        header = envelope.createAppendElement(SOAP.ENV, 'Header')
        body = envelope.createAppendElement(SOAP.ENV, 'Body')
        encryptedData = body.createAppendElement(ENCRYPTION.BASE, 'EncryptedData')
        encryptedData.setNamespaceAttribute('ds',   DSIG.BASE)
        encryptedData.setNamespaceAttribute('xenc', ENCRYPTION.BASE)
        encryptedData.setAttributeNS(None,  'Type', self.ENCRYPTED_DATA_TYPE)

        encryptionMethod = encryptedData.createAppendElement(ENCRYPTION.BASE, 'EncryptionMethod')
        encryptionMethod.setAttributeNS(None, 'Algorithm',  self.ENCRYPTION_ALGORITM)

        keyInfo = encryptedData.createAppendElement(DSIG.BASE, 'KeyInfo')
        encryptedKey = keyInfo.createAppendElement(ENCRYPTION.BASE, 'EncryptedKey')
        encryptionMethod = encryptedKey.createAppendElement(ENCRYPTION.BASE, 'EncryptionMethod')
        encryptionMethod.setAttributeNS(None, 'Algorithm',  self.KEY_TRANSPORT)

        keyInfo = encryptedKey.createAppendElement(DSIG.BASE, 'KeyInfo')
        x509Data = keyInfo.createAppendElement(DSIG.BASE, 'X509Data')
        x509Certificate = x509Data.createAppendElement(DSIG.BASE, 'X509Certificate')
        x509Certificate.createAppendTextNode( senderCertBytes.encode('base64') )

        cipherData = encryptedKey.createAppendElement(ENCRYPTION.BASE, 'CipherData')
        cipherValue = cipherData.createAppendElement(ENCRYPTION.BASE, 'CipherValue')
        cipherValue.createAppendTextNode( ktBytes.encode('base64') )

        cipherData = encryptedData.createAppendElement(ENCRYPTION.BASE, 'CipherData')
        cipherValue = cipherData.createAppendElement(ENCRYPTION.BASE, 'CipherValue')
        cipherValue.createAppendTextNode( ciphertext.encode('base64') )

        return envelope, header, body

    #########################################################################
    # for verify ############################################################
    #########################################################################

    def _decrypt(self, body):
        faultMessage = None
        try:
            fault = getElement(body, SOAP.ENV, 'Fault')
            faultString = getElement(fault, None, 'faultstring')
            faultMessage = ''.join(childNode.data for childNode in faultString.childNodes if childNode.TEXT_NODE)
        except:
            pass
        if faultMessage:
            raise Exception(u'Сервис ФСС сообщает:\n%s' % anyToUnicode(faultMessage))
        encryptedData = getElement(body, ENCRYPTION.BASE, 'EncryptedData')
#        exploreAttrs(encryptedData)

        verifyAttributeValue(encryptedData, None,  'Type', self.ENCRYPTED_DATA_TYPE)

        encryptionMethod = getElement(encryptedData, ENCRYPTION.BASE, 'EncryptionMethod')
        verifyAttributeValue(encryptionMethod, None, 'Algorithm',  self.ENCRYPTION_ALGORITM)

        keyInfo = getElement(encryptedData, DSIG.BASE, 'KeyInfo')
        encryptedKey = getElement(keyInfo, ENCRYPTION.BASE, 'EncryptedKey')
        encryptionMethod = getElement(encryptedKey, ENCRYPTION.BASE, 'EncryptionMethod')
        verifyAttributeValue(encryptionMethod, None, 'Algorithm',  self.KEY_TRANSPORT)

        keyInfo = getElement(encryptedKey, DSIG.BASE, 'KeyInfo')
        x509Data = getElement(keyInfo, DSIG.BASE, 'X509Data')
        x509Certificate = getElement(x509Data, DSIG.BASE, 'X509Certificate')
        sendedCertBytes = getDecodedText(x509Certificate)
        assert sendedCertBytes

        cipherData = getElement(encryptedKey, ENCRYPTION.BASE, 'CipherData')
        cipherValue = getElement(cipherData, ENCRYPTION.BASE, 'CipherValue')
        keyTransportBytes = getDecodedText(cipherValue)

        cipherData = getElement(encryptedData, ENCRYPTION.BASE, 'CipherData')
        cipherValue = getElement(cipherData, ENCRYPTION.BASE, 'CipherValue')
        ciphertext = getDecodedText(cipherValue)

#        print 'lens of sendedCertBytes, keyTransportBytes, ciphertext) is ', len(sendedCertBytes), len(keyTransportBytes), len(ciphertext)

        api = self.api
        kt = GostR3410_KeyTransport.decode(keyTransportBytes)

        epkb = api.PublicKeyBlob()
        epkb.keyAlgId = api.findAlgIdByOid(kt.transportParameters.ephemeralPublicKey.algorithm.algorithm)
        epkb.paramSetBytes = Asn1Sequence(kt.transportParameters.ephemeralPublicKey.algorithm.parameters).encode()
        epkb.publicKeyBytes = Asn1Base.decode(kt.transportParameters.ephemeralPublicKey.subjectPublicKey[1]).value
        epkb.bitLen   = len(epkb.publicKeyBytes)*8

        ePublicKeyBlobBytes = epkb.encode()

        sb = api.SimpleBlob()
        sb.keyAlgId           = api.CALG_CRYPT_GR28147
        sb.encryptKeyAlgId    = api.CALG_CRYPT_GR28147
        sb.sv                 = kt.transportParameters.ukm
        sb.encryptedKey       = kt.sessionEncryptedKey.encryptedKey
        sb.macKey             = kt.sessionEncryptedKey.macKey
        sb.encryptionParamSet = Asn1Sequence([Asn1Oid(kt.transportParameters.encryptionParamSet)]).encode()

        eSimpleBlobBytes = sb.encode()

        with self._getProvider() as provider:
            with provider.key(api.AT_KEYEXCHANGE) as myKey:
                with provider.importKey(ePublicKeyBlobBytes, myKey, flags=api.CRYPT_EXPORTABLE) as exchangeKey:
# этот код «правильный»:
#                    keyOid = self.userCert.keyOid()
#                    exchangeKey.setParam(api.KP_EXPORT_ALGID, api.getProtectedKeyExportAlgIdByKeyOid(keyOid))
# а этот работает с ФСС:
                    exchangeKey.setParam(api.KP_EXPORT_ALGID, api.CALG_PRO_EXPORT)
                    with provider.importKey(eSimpleBlobBytes, exchangeKey, flags=api.CRYPT_EXPORTABLE) as sessionKey:
                        sessionKey.setParam(api.KP_MODE, api.CRYPT_MODE_CBC)
#                        sessionKey.setParam(api.KP_PADDING, api.ISO10126_PADDING)
                        sessionKey.setParam(api.KP_IV, ciphertext[:8])
                        decryptedMessage = sessionKey.decrypt(ciphertext[8:], final=False)
                        padLen = ord(decryptedMessage[-1])
                        assert padLen<=8
                        decryptedMessage = decryptedMessage[:-padLen]

                        logger = logging.getLogger()
                        logger.info(u'after decryption: %s' % anyToUnicode(decryptedMessage))

                        return decryptedMessage


    def _getProvider(self):
        if self.userCert:
            return self.userCert.provider()
        assert False, u'encryptionHandler._getProvider failed'
