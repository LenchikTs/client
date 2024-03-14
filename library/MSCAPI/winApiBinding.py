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
##    непосредственно связывание с библиотеками в windows
##
#############################################################################

from ctypes import windll

from .errors import ftGetLastError, ftFormatMessageW, ftSetLastError
from .capi10 import (
                     ftCryptGenKey,
                     ftCryptReleaseContext,
                     ftCryptVerifySignature,
                     ftCryptDuplicateHash,
                     ftCryptDestroyHash,
                     ftCryptHashData,
                     ftCryptGetProvParam,
                     ftCryptGetHashParam,
                     ftCryptGetUserKey,
                     ftCryptSetProvParam,
                     ftCryptEnumProvidersW,
                     ftCryptGenRandom,
                     ftCryptGetKeyParam,
                     ftCryptEncrypt,
                     ftCryptDecrypt,
                     ftCryptEnumProviderTypesW,
                     ftCryptCreateHash,
                     ftCryptImportKey,
                     ftCryptExportKey,
                     ftCryptSignHash,
                     ftCryptSetKeyParam,
                     ftCryptAcquireContext,
                     ftCryptDestroyKey,
                     ftCryptGetDefaultProviderW,
                     ftCryptDuplicateKey,
                    )
from .capi20 import (
                     ftCryptImportPublicKeyInfo,
                     ftCertOpenSystemStoreW,
                     ftCertOpenStore,
                     ftCertFreeCertificateContext,
                     ftCertVerifyCertificateChainPolicy,
                     ftCryptAcquireCertificatePrivateKey,
                     ftCryptFindOIDInfo,
                     ftCertCloseStore,
                     ftCertFreeCertificateChain,
                     ftCertDuplicateCertificateContext,
                     ftCertGetCertificateContextProperty,
                     ftCertGetCertificateChain,
                     ftCertEnumCertificatesInStore,
                     ftCertCreateCertificateContext,
                     ftCertNameToStr,
                     ftCryptSignMessage,
                     ftCryptVerifyDetachedMessageSignature,
                    )


class WinApiBindingMixin:
    u'''
        Настройка абстрактного API на конкретные библиотеки
    '''
    __libAdvapi32Name = 'advapi32'
    __libCrypt32Name  = 'crypt32'

    def __init__(self):
        self._hLibAnvapi32 = windll.LoadLibrary(self.__libAdvapi32Name)
        self._hLibCrypt32  = windll.LoadLibrary(self.__libCrypt32Name)

        self._fGetLastError  = ftGetLastError(('GetLastError', windll.kernel32))
        self._fSetLastError  = ftSetLastError(('SetLastError', windll.kernel32))
        self._fFormatMessage = ftFormatMessageW(('FormatMessageW', windll.kernel32))

        self._fCryptEnumProviderTypes  = ftCryptEnumProviderTypesW(('CryptEnumProviderTypesW', self._hLibAnvapi32))
        self._fCryptEnumProviders      = ftCryptEnumProvidersW(('CryptEnumProvidersW', self._hLibAnvapi32))
        self._fCryptGetDefaultProvider = ftCryptGetDefaultProviderW(('CryptGetDefaultProviderW', self._hLibAnvapi32))

        self._fCryptAcquireContext     = ftCryptAcquireContext(('CryptAcquireContextW', self._hLibAnvapi32))
        self._fCryptReleaseContext     = ftCryptReleaseContext(('CryptReleaseContext', self._hLibAnvapi32))
        self._fCryptGetProvParam       = ftCryptGetProvParam(('CryptGetProvParam', self._hLibAnvapi32))
        self._fCryptSetProvParam       = ftCryptSetProvParam(('CryptSetProvParam', self._hLibAnvapi32))
        self._fCryptGenRandom          = ftCryptGenRandom(('CryptGenRandom', self._hLibAnvapi32))

        self._fCryptGenKey             = ftCryptGenKey(('CryptGenKey', self._hLibAnvapi32))
        self._fCryptDuplicateKey       = ftCryptDuplicateKey(('CryptDuplicateKey', self._hLibAnvapi32))
        self._fCryptGetUserKey         = ftCryptGetUserKey(('CryptGetUserKey', self._hLibAnvapi32))
        self._fCryptImportKey          = ftCryptImportKey(('CryptImportKey', self._hLibAnvapi32))
        self._fCryptGetKeyParam        = ftCryptGetKeyParam(('CryptGetKeyParam', self._hLibAnvapi32))
        self._fCryptSetKeyParam        = ftCryptSetKeyParam(('CryptSetKeyParam', self._hLibAnvapi32))
        self._fCryptExportKey          = ftCryptExportKey(('CryptExportKey', self._hLibAnvapi32))
        self._fCryptDestroyKey         = ftCryptDestroyKey(('CryptDestroyKey', self._hLibAnvapi32))

        self._fCryptCreateHash         = ftCryptCreateHash(('CryptCreateHash', self._hLibAnvapi32))
        self._fCryptDuplicateHash      = ftCryptDuplicateHash(('CryptDuplicateHash', self._hLibAnvapi32))
        self._fCryptHashData           = ftCryptHashData(('CryptHashData', self._hLibAnvapi32))
        self._fCryptGetHashParam       = ftCryptGetHashParam(('CryptGetHashParam', self._hLibAnvapi32))
        self._fCryptSignHash           = ftCryptSignHash(('CryptSignHashW', self._hLibAnvapi32))
        self._fCryptVerifySignature    = ftCryptVerifySignature(('CryptVerifySignatureW', self._hLibAnvapi32))
        self._fCryptDestroyHash        = ftCryptDestroyHash(('CryptDestroyHash', self._hLibAnvapi32))

        self._fCryptEncrypt            = ftCryptEncrypt(('CryptEncrypt', self._hLibAnvapi32))
        self._fCryptDecrypt            = ftCryptDecrypt(('CryptDecrypt', self._hLibAnvapi32))

        self._fCryptFindOIDInfo                  = ftCryptFindOIDInfo(('CryptFindOIDInfo', self._hLibCrypt32))

        self._fCertOpenStore                     = ftCertOpenStore(('CertOpenStore', self._hLibCrypt32))
        self._fCertOpenSystemStore               = ftCertOpenSystemStoreW(('CertOpenSystemStoreW', self._hLibCrypt32))
        self._fCertCloseStore                    = ftCertCloseStore(('CertCloseStore', self._hLibCrypt32))

        self._fCryptImportPublicKeyInfo          = ftCryptImportPublicKeyInfo(('CryptImportPublicKeyInfo', self._hLibCrypt32))

        self._fCertEnumCertificatesInStore       = ftCertEnumCertificatesInStore(('CertEnumCertificatesInStore', self._hLibCrypt32))
        self._fCertCreateCertificateContext      = ftCertCreateCertificateContext(('CertCreateCertificateContext', self._hLibCrypt32))
        self._fCertDuplicateCertificateContext   = ftCertDuplicateCertificateContext(('CertDuplicateCertificateContext', self._hLibCrypt32))
        self._fCertFreeCertificateContext        = ftCertFreeCertificateContext(('CertFreeCertificateContext', self._hLibCrypt32))
        self._fCertNameToStr                     = ftCertNameToStr(('CertNameToStrW', self._hLibCrypt32))
        self._fCertGetCertificateContextProperty = ftCertGetCertificateContextProperty(('CertGetCertificateContextProperty', self._hLibCrypt32))
        self._fCryptAcquireCertificatePrivateKey = ftCryptAcquireCertificatePrivateKey(('CryptAcquireCertificatePrivateKey', self._hLibCrypt32))
        self._fCertGetCertificateChain           = ftCertGetCertificateChain(('CertGetCertificateChain', self._hLibCrypt32))
        self._fCertVerifyCertificateChainPolicy  = ftCertVerifyCertificateChainPolicy(('CertVerifyCertificateChainPolicy', self._hLibCrypt32))
        self._fCertFreeCertificateChain          = ftCertFreeCertificateChain(('CertFreeCertificateChain', self._hLibCrypt32))
        self._fCryptSignMessage                  = ftCryptSignMessage(('CryptSignMessage', self._hLibCrypt32))
        self._fCryptVerifyDetachedMessageSignature = ftCryptVerifyDetachedMessageSignature(('CryptVerifyDetachedMessageSignature', self._hLibCrypt32))

#        self._f     = ft(('', self._hLibCrypt32))





