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
##    непосредственно связывание с библиотеками ViPNetCSP
##    для posix-систем (linux, главным образом)
##
#############################################################################

u'''
Microsoft CryptoAPI:
 привязка ViPNet CSP для linux
'''
import os.path

from ctypes import cdll

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
                     ftCryptEnumProvidersA,
                     ftCryptGetUserKey,
                     ftCryptSetProvParam,
                     ftCryptGenRandom,
                     ftCryptEnumProviderTypesA,
                     ftCryptGetKeyParam,
                     ftCryptEncrypt,
                     ftCryptDecrypt,
                     ftCryptCreateHash,
                     ftCryptImportKey,
                     ftCryptExportKey,
                     ftCryptGetDefaultProviderA,
                     ftCryptSignHash,
                     ftCryptSetKeyParam,
                     ftCryptAcquireContext,
                     ftCryptDestroyKey,
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

__all__ = ( 'PosixViPNetApiBindingMixin',
          )


class PosixViPNetApiBindingMixin:
    u'''
        Настройка абстрактного API на конкретные библиотеки
    '''
    __libDir   = '/opt/itcs/lib'
    __libkernel32Name = 'libkernel32.so'
    __libadvapi32Name = 'libadvapi32.so'
    __libcrypt32Name  = 'libcrypt32.so'

    def __init__(self):
        libDir = self.__libDir

        libkernel32Name = self.__libkernel32Name
        libadvapi32Name = self.__libadvapi32Name
        libcrypt32Name  = self.__libcrypt32Name

        libkernel32Path = os.path.join(libDir, libkernel32Name)
        libadvapi32Path = os.path.join(libDir, libadvapi32Name)
        libcrypt32Path  = os.path.join(libDir, libcrypt32Name)

        self._hlibkernel32 = cdll.LoadLibrary(libkernel32Path)
        self._hlibadvapi32 = cdll.LoadLibrary(libadvapi32Path)
        self._hlibcrypt32  = cdll.LoadLibrary(libcrypt32Path)

        self._fGetLastError  = ftGetLastError(('GetLastError',     self._hlibkernel32))
        self._fSetLastError  = ftSetLastError(('SetLastError',     self._hlibkernel32))
        self._fFormatMessage = ftFormatMessageW(('FormatMessageW', self._hlibkernel32))

        self._fCryptEnumProviderTypes  = ftCryptEnumProviderTypesA(('CryptEnumProviderTypes',   self._hlibcrypt32))
        self._fCryptEnumProviders      = ftCryptEnumProvidersA(('CryptEnumProviders',           self._hlibcrypt32))
        self._fCryptGetDefaultProvider = ftCryptGetDefaultProviderA(('CryptGetDefaultProvider', self._hlibadvapi32))

        self._fCryptAcquireContext     = ftCryptAcquireContext(('CryptAcquireContextW',         self._hlibadvapi32))
        self._fCryptReleaseContext     = ftCryptReleaseContext(('CryptReleaseContext',          self._hlibadvapi32))
        self._fCryptGetProvParam       = ftCryptGetProvParam(('CryptGetProvParam',              self._hlibadvapi32))
        self._fCryptSetProvParam       = ftCryptSetProvParam(('CryptSetProvParam',              self._hlibadvapi32))
        self._fCryptGenRandom          = ftCryptGenRandom(('CryptGenRandom',                    self._hlibadvapi32))

        self._fCryptGenKey             = ftCryptGenKey(('CryptGenKey',                          self._hlibadvapi32))

        self._fCryptDuplicateKey       = ftCryptDuplicateKey(('CryptDuplicateKey',              self._hlibadvapi32))
        self._fCryptGetUserKey         = ftCryptGetUserKey(('CryptGetUserKey',                  self._hlibadvapi32))
        self._fCryptImportKey          = ftCryptImportKey(('CryptImportKey',                    self._hlibadvapi32))
        self._fCryptGetKeyParam        = ftCryptGetKeyParam(('CryptGetKeyParam',                self._hlibadvapi32))
        self._fCryptSetKeyParam        = ftCryptSetKeyParam(('CryptSetKeyParam',                self._hlibadvapi32))
        self._fCryptExportKey          = ftCryptExportKey(('CryptExportKey',                    self._hlibadvapi32))
        self._fCryptDestroyKey         = ftCryptDestroyKey(('CryptDestroyKey',                  self._hlibadvapi32))

        self._fCryptCreateHash         = ftCryptCreateHash(('CryptCreateHash',                  self._hlibadvapi32))
        self._fCryptDuplicateHash      = ftCryptDuplicateHash(('CryptDuplicateHash',            self._hlibadvapi32))
        self._fCryptHashData           = ftCryptHashData(('CryptHashData',                      self._hlibadvapi32))
        self._fCryptGetHashParam       = ftCryptGetHashParam(('CryptGetHashParam',              self._hlibadvapi32))
        self._fCryptSignHash           = ftCryptSignHash(('CryptSignHashW',                     self._hlibadvapi32))
        self._fCryptVerifySignature    = ftCryptVerifySignature(('CryptVerifySignatureW',       self._hlibadvapi32))
        self._fCryptDestroyHash        = ftCryptDestroyHash(('CryptDestroyHash',                self._hlibadvapi32))

        self._fCryptEncrypt            = ftCryptEncrypt(('CryptEncrypt',                        self._hlibadvapi32))
        self._fCryptDecrypt            = ftCryptDecrypt(('CryptDecrypt',                        self._hlibadvapi32))

        self._fCryptFindOIDInfo        = ftCryptFindOIDInfo(('CryptFindOIDInfo',                self._hlibcrypt32))

        self._fCertOpenStore                     = ftCertOpenStore(('CertOpenStore',            self._hlibcrypt32))
        self._fCertOpenSystemStore               = ftCertOpenSystemStoreW(('CertOpenSystemStore',self._hlibcrypt32))
        self._fCertCloseStore                    = ftCertCloseStore(('CertCloseStore',          self._hlibcrypt32))
        self._fCryptImportPublicKeyInfo          = ftCryptImportPublicKeyInfo(('CryptImportPublicKeyInfo', self._hlibcrypt32))
        self._fCertEnumCertificatesInStore       = ftCertEnumCertificatesInStore(('CertEnumCertificatesInStore', self._hlibcrypt32))
        self._fCertCreateCertificateContext      = ftCertCreateCertificateContext(('CertCreateCertificateContext', self._hlibcrypt32))
        self._fCertDuplicateCertificateContext   = ftCertDuplicateCertificateContext(('CertDuplicateCertificateContext', self._hlibcrypt32))
        self._fCertFreeCertificateContext        = ftCertFreeCertificateContext(('CertFreeCertificateContext', self._hlibcrypt32))
        self._fCertNameToStr                     = ftCertNameToStr(('CertNameToStrW', self._hlibcrypt32))
        self._fCertGetCertificateContextProperty = ftCertGetCertificateContextProperty(('CertGetCertificateContextProperty', self._hlibcrypt32))
        self._fCryptAcquireCertificatePrivateKey = ftCryptAcquireCertificatePrivateKey(('CryptAcquireCertificatePrivateKey', self._hlibcrypt32))
        self._fCertGetCertificateChain           = ftCertGetCertificateChain(('CertGetCertificateChain', self._hlibcrypt32))
        self._fCertVerifyCertificateChainPolicy  = ftCertVerifyCertificateChainPolicy(('CertVerifyCertificateChainPolicy', self._hlibcrypt32))
        self._fCertFreeCertificateChain          = ftCertFreeCertificateChain(('CertFreeCertificateChain', self._hlibcrypt32))
        self._fCryptSignMessage                  = ftCryptSignMessage(('CryptSignMessage', self._hlibcrypt32))
        self._fCryptVerifyDetachedMessageSignature = ftCryptVerifyDetachedMessageSignature(('CryptVerifyDetachedMessageSignature', self._hlibcrypt32))

#        self._f     = ft(('', self._hlibcapi20))

