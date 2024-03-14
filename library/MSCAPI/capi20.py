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
##    описание общей части CryptoAPI, вторая часть функций
##
#############################################################################

from ctypes import Union, Structure, addressof, cast, string_at, sizeof, create_string_buffer, c_char_p, c_void_p, c_size_t, POINTER
from .wintypes import PDWORD, FILETIME, LONG, DWORD, ULONG_PTR, LPCSTR, CAPIFUNCTYPE, HANDLE, PBOOL, LPCWSTR, LPWSTR, PBYTE, LPFILETIME, BOOL, LPSTR
from .capi10 import HCRYPTPROV, PHCRYPTPROV, PHCRYPTKEY
from .capi10 import ALG_ID

#############################################################################
#
# CAPI 2.0
#
#############################################################################

HCERTSTORE = ULONG_PTR
HCERTCHAINENGINE = HANDLE

# https://msdn.microsoft.com/en-us/library/aa381394(v=vs.85).aspx

PFN_CRYPT_ALLOC = CAPIFUNCTYPE(c_void_p, c_size_t)
PFN_CRYPT_FREE  = CAPIFUNCTYPE(None, c_void_p)

class CRYPT_ENCODE_PARA(Structure):
    _fields_ = (
                  ('cbSize',   DWORD),
                  ('pfnAlloc', PFN_CRYPT_ALLOC),
                  ('pfnFree',  PFN_CRYPT_FREE),
               )

CRYPT_DECODE_PARA = CRYPT_ENCODE_PARA
PCRYPT_ENCODE_PARA = POINTER(CRYPT_ENCODE_PARA)
PCRYPT_DECODE_PARA = PCRYPT_ENCODE_PARA

class allocator:
    def __init__(self):
        self.allocated = {}
        self.cep = CRYPT_ENCODE_PARA()
        self.cep.cbSize   = sizeof(self.cep)
        self.cep.pfnAlloc = PFN_CRYPT_ALLOC(self._alloc)
        self.cep.pfnFree  = PFN_CRYPT_FREE(self._free)

    def _alloc(self, size):
        if size:
            buffer = create_string_buffer(size)
            addr = addressof(buffer)
            self.allocated[ addr ] = buffer
            return addr
        else:
            return 0

    def _free(self, addr):
        if addr:
            if addr not in self.allocated:
                print '--- addr', hex(addr), '--- not found in allocated list'
            del self.allocated[addr]


# https://msdn.microsoft.com/en-us/library/aa381414(v=vs.85).aspx
class CRYPTOAPI_BLOB(Structure):
    _fields_ = (
                 ('cbData', DWORD),
                 ('pbData', PBYTE),
               )

    def _getData(self):
        return string_at(self.pbData, self.cbData)


    def _setData(self, data):
        self.pbData, self.cbData = cast(data, c_void_p), len(data) if data is not None else 0


    data = property(_getData, _setData)


PCRYPTOAPI_BLOB = POINTER(CRYPTOAPI_BLOB)

CRYPT_INTEGER_BLOB,  PCRYPT_INTEGER_BLOB  = CRYPTOAPI_BLOB, PCRYPTOAPI_BLOB
CRYPT_UINT_BLOB,     PCRYPT_UINT_BLOB     = CRYPTOAPI_BLOB, PCRYPTOAPI_BLOB
CRYPT_OBJID_BLOB,    PCRYPT_OBJID_BLOB    = CRYPTOAPI_BLOB, PCRYPTOAPI_BLOB
CERT_NAME_BLOB,      PCERT_NAME_BLOB      = CRYPTOAPI_BLOB, PCRYPTOAPI_BLOB
CERT_RDN_VALUE_BLOB, PCERT_RDN_VALUE_BLOB = CRYPTOAPI_BLOB, PCRYPTOAPI_BLOB
CERT_BLOB,           PCERT_BLOB           = CRYPTOAPI_BLOB, PCRYPTOAPI_BLOB
CRL_BLOB,            PCRL_BLOB            = CRYPTOAPI_BLOB, PCRYPTOAPI_BLOB
DATA_BLOB,           PDATA_BLOB           = CRYPTOAPI_BLOB, PCRYPTOAPI_BLOB
CRYPT_DATA_BLOB,     PCRYPT_DATA_BLOB     = CRYPTOAPI_BLOB, PCRYPTOAPI_BLOB
CRYPT_HASH_BLOB,     PCRYPT_HASH_BLOB     = CRYPTOAPI_BLOB, PCRYPTOAPI_BLOB
CRYPT_DIGEST_BLOB,   PCRYPT_DIGEST_BLOB   = CRYPTOAPI_BLOB, PCRYPTOAPI_BLOB
CRYPT_DER_BLOB,      PCRYPT_DER_BLOB      = CRYPTOAPI_BLOB, PCRYPTOAPI_BLOB
CRYPT_ATTR_BLOB,     PCRYPT_ATTR_BLOB     = CRYPTOAPI_BLOB, PCRYPTOAPI_BLOB

#https://msdn.microsoft.com/en-us/library/aa381165(v=vs.85).aspx
class CRYPT_BIT_BLOB(Structure):
    _fields_ = (
                 ('cbData',      DWORD),
                 ('pbData',      PBYTE),
                 ('cUnusedBits', DWORD),
               )

PCRYPT_BIT_BLOB = POINTER(CRYPT_BIT_BLOB)


# https://msdn.microsoft.com/en-us/library/aa381133(v=vs.85).aspx
class CRYPT_ALGORITHM_IDENTIFIER(Structure):
    _fields_ = (
                 ('pszObjId',   LPSTR),
                 ('Parameters', CRYPT_OBJID_BLOB),
               )

# куча ObjId :)

# https://msdn.microsoft.com/en-us/library/aa381435(v=vs.85).aspx
# в варианте крипто-про :(

class CRYPT_OID_INFO(Structure):
    _fields_ = (
                   ('cbSize',              DWORD),
                   ('pszOID',              LPCSTR),
                   ('pwszName',            LPCWSTR),
                   ('dwGroupId',           DWORD),
                   ('AlgId',               ALG_ID),
                   ('ExtraInfo',           CRYPT_DATA_BLOB),
               )
PCRYPT_OID_INFO = POINTER(CRYPT_OID_INFO)


# https://msdn.microsoft.com/en-us/library/aa377463(v=vs.85).aspx
class CERT_PUBLIC_KEY_INFO(Structure):
    _fields_ = (
                 ('Algorithm', CRYPT_ALGORITHM_IDENTIFIER),
                 ('PublicKey', CRYPT_BIT_BLOB),
               )
PCERT_PUBLIC_KEY_INFO = POINTER(CERT_PUBLIC_KEY_INFO)


# https://msdn.microsoft.com/en-us/library/aa377195(v=vs.85).aspx
class CERT_EXTENSION(Structure):
    _fields_ = (
                 ('pszObjId',  LPSTR),
                 ('fCritical', BOOL),
                 ('Value',     CRYPT_OBJID_BLOB),
               )

PCERT_EXTENSION = POINTER(CERT_EXTENSION)


# https://msdn.microsoft.com/en-us/library/aa377200(v=vs.85).aspx
class CERT_INFO(Structure):
    _fields_ = (
                 ('dwVersion',            DWORD),
                 ('SerialNumber',         CRYPT_INTEGER_BLOB),
                 ('SignatureAlgorithm',   CRYPT_ALGORITHM_IDENTIFIER),
                 ('Issuer',               CERT_NAME_BLOB),
                 ('NotBefore',            FILETIME),
                 ('NotAfter',             FILETIME),
                 ('Subject',              CERT_NAME_BLOB),
                 ('SubjectPublicKeyInfo', CERT_PUBLIC_KEY_INFO),
                 ('IssuerUniqueId',       CRYPT_BIT_BLOB),
                 ('SubjectUniqueId',      CRYPT_BIT_BLOB),
                 ('cExtension',           DWORD),
                 ('rgExtension',          PCERT_EXTENSION),
               )

PCERT_INFO = POINTER(CERT_INFO)


# https://msdn.microsoft.com/en-us/library/aa377189(v=vs.85).aspx
class CERT_CONTEXT(Structure):
    _fields_ = (
                 ('dwCertEncodingType', DWORD),
                 ('pbCertEncoded',      PBYTE),
                 ('cbCertEncoded',      DWORD),
                 ('pCertInfo',          PCERT_INFO),
                 ('hCertStore',         HCERTSTORE),
               )

PCERT_CONTEXT = PCCERT_CONTEXT = POINTER(CERT_CONTEXT)

# https://msdn.microsoft.com/en-us/library/aa377205(v=vs.85).aspx
class _CERT_KEY_CONTEXT_union(Union):
    _fields_ = (
                 ('hCryptProv',        HCRYPTPROV),
                 ('hNCryptKey',        c_void_p),
               )

class CERT_KEY_CONTEXT(Structure):
    _anonymous_ = ('u', )
    _fields_ = (
                 ('cbSize',            DWORD),
                 ('u',                 _CERT_KEY_CONTEXT_union),
                 ('dwKeySpec',         DWORD),
               )


# https://msdn.microsoft.com/en-us/library/aa381493(v=vs.85).aspx
class CTL_USAGE(Structure):
    _fields_ = (
                  ('cUsageIdentifier',     DWORD ),
                  ('rgpszUsageIdentifier', POINTER(LPSTR)),
               )

CERT_ENHKEY_USAGE = CTL_USAGE
PCTL_USAGE = PCERT_ENHKEY_USAGE = POINTER(CTL_USAGE)


# https://msdn.microsoft.com/en-us/library/aa377593(v=vs.85).aspx
class CERT_USAGE_MATCH(Structure):
    _fields_ = (
                 ('dwType', DWORD),
                 ('Usage',  CERT_ENHKEY_USAGE),
               )

    def setUsage(self, dwType, keys):
        assert not self.Usage.rgpszUsageIdentifier
        self.dwType = dwType
        self.Usage.cUsageIdentifier = len(keys)
        self.Usage.rgpszUsageIdentifier = ( LPSTR*len(keys) )( *keys )


PCERT_USAGE_MATCH = POINTER(CERT_USAGE_MATCH)


# https://msdn.microsoft.com/en-us/library/aa377186(v=vs.85).aspx
class CERT_CHAIN_PARA(Structure):
    _fields_ = (
                 ('cbSize',                        DWORD),
                 ('RequestedUsage',                CERT_USAGE_MATCH),
                 ('RequestedIssuancePolicy',       CERT_USAGE_MATCH),
                 ('dwUrlRetrievalTimeout',         DWORD),
                 ('fCheckRevocationFreshnessTime', BOOL),
                 ('dwRevocationFreshnessTime',     DWORD),
# далее - свойства, появившиеся в Windows Vista и дальше.
# криптопро о этих данных ничего не знает :)
#                 ('pftCacheResync',                LPFILETIME), # 
#                 ('pStrongSignPara',               PCCERT_STRONG_SIGN_PARA),
#                 ('dwStrongSignFlags',             DWORD),
               )

    def __init__(self):
        self.cbSize = sizeof(self)

PCERT_CHAIN_PARA = POINTER(CERT_CHAIN_PARA)


# https://msdn.microsoft.com/en-us/library/aa377590(v=vs.85).aspx
class CERT_TRUST_STATUS(Structure):
    _fields_ = (
                 ('dwErrorStatus', DWORD),
                 ('dwInfoStatus',  DWORD),
               )


# https://msdn.microsoft.com/en-us/library/aa377182(v=vs.85).aspx
class CERT_CHAIN_CONTEXT(Structure):
    pass

PCERT_CHAIN_CONTEXT = PCCERT_CHAIN_CONTEXT = POINTER(CERT_CHAIN_CONTEXT)
PPCERT_SIMPLE_CHAIN = PPCCERT_CHAIN_CONTEXT = POINTER(PCCERT_CHAIN_CONTEXT)

CERT_CHAIN_CONTEXT._fields_ = (
                                ('cbSize',                      DWORD),
                                ('TrustStatus',                 CERT_TRUST_STATUS),
                                ('cChain',                      DWORD),
                                ('rgpChain',                    PPCERT_SIMPLE_CHAIN),
                                ('cLowerQualityChainContext',   DWORD),
                                ('rgpLowerQualityChainContext', PCCERT_CHAIN_CONTEXT),
                                ('fHasRevocationFreshnessTime', BOOL),
                                ('dwRevocationFreshnessTime',   DWORD),
                              )


# https://msdn.microsoft.com/en-us/library/aa377187(v=vs.85).aspx
class CERT_CHAIN_POLICY_PARA(Structure):
    _fields_ = (
                   ('cbSize',            DWORD),
                   ('dwFlags',           DWORD),
                   ('pvExtraPolicyPara', c_void_p),
               )
PCERT_CHAIN_POLICY_PARA = POINTER(CERT_CHAIN_POLICY_PARA)


# https://msdn.microsoft.com/en-us/library/aa377188(v=vs.85).aspx
class CERT_CHAIN_POLICY_STATUS(Structure):
    _fields_ = (
                   ('cbSize',              DWORD),
                   ('dwError',             DWORD),
                   ('lChainIndex',         LONG),
                   ('lElementIndex',       LONG),
                   ('pvExtraPolicyStatus', c_void_p),
               )
PCERT_CHAIN_POLICY_STATUS = POINTER(CERT_CHAIN_POLICY_STATUS)


# https://docs.microsoft.com/en-us/windows/desktop/api/wincrypt/ns-wincrypt-_crypt_attribute
class CRYPT_ATTRIBUTE(Structure):
    _fields_ = (
                   ('pszObjId',          LPSTR),
                   ('cValue',            DWORD),
                   ('rgValue',           PCRYPT_ATTR_BLOB),
               )
PCRYPT_ATTRIBUTE = POINTER(CRYPT_ATTRIBUTE)


# https://docs.microsoft.com/en-us/windows/desktop/api/wincrypt/ns-wincrypt-_crl_entry
class CRL_ENTRY(Structure):
                   ('SerialNumber',   CRYPT_INTEGER_BLOB),
                   ('RevocationDate', FILETIME),
                   ('cExtension',     DWORD),
                   ('rgExtension',    PCERT_EXTENSION),
PCRL_ENTRY = POINTER(CRL_ENTRY)


# https://docs.microsoft.com/en-us/windows/desktop/api/wincrypt/ns-wincrypt-_crl_info
class CRL_INFO(Structure):
    _fields_ = (
                   ('dwVersion',          DWORD),
                   ('SignatureAlgorithm', CRYPT_ALGORITHM_IDENTIFIER),
                   ('Issuer',             CERT_NAME_BLOB),
                   ('ThisUpdate',         FILETIME),
                   ('NextUpdate',         FILETIME),
                   ('cCRLEntry',          DWORD),
                   ('rgCRLEntry',         PCRL_ENTRY),
                   ('cExtension',         DWORD),
                   ('rgExtension',        PCERT_EXTENSION),
               )
PCRL_INFO = POINTER(CRL_INFO)


# https://docs.microsoft.com/en-us/windows/desktop/api/wincrypt/ns-wincrypt-_crl_context
class CRL_CONTEXT(Structure):
    _fields_ = (
                   ('dwCertEncodingType', DWORD),
                   ('pbCrlEncoded',       PBYTE),
                   ('cbCrlEncoded',       DWORD),
                   ('pCrlInfo',           PCRL_INFO),
                   ('hCertStore',         HCERTSTORE),
               )
PCCRL_CONTEXT = PCRL_CONTEXT = POINTER(CRL_CONTEXT)

# https://docs.microsoft.com/en-us/windows/desktop/api/wincrypt/ns-wincrypt-_crypt_sign_message_para
class CRYPT_SIGN_MESSAGE_PARA(Structure):
    _fields_ = (
                   ('cbSize',                   DWORD),
                   ('dwMsgEncodingType',        DWORD),
                   ('pSigningCert',             PCCERT_CONTEXT),
                   ('HashAlgorithm',            CRYPT_ALGORITHM_IDENTIFIER),
                   ('pvHashAuxInfo',            c_void_p),
                   ('cMsgCert',                 DWORD),
                   ('rgpMsgCert',               POINTER(PCCERT_CONTEXT)),
                   ('cMsgCrl',                  DWORD),
                   ('rgpMsgCrl',                POINTER(PCCRL_CONTEXT)),
                   ('cAuthAttr',                DWORD),
                   ('rgAuthAttr',               PCRYPT_ATTRIBUTE),
                   ('cUnauthAttr',              DWORD),
                   ('rgUnauthAttr',             PCRYPT_ATTRIBUTE),
                   ('dwFlags',                  DWORD),
                   ('dwInnerContentType',       DWORD),
#                   ('HashEncryptionAlgorithm',  CRYPT_ALGORITHM_IDENTIFIER),
#                   ('pvHashEncryptionAuxInfo',  c_void_p),
               )
PCRYPT_SIGN_MESSAGE_PARA = POINTER(CRYPT_SIGN_MESSAGE_PARA)


# https://docs.microsoft.com/en-us/windows/desktop/api/wincrypt/ns-wincrypt-_crypt_verify_message_para
class CRYPT_VERIFY_MESSAGE_PARA(Structure):
    _fields_ = (
                   ('cbSize',                   DWORD),
                   ('dwMsgAndCertEncodingType', DWORD),
                   ('hCryptProv',               HCRYPTPROV),
#                   ('pfnGetSignerCertificate',   PFN_CRYPT_GET_SIGNER_CERTIFICATE),
                   ('_pfnGetSignerCertificate',  c_void_p),
                   ('pvGetArg',                 c_void_p),
#                   ('pStrongSignPara',          PCCERT_STRONG_SIGN_PARA),
                   ('_pStrongSignPara',         c_void_p),
               )
PCRYPT_VERIFY_MESSAGE_PARA = POINTER(CRYPT_VERIFY_MESSAGE_PARA)


# https://msdn.microsoft.com/en-us/library/aa379938(v=vs.85).aspx
ftCryptFindOIDInfo       = CAPIFUNCTYPE(PCRYPT_OID_INFO, # result
                                        DWORD,       # _In_ DWORD dwKeyType,
                                        c_void_p,    # _In_ void  *pvKey,
                                        DWORD        # _In_ DWORD dwGroupId
                                       )


# https://msdn.microsoft.com/en-us/library/aa379911(v=vs.85).aspx
ftCryptDecodeObject =      CAPIFUNCTYPE(BOOL,        # result
                                        DWORD,       # _In_          DWORD  dwCertEncodingType,
                                        LPCSTR,      # _In_          LPCSTR lpszStructType,
                                        PBYTE,       # _In_    const BYTE   *pbEncoded,
                                        DWORD,       # _In_          DWORD  cbEncoded,
                                        DWORD,       # _In_          DWORD  dwFlags,
                                        c_void_p,    # _Out_         void   *pvStructInfo,
                                        PDWORD       # _Inout_       DWORD  *pcbStructInfo
                                       )

# https://msdn.microsoft.com/en-us/library/aa379912(v=vs.85).aspx
ftCryptDecodeObjectEx =    CAPIFUNCTYPE(BOOL,               # result
                                        DWORD,              # _In_          DWORD  dwCertEncodingType,
                                        LPCSTR,             # _In_          LPCSTR lpszStructType,
                                        PBYTE,              # _In_    const BYTE   *pbEncoded,
                                        DWORD,              # _In_          DWORD  cbEncoded,
                                        DWORD,              # _In_          DWORD  dwFlags,
                                        PCRYPT_DECODE_PARA, # _In_          PCRYPT_DECODE_PARA pDecodePara,
                                        c_void_p,           # _Out_         void   *pvStructInfo,
                                        PDWORD              # _Inout_       DWORD  *pcbStructInfo
                                       )

# https://msdn.microsoft.com/en-us/library/aa379921(v=vs.85).aspx
ftCryptEncodeObject =      CAPIFUNCTYPE(BOOL,        # result
                                        DWORD,       # _In_          DWORD              dwCertEncodingType,
                                        LPCSTR,      # _In_          LPCSTR             lpszStructType,
                                        c_char_p,    # _In_          const void         *pvStructInfo,
                                        PBYTE,       # _Out_         void               *pvEncoded,
                                        PDWORD       # _Inout_       DWORD              *pcbEncoded
                                       )


## https://msdn.microsoft.com/en-us/library/aa379922(v=vs.85).aspx
#ftCryptEncodeObjectEx =    CAPIFUNCTYPE(BOOL,        # result
#                                     DWORD,       # _In_          DWORD              dwCertEncodingType,
#                                     LPCSTR,      # _In_          LPCSTR             lpszStructType,
#                                     LPSTR,       # _In_    const void               *pvStructInfo,
#                                     DWORD,       # _In_          DWORD              dwFlags,
#                                     PCRYPT_ENCODE_PARA, # _In_   PCRYPT_ENCODE_PARA pEncodePara,
#                                     PBYTE,       # _Out_         void               *pvEncoded,
#                                     PDWORD       # _Inout_       DWORD              *pcbEncoded
#                                    )
#e: CRYPT_E_BAD_ENCODE   An error was encountered while encoding.
#e: ERROR_FILE_NOT_FOUND An encoding function could not be found for the specified dwCertEncodingType and lpszStructType.
#e: ERROR_MORE_DATA      If the buffer specified by the pvEncoded parameter is not large enough to hold the returned data, the function sets the ERROR_MORE_DATA code and stores the required buffer size, in bytes, in the variable pointed to by pcbEncoded.


# https://msdn.microsoft.com/en-us/library/aa380209(v=vs.85).aspx
ftCryptImportPublicKeyInfo=CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTPROV,  # _In_  HCRYPTPROV hProv,       // The handle of a CSP obtained with the CryptAcquireContext function.
                                        DWORD,       # _In_  DWORD                 dwCertEncodingType, // Specifies the encoding type used. usualy X509_ASN_ENCODING
                                        PCERT_PUBLIC_KEY_INFO, # _In_  PCERT_PUBLIC_KEY_INFO pInfo,    //
                                        PHCRYPTKEY   # _Out_ HCRYPTKEY             *phKey              // A pointer to a HCRYPTKEY value that receives the handle of the imported key.
                                       )
#e: ERROR_FILE_NOT_FOUND  An import function that can be installed or registered could not be found for the specified dwCertEncodingType and pInfo->Algorithm.pszObjId parameters.


# https://msdn.microsoft.com/en-us/library/aa376559(v=vs.85).aspx
ftCertOpenStore =          CAPIFUNCTYPE(HCERTSTORE,  # return
                                        LPCSTR,      # _In_       LPCSTR            lpszStoreProvider,
                                        DWORD,       # _In_       DWORD             dwMsgAndCertEncodingType,
                                        HCRYPTPROV,  # _In_       HCRYPTPROV_LEGACY hCryptProv,               // must be NULL?
                                        DWORD,       # _In_       DWORD             dwFlags,
                                        c_void_p     # _In_ const void              *pvPara
                                       )

# https://msdn.microsoft.com/en-us/library/aa376560(v=vs.85).aspx
ftCertOpenSystemStoreA =   CAPIFUNCTYPE(HCERTSTORE,  # return
                                        HCRYPTPROV,  # _In_ HCRYPTPROV_LEGACY hprov,               // must be NULL?
                                        LPCSTR       # _In_ LPCSTR            szSubsystemProtocol  // most valuable "MY"
                                       )

ftCertOpenSystemStoreW =   CAPIFUNCTYPE(HCERTSTORE,  # return
                                        HCRYPTPROV,  # _In_ HCRYPTPROV_LEGACY hprov,               // must be NULL?
                                        LPCWSTR      # _In_ LPTCSTR           szSubsystemProtocol  // most valuable "MY"
                                       )

# https://msdn.microsoft.com/en-us/library/aa376026(v=vs.85).aspx
ftCertCloseStore =         CAPIFUNCTYPE(BOOL,        # return
                                        HCERTSTORE,  # _In_ HCERTSTORE hCertStore,
                                        DWORD        # _In_ DWORD      dwFlags
                                       )

# https://msdn.microsoft.com/en-us/library/aa376050(v=vs.85).aspx
ftCertEnumCertificatesInStore = CAPIFUNCTYPE(PCCERT_CONTEXT, # return
                                             HCERTSTORE,     # _In_ HCERTSTORE     hCertStore,
                                             PCCERT_CONTEXT  # _In_ PCCERT_CONTEXT pPrevCertContext
                                            )

# https://msdn.microsoft.com/en-us/library/aa376033(v=vs.85).aspx
ftCertCreateCertificateContext= CAPIFUNCTYPE(PCCERT_CONTEXT, # return
                                             DWORD, #  _In_       DWORD dwCertEncodingType,
                                             PBYTE, #  _In_ const BYTE  *pbCertEncoded,
                                             DWORD  #  _In_       DWORD cbCertEncoded
                                            )

# https://msdn.microsoft.com/en-us/library/aa376045(v=vs.85).aspx
ftCertDuplicateCertificateContext = CAPIFUNCTYPE(PCCERT_CONTEXT, # return
                                                 PCCERT_CONTEXT  # _In_ PCCERT_CONTEXT pCertContext
                                                )

# https://msdn.microsoft.com/en-us/library/aa376075(v=vs.85).aspx
ftCertFreeCertificateContext      = CAPIFUNCTYPE(BOOL,           # return
                                                PCCERT_CONTEXT   # _In_ PCCERT_CONTEXT pCertContext
                                                )


#https://msdn.microsoft.com/en-us/library/aa376556(v=vs.85).aspx
ftCertNameToStr                   = CAPIFUNCTYPE(DWORD,          # return
                                                 DWORD,          # _In_  DWORD           dwCertEncodingType,
                                                 PCERT_NAME_BLOB,# _In_  PCERT_NAME_BLOB pName,
                                                 DWORD,          # _In_  DWORD           dwStrType,
                                                 LPWSTR,         # _Out_ LPTSTR          psz,
                                                 DWORD           # _In_  DWORD           csz
                                                )

##https://msdn.microsoft.com/en-us/library/aa376086(v=vs.85).aspx
#CertGetNameString в крипто-про практически не реализовано (см. http://www.cryptopro.ru/forum2/default.aspx?g=posts&t=5084 )

# https://msdn.microsoft.com/en-us/library/aa376079(v=vs.85).aspx
ftCertGetCertificateContextProperty=CAPIFUNCTYPE(BOOL,           # return
                                                 PCCERT_CONTEXT, # _In_    PCCERT_CONTEXT pCertContext,
                                                 DWORD,          # _In_    DWORD          dwPropId,
                                                 c_void_p,       # _Out_   void           *pvData,
                                                 PDWORD          # _Inout_ DWORD          *pcbData
                                                )


# https://msdn.microsoft.com/en-us/library/aa379885(v=vs.85).aspx
ftCryptAcquireCertificatePrivateKey=CAPIFUNCTYPE(BOOL,           # return
                                                 PCCERT_CONTEXT, # _In_     PCCERT_CONTEXT                  pCert,
                                                 DWORD,          # _In_     DWORD                           dwFlags,
                                                 c_void_p,       # _In_opt_ void                            *pvParameters,
                                                 PHCRYPTPROV,    # _Out_    HCRYPTPROV_OR_NCRYPT_KEY_HANDLE *phCryptProvOrNCryptKey,
                                                 PDWORD,         # _Out_    DWORD                           *pdwKeySpec,
                                                 PBOOL           # _Out_    BOOL                            *pfCallerFreeProvOrNCryptKey
                                                )


# https://msdn.microsoft.com/en-us/library/aa376078(v=vs.85).aspx
ftCertGetCertificateChain         = CAPIFUNCTYPE(BOOL,                # return
                                                 HCERTCHAINENGINE,    # _In_opt_ HCERTCHAINENGINE     hChainEngine,
                                                 PCCERT_CONTEXT,      # _In_     PCCERT_CONTEXT       pCertContext,
                                                 LPFILETIME,          # _In_opt_ LPFILETIME           pTime,
                                                 HCERTSTORE,          # _In_     HCERTSTORE           hAdditionalStore,
                                                 PCERT_CHAIN_PARA,    # _In_     PCERT_CHAIN_PARA     pChainPara,
                                                 DWORD,               # _In_     DWORD                dwFlags,
                                                 c_void_p,            # _In_     LPVOID               pvReserved,
                                                 PPCCERT_CHAIN_CONTEXT# _Out_    PCCERT_CHAIN_CONTEXT *ppChainContext
                                                )


# https://msdn.microsoft.com/en-us/library/aa377163(v=vs.85).aspx
ftCertVerifyCertificateChainPolicy= CAPIFUNCTYPE(BOOL,                # return
                                                 c_void_p,            #  _In_    LPCSTR                    pszPolicyOID,
                                                 PCCERT_CHAIN_CONTEXT,#  _In_    PCCERT_CHAIN_CONTEXT      pChainContext,
                                                 PCERT_CHAIN_POLICY_PARA,  #  _In_    PCERT_CHAIN_POLICY_PARA   pPolicyPara,
                                                 PCERT_CHAIN_POLICY_STATUS #  _Inout_ PCERT_CHAIN_POLICY_STATUS pPolicyStatus
                                                )

# https://msdn.microsoft.com/en-us/library/aa376073(v=vs.85).aspx
ftCertFreeCertificateChain        = CAPIFUNCTYPE(None,                # return
                                                 PCCERT_CHAIN_CONTEXT # _In_ PCCERT_CHAIN_CONTEXT pChainContext
                                                )

# https://docs.microsoft.com/en-us/windows/desktop/api/wincrypt/nf-wincrypt-cryptsignmessage
ftCryptSignMessage                = CAPIFUNCTYPE(BOOL,                     # return
                                                 PCRYPT_SIGN_MESSAGE_PARA, # _In_    PCRYPT_SIGN_MESSAGE_PARA pSignPara,
                                                 BOOL,                     # _In_    BOOL                     fDetachedSignature,
                                                 DWORD,                    # _In_    DWORD                    cToBeSigned,
                                                 POINTER(c_char_p),        # _In_    BYTE * []                rgpbToBeSigned,
                                                 PDWORD,                   # _in_    DWORD []                 rgcbToBeSigned,
                                                 PBYTE,                    # _In_    BYTE                     *pbSignedBlob,
                                                 PDWORD                    # _InOut_ DWORD                    *pcbSignedBlob
                                                )

# https://docs.microsoft.com/en-us/windows/desktop/api/wincrypt/nf-wincrypt-cryptverifydetachedmessagesignature
ftCryptVerifyDetachedMessageSignature = CAPIFUNCTYPE(BOOL,                       # return
                                                     PCRYPT_VERIFY_MESSAGE_PARA, # _In_          PCRYPT_VERIFY_MESSAGE_PARA pVerifyPara,
                                                     DWORD,                      # _In_          DWORD                      dwSignerIndex,
                                                     PBYTE,                      # _In_    const BYTE                       *pbDetachedSignBlob,
                                                     DWORD,                      # _In_          DWORD                      cbDetachedSignBlob,
                                                     DWORD,                      # _In_          DWORD                      cToBeVerified,
                                                     POINTER(c_char_p),          # _in_          const BYTE * []            rgpbToVerified,
                                                     PDWORD,                     # _In_          DWORD []                   rgcbToBeVerified,
                                                     POINTER(PCCERT_CONTEXT)     # _Out_         PCCERT_CONTEXT             *ppSignerCert
                                                    )
