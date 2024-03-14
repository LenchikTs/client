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
##    специфичные константы для ViPNetCSP
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


class ViPNetApi(AbstractApi):
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
    VPN_PROV_TYPE           =  2 # Тип провайдера на основе алгоритма ГОСТ Р 34.10-2001
    VPN_PROV_TYPE_2012_512  = 77 # Тип провайдера на основе алгоритма ГОСТ Р 34.10-2012 с длиной ключа 256 бит
    VPN_PROV_TYPE_2012_1024 = 78 # Тип провайдера на основе алгоритма ГОСТ Р 34.10-2012 с длиной ключа 512 бит

    # алгоритмы кодируются как тройка класс - тип - subId
    # классы алгоритмов

    # типы алгоритмов
    ALG_TYPE_GR3410        =  (7 << 9)

    # SID(ы) алгоритмов (см. GET_ALG_SID из WinCrypt).
    # ГОСТ 28147-89, ГОСТ Р 34.11-94, ГОСТ Р 34.10-2001
    ALG_SID_HASH_CPCSP         = 30 # SID алгоритма хеширования по ГОСТ Р 34.11-94
    ALG_SID_ENCRYPT_CPCSP      = 30 # SID алгоритма шифрования по ГОСТ 28147-89
    ALG_SID_G28147_MAC         = 31 # SID алгоритма вычисления имитовставки по ГОСТ 28147-89
    ALG_SID_PRO_EXP            = 31 # SID алгоритма экспорта/импорта ключа по RFC 4357  (п. 6.3)
    ALG_SID_SIMPLE_EXP         = 32 # SID алгоритма экспорта/импорта ключа по RFC 4357  (п. 6.1) применяется для хранения и конвертации ключей
    ALG_SID_TLS1_MASTER_HASH   = 32 # SID алгоритма выработки мастер ключа для протокола TLS на основе ГОСТ Р 34.10-2001
    ALG_SID_SIGN_ELLIP         = 35 # SID алгоритма подписи по ГОСТ Р 34.10-2001
    ALG_SID_DH_EL              = 36 # SID алгоритма согласования ключей Диффи-Хелмана на основе ГОСТ Р 34.10-2001
    ALG_SID_DH_EL_EPHEM        = 37 # SID алгоритма согласования ключей Диффи-Хелмана на основе ГОСТ Р 34.10-2001 для эфемерного ключа
    ALG_SIG_ITCS_EXPORT        = 46 # SID алгоритма экспорта/импорта ключа в формате Инфотекс. Ключ экспортируется с дополнительной информацией, которая также защищена имитовставкой.
#    ALG_SID_SCHANNEL_MAC_KEY   =  3 # SID алгоритма вычисления имитовставки для алгоритма TLS на основе ГОСТ Р 34.10-2001
#    ALG_SID_SCHANNEL_ENC_KEY   =  7 # SID алгоритма шифрования для алгоритма TLS на основе ГОСТ Р 34.10-2001

    ALG_SID_TLS1_MASTER        =  6 # SID алгоритма мастер ключа для протокола TLS на основе ГОСТ Р 34.10-2001
    ALG_SID_MASTER_DERIVE_HASH = 80 # SID алгоритма выработки симметричного ключа из мастер хеш-функции.

    # ГОСТ ГОСТ Р 34.11-2012, ГОСТ Р 34.10-2012
    ALG_SID_HASH_2012_256BIT   = 33 # SID алгоритма хеширования по ГОСТ Р 34.11-2012 с размером результата 256 бит
    ALG_SID_HASH_2012_512BIT   = 34 # SID алгоритма хеширования по ГОСТ Р 34.11-2012 с размером результата 512 бит
    ALG_SID_2012_256_SIGN_CSP  = 73 # SID алгоритма подписи по ГОСТ Р 34.10-2012 с длиной ключа 256 бит
    ALG_SID_2012_512_SIGN_CSP  = 61 # SID алгоритма подписи по ГОСТ Р 34.10-2012 с длиной ключа 512 бит
    ALG_SID_2012_256_EXCHANGE_CSP = 70 # SID алгоритма Диффи-Хелмана по ГОСТ Р 34.10-2012 с длиной ключа 256 бит
    ALG_SID_2012_512_EXCHANGE_CSP = 66 # SID алгоритма Диффи-Хелмана по ГОСТ Р 34.10-2012 с длиной ключа 512 бит
    ALG_SID_2012_256_EXCHANGE_CSP_EPHEM = 71 # SID алгоритма эфемерного Диффи-Хелмана по ГОСТ Р 34.10-2012 с длиной ключа 256 бит
    ALG_SID_2012_512_EXCHANGE_CSP_EPHEM = 67 # SID алгоритма эфемерного Диффи-Хелмана по ГОСТ Р 34.10-2012 с длиной ключа 512 бит
    ALG_SID_PRO12_EXP          = 33 # SID алгоритма экспорта/импорта ключа по Р 50.1.113-2016
    ALG_SID_TLS1PRF_2012_256   = 49 # SID алгоритма псевдослучайной функции (PRF) протокола по Р 50.1.113-2016 на основе функции хеширования с длиной выхода 256 бит
    ALG_SID_TLS1PRF_2012_512   = 50 # SID алгоритма псевдослучайной функции протокола по Р 50.1.113-2016 на основе функции хеширования с длиной выхода 512 бит
    ALG_SID_TLS1_MASTER_HASH_2012_256   = 54 # SID алгоритма "ключевого мастера" по протоколу TLS на основе Рекомендаций по стандартизации ТК26 "Использование наборов алгоритмов шифрования на основе ГОСТ 28147-89 для протокола безопасности транспортного уровня." с длиной выхода 256 бит.
#    ALG_SID_TLS1_MASTER_HASH_2012_512   = 55 # SID алгоритма "ключевого мастера" по протоколу TLS на основе Рекомендаций по стандартизации ТК26 "Использование наборов алгоритмов шифрования на основе ГОСТ 28147-89 для протокола безопасности // транспортного уровня." с длиной выхода 512 бит. На данный момент не поддерживается.
    ALG_SID_2012_256_SIGN_V2_CSP        = 81 # SID алгоритма подписи по ГОСТ Р 34.10-2012 с длиной ключа 256 бит в соответствии с Рекомендации по стандартизации (проект) использование алгоритмов ГОСТ Р 34.10-2012, ГОСТ Р 34.11-2012 в сертификате, списке аннулированных сертификатов (CRL) и запросе на сертификат PKCS#10 инфраструктуры открытых ключей X.509
    ALG_SID_2012_512_SIGN_V2_CSP        = 82 # SID алгоритма подписи по ГОСТ Р 34.10-2012 с длиной ключа 512 бит в соответствии с Рекомендации по стандартизации (проект) использование алгоритмов ГОСТ Р 34.10-2012, ГОСТ Р 34.11-2012 в сертификате, списке аннулированных сертификатов (CRL) и запросе на сертификат PKCS#10 инфраструктуры открытых ключей X.509

    # CALG алгоритмов.
    # ГОСТ 28147-89, ГОСТ Р 34.11-94, ГОСТ Р 34.10-2001
    CPCSP_HASH_ID         = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_HASH_CPCSP )             # CALG алгоритма хеширования по ГОСТ Р 34.11-94
    CPCSP_ENCRYPT_ID      = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_ENCRYPT_CPCSP) # CALG алгоритма шифрования по ГОСТ 28147-89
    CPCSP_IMITO_ID        = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_G28147_MAC)              # CALG алгоритма вычисления имитовставки по ГОСТ 28147-89
    CALG_PRO_EXPORT       = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_PRO_EXP)       # CALG алгоритма экспорта/импорта ключа по RFC 4357  (п. 6.3)
    CALG_SIMPLE_EXPORT    = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_SIMPLE_EXP)    # CALG алгоритма экспорта/импорта ключа по RFC 4357  (п. 6.1) применяется для хранения и конвертации ключей
    CALG_TLS1_MASTER_HASH = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_TLS1_MASTER_HASH )       # CALG алгоритма выработки мастер ключа для протокола TLS на основе ГОСТ Р 34.10-2001
    ELLIP_SIGN_ID         = (ALG_CLASS_SIGNATURE | ALG_TYPE_GR3410 | ALG_SID_SIGN_ELLIP)      # CALG алгоритма подписи по ГОСТ Р 34.10-2001
    CPCSP_DH_EL_ID        = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH |  ALG_SID_DH_EL)           # CALG алгоритма согласования ключей Диффи-Хелмана на основе ГОСТ Р 34.10-2001
    CALG_DH_EL_EPHEM      = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH | ALG_SID_DH_EL_EPHEM)      # CALG алгоритма согласования ключей Диффи-Хелмана на основе ГОСТ Р 34.10-2001 для эфемерного ключа
    CALG_ITCS_EXPORT      = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SIG_ITCS_EXPORT)   # CALG алгоритма экспорта/импорта ключа в формате Инфотекс. Ключ экспортируется с дополнительной информацией, которая также защищена имитовставкой.
#    CALG_TLS1_MAC_KEY     = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_SECURECHANNEL | ALG_SID_SCHANNEL_MAC_KEY) # CALG алгоритма вычисления имитовставки для алгоритма TLS на основе ГОСТ Р 34.10-2001
#    CALG_TLS1_ENC_KEY     = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_SECURECHANNEL | ALG_SID_SCHANNEL_ENC_KEY) # CALG алгоритма шифрования для алгоритма TLS на основе ГОСТ Р 34.10-2001
    CALG_MASTER_DERIVE_HASH = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_MASTER_DERIVE_HASH ) # CALG алгоритма выработки симметричного ключа из мастер хеша.

    # ГОСТ ГОСТ Р 34.11-2012, ГОСТ Р 34.10-2012
    CSP_HASH_2012_256BIT_ID = ( ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_HASH_2012_256BIT )   # CALG алгоритма хеширования по ГОСТ Р 34.11-2012 с размером результата 256 бит
    CSP_HASH_2012_512BIT_ID = ( ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_HASH_2012_512BIT )   # CALG алгоритма хеширования по ГОСТ Р 34.11-2012 с размером результата 512 бит
    CSP_2012_256_SIGN_ID    = (ALG_CLASS_SIGNATURE | ALG_TYPE_GR3410 | ALG_SID_2012_256_SIGN_CSP) # CALG алгоритма подписи по ГОСТ Р 34.10-2012 с длиной ключа 256 бит
    CSP_2012_512_SIGN_ID    = (ALG_CLASS_SIGNATURE | ALG_TYPE_GR3410 | ALG_SID_2012_512_SIGN_CSP) # CALG алгоритма подписи по ГОСТ Р 34.10-2012 с длиной ключа 512 бит
    CSP_2012_256_EXCHANGE_ID= (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH |  ALG_SID_2012_256_EXCHANGE_CSP) # CALG алгоритма Диффи-Хелмана по ГОСТ Р 34.10-2012 с длиной ключа 256 бит
    CSP_2012_512_EXCHANGE_ID= (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH |  ALG_SID_2012_512_EXCHANGE_CSP) # CALG алгоритма Диффи-Хелмана по ГОСТ Р 34.10-2012 с длиной ключа 512 бит
    CSP_2012_256_EXCHANGE_ID_EPHEM = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH |  ALG_SID_2012_256_EXCHANGE_CSP_EPHEM) # CALG алгоритма эфемерного Диффи-Хелмана по ГОСТ Р 34.10-2012 с длиной ключа 256 бит
    CSP_2012_512_EXCHANGE_ID_EPHEM = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH |  ALG_SID_2012_512_EXCHANGE_CSP_EPHEM) # CALG алгоритма эфемерного Диффи-Хелмана по ГОСТ Р 34.10-2012  с длиной ключа 512 бит
    CALG_PRO12_EXPORT       = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_PRO12_EXP) # CALG алгоритма экспорта/импорта ключа по Р 50.1.113-2016
    CALG_TLS1PRF_2012_256   = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_TLS1PRF_2012_256)    # CALG алгоритма псевдослучайной функции (PRF) протокола по Р 50.1.113-2016 на основе функции хеширования с длиной выхода 256 бит
    CALG_TLS1PRF_2012_512   = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_TLS1PRF_2012_512)    # CALG алгоритма псевдослучайной функции (PRF) протокола по Р 50.1.113-2016 на основе функции хеширования с длиной выхода 512 бит
    CALG_TLS1_MASTER_HASH_2012_256 = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_TLS1_MASTER_HASH_2012_256 ) # CALG алгоритма "ключевого мастера" по протоколу TLS на основе Рекомендаций по стандартизации ТК26 "Использование наборов алгоритмов шифрования на основе ГОСТ 28147-89 для протокола безопасности транспортного уровня." с длиной выхода 256 бит.
#    CALG_TLS1_MASTER_HASH_2012_512 = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_TLS1_MASTER_HASH_2012_512 ) # CALG алгоритма "ключевого мастера" по протоколу TLS на основе Рекомендаций по стандартизации ТК26 "Использование наборов алгоритмов шифрования на основе ГОСТ 28147-89 для протокола безопасности транспортного уровня." с длиной выхода 512 бит. На данный момент не поддерживается.
    CSP_2012_256_SIGN_V2_ID = (ALG_CLASS_SIGNATURE | ALG_TYPE_GR3410 | ALG_SID_2012_256_SIGN_V2_CSP) # CALG алгоритма подписи по ГОСТ Р 34.10-2012 с длиной ключа 256 бит в соответствии с Рекомендации по стандартизации (проект) использование алгоритмов ГОСТ Р 34.10-2012, ГОСТ Р 34.11-2012 в сертификате, списке аннулированных сертификатов (CRL) и запросе на сертификат PKCS#10 инфраструктуры открытых ключей X.509
    CSP_2012_512_SIGN_V2_ID = (ALG_CLASS_SIGNATURE | ALG_TYPE_GR3410 | ALG_SID_2012_512_SIGN_V2_CSP) # CALG алгоритма подписи по ГОСТ Р 34.10-2012 с длиной ключа 512 бит в соответствии с Рекомендации по стандартизации (проект) использование алгоритмов ГОСТ Р 34.10-2012, ГОСТ Р 34.11-2012 в сертификате, списке аннулированных сертификатов (CRL) и запросе на сертификат PKCS#10 инфраструктуры открытых ключей X.509

    # параметры CryptGetKeyParam и CryptSetKeyParam
    KP_MIXMODE              = 101 # режим модификации ключа. см. RFC 4357.
    KP_HASHOID              = 103 # идентификатор параметров хеширования ГОСТ Р 34.11-2001 и RFC 4357.
    KP_CIPHEROID            = 104 # идентификатор параметров шифрования (узел замены, подстановка) в контексте ключа. см. ГОСТ 28147-89 и RFC 4357.
    KP_SIGNATUREOID         = 105 # идентификатор параметров подписи (эллиптическая кривая) в контексте ключа. см. ГОСТ Р 34.10-2001, ГОСТ Р 34.10-2012, RFC 4357, Р 50.1.114.
    KP_DHOID                = 106 # идентификатор параметров Диффи-Хелмана (эллиптическая кривая) в контексте ключа. см. ГОСТ Р 34.10-2001, ГОСТ Р 34.10-2012, RFC 4357, Р 50.1.114.
    KP_EXPORTID             = 108 # алгоритм экспорта ключа. В качестве pbData должен передаваться [указатель на DWORD, представляющая алгоритм (CALG) экспорта ключа.

    # KP_PADDING
    # KP_MODE
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
    # dwFlags в CertGetCertificateChain:


    # Структуры.
    # magic-и вроде как специфичны для крипто-про :(
    # Но в ViPNet я пока не нашёл описаний

    GR3410_1_MAGIC = 0x3147414D # == 'MAG1'
    G28147_MAGIC   = 0x374a51fd

    # dwKeyType для CryptFindOIDInfo

    ####################################################################
    #
    # унификация
    #
    ####################################################################

    # ГОСТ 2001:
    PROV_GOSTR_2001           = VPN_PROV_TYPE
    CALG_HASH_GOSTR_3411_94   = CPCSP_HASH_ID
    CALG_SIGN_GOSTR_3410_2001 = ELLIP_SIGN_ID

    CALG_CRYPT_GR28147 = CPCSP_ENCRYPT_ID

    # ГОСТ 2012, 256 бит:
    PROV_GOSTR_2012_256           = VPN_PROV_TYPE_2012_512
    CALG_HASH_GOSTR_3411_2012_256 = CSP_HASH_2012_256BIT_ID # hash
    CALG_SIGN_GOSTR_3410_2012_256 = CSP_2012_256_SIGN_ID    # sign

    # ГОСТ 2012, 512 бит:
    PROV_GOSTR_2012_512           = VPN_PROV_TYPE_2012_1024
    CALG_HASH_GOSTR_3411_2012_512 = CSP_HASH_2012_512BIT_ID # hash
    CALG_SIGN_GOSTR_3410_2012_512 = CSP_2012_512_SIGN_ID    # sign


    KP_EXPORT_ALGID = KP_EXPORTID


    def getProviderTypeByKeyOid(self, keyOid):
        if keyOid == oidKeyGostR3410_2001:
            return self.VPN_PROV_TYPE
        if keyOid == oidKeyGostR3410_2012_256:
            return self.VPN_PROV_TYPE_2012_512
        if keyOid == oidKeyGostR3410_2012_512:
            return self.VPN_PROV_TYPE_2012_1024
        raise Exception(u'Неизвестный идентификатор ключа OID=«%s»' % keyOid)


    def getHashAlgIdByOid(self, hashOid):
        if hashOid == oidHashGostR3411_94:
            return self.CPCSP_HASH_ID
        if hashOid == oidHashGostR3411_2012_256:
            return self.CSP_HASH_2012_256BIT_ID
        if hashOid == oidHashGostR3411_2012_512:
            return self.CSP_HASH_2012_512BIT_ID
        raise Exception('Невозможно получить идентификатор алгоритма хеширования по OID «%s»', hashOid)


    # Идентификатор алгоритма обмена ключей по Диффи-Хеллману на базе закрытого ключа эфемерной пары.
    # Identifier of the Diffie-Hellman key exchange algorithm based on the ephemeral pair's private key.
    def getDhElEphemAlgIdByKeyOid(self, keyOid):
        if keyOid == oidKeyGostR3410_2001:
            return self.CALG_DH_EL_EPHEM
        if keyOid == oidKeyGostR3410_2012_256:
            return self.CSP_2012_256_EXCHANGE_ID_EPHEM
        if keyOid == oidKeyGostR3410_2012_512:
            return self.CSP_2012_512_EXCHANGE_ID_EPHEM
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
