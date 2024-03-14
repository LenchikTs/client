#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2017-2018 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## "Транспортная" структура для передачи ключа ГОСТ Р 3410
## описание ASN.1 собрано из разных RFC4490 и далее по ссылкам
##
#############################################################################


from tinyAsn1 import Asn1BitString, Asn1OctetString, Asn1Oid, Asn1Sequence, Asn1Structure

#
#
#Описание ASN.1:
#
#    GostR3410-EncryptionSyntax
#        { iso(1) member-body(2) ru(643) rans(2) cryptopro(2)
#        other(1) modules(1) gostR3410-EncryptionSyntax(5) 2 }
#    DEFINITIONS ::=
#    BEGIN
#
#        Gost28147-89-Key ::= OCTET STRING (SIZE (32))
#        Gost28147-89-MAC ::= OCTET STRING (SIZE (1..4))
#
#        Gost28147-89-EncryptedKey ::=
#            SEQUENCE {
#                encryptedKey Gost28147-89-Key,
#                maskKey      [0] IMPLICIT Gost28147-89-Key OPTIONAL,
#                macKey       Gost28147-89-MAC (SIZE (4))
#            }
#
#        Gost28147-89-ParamSet ::= OBJECT IDENTIFIER
#
#        AlgorithmIdentifier  ::= SEQUENCE{
#        algorithm  OBJECT IDENTIFIER,
#        parameters ANY DEFINED BY algorithm OPTIONAL
#        }
#
#        SubjectPublicKeyInfo  ::=  SEQUENCE  {
#        algorithm            AlgorithmIdentifier,
#        subjectPublicKey     BIT STRING
#        }
#
#        GostR3410-TransportParameters ::=
#            SEQUENCE {
#                encryptionParamSet Gost28147-89-ParamSet,
#                ephemeralPublicKey [0]
#                    IMPLICIT SubjectPublicKeyInfo OPTIONAL,
#                ukm                OCTET STRING ( SIZE(8) )
#            }
#
#        GostR3410-KeyTransport ::=
#            SEQUENCE {
#                sessionEncryptedKey Gost28147-89-EncryptedKey,
#                transportParameters [0]
#                    IMPLICIT GostR3410-TransportParameters OPTIONAL
#            }
#    END -- GostR3410-EncryptionSyntax
#
#
#Образец закодированных данных:
#    3081a4302804208d4b5b4b0b6ec2edec51ac0b1f7955cac09dc5b7cc337a275e
#    2a8a697e6454e60404ec4935a7a07806072a850302021f01a063301c06062a85
#    03020213301206072a85030202240006072a850302021e010343000440a39fc2
#    7454d25cfa2095c9dcc51fe3789a082975dbb38fec86286189d26a32f6718ed8
#    7a6495b2ce678518d403631e0c9b6aaf1d0687bf41d88c381e939d7cd70408cd
#    0d493ccc9ee35e
#
#Декодированный образец (спасибо https://lapo.it/asn1js):
#
#    SEQUENCE(2 elem)    -- GostR3410KeyTransport
#        SEQUENCE(2 elem) -- Gost2814789EncryptedKey
#            OCTET STRING(32 byte) 8D4B5B4B0B6EC2EDEC51AC0B1F7955CAC09DC5B7CC337A275E2A8A697E6454E6 -- encryptedKey
#            OCTET STRING(4 byte) EC4935A7                                                          -- macKey
#        [0](3 elem) -- GostR3410TransportParameters
#            OBJECT IDENTIFIER 1.2.643.2.2.31.1 cryptoProCipherA(CryptoPro params A for GOST 28147-89) -- encryptionParamSet
#            [0](2 elem)                                                                               -- ephemeralPublicKey:  SubjectPublicKeyInfo
#                SEQUENCE(2 elem)   -- algorithm
#                    OBJECT IDENTIFIER 1.2.643.2.2.19 gostPublicKey(GOST R 34.10-2001 (ECC) public key) -- algorithm
#                    SEQUENCE(2 elem)                                                                   -- parameters
#                        OBJECT IDENTIFIER 1.2.643.2.2.36.0 cryptoProSignXA(CryptoPro ell.curve XA for GOST R 34.11-2001)
#                        OBJECT IDENTIFIER 1.2.643.2.2.30.1 cryptoProDigestA(CryptoPro digest params for GOST R 34.11-94)
#                BIT STRING(1 elem) -- subjectPublicKey
#                    OCTET STRING(64 byte) A39FC27454D25CFA2095C9DCC51FE3789A082975DBB38FEC86286189D26A32F6718ED87A6495B2CE678518D403631E0C9B6AAF1D0687BF41D88C381E939D7CD7
#            OCTET STRING(8 byte) CD0D493CCC9EE35E                                                     -- ukm


class Gost28147_89_EncryptedKey( Asn1Structure ):
    _fields_ = ( { 'name': 'encryptedKey', 'type': Asn1OctetString },
                 { 'name': 'masKey',       'type': Asn1OctetString, 'context-specific-tag': 0, 'optional': True },
                 { 'name': 'macKey',       'type': Asn1OctetString }
               )


class GOSTR3410_AlgorithmIdentifier( Asn1Structure ):
    _fields_ = ( { 'name': 'algorithm',           'type': Asn1Oid},
                 { 'name': 'parameters',          'type': Asn1Sequence}
               )

class GOSTR3410_SubjectPublicKeyInfo( Asn1Structure ):
    _fields_ = ( { 'name': 'algorithm',           'type': GOSTR3410_AlgorithmIdentifier},
                 { 'name': 'subjectPublicKey',    'type': Asn1BitString}
               )


class GostR3410_TransportParameters( Asn1Structure ):
    _fields_ = ( { 'name': 'encryptionParamSet', 'type': Asn1Oid },
                 { 'name': 'ephemeralPublicKey', 'type': GOSTR3410_SubjectPublicKeyInfo, 'context-specific-tag': 0, 'optional': True },
                 { 'name': 'ukm',                'type': Asn1OctetString }
               )


class GostR3410_KeyTransport( Asn1Structure ):
    _fields_ = ( { 'name': 'sessionEncryptedKey', 'type': Gost28147_89_EncryptedKey },
                 { 'name': 'transportParameters', 'type': GostR3410_TransportParameters, 'context-specific-tag': 0, 'optional': True }
               )

if __name__ == '__main__':
    ###############################
    # использование, что-то типа -
    ###############################

    data = '3081a4302804208d4b5b4b0b6ec2edec51ac0b1f7955cac09dc5b7cc337a275e' \
           '2a8a697e6454e60404ec4935a7a07806072a850302021f01a063301c06062a85' \
           '03020213301206072a85030202240006072a850302021e010343000440a39fc2' \
           '7454d25cfa2095c9dcc51fe3789a082975dbb38fec86286189d26a32f6718ed8' \
           '7a6495b2ce678518d403631e0c9b6aaf1d0687bf41d88c381e939d7cd70408cd' \
           '0d493ccc9ee35e'.decode('hex')

    kt = GostR3410_KeyTransport.decode(data)
    #print 'kt:', repr(kt)

    assert kt.sessionEncryptedKey.encryptedKey == '8D4B5B4B0B6EC2EDEC51AC0B1F7955CAC09DC5B7CC337A275E2A8A697E6454E6'.decode('hex')
    assert kt.sessionEncryptedKey.masKey       == None
    assert kt.sessionEncryptedKey.macKey       == 'EC4935A7'.decode('hex')

    assert kt.transportParameters.encryptionParamSet == '1.2.643.2.2.31.1'

    assert kt.transportParameters.ephemeralPublicKey.algorithm.algorithm == '1.2.643.2.2.19'
    assert len(kt.transportParameters.ephemeralPublicKey.algorithm.parameters) == 2
    assert kt.transportParameters.ephemeralPublicKey.algorithm.parameters[0].value == '1.2.643.2.2.36.0'
    assert kt.transportParameters.ephemeralPublicKey.algorithm.parameters[1].value == '1.2.643.2.2.30.1'
    assert kt.transportParameters.ephemeralPublicKey.subjectPublicKey == (0, '0440A39FC27454D25CFA2095C9DCC51FE3789A082975DBB38FEC86286189D26A32F6718ED87A6495B2CE678518D403631E0C9B6AAF1D0687BF41D88C381E939D7CD7'.decode('hex'))
    assert kt.transportParameters.ukm          == 'CD0D493CCC9EE35E'.decode('hex')

    newData = bytes(kt.encode())
    assert data == newData

    print '-*- self-test passed -*-'

    ###############################
