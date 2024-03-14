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
##    непосредственно связывание с библиотеками CryptoproCSP
##    для posix-систем (linux, главным образом)
##
#############################################################################


from ctypes import cdll, sizeof, c_void_p
import os.path

from .errors import ftFormatMessageA, ftGetLastError, ftSetLastError
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

__all__ = ( 'PosixCryptoProApiBindingMixin',
          )


class PosixCryptoProApiBindingMixin:
    u'''
        Настройка абстрактного API на конкретные библиотеки
    '''
    __32bitLibDir   = '/opt/cprocsp/lib/ia32'
    __64bitLibDir   = '/opt/cprocsp/lib/amd64'
    __librdrsupName = 'librdrsup.so'
    __libcapi10Name = 'libcapi10.so'
    __libcapi20Name = 'libcapi20.so'


    def __init__(self, version = ''):
        pointerSize = sizeof(c_void_p)
        if pointerSize == 8:
            libDir = self.__64bitLibDir
        elif pointerSize == 4:
            libDir = self.__32bitLibDir
        else:
            raise NotImplementedError('Path to CryptoPro libraries is not defined')

        librdrsupName = self.__librdrsupName
        libcapi10Name = self.__libcapi10Name
        libcapi20Name = self.__libcapi20Name
        if version:
            librdrsupName += '.' + version
            libcapi10Name += '.' + version
            libcapi20Name += '.' + version

        librdrsupPath = os.path.join(libDir, librdrsupName)
        libcapi10Path = os.path.join(libDir, libcapi10Name)
        libcapi20Path = os.path.join(libDir, libcapi20Name)

        self._hlibrdrsup = cdll.LoadLibrary(librdrsupPath)
        self._hlibcapi10 = cdll.LoadLibrary(libcapi10Path)
        self._hlibcapi20 = cdll.LoadLibrary(libcapi20Path)

        self._fGetLastError  = ftGetLastError(('GetLastError', self._hlibrdrsup))
        self._fSetLastError  = ftSetLastError(('SetLastError', self._hlibrdrsup))
        self._fFormatMessage = ftFormatMessageA(('FormatMessage', self._hlibrdrsup))

        self._fCryptEnumProviderTypes  = ftCryptEnumProviderTypesW(('CryptEnumProviderTypesW', self._hlibcapi10))
        self._fCryptEnumProviders      = ftCryptEnumProvidersW(('CryptEnumProvidersW', self._hlibcapi10))
        self._fCryptGetDefaultProvider = ftCryptGetDefaultProviderW(('CryptGetDefaultProviderW', self._hlibcapi10))

        self._fCryptAcquireContext     = ftCryptAcquireContext(('CryptAcquireContextW', self._hlibcapi10))
        self._fCryptReleaseContext     = ftCryptReleaseContext(('CryptReleaseContext', self._hlibcapi10))
        self._fCryptGetProvParam       = ftCryptGetProvParam(('CryptGetProvParam', self._hlibcapi10))
        self._fCryptSetProvParam       = ftCryptSetProvParam(('CryptSetProvParam', self._hlibcapi10))
        self._fCryptGenRandom          = ftCryptGenRandom(('CryptGenRandom', self._hlibcapi10))

        self._fCryptGenKey             = ftCryptGenKey(('CryptGenKey', self._hlibcapi10))
        self._fCryptDuplicateKey       = ftCryptDuplicateKey(('CryptDuplicateKey', self._hlibcapi10))
        self._fCryptGetUserKey         = ftCryptGetUserKey(('CryptGetUserKey', self._hlibcapi10))
        self._fCryptImportKey          = ftCryptImportKey(('CryptImportKey', self._hlibcapi10))
        self._fCryptGetKeyParam        = ftCryptGetKeyParam(('CryptGetKeyParam', self._hlibcapi10))
        self._fCryptSetKeyParam        = ftCryptSetKeyParam(('CryptSetKeyParam', self._hlibcapi10))
        self._fCryptExportKey          = ftCryptExportKey(('CryptExportKey', self._hlibcapi10))
        self._fCryptDestroyKey         = ftCryptDestroyKey(('CryptDestroyKey', self._hlibcapi10))

        self._fCryptCreateHash         = ftCryptCreateHash(('CryptCreateHash', self._hlibcapi10))
        self._fCryptDuplicateHash      = ftCryptDuplicateHash(('CryptDuplicateHash', self._hlibcapi10))
        self._fCryptHashData           = ftCryptHashData(('CryptHashData', self._hlibcapi10))
        self._fCryptGetHashParam       = ftCryptGetHashParam(('CryptGetHashParam', self._hlibcapi10))
        self._fCryptSignHash           = ftCryptSignHash(('CryptSignHashW', self._hlibcapi10))
        self._fCryptVerifySignature    = ftCryptVerifySignature(('CryptVerifySignatureW', self._hlibcapi10))
        self._fCryptDestroyHash        = ftCryptDestroyHash(('CryptDestroyHash', self._hlibcapi10))

        self._fCryptEncrypt            = ftCryptEncrypt(('CryptEncrypt', self._hlibcapi10))
        self._fCryptDecrypt            = ftCryptDecrypt(('CryptDecrypt', self._hlibcapi10))

        self._fCryptFindOIDInfo        = ftCryptFindOIDInfo(('CryptFindOIDInfo', self._hlibcapi10))

        self._fCertOpenStore                     = ftCertOpenStore(('CertOpenStore', self._hlibcapi20))
        self._fCertOpenSystemStore               = ftCertOpenSystemStoreW(('CertOpenSystemStoreW', self._hlibcapi20))
        self._fCertCloseStore                    = ftCertCloseStore(('CertCloseStore', self._hlibcapi20))
        self._fCryptImportPublicKeyInfo          = ftCryptImportPublicKeyInfo(('CryptImportPublicKeyInfo', self._hlibcapi20))
        self._fCertEnumCertificatesInStore       = ftCertEnumCertificatesInStore(('CertEnumCertificatesInStore', self._hlibcapi20))
        self._fCertCreateCertificateContext      = ftCertCreateCertificateContext(('CertCreateCertificateContext', self._hlibcapi20))
        self._fCertDuplicateCertificateContext   = ftCertDuplicateCertificateContext(('CertDuplicateCertificateContext', self._hlibcapi20))
        self._fCertFreeCertificateContext        = ftCertFreeCertificateContext(('CertFreeCertificateContext', self._hlibcapi20))
        self._fCertNameToStr                     = ftCertNameToStr(('CertNameToStrW', self._hlibcapi20))
        self._fCertGetCertificateContextProperty = ftCertGetCertificateContextProperty(('CertGetCertificateContextProperty', self._hlibcapi20))
        self._fCryptAcquireCertificatePrivateKey = ftCryptAcquireCertificatePrivateKey(('CryptAcquireCertificatePrivateKey', self._hlibcapi20))
        self._fCertGetCertificateChain           = ftCertGetCertificateChain(('CertGetCertificateChain', self._hlibcapi20))
        self._fCertVerifyCertificateChainPolicy  = ftCertVerifyCertificateChainPolicy(('CertVerifyCertificateChainPolicy', self._hlibcapi20))
        self._fCertFreeCertificateChain          = ftCertFreeCertificateChain(('CertFreeCertificateChain', self._hlibcapi20))
        self._fCryptSignMessage                  = ftCryptSignMessage(('CryptSignMessage', self._hlibcapi20))
        self._fCryptVerifyDetachedMessageSignature = ftCryptVerifyDetachedMessageSignature(('CryptVerifyDetachedMessageSignature', self._hlibcapi20))

#        self._f     = ft(('', self._hlibcapi20))

