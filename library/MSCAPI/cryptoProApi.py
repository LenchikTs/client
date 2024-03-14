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
## Биндинг к CryptoproCSP и ViPNetCSP средствами ctypes:
##    специфичные константы для CryptoproCSP
##
#############################################################################

from .api  import AbstractApi
from .oids import (
                    oidKeyGostR3410_2001,
                    oidKeyGostR3410_2012_256,
                    oidKeyGostR3410_2012_512,
                    oidHashGostR3411_94,
                    oidHashGostR3411_2012_256,
                    oidHashGostR3411_2012_512,
                  )


class CryptoProApi(AbstractApi):
    ALG_CLASS_HASH         = AbstractApi.ALG_CLASS_HASH
    ALG_CLASS_DATA_ENCRYPT = AbstractApi.ALG_CLASS_DATA_ENCRYPT
    ALG_CLASS_SIGNATURE    = AbstractApi.ALG_CLASS_SIGNATURE
    ALG_CLASS_KEY_EXCHANGE = AbstractApi.ALG_CLASS_KEY_EXCHANGE

    ALG_TYPE_ANY           = AbstractApi.ALG_TYPE_ANY
    ALG_TYPE_BLOCK         = AbstractApi.ALG_TYPE_BLOCK
    ALG_TYPE_DH            = AbstractApi.ALG_TYPE_DH
    ALG_TYPE_SECURECHANNEL = AbstractApi.ALG_TYPE_SECURECHANNEL

#    ALG_SID_SCHANNEL_MAC_KEY = AbstractApi.ALG_SID_SCHANNEL_MAC_KEY
#    ALG_SID_SCHANNEL_ENC_KEY = AbstractApi.ALG_SID_SCHANNEL_ENC_KEY

    ####################################################################
    #
    # CAPI 1.0
    #
    ####################################################################

    # всякие константы, потребные для этого протокола:

    # типы провайдеров:
    PROV_GOST_94_DH    = 71
    PROV_GOST_2001_DH  = 75
    PROV_GOST_2012_256 = 80
    PROV_GOST_2012_512 = 81

    # алгоритмы кодируются как тройка класс - тип - subId
    # классы алгоритмов
#    ALG_CLASS_UECSYMMETRIC =  (6 << 13)

    # типы алгоритмов
    ALG_TYPE_GR3410        =  (7 << 9)
    ALG_TYPE_SHAREDKEY     =  (8 << 9)
    # GR3411 sub-ids
    ALG_SID_GR3411                          = 30
    ALG_SID_GR3411_HASH                     = 39
    ALG_SID_GR3411_HASH34                   = 40
    ALG_SID_GR3411_HMAC_FIXEDKEY            = 55
    ALG_SID_UECMASTER_DIVERS                = 47
    ALG_SID_SHAREDKEY_HASH                  = 50
    ALG_SID_FITTINGKEY_HASH                 = 51
    # G28147 sub_ids
    ALG_SID_G28147                          = 30
    ALG_SID_PRODIVERS                       = 38
    ALG_SID_RIC1DIVERS                      = 40
    ALG_SID_PRO12DIVERS                     = 45
    ALG_SID_KDF_TREE_GOSTR3411_2012_256     = 35
    # Export Key sub_id
    ALG_SID_PRO_EXP                         = 31
    ALG_SID_SIMPLE_EXP                      = 32
    ALG_SID_PRO12_EXP                       = 33
    # GR3412 sub_ids
    ALG_SID_GR3412_2015_M                   = 48
    ALG_SID_GR3412_2015_K                   = 49
    # Hash sub ids
    ALG_SID_G28147_MAC                      = 31
    ALG_SID_G28147_CHV                      = 48
    ALG_SID_TLS1_MASTER_HASH                = 32
    ALG_SID_TLS1PRF_2012_256                = 49
    ALG_SID_TLS1_MASTER_HASH_2012_256       = 54

    ## GOST R 34.11-2012 hash sub ids
    ALG_SID_GR3411_2012_256                 = 33
    ALG_SID_GR3411_2012_512                 = 34
    ALG_SID_GR3411_2012_256_HMAC            = 52
    ALG_SID_GR3411_2012_512_HMAC            = 53
    ALG_SID_GR3411_2012_256_HMAC_FIXEDKEY   = 56
    ALG_SID_GR3411_2012_512_HMAC_FIXEDKEY   = 57
    ALG_SID_PBKDF2_2012_512                 = 58
    ALG_SID_PBKDF2_2012_256                 = 59
    ALG_SID_PBKDF2_94_256                   = 64
    ALG_SID_GR3411_PRFKEYMAT                = 74
    ALG_SID_GR3411_2012_256_PRFKEYMAT       = 75
    ALG_SID_GR3411_2012_512_PRFKEYMAT       = 76

    ## GOST R 34.13-2015 hash sub ids
    ALG_SID_GR3413_2015_M_IMIT              = 60
    ALG_SID_GR3413_2015_K_IMIT              = 61

    # VKO GOST R 34.10-2012 512-bit outputs sub-id
    ALG_SID_SYMMETRIC_512                   = 34

    ## GOST_DH sub ids
    ALG_SID_DH_EX_SF                        = 30
    ALG_SID_DH_EX_EPHEM                     = 31
    ALG_SID_PRO_AGREEDKEY_DH                = 33
    ALG_SID_GR3410                          = 30
    ALG_SID_GR3410EL                        = 35
    ALG_SID_GR3410_12_256                   = 73
    ALG_SID_GR3410_12_512                   = 61
    ALG_SID_DH_EL_SF                        = 36
    ALG_SID_DH_EL_EPHEM                     = 37
    ALG_SID_DH_GR3410_12_256_SF             = 70
    ALG_SID_DH_GR3410_12_256_EPHEM          = 71
    ALG_SID_DH_GR3410_12_512_SF             = 66
    ALG_SID_DH_GR3410_12_512_EPHEM          = 67
    ALG_SID_GR3410_94_ESDH                  = 39
    ALG_SID_GR3410_01_ESDH                  = 40
    ALG_SID_GR3410_12_256_ESDH              = 72
    ALG_SID_GR3410_12_512_ESDH              = 63
    ## EKE sub ids
    ALG_SID_EKE_CIPHER                      = 41
    ALG_SID_EKE_EXPORTPUBLIC                = 42
    ALG_SID_EKEVERIFY_HASH                  = 43

    ALG_SID_UECDIVERS                       = 44
    ALG_SID_UECSYMMETRIC                    = 46
    ALG_SID_UECSYMMETRIC_EPHEM              = 47

    # И вот собственно, алгоритмы
    # не то чтобы я знал - "кто все эти люди", но выбрасывать жаалко :)

    CALG_GR3411                        = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_GR3411)
    CALG_GR3411_2012_256               = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_GR3411_2012_256)
    CALG_GR3411_2012_512               = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_GR3411_2012_512)

    CALG_GR3411_HMAC                   = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_GR3411_HASH)
    CALG_GR3411_HMAC34                 = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_GR3411_HASH34)
    CALG_UECMASTER_DIVERS              = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_UECMASTER_DIVERS)
    CALG_GR3411_HMAC_FIXEDKEY          = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_GR3411_HMAC_FIXEDKEY)

    CALG_GR3411_2012_256_HMAC          = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_GR3411_2012_256_HMAC)
    CALG_GR3411_2012_512_HMAC          = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_GR3411_2012_512_HMAC)

    CALG_GR3411_2012_256_HMAC_FIXEDKEY = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_GR3411_2012_256_HMAC_FIXEDKEY)
    CALG_GR3411_2012_512_HMAC_FIXEDKEY = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_GR3411_2012_512_HMAC_FIXEDKEY)

    CALG_GR3411_PRFKEYMAT              = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_GR3411_PRFKEYMAT)
    CALG_GR3411_2012_256_PRFKEYMAT     = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_GR3411_2012_256_PRFKEYMAT)
    CALG_GR3411_2012_512_PRFKEYMAT     = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_GR3411_2012_512_PRFKEYMAT)

    CALG_G28147_MAC                    = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_G28147_MAC)

    CALG_G28147_IMIT                   = CALG_G28147_MAC

    CALG_GR3413_2015_M_IMIT            = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_GR3413_2015_M_IMIT)
    CALG_GR3413_2015_K_IMIT            = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_GR3413_2015_K_IMIT)

    CALG_G28147_CHV                    = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_ANY | ALG_SID_G28147_MAC)

    CALG_GR3410                        = (ALG_CLASS_SIGNATURE | ALG_TYPE_GR3410 | ALG_SID_GR3410)
    CALG_GR3410EL                      = (ALG_CLASS_SIGNATURE | ALG_TYPE_GR3410 | ALG_SID_GR3410EL)
    CALG_GR3410_12_256                 = (ALG_CLASS_SIGNATURE | ALG_TYPE_GR3410 | ALG_SID_GR3410_12_256)
    CALG_GR3410_12_512                 = (ALG_CLASS_SIGNATURE | ALG_TYPE_GR3410 | ALG_SID_GR3410_12_512)

    CALG_G28147                        = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_G28147)
    CALG_SYMMETRIC_512                 = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_SYMMETRIC_512)

    CALG_GR3412_2015_M                 = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_GR3412_2015_M)
    CALG_GR3412_2015_K                 = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_GR3412_2015_K)
    CALG_DH_EX_SF                      = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH | ALG_SID_DH_EX_SF)
    CALG_DH_EX_EPHEM                   = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH | ALG_SID_DH_EX_EPHEM)
    CALG_DH_EX                         = CALG_DH_EX_SF

    CALG_DH_EL_SF                      = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH | ALG_SID_DH_EL_SF)
    CALG_DH_EL_EPHEM                   = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH | ALG_SID_DH_EL_EPHEM)

    CALG_DH_GR3410_12_256_SF           = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH | ALG_SID_DH_GR3410_12_256_SF)
    CALG_DH_GR3410_12_256_EPHEM        = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH | ALG_SID_DH_GR3410_12_256_EPHEM)

    CALG_DH_GR3410_12_512_SF           = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH | ALG_SID_DH_GR3410_12_512_SF)
    CALG_DH_GR3410_12_512_EPHEM        = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH | ALG_SID_DH_GR3410_12_512_EPHEM)

#    CALG_UECSYMMETRIC                  = (ALG_CLASS_UECSYMMETRIC | ALG_TYPE_BLOCK | ALG_SID_UECSYMMETRIC)
#    CALG_UECSYMMETRIC_EPHEM            = (ALG_CLASS_UECSYMMETRIC | ALG_TYPE_BLOCK | ALG_SID_UECSYMMETRIC_EPHEM)


    CALG_GR3410_94_ESDH                = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH | ALG_SID_GR3410_94_ESDH)
    CALG_GR3410_01_ESDH                = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH | ALG_SID_GR3410_01_ESDH)
    CALG_GR3410_12_256_ESDH            = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH | ALG_SID_GR3410_12_256_ESDH)

    CALG_GR3410_12_512_ESDH            = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH | ALG_SID_GR3410_12_512_ESDH)

    CALG_PRO_AGREEDKEY_DH              = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_BLOCK | ALG_SID_PRO_AGREEDKEY_DH)

    CALG_PRO12_EXPORT                  = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_PRO12_EXP)
    CALG_PRO_EXPORT                    = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_PRO_EXP)
    CALG_SIMPLE_EXPORT                 = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_SIMPLE_EXP)

    CALG_TLS1PRF_2012_256              = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_TLS1PRF_2012_256)
    CALG_TLS1_MASTER_HASH              = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_TLS1_MASTER_HASH)
    CALG_TLS1_MASTER_HASH_2012_256     = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_TLS1_MASTER_HASH_2012_256)

#    CALG_TLS1_MAC_KEY                  = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_SECURECHANNEL | ALG_SID_SCHANNEL_MAC_KEY)
#    CALG_TLS1_ENC_KEY                  = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_SECURECHANNEL | ALG_SID_SCHANNEL_ENC_KEY)

    CALG_PBKDF2_2012_512               = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_PBKDF2_2012_512)
    CALG_PBKDF2_2012_256               = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_PBKDF2_2012_256)

    CALG_PBKDF2_94_256                 = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_PBKDF2_94_256)

    CALG_SHAREDKEY_HASH                = (ALG_CLASS_HASH | ALG_TYPE_SHAREDKEY | ALG_SID_SHAREDKEY_HASH)
    CALG_FITTINGKEY_HASH               = (ALG_CLASS_HASH | ALG_TYPE_SHAREDKEY | ALG_SID_FITTINGKEY_HASH)

    CALG_PRO_DIVERS                    = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_PRODIVERS)
    CALG_RIC_DIVERS                    = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_RIC1DIVERS)
    CALG_OSCAR_DIVERS                  = CALG_RIC_DIVERS
    CALG_PRO12_DIVERS                  = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_PRO12DIVERS)

    CALG_KDF_TREE_GOSTR3411_2012_256   = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_KDF_TREE_GOSTR3411_2012_256)

    CALG_EKE_CIPHER                    = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_BLOCK | ALG_SID_EKE_CIPHER)
    CALG_EKEVERIFY_HASH                = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_EKEVERIFY_HASH)


    # параметры CryptGetKeyParam и CryptSetKeyParam

    KP_MIXMODE              = 101 # Параметр ключа - режим модификации ключа. см. RFC 4357.
    KP_OID                  = 102 # ?
    KP_HASHOID              = 103 # Идентификатор функции хэширования. Строка, заканчивающаяся нулем. Необходимо устанавливать глобальным параметром PP_HASHOID до генерации ключа.
    KP_CIPHEROID            = 104 # Идентификатор узла замены. Строка, заканчивающаяся нулем.
    KP_SIGNATUREOID         = 105 # ?
    KP_DHOID                = 106 # Идентификатор параметров ключа ГОСТ Р 34.10-2001, применяемых в алгоритме Диффи-Хеллмана. Строка, заканчивающаяся нулем. Начиная с версии 3.6 допускается устанавливать идентификаторы подписи. Необходимо устанавливать глобальным параметром PP_DHOID до генерации ключа.
    KP_FP                   = 107 # ?
    KP_IV_BLOB              = 108 # ?

    # KP_PADDING
    ISO10126_PADDING        =   4 # padLen = 8 - len(clearText)%8; padding = random_chars(padLen-1) + chr(padLen)
    ANSI_X923_PADDING       =   5 # padLen = 8 - len(clearText)%8; padding = '\0'*(padLen-1) + chr(padLen)

    # KP_MODE
    CRYPT_MODE_CBCRFC4357   =  31 # блочный шифр с обратной связью на базе ГОСТ 28147-89, согласно RFC 4357;
    CRYPT_MODE_CTR          =  32 # Режим шифрования "гаммирование" по ГОСТ Р 34.13-2015.


    # KP_PERMISSIONS
    # dwFlags для CryptGenKey
    # dwBlobType для CryptExportKey
    # dwFlags для CryptExportKey
    # параметры CryptGetHashParam
    # dwKeySpec для CryptSignHash и CryptGetUserKey

    ####################################################################
    #
    # CAPI 2.0
    #
    ####################################################################

    # кодирование сертификатов:
    # dwType для CertGetNameString ( https://msdn.microsoft.com/en-us/library/aa376086(v=vs.85).aspx )
    # имена полей Subject-a
    # https://msdn.microsoft.com/en-us/library/aa386991(v=vs.85).aspx
    # спецификации формата для CertNameToStr
    # идентификаторы свойств для CertGetCertificateContextProperty
    # dwFlags для CryptAcquireCertificatePrivateKey
    #CERT_USAGE_MATCH.dwType
    # dwFlags в CertGetCertificateChain:

    # Структуры.
    # структуры вроде как специфичны для крипто-про :(

    GR3410_1_MAGIC = 0x3147414D # == 'MAG1'
    G28147_MAGIC   = 0x374a51fd

    # dwKeyType для CryptFindOIDInfo

    ####################################################################
    #
    # унификация
    #
    ####################################################################

    # ГОСТ 2001:
    PROV_GOSTR_2001               = PROV_GOST_2001_DH
    CALG_HASH_GOSTR_3411_94       = CALG_GR3411    # hash
    CALG_SIGN_GOSTR_3410_2001     = CALG_GR3410EL  # sign

    CALG_CRYPT_GR28147            = CALG_G28147

    # ГОСТ 2012, 256 бит:
    PROV_GOSTR_2012_256           = PROV_GOST_2012_256
    CALG_HASH_GOSTR_3411_2012_256 = CALG_GR3411_2012_256 # hash
    CALG_SIGN_GOSTR_3410_2012_256 = CALG_GR3410_12_256   # sign

    # ГОСТ 2012, 512 бит:
    PROV_GOSTR_2012_512           = PROV_GOST_2012_512
    CALG_HASH_GOSTR_3411_2012_512 = CALG_GR3411_2012_512 # hash
    CALG_SIGN_GOSTR_3410_2012_512 = CALG_GR3410_12_512   # sign


    KP_EXPORT_ALGID    = AbstractApi.KP_ALGID


    def getProviderTypeByKeyOid(self, keyOid):
        if keyOid == oidKeyGostR3410_2001:
            return self.PROV_GOST_2001_DH
        if keyOid == oidKeyGostR3410_2012_256:
            return self.PROV_GOST_2012_256
        if keyOid == oidKeyGostR3410_2012_512:
            return self.PROV_GOST_2012_512
        raise Exception(u'Неизвестный идентификатор ключа OID=«%s»' % keyOid)


    def getHashAlgIdByOid(self, hashOid):
        if hashOid == oidHashGostR3411_94:
            return self.CALG_GR3411
        if hashOid == oidHashGostR3411_2012_256:
            return self.CALG_GR3411_2012_256
        if hashOid == oidHashGostR3411_2012_512:
            return self.CALG_GR3411_2012_512
        raise Exception('Невозможно получить идентификатор алгоритма хеширования по OID «%s»', hashOid)


    # Идентификатор алгоритма обмена ключей по Диффи-Хеллману на базе закрытого ключа эфемерной пары.
    # Identifier of the Diffie-Hellman key exchange algorithm based on the ephemeral pair's private key.
    def getDhElEphemAlgIdByKeyOid(self, keyOid):
        if keyOid == oidKeyGostR3410_2001:
            return self.CALG_DH_EL_EPHEM
        if keyOid == oidKeyGostR3410_2012_256:
            return self.CALG_DH_GR3410_12_256_EPHEM
        if keyOid == oidKeyGostR3410_2012_512:
            return self.CALG_DH_GR3410_12_512_EPHEM
        raise Exception(u'Невозможно получить идентификатор алгоритма обмена ключей по Диффи-Хеллману на базе закрытого ключа эфемерной пары по ключу OID=«%s»' % keyOid)


    # Идентификатор алгоритма защищённого экспорта ключа.
    # Identifier of the protected export the key algorithm
    def getProtectedKeyExportAlgIdByKeyOid(self, keyOid):
        if keyOid == oidKeyGostR3410_2001:
            return self.CALG_PRO_EXPORT
        if keyOid == oidKeyGostR3410_2012_256:
            return self.CALG_PRO12_EXPORT
        if keyOid == oidKeyGostR3410_2012_512:
            return self.CALG_PRO12_EXPORT
        raise Exception(u'Невозможно получить идентификатор алгоритма защищённого экспорта ключа по ключу OID=«%s»' % keyOid)
