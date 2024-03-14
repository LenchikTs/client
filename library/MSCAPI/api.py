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
##    описание общей части CryptoAPI
##
#############################################################################


import hashlib
import re

from collections import namedtuple
from ctypes import (
                    addressof,
                    byref,
                    cast,
                    c_char_p,
                    create_string_buffer,
                    create_unicode_buffer,
                    c_void_p,
                    c_wchar_p,
                    memmove,
                    pointer,
                    POINTER,
                    sizeof,
                    string_at,
                    Structure,
                   )
from wintypes import WORD, BYTE, BOOL, DWORD
from oids   import (
                    getKeyOidName,
                    getHashOidByKeyOid,
                   )
from errors import (
                    ERROR_NO_MORE_ITEMS,
                    NTE_BAD_SIGNATURE,
                    MSCAPIError,
                    findErrorName,
                    ftFormatMessageA,
                    ftFormatMessageW,
                   )
from capi10 import (
                    ALG_ID,
                    HCRYPTHASH,
                    HCRYPTKEY,
                    HCRYPTPROV,
                    PROV_ENUMALGS,
                    PROV_ENUMALGS_EX,

                    ftCryptEnumProvidersA,
                    ftCryptEnumProvidersW,
                    ftCryptEnumProviderTypesA,
                    ftCryptEnumProviderTypesW,
                    ftCryptGetDefaultProviderA,
                    ftCryptGetDefaultProviderW,
                   )
from capi20 import (
                    CERT_CHAIN_PARA,
                    CERT_CHAIN_POLICY_PARA,
                    CERT_CHAIN_POLICY_STATUS,
                    CRYPT_DATA_BLOB,
                    CRYPT_SIGN_MESSAGE_PARA,
                    CRYPT_VERIFY_MESSAGE_PARA,
                    PCCERT_CHAIN_CONTEXT,
                    PCCERT_CONTEXT,
                   )


# для удобства просмотра результатов CryptEnum.*:
ProviderTypeDescr = namedtuple('ProviderTypeDescr', ('type', 'name'))
ProviderDescr     = namedtuple('ProviderDescr',     ('type', 'name'))
AlgDescr          = namedtuple('AlgDescr',          ('algId', 'name', 'bitLen'))
AlgDescrEx        = namedtuple('AlgDescrEx',        ('algId', 'name', 'longName', 'defaultLen', 'minLen', 'maxLen', 'protocols'))


class AbstractApi(object):
    ####################################################################
    #
    # CAPI 1.0
    #
    ####################################################################

    # всякие константы, потребные для этого протокола:

    # алгоритмы кодируются как тройка класс - тип - subId
    # классы алгоритмов
    ALG_CLASS_ANY          =  (0)
    ALG_CLASS_SIGNATURE    =  (1 << 13)
    ALG_CLASS_MSG_ENCRYPT  =  (2 << 13)
    ALG_CLASS_DATA_ENCRYPT =  (3 << 13)
    ALG_CLASS_HASH         =  (4 << 13)
    ALG_CLASS_KEY_EXCHANGE =  (5 << 13)
    ALG_CLASS_ALL          =  (7 << 13)

    # типы алгоритмов
    ALG_TYPE_ANY           =  (0)
    ALG_TYPE_DSS           =  (1 << 9)
    ALG_TYPE_RSA           =  (2 << 9)
    ALG_TYPE_BLOCK         =  (3 << 9)
    ALG_TYPE_STREAM        =  (4 << 9)
    ALG_TYPE_DH            =  (5 << 9)
    ALG_TYPE_SECURECHANNEL =  (6 << 9)

    ALG_SID_ANY                     = 0

    # Some RSA sub-ids
    ALG_SID_RSA_ANY                 = 0
    ALG_SID_RSA_PKCS                = 1
    ALG_SID_RSA_MSATWORK            = 2
    ALG_SID_RSA_ENTRUST             = 3
    ALG_SID_RSA_PGP                 = 4

    # Some DSS sub-ids
    ALG_SID_DSS_ANY                 = 0
    ALG_SID_DSS_PKCS                = 1
    ALG_SID_DSS_DMS                 = 2
    ALG_SID_ECDSA                   = 3

    # Block cipher sub ids
    # DES sub_ids
    ALG_SID_DES                     = 1
    ALG_SID_3DES                    = 3
    ALG_SID_DESX                    = 4
    ALG_SID_IDEA                    = 5
    ALG_SID_CAST                    = 6
    ALG_SID_SAFERSK64               = 7
    ALG_SID_SAFERSK128              = 8
    ALG_SID_3DES_112                = 9
    ALG_SID_CYLINK_MEK              = 12
    ALG_SID_RC5                     = 13
    ALG_SID_AES_128                 = 14
    ALG_SID_AES_192                 = 15
    ALG_SID_AES_256                 = 16
    ALG_SID_AES                     = 17

    # Fortezza sub-ids
    ALG_SID_SKIPJACK                = 10
    ALG_SID_TEK                     = 11

    # RC2 sub-ids
    ALG_SID_RC2                     = 2

    # Stream cipher sub-ids
    ALG_SID_RC4                     = 1
    ALG_SID_SEAL                    = 2

    # Diffie-Hellman sub-ids
    ALG_SID_DH_SANDF                = 1
    ALG_SID_DH_EPHEM                = 2
    ALG_SID_AGREED_KEY_ANY          = 3
    ALG_SID_KEA                     = 4
    ALG_SID_ECDH                    = 5

    # Hash sub ids
    ALG_SID_MD2                     = 1
    ALG_SID_MD4                     = 2
    ALG_SID_MD5                     = 3
    ALG_SID_SHA                     = 4
    ALG_SID_SHA1                    = 4
    ALG_SID_MAC                     = 5
    ALG_SID_RIPEMD                  = 6
    ALG_SID_RIPEMD160               = 7
    ALG_SID_SSL3SHAMD5              = 8
    ALG_SID_HMAC                    = 9
    ALG_SID_TLS1PRF                 = 10
    ALG_SID_HASH_REPLACE_OWF        = 11
    ALG_SID_SHA_256                 = 12
    ALG_SID_SHA_384                 = 13
    ALG_SID_SHA_512                 = 14

    # secure channel sub ids
    ALG_SID_SSL3_MASTER             = 1
    ALG_SID_SCHANNEL_MASTER_HASH    = 2
    ALG_SID_SCHANNEL_MAC_KEY        = 3
    ALG_SID_PCT1_MASTER             = 4
    ALG_SID_SSL2_MASTER             = 5
    ALG_SID_TLS1_MASTER             = 6
    ALG_SID_SCHANNEL_ENC_KEY        = 7

    # misc ECC sub ids
    ALG_SID_ECMQV                   = 1

    # И вот собственно, алгоритмы
    # не то чтобы я знал - "кто все эти люди", но выбрасывать жаалко :)
    CALG_MD2                = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_MD2)
    CALG_MD4                = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_MD4)
    CALG_MD5                = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_MD5)
    CALG_SHA                = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_SHA)
    CALG_SHA1               = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_SHA1)
    CALG_MAC                = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_MAC)
    CALG_RSA_SIGN           = (ALG_CLASS_SIGNATURE | ALG_TYPE_RSA | ALG_SID_RSA_ANY)
    CALG_DSS_SIGN           = (ALG_CLASS_SIGNATURE | ALG_TYPE_DSS | ALG_SID_DSS_ANY)
    CALG_NO_SIGN            = (ALG_CLASS_SIGNATURE | ALG_TYPE_ANY | ALG_SID_ANY)
    CALG_RSA_KEYX           = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_RSA | ALG_SID_RSA_ANY)
    CALG_DES                = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_DES)
    CALG_3DES_112           = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_3DES_112)
    CALG_3DES               = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_3DES)
    CALG_DESX               = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_DESX)
    CALG_RC2                = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_RC2)
    CALG_RC4                = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_STREAM | ALG_SID_RC4)
    CALG_SEAL               = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_STREAM | ALG_SID_SEAL)
    CALG_DH_SF              = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH | ALG_SID_DH_SANDF)
    CALG_DH_EPHEM           = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH | ALG_SID_DH_EPHEM)
    CALG_AGREEDKEY_ANY      = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH | ALG_SID_AGREED_KEY_ANY)
    CALG_KEA_KEYX           = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH | ALG_SID_KEA)
    CALG_HUGHES_MD5         = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_ANY | ALG_SID_MD5)
    CALG_SKIPJACK           = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_SKIPJACK)
    CALG_TEK                = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_TEK)
    CALG_CYLINK_MEK         = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_CYLINK_MEK)
    CALG_SSL3_SHAMD5        = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_SSL3SHAMD5)
    CALG_SSL3_MASTER        = (ALG_CLASS_MSG_ENCRYPT|ALG_TYPE_SECURECHANNEL|ALG_SID_SSL3_MASTER)
    CALG_SCHANNEL_MASTER_HASH = (ALG_CLASS_MSG_ENCRYPT | ALG_TYPE_SECURECHANNEL | ALG_SID_SCHANNEL_MASTER_HASH)
    CALG_SCHANNEL_MAC_KEY   = (ALG_CLASS_MSG_ENCRYPT | ALG_TYPE_SECURECHANNEL | ALG_SID_SCHANNEL_MAC_KEY)
    CALG_SCHANNEL_ENC_KEY   = (ALG_CLASS_MSG_ENCRYPT | ALG_TYPE_SECURECHANNEL | ALG_SID_SCHANNEL_ENC_KEY)
    CALG_PCT1_MASTER        = (ALG_CLASS_MSG_ENCRYPT | ALG_TYPE_SECURECHANNEL | ALG_SID_PCT1_MASTER)
    CALG_SSL2_MASTER        = (ALG_CLASS_MSG_ENCRYPT | ALG_TYPE_SECURECHANNEL | ALG_SID_SSL2_MASTER)
    CALG_TLS1_MASTER        = (ALG_CLASS_MSG_ENCRYPT | ALG_TYPE_SECURECHANNEL | ALG_SID_TLS1_MASTER)
    CALG_RC5                = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_RC5)
    CALG_HMAC               = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_HMAC)
    CALG_TLS1PRF            = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_TLS1PRF)
    CALG_HASH_REPLACE_OWF   = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_HASH_REPLACE_OWF)
    CALG_AES_128            = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_AES_128)
    CALG_AES_192            = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_AES_192)
    CALG_AES_256            = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_AES_256)
    CALG_AES                = (ALG_CLASS_DATA_ENCRYPT | ALG_TYPE_BLOCK | ALG_SID_AES)
    CALG_SHA_256            = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_SHA_256)
    CALG_SHA_384            = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_SHA_384)
    CALG_SHA_512            = (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_SHA_512)
    CALG_ECDH               = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_DH | ALG_SID_ECDH)
    CALG_ECMQV              = (ALG_CLASS_KEY_EXCHANGE | ALG_TYPE_ANY | ALG_SID_ECMQV)
    CALG_ECDSA              = (ALG_CLASS_SIGNATURE | ALG_TYPE_DSS | ALG_SID_ECDSA)

    # dwFlags для CryptGetDefaultProvider:
    CRYPT_MACHINE_DEFAULT = 0x00000001 # Returns the computer default CSP of the specified type.
    CRYPT_USER_DEFAULT    = 0x00000002 # Returns the user-context default CSP of the specified type.

    # dwFlags для CryptAcquireContext:
    CRYPT_VERIFYCONTEXT              = 0xF0000000 # This option is intended for applications that are using ephemeral keys, or applications that do not require access to persisted private keys, such as applications that perform only hashing, encryption, and digital signature verification.
    CRYPT_NEWKEYSET                  = 0x00000008 # Creates a new key container with the name specified by pszContainer. If pszContainer is NULL, a key container with the default name is created.
    CRYPT_DELETEKEYSET               = 0x00000010 # Delete the key container specified by pszContainer.
    CRYPT_MACHINE_KEYSET             = 0x00000020 # As opposition to ddfault user keys
    CRYPT_SILENT                     = 0x00000040 # CRYPT_SILENT is intended for use with applications for which the UI cannot be displayed by the CSP.
    CRYPT_DEFAULT_CONTAINER_OPTIONAL = 0x00000080 # Obtains a context for a smart card CSP that can be used for hashing and symmetric key operations but cannot be used for any operation that requires authentication to a smart card using a PIN.


    # dwflags для CryptGetProvParam:
    # The following values are defined for use with PP_ENUMALGS, PP_ENUMALGS_EX, and PP_ENUMCONTAINERS.
    CRYPT_FIRST                      = 1 # Retrieve the first element in the enumeration. This has the same effect as resetting the enumerator.
    CRYPT_NEXT                       = 2 # Retrieve the next element in the enumeration. When there are no more elements to retrieve, this function will fail and set the last error to ERROR_NO_MORE_ITEMS.

    # dwFlags definitions for CryptSignHash and CryptVerifySignature
    CRYPT_NOHASHOID                  = 0x00000001
    CRYPT_TYPE2_FORMAT               = 0x00000002
    CRYPT_X931_FORMAT                = 0x00000004

    # параметры CryptGetProvParam
    # пригодилось -
    PP_ENUMALGS            =  1 # A PROV_ENUMALGS structure that contains information about one algorithm supported by the CSP being queried.
    PP_ENUMALGS_EX         = 22 # A PROV_ENUMALGS_EX structure that contains information about one algorithm supported by the CSP being queried. The structure returned contains more information about the algorithm than the structure returned for PP_ENUMALGS.
    PP_ENUMCONTAINERS      =  2 # The name of one of the key containers maintained by the CSP in the form of a null-terminated CHAR string.
    PP_NAME                =  4 # The name of the CSP in the form of a null-terminated CHAR string. This string is identical to the one passed in the pszProvider parameter of the CryptAcquireContext function to specify that the current CSP be used.
    PP_VERSION             =  5 # The version number of the CSP. The least significant byte contains the minor version number and the next most significant byte the major version number. Version 2.0 is represented as 0x00000200. To maintain backward compatibility with earlier versions of the Microsoft Base Cryptographic Provider and the Microsoft Enhanced Cryptographic Provider, the provider names retain the "v1.0" designation in later versions.
    PP_CONTAINER           =  6 # The name of the current key container as a null-terminated CHAR string. This string is exactly the same as the one passed in the pszContainer parameter of the CryptAcquireContext function to specify the key container to use. The pszContainer parameter can be read to determine the name of the default key container.
    PP_KEYSET_TYPE         = 27 # Determines whether the hProv parameter is a computer key set. The pbData parameter must be a DWORD; the DWORD will be set to the CRYPT_MACHINE_KEYSET flag if that flag was passed to the CryptAcquireContext function.
    PP_UNIQUE_CONTAINER    = 36 # The unique container name of the current key container in the form of a null-terminated CHAR string. For many CSPs, this name is the same name returned when the PP_CONTAINER value is used. The CryptAcquireContext function must work with this container name.
    PP_KEYSPEC             = 39 # Returns information about the key specifier values that the CSP supports. Key specifier values are joined in a logical OR and returned in the pbData parameter of the call as a DWORD. For example, the Microsoft Base Cryptographic Provider version 1.0 returns a DWORD value of AT_SIGNATURE | AT_KEYEXCHANGE.
    PP_SMARTCARD_READER    = 43 # Obtains the name of the smart card reader. The pbData parameter is the address of an ANSI character array that receives a null-terminated ANSI string that contains the name of the smart card reader. The size of this buffer, contained in the variable pointed to by the pdwDataLen parameter, must include the NULL terminator.

    PP_HASHOID             = 92 # Получает и/или устанавливает заданный в контейнере OID узла замены функции хэширования ГОСТ Р 34.11-94 для наследования криптографическими объектами
#    PP_CIPHEROID           = 93
#    PP_SIGNATUREOID        = 94
    PP_DHOID               = 95 # Получает и/или устанавливает заданный в контейнере OID параметров алгоритма Диффи-Хеллмана в зависимости от типа провайдера

#    # не пригодилось -
#    PP_ADMIN_PIN           = 31 # Returns the administrator personal identification number (PIN) in the pbData parameter as a LPSTR.
#    PP_APPLI_CERT          = 18 # This constant is not used.
#    PP_CHANGE_PASSWORD     =  7 # This constant is not used.
#    PP_CERTCHAIN           =  9 # Returns the certificate chain associated with the hProv handle. The returned certificate chain is X509_ASN_ENCODING encoded.
#    PP_CRYPT_COUNT_KEY_USE = 41 # Not implemented by Microsoft CSPs. This behavior may be implemented by other CSPs.
#    PP_ENUMELECTROOTS      = 26 # This constant is not used.
#    PP_ENUMEX_SIGNING_PROT = 40 # Indicates that the current CSP supports the dwProtocols member of the PROV_ENUMALGS_EX structure. If this function succeeds, the CSP supports the dwProtocols member of the PROV_ENUMALGS_EX structure. If this function fails with an NTE_BAD_TYPE error code, the CSP does not support the dwProtocols member.
#    PP_ENUMMANDROOTS       = 25 # This constant is not used.
#    PP_IMPTYPE             =  3 # A DWORD value that indicates how the CSP is implemented. For a table of possible values, see Remarks.
#    PP_KEY_TYPE_SUBTYPE    = 10 # This query is not used.
#    PP_KEYEXCHANGE_PIN     = 32 # Specifies that the key exchange PIN is contained in pbData. The PIN is represented as a null-terminated ASCII string.
#    PP_KEYSET_SEC_DESCR    =  8 # Retrieves the security descriptor for the key storage container. The pbData parameter is the address of a SECURITY_DESCRIPTOR structure that receives the security descriptor for the key storage container. The security descriptor is returned in self-relative format.
#    PP_KEYSTORAGE          = 17 # Returns a DWORD value of CRYPT_SEC_DESCR.
#    PP_KEYX_KEYSIZE_INC    = 35 # The number of bits for the increment length of AT_KEYEXCHANGE. This information is used with information returned in the PP_ENUMALGS_EX value. With the information returned when using PP_ENUMALGS_EX and PP_KEYX_KEYSIZE_INC, the valid key lengths for AT_KEYEXCHANGE can be determined. These key lengths can then be used with CryptGenKey. For example if a CSP enumerates CALG_RSA_KEYX (AT_KEYEXCHANGE) with a minimum key length of 512 bits and a maximum of 1024 bits, and returns the increment length as 64 bits, then valid key lengths are 512, 576, 640,… 1024.
#    PP_PROVTYPE            = 16 # A DWORD value that indicates the provider type of the CSP.
#    PP_ROOT_CERTSTORE      = 46 # Obtains the root certificate store for the smart card. This certificate store contains all of the root certificates that are stored on the smart card.
#    PP_SESSION_KEYSIZE     = 20 # The size, in bits, of the session key.
#    PP_SGC_INFO            = 37 # Used with server gated cryptography.
#    PP_SIG_KEYSIZE_INC     = 34 # The number of bits for the increment length of AT_SIGNATURE. This information is used with information returned in the PP_ENUMALGS_EX value. With the information returned when using PP_ENUMALGS_EX and PP_SIG_KEYSIZE_INC, the valid key lengths for AT_SIGNATURE can be determined. These key lengths can then be used with CryptGenKey.
#    PP_SIGNATURE_PIN       = 33 # Specifies that the key signature PIN is contained in pbData. The PIN is represented as a null-terminated ASCII string.
#    PP_SMARTCARD_GUID      = 45 # Obtains the identifier of the smart card. The pbData parameter is the address of a GUID structure that receives the identifier of the smart card.
#    PP_SYM_KEYSIZE         = 19 # The size of the symmetric key.
#    PP_UI_PROMPT           = 21 # This query is not used.
#    PP_USE_HARDWARE_RNG    = 38 # Indicates whether a hardware random number generator (RNG) is supported. When PP_USE_HARDWARE_RNG is specified, the function succeeds and returns TRUE if a hardware RNG is supported. The function fails and returns FALSE if a hardware RNG is not supported. If a RNG is supported, PP_USE_HARDWARE_RNG can be set in CryptSetProvParam to indicate that the CSP must exclusively use the hardware RNG for this provider context. When PP_USE_HARDWARE_RNG is used, the pbData parameter must be NULL and dwFlags must be zero.
#    PP_USER_CERTSTORE      = 42 # Obtains the user certificate store for the smart card. This certificate store contains all of the user certificates that are stored on the smart card. The certificates in this store are encoded by using PKCS_7_ASN_ENCODING or X509_ASN_ENCODING encoding and should contain the CERT_KEY_PROV_INFO_PROP_ID property.
####



    # параметры CryptGetKeyParam и CryptSetKeyParam
    KP_IV                   =  1 # Initialization vector
    KP_SALT                 =  2 # Salt value
    KP_PADDING              =  3 # Padding values
    KP_MODE                 =  4 # Mode of the cipher
    KP_MODE_BITS            =  5 # Number of bits to feedback
    KP_PERMISSIONS          =  6 # Key permissions DWORD
    KP_ALGID                =  7 # Key algorithm
    KP_BLOCKLEN             =  8 # Block size of the cipher
    KP_KEYLEN               =  9 # Length of key in bits
    KP_SALT_EX              = 10 # Length of salt in bytes
    KP_P                    = 11 # DSS/Diffie-Hellman P value
    KP_G                    = 12 # DSS/Diffie-Hellman G value
    KP_Q                    = 13 # DSS Q value
    KP_X                    = 14 # Diffie-Hellman X value
    KP_Y                    = 15 # Y value
    KP_RA                   = 16 # Fortezza RA value
    KP_RB                   = 17 # Fortezza RB value
    KP_INFO                 = 18 # for putting information into an RSA envelope
    KP_EFFECTIVE_KEYLEN     = 19 # setting and getting RC2 effective key length
    KP_SCHANNEL_ALG         = 20 # for setting the Secure Channel algorithms
    KP_CLIENT_RANDOM        = 21 # for setting the Secure Channel client random data
    KP_SERVER_RANDOM        = 22 # for setting the Secure Channel server random data
    KP_RP                   = 23
    KP_PRECOMP_MD5          = 24
    KP_PRECOMP_SHA          = 25
    KP_CERTIFICATE          = 26 # for setting Secure Channel certificate data (PCT1)
    KP_CLEAR_KEY            = 27 # for setting Secure Channel clear key data (PCT1)
    KP_PUB_EX_LEN           = 28
    KP_PUB_EX_VAL           = 29
    KP_KEYVAL               = 30
    KP_ADMIN_PIN            = 31
    KP_KEYEXCHANGE_PIN      = 32
    KP_SIGNATURE_PIN        = 33
    KP_PREHASH              = 34
    KP_ROUNDS               = 35
#    KP_OAEP_PARAMS          = 36 # for setting OAEP params on RSA keys
#    KP_CMS_KEY_INFO         = 37
#    KP_CMS_DH_KEY_INFO      = 38
#    KP_PUB_PARAMS           = 39 # for setting public parameters
#    KP_VERIFY_PARAMS        = 40 # for verifying DSA and DH parameters
#    KP_HIGHEST_VERSION      = 41 # for TLS protocol version setting
#    KP_GET_USE_COUNT        = 42 # for use with PP_CRYPT_COUNT_KEY_USE contexts
#    KP_PIN_ID               = 43
#    KP_PIN_INFO             = 44

    # KP_PADDING
    PKCS5_PADDING           =  1 # PKCS 5 (sec 6.2) padding method; padLen = 8 - len(clearText)%8; padding = chr(padLen)*padLen; encrypt(clearText + padding)
    RANDOM_PADDING          =  2 # padLen = (8 - len(clearText)%8)%8; padding=random_chars(padLen)
    ZERO_PADDING            =  3 # padLen = (8 - len(clearText)%8)%8; padding='\0'*padLen

    # KP_MODE
    CRYPT_MODE_CBC          =  1 # Cipher block chaining
    CRYPT_MODE_ECB          =  2 # Electronic code book
    CRYPT_MODE_OFB          =  3 # Output feedback mode
    CRYPT_MODE_CFB          =  4 # Cipher feedback mode
    CRYPT_MODE_CTS          =  5 # Ciphertext stealing mode
#    CRYPT_MODE_CBCI         =  6 # ANSI CBC Interleaved
#    CRYPT_MODE_CFBP         =  7 # ANSI CFB Pipelined
#    CRYPT_MODE_OFBP         =  8 # ANSI OFB Pipelined
#    CRYPT_MODE_CBCOFM       =  9 # ANSI CBC + OF Masking
#    CRYPT_MODE_CBCOFMI      = 10 # ANSI CBC + OFM Interleaved



    # KP_PERMISSIONS
    CRYPT_ENCRYPT           = 0x0001 # Allow encryption
    CRYPT_DECRYPT           = 0x0002 # Allow decryption
    CRYPT_EXPORT            = 0x0004 # Allow key to be exported
    CRYPT_READ              = 0x0008 # Allow parameters to be read
    CRYPT_WRITE             = 0x0010 # Allow parameters to be set
    CRYPT_MAC               = 0x0020 # Allow MACs to be used with key
    CRYPT_EXPORT_KEY        = 0x0040 # Allow key to be used for exporting keys
    CRYPT_IMPORT_KEY        = 0x0080 # Allow key to be used for importing keys
    CRYPT_ARCHIVE           = 0x0100 # Allow key to be exported at creation only

    # dwFlags для CryptGenKey
    CRYPT_EXPORTABLE        = 0x00000001 # If this flag is set, then the key can be transferred out of the CSP into a key BLOB by using the CryptExportKey function.
    CRYPT_USER_PROTECTED    = 0x00000002 # If this flag is set, the user is notified through a dialog box or another method when certain actions are attempting to use this key
    CRYPT_CREATE_SALT       = 0x00000004 # If this flag is set, then the key is assigned a random salt value automatically; If this flag is not set, then the key is given a salt value of zero.
#    CRYPT_UPDATE_KEY        = 0x00000008
    CRYPT_NO_SALT           = 0x00000010 # This flag specifies that a no salt value gets allocated for a forty-bit symmetric key. For more information, see Salt Value Functionality.
    CRYPT_PREGEN            = 0x00000040 # Если этот флаг установлен, то генерируется "пустая" ключевая пара обмена. Параметры этой ключевой пары должны быть установлены с использованием функции SetKeyParam().
#    CRYPT_RECIPIENT         = 0x00000010
#    CRYPT_INITIATOR         = 0x00000040
#    CRYPT_ONLINE            = 0x00000080
#    CRYPT_SF                = 0x00000100
#    CRYPT_CREATE_IV         = 0x00000200
#    CRYPT_KEK               = 0x00000400
#    CRYPT_DATA_KEY          = 0x00000800
#    CRYPT_VOLATILE          = 0x00001000
#    CRYPT_SGCKEY            = 0x00002000
#    CRYPT_ARCHIVABLE        = 0x00004000
#    CRYPT_FORCE_KEY_PROTECTION_HIGH = 0x00008000

    # dwBlobType для CryptExportKey
    SIMPLEBLOB           =  1 # Used to transport session keys.
    PUBLICKEYBLOB        =  6 # Used to transport public keys.
    PRIVATEKEYBLOB       =  7 # Used to transport public/private key pairs.
    PLAINTEXTKEYBLOB     =  8 # A PLAINTEXTKEYBLOB used to export any key supported by the CSP in use.
    OPAQUEKEYBLOB        =  9 # Used to store session keys in an Schannel CSP or any other vendor-specific format. OPAQUEKEYBLOBs are nontransferable and must be used within the CSP that generated the BLOB.
    SYMMETRICWRAPKEYBLOB = 11 # Used to export and import a symmetric key wrapped with another symmetric key. The actual wrapped key is in the format specified in the IETF RFC 3217 standard.

    # dwFlags для CryptExportKey
    CRYPT_BLOB_VER3     = 0x00000080 # This flag causes this function to export version 3 of a BLOB type.
    CRYPT_DESTROYKEY    = 0x00000004 # This flag destroys the original key in the OPAQUEKEYBLOB. This flag is available in Schannel CSPs only.
    CRYPT_OAEP          = 0x00000040 # This flag causes PKCS #1 version 2 formatting to be created with the RSA encryption and decryption when exporting SIMPLEBLOBs.
    CRYPT_SSL2_FALLBACK = 0x00000002 # The first eight bytes of the RSA encryption block padding must be set to 0x03 rather than to random data. This prevents version rollback attacks and is discussed in the SSL3 specification. This flag is available for Schannel CSPs only.
    CRYPT_Y_ONLY        = 0x00000001 # This flag is not used.


    # параметры CryptGetHashParam
    HP_ALGID    = 0x0001  # Hash algorithm
    HP_HASHVAL  = 0x0002  # Hash value
    HP_HASHSIZE = 0x0004  # Hash value size

    # dwKeySpec для CryptSignHash и CryptGetUserKey
    AT_KEYEXCHANGE = 1    # ??
    AT_SIGNATURE   = 2    # ??

    ####################################################################
    #
    # CAPI 2.0
    #
    ####################################################################


    # кодирование сертификатов:
    X509_ASN_ENCODING   = 0x00000001 # X.509-кодирование сертификатов.
    PKCS_7_ASN_ENCODING = 0x00010000 # PKCS#7-кодирование сообщений.


    # dwType для CertGetNameString ( https://msdn.microsoft.com/en-us/library/aa376086(v=vs.85).aspx )
    CERT_NAME_EMAIL_TYPE            = 1
    CERT_NAME_RDN_TYPE              = 2
    CERT_NAME_ATTR_TYPE             = 3
    CERT_NAME_SIMPLE_DISPLAY_TYPE   = 4
    CERT_NAME_FRIENDLY_DISPLAY_TYPE = 5
    CERT_NAME_DNS_TYPE              = 6
    CERT_NAME_URL_TYPE              = 7
    CERT_NAME_UPN_TYPE              = 8


    # имена полей Subject-a
    # https://msdn.microsoft.com/en-us/library/aa386991(v=vs.85).aspx
    szOID_COMMON_NAME              = '2.5.4.3'  # 'CommonName', 'CN': For user certificates, the person's full name.
                                                # For computer certificates, the fully qualified HostName/Path used in Domain Name System (DNS) lookups (for example, HostName.Example.com).
    szOID_SUR_NAME                 = '2.5.4.4'  # 'SurName', 'SN': Last name of the subject.
    szOID_DEVICE_SERIAL_NUMBER     = '2.5.4.5'  # 'DeviceSerialNumber': Device serial number.
    szOID_COUNTRY_NAME             = '2.5.4.6'  # 'Country', 'C': The subject's country or region. This is an X.500 two-character country/region code (for example US for United States or CA for Canada).
    szOID_LOCALITY_NAME            = '2.5.4.7'  # 'Locality', 'L': Name of the subject's city.
    szOID_STATE_OR_PROVINCE_NAME   = '2.5.4.8'  # 'State', 'ST', 'S': Full name of the subject's state or province (for example, California).
    szOID_STREET_ADDRESS           = '2.5.4.9'  # 'StreetAddress', 'Street': Subject's street address or PO Box.
    szOID_ORGANIZATION_NAME        = '2.5.4.10' # 'Org', 'O': Legal name of the subject's organization.
    szOID_ORGANIZATIONAL_UNIT_NAME = '2.5.4.11' # 'OrgUnit', 'OrganizationUnit', 'OrganizationalUnit', 'OU': Name of the subject's sub-organization or department.
    szOID_TITLE                    = '2.5.4.12' # 'Title', 'T': Title of individual who requested the certificate (optional).
    szOID_GIVEN_NAME               = '2.5.4.42' # 'GivenName', 'GN': First name of the subject.
    szOID_INITIALS                 = '2.5.4.43' # 'Initials', 'I': Initials of the subject (optional).
    szOID_RSA_emailAddr            = '1.2.840.113549.1.9.1' # 'EMail', 'E': Email address (for example, "someone@example.com").
    szOID_RSA_unstructName         = '1.2.840.113549.1.9.2' # 'UnstructuredName': Unstructured name.
    szOID_RSA_unstructAddr         = '1.2.840.113549.1.9.8' # 'UnstructuredAddress': Unstructured address.

    szOID_DOMAIN_COMPONENT         = '0.9.2342.19200300.100.1.25' # 'DomainComponent': Component of a Domain Name System (DNS) name.

    szOID_INN                      = '1.2.643.3.131.1.1' # 'INN'   : ИНН
    szOID_OGRN                     = '1.2.643.100.1'     # 'OGRN'  : ОГРН
    szOID_SNILS                    = '1.2.643.100.3'     # 'SNILS' : СНИЛС
    szOID_OGRNIP                   = '1.2.643.100.5'     # 'OGRNIP': ОГРН ИП

    # спецификации формата для CertNameToStr
    CERT_SIMPLE_NAME_STR           = 1
    CERT_OID_NAME_STR              = 2
    CERT_X500_NAME_STR             = 3

    # идентификаторы свойств для CertGetCertificateContextProperty
    CERT_KEY_PROV_HANDLE_PROP_ID  =  1
    CERT_KEY_PROV_INFO_PROP_ID    =  2
    CERT_SHA1_HASH_PROP_ID        =  3
    CERT_MD5_HASH_PROP_ID         =  4
    CERT_KEY_CONTEXT_PROP_ID      =  5
    CERT_KEY_SPEC_PROP_ID         =  6

    # dwFlags для CryptAcquireCertificatePrivateKey
    CRYPT_ACQUIRE_CACHE_FLAG         = 0x00000001
    CRYPT_ACQUIRE_USE_PROV_INFO_FLAG = 0x00000002
    CRYPT_ACQUIRE_COMPARE_KEY_FLAG   = 0x00000004
    CRYPT_ACQUIRE_SILENT_FLAG        = 0x00000040


    #CERT_USAGE_MATCH.dwType
    USAGE_MATCH_TYPE_AND = 0
    USAGE_MATCH_TYPE_OR  = 1


    szOID_PKIX_KP  =              "1.3.6.1.5.5.7.3"

    szOID_PKIX_KP_SERVER_AUTH =     "1.3.6.1.5.5.7.3.1" # Consistent key usage bits: DIGITAL_SIGNATURE, KEY_ENCIPHERMENT or KEY_AGREEMENT
    szOID_PKIX_KP_CLIENT_AUTH =     "1.3.6.1.5.5.7.3.2" # Consistent key usage bits: DIGITAL_SIGNATURE
    szOID_PKIX_KP_CODE_SIGNING =    "1.3.6.1.5.5.7.3.3" # Consistent key usage bits: DIGITAL_SIGNATURE
    szOID_PKIX_KP_EMAIL_PROTECTION= "1.3.6.1.5.5.7.3.4" # Consistent key usage bits: DIGITAL_SIGNATURE, NON_REPUDIATION and/or (KEY_ENCIPHERMENT or KEY_AGREEMENT)
    szOID_PKIX_KP_IPSEC_END_SYSTEM= "1.3.6.1.5.5.7.3.5" # Consistent key usage bits: DIGITAL_SIGNATURE and/or (KEY_ENCIPHERMENT or KEY_AGREEMENT)
    szOID_PKIX_KP_IPSEC_TUNNEL =    "1.3.6.1.5.5.7.3.6" # Consistent key usage bits: DIGITAL_SIGNATURE and/or (KEY_ENCIPHERMENT or KEY_AGREEMENT)
    szOID_PKIX_KP_IPSEC_USER =      "1.3.6.1.5.5.7.3.7" # Consistent key usage bits: DIGITAL_SIGNATURE and/or (KEY_ENCIPHERMENT or KEY_AGREEMENT)
    szOID_PKIX_KP_TIMESTAMP_SIGNING="1.3.6.1.5.5.7.3.8" # Consistent key usage bits: DIGITAL_SIGNATURE or NON_REPUDIATION

#
#// IKE (Internet Key Exchange) Intermediate KP for an IPsec end entity.
#// Defined in draft-ietf-ipsec-pki-req-04.txt, December 14, 1999.
##define szOID_IPSEC_KP_IKE_INTERMEDIATE "1.3.6.1.5.5.8.2.2"

    # dwFlags в CertGetCertificateChain:
    CERT_CHAIN_CACHE_END_CERT                  = 0x00000001 # When this flag is set, the end certificate is cached, which might speed up the chain-building process. By default, the end certificate is not cached, and it would need to be verified each time a chain is built for it.
    CERT_CHAIN_REVOCATION_CHECK_CACHE_ONLY     = 0x80000000 # Revocation checking only accesses cached URLs.
    CERT_CHAIN_REVOCATION_CHECK_OCSP_CERT      = 0x04000000 # This flag is used internally during chain building for an online certificate status protocol (OCSP) signer certificate to prevent cyclic revocation checks. During chain building, if the OCSP response is signed by an independent OCSP signer, then, in addition to the original chain build, there is a second chain built for the OCSP signer certificate itself. This flag is used during this second chain build to inhibit a recursive independent OCSP signer certificate. If the signer certificate contains the szOID_PKIX_OCSP_NOCHECK extension, revocation checking is skipped for the leaf signer certificate. Both OCSP and CRL checking are allowed. Windows Server 2003 and Windows XP:  This value is not supported.
    CERT_CHAIN_CACHE_ONLY_URL_RETRIEVAL        = 0x00000004 # Uses only cached URLs in building a certificate chain. The Internet and intranet are not searched for URL-based objects. Note  This flag is not applicable to revocation checking. Set CERT_CHAIN_REVOCATION_CHECK_CACHE_ONLY to use only cached URLs for revocation checking.
    CERT_CHAIN_DISABLE_PASS1_QUALITY_FILTERING = 0x00000040 # For performance reasons, the second pass of chain building only considers potential chain paths that have quality greater than or equal to the highest quality determined during the first pass. The first pass only considers valid signature, complete chain, and trusted roots to calculate chain quality. This flag can be set to disable this optimization and consider all potential chain paths during the second pass.
    CERT_CHAIN_DISABLE_MY_PEER_TRUST           = 0x00000800 # This flag is not supported. Certificates in the "My" store are never considered for peer trust.
    CERT_CHAIN_ENABLE_PEER_TRUST               = 0x00000400 # End entity certificates in the "TrustedPeople" store are trusted without performing any chain building. This function does not set the CERT_TRUST_IS_PARTIAL_CHAIN or CERT_TRUST_IS_UNTRUSTED_ROOT dwErrorStatus member bits of the ppChainContext parameter. Windows Server 2003 and Windows XP:  This flag is not supported.
    CERT_CHAIN_OPT_IN_WEAK_SIGNATURE           = 0x00010000 # Setting this flag indicates the caller wishes to opt into weak signature checks. This flag is available in the rollup update for each OS starting with Windows 7 and Windows Server 2008 R2.
    CERT_CHAIN_RETURN_LOWER_QUALITY_CONTEXTS   = 0x00000080 # The default is to return only the highest quality chain path. Setting this flag will return the lower quality chains. These are returned in the cLowerQualityChainContext and rgpLowerQualityChainContext fields of the chain context.
    CERT_CHAIN_DISABLE_AUTH_ROOT_AUTO_UPDATE   = 0x00000100 # Setting this flag inhibits the auto update of third-party roots from the Windows Update Web Server.
    CERT_CHAIN_REVOCATION_ACCUMULATIVE_TIMEOUT = 0x08000000 # When you set CERT_CHAIN_REVOCATION_ACCUMULATIVE_TIMEOUT and you also specify a value for the dwUrlRetrievalTimeout member of the CERT_CHAIN_PARA structure, the value you specify in dwUrlRetrievalTimeout represents the cumulative timeout across all revocation URL retrievals.
    CERT_CHAIN_TIMESTAMP_TIME                  = 0x00000200 # When this flag is set, pTime is used as the time stamp time to determine whether the end certificate was time valid. Current time can also be used to determine whether the end certificate remains time valid. All other certification authority (CA) and root certificates in the chain are checked by using current time and not pTime.
    CERT_CHAIN_DISABLE_AIA                     = 0x00002000 # Setting this flag explicitly turns off Authority Information Access (AIA) retrievals.

    CERT_CHAIN_REVOCATION_CHECK_END_CERT       = 0x10000000 # Revocation checking is done on the end certificate and only the end certificate.
    CERT_CHAIN_REVOCATION_CHECK_CHAIN          = 0x20000000 # Revocation checking is done on all of the certificates in every chain.
    CERT_CHAIN_REVOCATION_CHECK_CHAIN_EXCLUDE_ROOT = 0x40000000 # Revocation checking is done on all certificates in all of the chains except the root certificate.

    # Predefined verify chain policies (CertVerifyCertificateChainPolicy)
    CERT_CHAIN_POLICY_BASE              = 1 # Implements the base chain policy verification checks. The dwFlags member of the structure pointed to by pPolicyPara can be set to alter the default policy checking behavior.
#    CERT_CHAIN_POLICY_AUTHENTICODE      = 2 #
#    CERT_CHAIN_POLICY_AUTHENTICODE_TS   = 3
#    CERT_CHAIN_POLICY_SSL               = 4
#    CERT_CHAIN_POLICY_BASIC_CONSTRAINTS = 5
#    CERT_CHAIN_POLICY_NT_AUTH           = 6
#    CERT_CHAIN_POLICY_MICROSOFT_ROOT    = 7

    # Структуры.
    # структуры вроде как специфичны для крипто-про :(
    # Но мне пока других и не надо...

    GR3410_1_MAGIC = 0x3147414D # == 'MAG1'
    G28147_MAGIC   = 0x374a51fd

    # dwKeyType для CryptFindOIDInfo
    CRYPT_OID_INFO_OID_KEY                 = 1
    CRYPT_OID_INFO_NAME_KEY                = 2
    CRYPT_OID_INFO_ALGID_KEY               = 3
    CRYPT_OID_INFO_SIGN_KEY                = 4
    CRYPT_OID_INFO_PUBKEY_SIGN_KEY_FLAG    = 0x80000000
    CRYPT_OID_INFO_PUBKEY_ENCRYPT_KEY_FLAG = 0x40000000

    # store name
    SN_MY             = 'MY'
    SN_ADDRESS_BOOK   = 'AddressBook'
    SN_TRUSTED_PEOPLE = 'TrustedPeople'

    # store name set
    SNS_OWN_CERTIFICATES   = ( SN_MY, )
    SNS_OTHER_CERTIFICATES = ( SN_ADDRESS_BOOK, SN_TRUSTED_PEOPLE, )


    # lpszStoreProvider в CertOpenStore:
    CERT_STORE_PROV_PKCS7                  = c_char_p(5)

    # dwFlags в CertOpenStore:
    CERT_STORE_OPEN_EXISTING_FLAG          = 0x00004000
    CERT_STORE_CREATE_NEW_FLAG             = 0x00002000
    CERT_STORE_READONLY_FLAG               = 0x00008000

    ####################################################################

    def __init__(self, ansiEncoding=None):
        self._ansiEncoding = ansiEncoding

        self._fGetLastError            = None
        self._fSetLastError            = None
        self._fFormatMessage           = None

        # 1.0
        self._fCryptEnumProviderTypes  = None
        self._fCryptEnumProviders      = None
        self._fCryptGetDefaultProvider = None
        self._fCryptAcquireContext     = None
        self._fCryptGetProvParam       = None
        self._fCryptSetProvParam       = None
        self._fCryptGenRandom          = None

        self._fCryptGenKey             = None
        self._fCryptDuplicateKey       = None
        self._fCryptGetUserKey         = None
        self._fCryptImportKey          = None
        self._fCryptGetKeyParam        = None
        self._fCryptSetKeyParam        = None
        self._fCryptExportKey          = None
        self._fCryptDestroyKey         = None

        self._fCryptCreateHash         = None
        self._fCryptDuplicateHash      = None
        self._fCryptHashData           = None
        self._fCryptGetHashParam       = None
        self._fCryptSignHash           = None
        self._fCryptVerifySignature    = None
        self._fCryptDestroyHash        = None

        self._fCryptEncrypt            = None
        self._fCryptDecrypt            = None

        # 2.0
        self._fCryptFindOIDInfo        = None
        self._fCryptImportPublicKeyInfo= None

        self._fCertOpenStore           = None
        self._fCertOpenSystemStore     = None
        self._fCertCloseStore          = None

        self._fCertEnumCertificatesInStore     = None
        self._fCertCreateCertificateContext    = None
        self._fCertDuplicateCertificateContext = None
        self._fCertFreeCertificateContext      = None
        self._fCertNameToStr                   = None
        self._fCertGetCertificateContextProperty = None
        self._fCryptAcquireCertificatePrivateKey = None
        self._fCertGetCertificateChain           = None
        self._fCertVerifyCertificateChainPolicy  = None
        self._fCertFreeCertificateChain          = None
        self._fCryptSignMessage                  = None
        self._fCryptVerifyDetachedMessageSignature = None

    # фактории

    def Error(self, errorCode = None):
        if errorCode is None:
            errorCode = self._fGetLastError()
        errDescr = self.getErrorText(errorCode) or '[?]'
        errName  = findErrorName(errorCode) or 'UNKNOWN'
        message = '%s: %d (0x%08X) %s' % ( errName, errorCode, errorCode, errDescr )
        return MSCAPIError(errorCode, message)


    def PublicKeyBlob(self):
        return CPPublicKeyBlob(self)


    def SimpleBlob(self):
        return CPSimpleBlob(self)


    # low level

    def _acquireContext(self, flags, providerType, providerName, contaiterName):
        assert self._fCryptAcquireContext is not None

        hProvider = HCRYPTPROV()

        ok = self._fCryptAcquireContext( byref(hProvider),
                                         None if contaiterName is None else c_wchar_p(contaiterName),
                                         None if providerName  is None else c_wchar_p(providerName),
                                         providerType,
                                         flags )
        if not ok:
            raise self.Error()
        return hProvider.value


    def _acquireContextByCertContext(self, certContext):
        assert self._fCryptAcquireCertificatePrivateKey is not None
        hProvider = HCRYPTPROV()
#        dwKeySpec  = DWORD()
        fCallerFreeProv = BOOL()

        ok = self._fCryptAcquireCertificatePrivateKey(certContext,
                                                      0, # api.CRYPT_ACQUIRE_CACHE_FLAG, # | api.CRYPT_ACQUIRE_USE_PROV_INFO_FLAG,
                                                      None,
                                                      byref(hProvider),
                                                      None, # byref(dwKeySpec),
                                                      byref(fCallerFreeProv)
                                                     )
        if not ok:
            raise self.Error()
        return hProvider.value, fCallerFreeProv.value


    def _releaseContext(self, hProvider):
        assert self._fCryptReleaseContext is not None

        ok = self._fCryptReleaseContext(hProvider, 0)
        if not ok:
            raise self.Error()


    def _getProvParam(self, hProvider, dwParam, pbData, pdwDataLen, dwFlags):
        assert self._fGetLastError is not None
        assert self._fCryptGetProvParam is not None

        ok = self._fCryptGetProvParam(hProvider, dwParam, pbData, pdwDataLen, dwFlags)
        return 0 if ok else self._fGetLastError()


    def _CryptGenRandom(self, hProvider, buffLen):
        assert self._fCryptGenRandom is not None

        buff = create_string_buffer(buffLen)
        ok = self._fCryptGenRandom(hProvider, buffLen, buff)
        if not ok:
            raise self.Error()
        return buff.raw


    def _genKey(self, hProvider, algId, dwFlags):
        assert self._fGetLastError is not None
        assert self._fCryptGenKey is not None

        hKey = HCRYPTKEY()
        ok = self._fCryptGenKey(hProvider, algId, dwFlags, byref(hKey))
        if not ok:
            raise self.Error()
        return hKey.value


    def _getUserKey(self, hProvider, keySpec):
        assert self._fGetLastError is not None
        assert self._fCryptGetUserKey is not None

        hKey = HCRYPTKEY()
        ok = self._fCryptGetUserKey(hProvider, keySpec, byref(hKey))
        if not ok:
            raise self.Error()
        return hKey.value


    def _importKey(self, hProvider, pbData, dwDataLen, hPubKey, dwFlags):
        assert self._fGetLastError is not None
        assert self._fCryptImportKey is not None
        hKey = HCRYPTKEY()
        ok = self._fCryptImportKey(hProvider,
                                   pbData,
                                   dwDataLen,
                                   hPubKey,
                                   dwFlags,
                                   byref(hKey))
        if not ok:
            raise self.Error()
        return hKey.value


    def _importPubKeyInfo(self, hProvider, pubKeyInfo):
        assert self._fGetLastError is not None
        assert self._fCryptImportPublicKeyInfo is not None

        hKey = HCRYPTKEY()
        ok = self._fCryptImportPublicKeyInfo(hProvider,
                                             self.X509_ASN_ENCODING,
                                             byref(pubKeyInfo),
                                             byref(hKey))
        if not ok:
            raise self.Error()
        return hKey.value


    def _getKeyParam(self, hKey, dwParam, pbData, pdwDataLen):
        assert self._fGetLastError is not None
        assert self._fCryptGetKeyParam is not None

        ok = self._fCryptGetKeyParam(hKey, dwParam, pbData, pdwDataLen, 0)
        return 0 if ok else self._fGetLastError()


    def _setKeyParam(self, hKey, dwParam, pbData):
        assert self._fGetLastError is not None
        assert self._fCryptSetKeyParam is not None

        ok = self._fCryptSetKeyParam(hKey, dwParam, pbData, 0)
        return 0 if ok else self._fGetLastError()


    def _exportKey(self, hKey, hExpKey, dwBlobType, dwFlags, pbData, pdwDataLen):
        assert self._fGetLastError is not None
        assert self._fCryptExportKey is not None
        ok = self._fCryptExportKey(hKey, hExpKey, dwBlobType, dwFlags, pbData, pdwDataLen)
        if not ok:
            raise self.Error()
        return 0


    def _destroyKey(self, hKey):
        assert self._fGetLastError is not None
        assert self._fCryptDestroyKey is not None

        ok = self._fCryptDestroyKey(hKey)
        if not ok:
            raise self.Error()


    def _createHash(self, hProvider, algId, hKey=None):
        assert self._fGetLastError is not None
        assert self._fCryptCreateHash is not None

        hHash = HCRYPTHASH()
        ok = self._fCryptCreateHash(hProvider, algId, hKey, 0, byref(hHash))
        if not ok:
            raise self.Error()
        return hHash.value


    def _duplicateHash(self, hSourceHash):
        assert self._fGetLastError is not None
        assert self._fCryptDuplicateHash is not None

        hHash = HCRYPTHASH()
        ok = self._fCryptDuplicateHash(hSourceHash, None, 0, byref(hHash))
        if not ok:
            raise self.Error()
        return hHash.value


    def _hashData(self, hHash, data):
        assert self._fGetLastError is not None
        assert self._fCryptHashData is not None

#        b = bytes(data.encode('utf-8') if isinstance(data, unicode) else data)
        b = bytes(data)
        ok = self._fCryptHashData(hHash, c_char_p(b), len(b), 0)
        if not ok:
            raise self.Error()


    def _getHashParam(self, hHash, dwParam, pbData, pdwDataLen):
        assert self._fGetLastError is not None
        assert self._fCryptGetHashParam is not None

        ok = self._fCryptGetHashParam(hHash, dwParam, pbData, pdwDataLen, 0)
        if not ok:
            raise self.Error()


    def _signHash(self, hHash, dwKeySpec, dwFlags, pbSignature, pdwSignatureLen):
        assert self._fGetLastError is not None
        assert self._fCryptSignHash is not None
        ok = self._fCryptSignHash(hHash, dwKeySpec, None, dwFlags, pbSignature, pdwSignatureLen)
        if not ok:
            raise self.Error()


    def _verifySignature(self, hHash, pbSignature, pdwSignatureLen, hKey):
        assert self._fGetLastError is not None
        assert self._fCryptVerifySignature is not None

        ok = self._fCryptVerifySignature(hHash,
                                         pbSignature,
                                         pdwSignatureLen,
                                         hKey,
                                         None,
                                         0
                                        )

        if ok:
            return True
        errorCode = self._fGetLastError()
        if errorCode == NTE_BAD_SIGNATURE:
            return False
        raise self.Error(errorCode)


    def _destroyHash(self, hHash):
        assert self._fGetLastError is not None
        assert self._fCryptDestroyHash is not None

        ok = self._fCryptDestroyHash(hHash)
        if not ok:
            raise self.Error()


    def _closeStore(self, hStore, flags=0):
        assert self._fGetLastError is not None
        assert self._fCertCloseStore is not None

        ok = self._fCertCloseStore(hStore, flags)
        if not ok:
            raise self.Error()


    # high level

    def getErrorText(self, errorCode):
        assert self._fFormatMessage
        if isinstance(self._fFormatMessage, ftFormatMessageA):
            buff = create_string_buffer(2048)
        elif isinstance(self._fFormatMessage, ftFormatMessageW):
            buff = create_unicode_buffer(2048)
        else:
            raise TypeError('FormatMessage should be either ftFormatMessageA or ftFormatMessageW')

        ok = self._fFormatMessage(
            0x00001000, # FORMAT_MESSAGE_FROM_SYSTEM
            None,       #
            errorCode,  # returned by GetLastError()
            0x0400,     # MAKELANGID(LANG_NEUTRAL,SUBLANG_DEFAULT),
            buff,       #
            len(buff)-1,#
            None )
        if ok:
            return buff.value
        return None


    def listProviderTypes(self):
        assert self._fGetLastError is not None
        assert self._fCryptEnumProviderTypes is not None
        if isinstance(self._fCryptEnumProviderTypes, ftCryptEnumProviderTypesA):
            buffConstructor = create_string_buffer
            buffDecoder     = lambda s: s.decode(self._ansiEncoding)
        elif isinstance(self._fCryptEnumProviderTypes, ftCryptEnumProviderTypesW):
            buffConstructor = create_unicode_buffer
            buffDecoder     = lambda u: u
        else:
            raise TypeError('CryptEnumProviderTypes should be either ftCryptEnumProviderTypesA or ftCryptEnumProviderTypesW')
        result = []
        dwIndex = 0
        while True:
            dwType = DWORD(0)
            cbName = DWORD(0)
            ok = self._fCryptEnumProviderTypes(dwIndex,
                                               None,
                                               0,
                                               byref(dwType),
                                               None,
                                               byref(cbName)
                                              )
            if not ok:
                errorCode = self._fGetLastError()
                if  errorCode == ERROR_NO_MORE_ITEMS:
                    break;
                raise self.Error(errorCode)

            pszName = buffConstructor(cbName.value)
            ok = self._fCryptEnumProviderTypes(dwIndex,
                                               None,
                                               0,
                                               byref(dwType),
                                               pszName,
                                               byref(cbName))
            if not ok:
                raise self.Error()
            result.append( ProviderTypeDescr(int(dwType.value), buffDecoder(pszName.value)) )
            dwIndex += 1
        return result


    def listProviders(self):
        assert self._fGetLastError is not None
        assert self._fCryptEnumProviders is not None
        if isinstance(self._fCryptEnumProviders, ftCryptEnumProvidersA):
            buffConstructor = create_string_buffer
            buffDecoder     = lambda s: s.decode(self._ansiEncoding)
        elif isinstance(self._fCryptEnumProviders, ftCryptEnumProvidersW):
            buffConstructor = create_unicode_buffer
            buffDecoder     = lambda u: u
        else:
            raise TypeError('CryptEnumProviders should be either ftCryptEnumProvidersA or ftCryptEnumProvidersW')

        result = []
        dwIndex = 0
        while True:
            dwType = DWORD(0)
            cbName = DWORD(0)
            ok = self._fCryptEnumProviders(dwIndex,
                                           None,
                                           0,
                                           byref(dwType),
                                           None,
                                           byref(cbName)
                                          )
            if not ok:
                errorCode = self._fGetLastError()
                if  errorCode == ERROR_NO_MORE_ITEMS:
                    break;
                raise self.Error(errorCode)

            pszName = buffConstructor(cbName.value)
            ok = self._fCryptEnumProviders(dwIndex,
                                           None,
                                           0,
                                           byref(dwType),
                                           pszName,
                                           byref(cbName))
            if not ok:
                raise self.Error()
            result.append( ProviderDescr(int(dwType.value), buffDecoder(pszName.value)) )
            dwIndex += 1
        return result


    def getDefaultProvider(self, provType, machineDefault = False):
        assert self._fGetLastError is not None
        assert self._fCryptGetDefaultProvider is not None
        if isinstance(self._fCryptGetDefaultProvider, ftCryptGetDefaultProviderA):
            buffConstructor = create_string_buffer
            buffDecoder     = lambda s: s.decode(self._ansiEncoding)
        elif isinstance(self._fCryptGetDefaultProvider, ftCryptGetDefaultProviderW):
            buffConstructor = create_unicode_buffer
            buffDecoder     = lambda u: u
        else:
            raise TypeError('CryptGetDefaultProvider should be either ftCryptGetDefaultProviderA or ftCryptGetDefaultProviderW')

        flags = self.CRYPT_MACHINE_DEFAULT if machineDefault else self.CRYPT_USER_DEFAULT
        cbName = DWORD(0)
        ok = self._fCryptGetDefaultProvider(provType,
                                           None,
                                           flags,
                                           None,
                                           byref(cbName)
                                          )
        if not ok:
            raise self.Error()
        pszName = buffConstructor(cbName.value)
        ok = self._fCryptGetDefaultProvider(provType,
                                           None,
                                           flags,
                                           pszName,
                                           byref(cbName)
                                          )
        if not ok:
            raise self.Error()
        return buffDecoder(pszName.value)


    def provider(self, flags=0, providerType=0, providerName=None, containerName=None):
        return Provider(self, flags, providerType, providerName, containerName)


    def findAlgIdByOid(self, oid):
        assert self._fCryptFindOIDInfo is not None

        pOidInfo = self._fCryptFindOIDInfo( self.CRYPT_OID_INFO_OID_KEY, oid, 0)
        if pOidInfo:
            return pOidInfo.contents.AlgId
        else:
            return None


    def findOidByAlgId(self, algId):
        assert self._fCryptFindOIDInfo is not None

        aiAlgId = ALG_ID(algId)
        pOidInfo = self._fCryptFindOIDInfo( self.CRYPT_OID_INFO_ALGID_KEY, byref(aiAlgId), 0)
        if pOidInfo:
            return pOidInfo.contents.pszOID
        else:
            return None


    def signatureAsStore(self, signatureBytes):
        assert self._fGetLastError is not None
        assert self._fCertOpenStore is not None

        blob = CRYPT_DATA_BLOB()
        blob.data = signatureBytes

        result = self._fCertOpenStore(self.CERT_STORE_PROV_PKCS7,                        # lpszStoreProvider
                                      self.X509_ASN_ENCODING | self.PKCS_7_ASN_ENCODING, # dwEncodingType
                                      None,                                              # HCRYPTPROV_LEGACY hCryptProv
                                      0,                                                 # dwFlags
                                      byref(blob)                                        # *pvPara
                                     )
        if not result:
            raise self.Error()
        return CertStore(self, result)


    def systemStore(self, subsystemProtocol):
        assert self._fGetLastError is not None
        assert self._fCertOpenSystemStore is not None

        result = self._fCertOpenSystemStore(None, c_wchar_p(subsystemProtocol))
#        print result, type(result)
        if not result:
            raise self.Error()
        return CertStore(self, result)


    def cert(self, certBytes):
        assert self._fGetLastError is not None
        assert self._fCertCreateCertificateContext is not None

        pCertContext = self._fCertCreateCertificateContext(self.X509_ASN_ENCODING, c_char_p(certBytes), len(certBytes) )
        if not pCertContext:
            raise self.Error()
        return Cert(self, pCertContext)


    def findCertInStores(self,
                         storeNames,
                         sha1hex=None,
                         ogrn=None,
                         snils=None,
                         datetime=None,
                         keyOids=None,
                         weakOgrn=None, # желательно с этим ogrn, но не обязательно
                        ):
        if sha1hex:
            sha1hex = sha1hex.lower()

        result = None
        resultScore = None
        if type(storeNames) is list:
            tuple_of_tuples = tuple()
            for x in storeNames:
                tuple_of_tuples += tuple(x)
            storeNames = tuple_of_tuples
        for storeName in storeNames:
            with self.systemStore(storeName) as store:
                for cert in store.listCerts():
                    if (    (not sha1hex  or sha1hex == cert.sha1().encode('hex').lower())
                        and (not ogrn     or ogrn    == cert.ogrn())
                        and (not snils    or snils   == cert.snils())
                        and (not datetime or cert.notBefore() <= datetime <= cert.notAfter())
                        and (not keyOids  or cert.keyOid() in keyOids)
                       ):
                        if weakOgrn:
                            certOgrn = cert.ogrn()
                            if weakOgrn == certOgrn:
                                ogrnScore = 3 # с нужным orgn - лучше всего
                            elif not certOgrn:
                                ogrnScore = 2 # без orgn - тоже не слишком плохо
                            else:
                                ogrnScore = 1 # если ничего лучше не найдётся, то покатит
                        else:
                            ogrnScore = 0 # всё равно

                        certScore = ogrnScore, cert.notAfter()
                        if resultScore is None or resultScore < certScore:
                            result, resultScore = cert, certScore
        return result


    def createDetachedSignature(self, pCertContext, data):
        assert self._fCryptSignMessage is not None
        assert isinstance(data, bytes)

        signMessagePara = CRYPT_SIGN_MESSAGE_PARA()
        signMessagePara.cbSize = sizeof(CRYPT_SIGN_MESSAGE_PARA)
        signMessagePara.dwMsgEncodingType = self.X509_ASN_ENCODING | self.PKCS_7_ASN_ENCODING
        signMessagePara.pSigningCert = pCertContext
        signMessagePara.HashAlgorithm.pszObjId = getHashOidByKeyOid(pCertContext.contents.pCertInfo.contents.SubjectPublicKeyInfo.Algorithm.pszObjId)
        signMessagePara.cMsgCert = 1
        signMessagePara.rgpMsgCert = pointer(pCertContext)
        dwDataLen = DWORD(len(data))
        pData     = c_char_p(data)
        dwSignatureLen = DWORD()
        ok = self._fCryptSignMessage( byref(signMessagePara),
                                      True,
                                      1,
                                      byref(pData),
                                      byref(dwDataLen),
                                      None,
                                      byref(dwSignatureLen)
                                    )
        if not ok:
            raise self.Error()
        bSignature = create_string_buffer(dwSignatureLen.value)
        ok = self._fCryptSignMessage( byref(signMessagePara),
                                      True,
                                      1,
                                      byref(pData),
                                      byref(dwDataLen),
                                      bSignature,
                                      byref(dwSignatureLen)
                                    )
        if not ok:
            raise self.Error()
        return bSignature.raw[:dwSignatureLen.value]


    def verifyDetachedSignature(self, data, detachedSignature):
        assert self._fCryptVerifyDetachedMessageSignature is not None
        assert isinstance(detachedSignature, bytes)

        verifyMessagePara = CRYPT_VERIFY_MESSAGE_PARA()
        verifyMessagePara.cbSize = sizeof(CRYPT_VERIFY_MESSAGE_PARA)
        verifyMessagePara.dwMsgAndCertEncodingType = self.X509_ASN_ENCODING | self.PKCS_7_ASN_ENCODING

        dwDataLen = DWORD(len(data))
        pSignerCertContext = PCCERT_CONTEXT()

        ok = self._fCryptVerifyDetachedMessageSignature( byref(verifyMessagePara),
                                                         0,
                                                         detachedSignature,
                                                         len(detachedSignature),
                                                         1,
                                                         c_char_p(data),
                                                         byref(dwDataLen),
                                                         byref(pSignerCertContext) );
        if not ok:
            raise self.Error()
        return Cert(self, pSignerCertContext)



class Provider(object):
    def __init__(self, api, flags=0, providerType=0, providerName=None, containerName=None, pCertContext=None):
        self.api           = api
        self.flags         = flags
        self.providerType  = providerType
        self.providerName  = providerName
        self.containerName = containerName
        self.pCertContext  = pCertContext

        self.handle        = None
        self.toRelease     = None


    def __enter__(self):
        if self.pCertContext:
            self.handle, self.toRelease = self.api._acquireContextByCertContext(self.pCertContext)
        else:
            self.handle, self.toRelease = self.api._acquireContext(self.flags, self.providerType, self.providerName, self.containerName), True
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        if self.toRelease:
            self.api._releaseContext(self.handle)
        self.toRelease = self.handle = None


    def listAlgs(self):
        api = self.api
        item = PROV_ENUMALGS()
        itemSize = DWORD(sizeof(PROV_ENUMALGS))
        result = []
        dwFlags = api.CRYPT_FIRST
        while True:
            errorCode = api._getProvParam(self.handle, api.PP_ENUMALGS, byref(item), byref(itemSize), dwFlags)
            if errorCode == ERROR_NO_MORE_ITEMS:
                 break
            if errorCode:
                 raise api.Error(errorCode)
            result.append( AlgDescr(int(item.aiAlgid),
                                    item.szName[:item.dwNameLen].decode(api._ansiEncoding),
                                    int(item.dwBitLen)
                                   )
                         )
            dwFlags = self.api.CRYPT_NEXT
        return result


    def listAlgsEx(self):
        api = self.api
        item = PROV_ENUMALGS_EX()
        itemSize = DWORD(sizeof(PROV_ENUMALGS_EX))
        result = []
        dwFlags = api.CRYPT_FIRST
        while True:
            errorCode = self.api._getProvParam(self.handle, api.PP_ENUMALGS_EX, byref(item), byref(itemSize), dwFlags)
            if errorCode == ERROR_NO_MORE_ITEMS:
                 break
            if errorCode:
                 raise api.Error(errorCode)
            result.append( AlgDescrEx(int(item.aiAlgid),
                                      item.szName[:item.dwNameLen].decode(api._ansiEncoding),
                                      item.szLongName[:item.dwLongNameLen].decode(api._ansiEncoding),
                                      int(item.dwDefaultLen),
                                      int(item.dwMinLen),
                                      int(item.dwMaxLen),
                                      item.dwProtocols
                                     )
                         )
            dwFlags = self.api.CRYPT_NEXT
        return result


    def listContainers(self):
        api = self.api
        result = []
        bufferSize = DWORD()
        dwFlags = api.CRYPT_FIRST
        errorCode = api._getProvParam(self.handle, api.PP_ENUMCONTAINERS, None, byref(bufferSize), dwFlags)
        if errorCode == ERROR_NO_MORE_ITEMS:
            return result
        if errorCode:
            raise api.Error(errorCode)
        buffer = create_string_buffer(bufferSize.value)
        while True:
            bufferSize.value = len(buffer)
            errorCode = self.api._getProvParam(self.handle, api.PP_ENUMCONTAINERS, buffer, byref(bufferSize), dwFlags)
            if errorCode == ERROR_NO_MORE_ITEMS:
                 break
            if errorCode:
                 raise api.Error(errorCode)
            result.append( buffer.value[:bufferSize.value].decode(api._ansiEncoding) )
            dwFlags = api.CRYPT_NEXT
        return result


    def _getDwordParam(self, param):
        api = self.api
        buffer = DWORD()
        bufferSize = DWORD( sizeof(buffer) )
        errorCode = api._getProvParam(self.handle, param, byref(buffer), byref(bufferSize), 0)
        if errorCode:
             raise api.Error(errorCode)
        return int(buffer.value)


    def _getStrParam(self, param):
        api = self.api
        bufferSize = DWORD()
        errorCode = api._getProvParam(self.handle, param, None, byref(bufferSize), 0)
        if errorCode:
            raise api.Error(errorCode)
        buffer = create_string_buffer(bufferSize.value)
        errorCode = api._getProvParam(self.handle, param, buffer, byref(bufferSize), 0)
        if errorCode:
             raise api.Error(errorCode)
        return buffer.value[:bufferSize.value].decode(api._ansiEncoding)


    def name(self):
        return self._getStrParam(self.api.PP_NAME)


    def version(self):
        v = self._getDwordParam(self.api.PP_VERSION)
        return '%d.%d' % divmod(v, 256)


    def container(self):
        return self._getStrParam(self.api.PP_CONTAINER)


    def keySetType(self):
        return self._getDwordParam(self.api.PP_KEYSET_TYPE)


    def reader(self):
        return self._getStrParam(self.api.PP_SMARTCARD_READER)


    def keySpec(self):
        return self._getDwordParam(self.api.PP_KEYSPEC)


    def uniqueContainer(self):
        return self._getStrParam(self.api.PP_UNIQUE_CONTAINER)


    def genRandom(self, buffLen):
        return self.api._CryptGenRandom(self.handle, buffLen)


    def hash(self, algId):
        return Hash(provider=self, algId=algId)


    def genKey(self, algId, flags = 0):
        handle = self.api._genKey(self.handle, algId, flags)
        return Key(self.api, handle)


    def key(self, keySpec=None):
        if keySpec is None:
            keySpec = self.api.AT_KEYEXCHANGE
        handle = self.api._getUserKey(self.handle, keySpec)
        return Key(self.api, handle)


    def importKey(self, keyBytes, pubKey=None, flags=0):
        assert pubKey is None or pubKey.handle is not None
        handle = self.api._importKey(self.handle, c_char_p(keyBytes), len(keyBytes), pubKey.handle if pubKey else None, flags)
        return Key(self.api, handle)


    def importPubKeyfromCert(self, cert):
        pubKeyInfo = cert._pubKeyInfo()
        assert pubKeyInfo
        handle = self.api._importPubKeyInfo(self.handle, pubKeyInfo)
        return Key(self.api, handle)


# шут разберёт - это публичный ключ, приватный или сразу оба... :(
class Key(object):
    def __init__(self, api, handle):
        self.api = api
        self.handle = handle
        self.blockSize = None


    def __del__(self):
        if self.handle:
            self.api._destroyKey(self.handle)
            self.handle = None


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()


    def _getBinParam(self, param):
        api = self.api
        bufferSize = DWORD()
        errorCode = api._getKeyParam(self.handle, param, None, byref(bufferSize))
        if errorCode:
            raise api.Error(errorCode)
        buffer = create_string_buffer(bufferSize.value)
        errorCode = api._getKeyParam(self.handle, param, buffer, byref(bufferSize))
        if errorCode:
            raise api.Error(errorCode)
        return buffer.raw


    def _getDwordParam(self, param):
        api = self.api
        buffer = DWORD()
        bufferSize = DWORD(sizeof(buffer))
        errorCode = api._getKeyParam(self.handle, param, byref(buffer), byref(bufferSize))
        if errorCode:
            raise api.Error(errorCode)
        return buffer.value


    def _setBinParam(self, param, pcval):
        api = self.api
        errorCode = api._setKeyParam(self.handle, param, pcval)
        if errorCode:
             raise api.Error(errorCode)


    def certBytes(self):
        return self._getBinParam(self.api.KP_CERTIFICATE)


    def setParam(self, param, value):
        if isinstance(value, (int, long)):
            val = DWORD(value)
            self._setBinParam(param, byref(val))
        elif isinstance(value, (bytes, bytearray)):
            self._setBinParam(param, c_char_p(value))
        elif value is None:
            self._setBinParam(param, c_char_p())
        else:
            raise TypeError('value should be either int or bytes')


    def dup(self):
        api = self.api
        assert api._fCryptDuplicateKey is not None

        hKey = HCRYPTKEY()
        ok = api._fCryptDuplicateKey(self.handle, None, 0, byref(hKey))
        if not ok:
            raise self.Error()
        return Key(api, hKey.value)


    def export(self, blobType, expKey=None):
        assert expKey is None or expKey.handle is not None

        api = self.api
        hExpKey = expKey.handle if expKey else None
        bufferSize = DWORD()
#        errorCode = api._exportKey(self.handle, hExpKey, blobType, 0,  None, byref(bufferSize))
        api._exportKey(self.handle, hExpKey, blobType, 0,  None, byref(bufferSize))
        buffer = create_string_buffer(bufferSize.value)
        api._exportKey(self.handle, hExpKey, blobType, 0,  buffer, byref(bufferSize))
#        errorCode = api._exportKey(self.handle, hExpKey, blobType, 0,  buffer, byref(bufferSize))
#        if errorCode:
#            raise api.Error(errorCode)
        return buffer.raw


    def exportPublicKeyBlob(self, expKey=None):
        result = self.api.PublicKeyBlob()
        result.decode(self.export(blobType=self.api.PUBLICKEYBLOB, expKey=expKey))
        return result


    def exportSimpleBlob(self, expKey=None):
        result = self.api.SimpleBlob()
        result.decode(self.export(blobType=self.api.SIMPLEBLOB, expKey=expKey))
        return result


    def getIV(self):
        return self._getBinParam(self.api.KP_IV)


    def setIV(self, iv):
        return self.setParam(self.api.KP_IV, iv)


    def getPadding(self):
        return self._getDwordParam(self.api.KP_PADDING)


    def setPadding(self, value):
        return self.setParam(self.api.KP_PADDING, value)


    def getMode(self):
        return self._getDwordParam(self.api.KP_MODE)


    def setMode(self, value):
        return self.setParam(self.api.KP_Mode, value)


    def getAlgId(self):
        return self._getDwordParam(self.api.KP_ALGID)


    def setAlgId(self, value):
        return self.setParam(self.api.KP_ALGID, value)


#    def getBlockSize(self):
#        if self.blockSize is None:
#            self.blockSize = self._getDwordParam(self.api.KP_BLOCKLEN)
#        return self.blockSize


    def encrypt(self, plaintext, final = True):
        api = self.api
        dwDataLen  = DWORD(len(plaintext))
        ok = api._fCryptEncrypt( self.handle,      # HCRYPTKEY  hKey,
                                 None,             # HCRYPTHASH hHash,
                                 final,            # BOOL       Final,
                                 0,                # DWORD      dwFlags,
                                 None,             # BYTE       *pbData,
                                 byref(dwDataLen), # DWORD      *pdwDataLen,
                                 0)                # DWORD      dwBufLen
        if not ok:
            raise api.Error()
#        print 'encrypt(1):', 'len(plaintext)=', len(plaintext), 'dataLen=', dwDataLen.value

        buffer     = create_string_buffer(plaintext, dwDataLen.value)
        dwDataLen  = DWORD(len(plaintext))
        ok = api._fCryptEncrypt( self.handle,      # HCRYPTKEY  hKey,
                                 None,             # HCRYPTHASH hHash,
                                 final,            # BOOL       Final,
                                 0,                # DWORD      dwFlags,
                                 buffer,           # BYTE       *pbData,
                                 byref(dwDataLen), # DWORD      *pdwDataLen,
                                 len(buffer))      # DWORD      dwBufLen
        if not ok:
            raise api.Error()

#        print 'encrypt(2):', 'len(plaintext)=', len(plaintext), 'len(buffer)=', len(buffer), 'dataLen=', dwDataLen.value
        return buffer.raw[:dwDataLen.value]


    def encrypt2(self, plaintext, final = True):
        api = self.api
        buffer     = create_string_buffer(plaintext, len(plaintext)+64)
        dwDataLen  = DWORD(len(plaintext))
        ok = api._fCryptEncrypt( self.handle,      # HCRYPTKEY  hKey,
                                 None,             # HCRYPTHASH hHash,
                                 final,            # BOOL       Final,
                                 0,                # DWORD      dwFlags,
                                 buffer,           # BYTE       *pbData,
                                 byref(dwDataLen), # DWORD      *pdwDataLen,
                                 len(buffer))      # DWORD      dwBufLen
        if not ok:
            raise api.Error()

#        print 'encrypt2:', 'len(plaintext)=', len(plaintext), 'len(buffer)=', len(buffer), 'dataLen=', dwDataLen.value
        return buffer.raw[:dwDataLen.value]


    def decrypt(self, ciphertext, final = True):
        api = self.api
        buffer     = create_string_buffer(ciphertext)
        dwDataLen  = DWORD(len(ciphertext))
        ok = api._fCryptDecrypt( self.handle,      # HCRYPTKEY  hKey,
                                 None,             # HCRYPTHASH hHash,
                                 final,            # BOOL       Final,
                                 0,                # DWORD      dwFlags,
                                 buffer,           # BYTE       *pbData,
                                 byref(dwDataLen)) # DWORD      *pdwDataLen
        if not ok:
            raise api.Error()
        return buffer.raw[:dwDataLen.value]


class Hash(object):
    def __init__(self, provider=None, algId=None, orig=None):
        assert (algId is None) == (provider is None)
        assert (algId is None) != (orig is None)
        assert provider is None or provider.handle is not None
        assert orig is None or orig.handle is not None

        self.handle = None

        if orig is None:
            self.api = provider.api
#            self.algId = algId
            self.handle = self.api._createHash(provider.handle, algId)
        else:
            self.api    = orig.api
#            self.algId  = orig.algId
            self.handle = self.api._duplicateHash(orig.handle)



    def __del__(self):
        if self.handle:
            self.api._destroyHash(self.handle)
            self.handle = None


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()


    def clone(self):
        return Hash(orig=self)


    def update(self, data):
        self.api._hashData(self.handle, data)


    def digest(self):
        api = self.api
        dwBufferSize = DWORD()
        api._getHashParam(self.handle, api.HP_HASHVAL, None, byref(dwBufferSize))
        buffer = create_string_buffer(dwBufferSize.value)
        api._getHashParam(self.handle, api.HP_HASHVAL, buffer, byref(dwBufferSize))
        return buffer.raw


    def sign(self, keySpec=None, flags=0):
        api = self.api
        if keySpec is None:
            keySpec = api.AT_KEYEXCHANGE
        dwSignatureSize = DWORD()
        api._signHash(self.handle, keySpec, flags, None, byref(dwSignatureSize))
#        print 'signature size:', dwSignatureSize.value
        signature = create_string_buffer(dwSignatureSize.value)
        api._signHash(self.handle, keySpec, flags, signature, byref(dwSignatureSize))
        return signature.raw


    def verifySignature(self, signature, pubKey):
        api = self.api
        rc = api._verifySignature(self.handle,
                                  c_char_p(signature),
                                  len(signature),
                                  pubKey.handle)
        return rc


class CertStore(object):
    def __init__(self, api, handle):
        self.api = api
        self.handle = handle

    def __del__(self):
        if self.handle:
            self.api._closeStore(self.handle)
            self.handle = None


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()


    def listCerts(self):
        result = []
        api = self.api
        fox = PCCERT_CONTEXT()
        while True:
            fox = api._fCertEnumCertificatesInStore(self.handle, fox)
            if not fox:
                break
            result.append( Cert(self.api, api._fCertDuplicateCertificateContext(fox)) )
        return result


class Cert(object):
    def __init__(self, api, pCertContext):
        self.api = api
        self.pCertContext = pCertContext
        self._issuer = None
        self._subject = None


    def __del__(self):
        if self.pCertContext:
            self.api._fCertFreeCertificateContext( self.pCertContext )
            self.pCertContext = None


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()


    def encoded(self):
        cc = self.pCertContext.contents
        return string_at( cc.pbCertEncoded, cc.cbCertEncoded )


    def sha1(self):
        bytes = self.encoded()
        return hashlib.sha1(bytes).digest()


    def _pubKeyInfo(self):
        pCertInfo = self.pCertContext.contents.pCertInfo
        if not pCertInfo:
            return None
        return pCertInfo.contents.SubjectPublicKeyInfo


    def info(self):
        cc = self.pCertContext.contents
        if cc.pCertInfo:
            return cc.pCertInfo.contents
        else:
            return None


    def notBefore(self):
        info = self.info()
        if info:
            return info.NotBefore.datetime
        else:
            return None


    def notAfter(self):
        info = self.info()
        if info:
            return info.NotAfter.datetime
        else:
            return None


    def _parseNameBlob(self, pNameBlob):
        api = self.api
        size = api._fCertNameToStr(api.X509_ASN_ENCODING, pNameBlob, api.CERT_OID_NAME_STR, None, 0)
        if size == 0:
            raise api.Error()
        buff = create_unicode_buffer(size)
        api._fCertNameToStr(api.X509_ASN_ENCODING, pNameBlob, api.CERT_OID_NAME_STR, buff, size)
        nameStr = buff.value

        p = re.compile(r'''([0-9.]+)  # OID
                           =          # delimiter
                           (          # value
                               [^",]*       # simple value
                             |              # or
                               (?:"[^"]*")+ # quoted value with double quotes
                           )
                           \s*(?:$|,\s*)    # sep to next
                        ''',
                       re.DOTALL|re.VERBOSE|re.UNICODE
                      )

        result = {}
        start = 0
        while True:
            m = p.match(nameStr, start)
            if not m:
                break
            key = m.group(1)
            val = m.group(2)
            if val.startswith('"'):
                assert val.endswith('"')
                val = val[1:-1].replace('""', '"')
            result[key] = val
            start = m.end()
        return result


    def issuer(self):
        if self._issuer is None:
            self._issuer = self._parseNameBlob(self.pCertContext.contents.pCertInfo.contents.Issuer)
        return self._issuer


    def issuerName(self):
        return self.issuer().get(self.api.szOID_COMMON_NAME)


    def subject(self):
        if self._subject is None:
            self._subject = self._parseNameBlob(self.pCertContext.contents.pCertInfo.contents.Subject)
        return self._subject


    def commonName(self):
        return self.subject().get(self.api.szOID_COMMON_NAME)


    def surName(self):
        return self.subject().get(self.api.szOID_SUR_NAME)


    def givenName(self):
        return self.subject().get(self.api.szOID_GIVEN_NAME)


    def country(self):
        return self.subject().get(self.api.szOID_COUNTRY_NAME)


    def state(self):
        return self.subject().get(self.api.szOID_STATE_OR_PROVINCE_NAME)


    def locality(self):
        return self.subject().get(self.api.szOID_LOCALITY_NAME)


    def streetAddress(self):
        return self.subject().get(self.api.szOID_STREET_ADDRESS)


    def org(self):
        return self.subject().get(self.api.szOID_ORGANIZATION_NAME)


    def orgUnit(self):
        return self.subject().get(self.api.szOID_ORGANIZATIONAL_UNIT_NAME)


    def title(self):
        return self.subject().get(self.api.szOID_TITLE)


    def email(self):
        return self.subject().get(self.api.szOID_RSA_emailAddr)


    def inn(self):
        return self.subject().get(self.api.szOID_INN)


    def ogrn(self):
        return self.subject().get(self.api.szOID_OGRN)


    def snils(self):
        return self.subject().get(self.api.szOID_SNILS)


    def serialNumber(self):
        return ''.join('%02x' % ord(c) for c in self.pCertContext.contents.pCertInfo.contents.SerialNumber.data[::-1])


    def keyOid(self):
        return self.pCertContext.contents.pCertInfo.contents.SubjectPublicKeyInfo.Algorithm.pszObjId


    def keyOidName(self):
        return getKeyOidName(self.pCertContext.contents.pCertInfo.contents.SubjectPublicKeyInfo.Algorithm.pszObjId)


    def createDetachedSignature(self, data):
        return self.api.createDetachedSignature(self.pCertContext, data)


#    def hCryptProv(self):
#        api = self.api
#        hCryptProv = HCRYPTPROV()
#        valueSize  = DWORD( sizeof(hCryptProv) )
#        ok = api._fCertGetCertificateContextProperty(self.pCertContext, api.CERT_KEY_PROV_HANDLE_PROP_ID, byref(hCryptProv), byref(valueSize))
#        if not ok:
#            errorCode = api._fGetLastError()
#            if errorCode == CRYPT_E_NOT_FOUND:
#                return None
#            raise api.Error(errorCode)
#        print hCryptProv, hCryptProv.value
#        return hCryptProv.value


#    def hCryptProv2(self):
#        api = self.api
#        hCryptProv = HCRYPTPROV()
#        dwKeySpec  = DWORD()
#        fCallerFreeProv = BOOL()
#
#        ok = api._fCryptAcquireCertificatePrivateKey(self.pCertContext,
#                                                     0, # api.CRYPT_ACQUIRE_CACHE_FLAG, # | api.CRYPT_ACQUIRE_USE_PROV_INFO_FLAG,
#                                                     None,
#                                                     byref(hCryptProv),
#                                                     byref(dwKeySpec),
#                                                     byref(fCallerFreeProv)
#                                                    )
#        if not ok:
#            raise api.Error()
#        print hCryptProv, hCryptProv.value, 'keySpec:', hex(dwKeySpec.value), 'free:', fCallerFreeProv.value
#        return hCryptProv.value


#    def hCryptProv3(self):
#        api = self.api
#        ckc = CERT_KEY_CONTEXT()
#        ckc.dwSize = sizeof(ckc)
#
#        valueSize  = DWORD( sizeof(ckc) )
#        ok = api._fCertGetCertificateContextProperty(self.pCertContext, api.CERT_KEY_CONTEXT_PROP_ID, byref(ckc), byref(valueSize))
#        if not ok:
#            errorCode = api._fGetLastError()
#            if errorCode == CRYPT_E_NOT_FOUND:
#                return None
#            raise api.Error(errorCode)
#        print 'ckc.size=', ckc.cbSize,
#        print 'ckc.hCryptProv=', ckc.hCryptProv,
#        print 'ckc.dwKeySpec=', ckc.dwKeySpec
#        return ckc.hCryptProv


    def provider(self):
        return Provider(self.api, pCertContext=self.pCertContext)




#    CRYPT_ACQUIRE_CACHE_FLAG         = 0x00000001
#    CRYPT_ACQUIRE_USE_PROV_INFO_FLAG = 0x00000002
#    CRYPT_ACQUIRE_COMPARE_KEY_FLAG   = 0x00000004
#    CRYPT_ACQUIRE_SILENT_FLAG        = 0x00000040


    def verifyChain(self):
        api = self.api
        assert api._fCertGetCertificateChain is not None
        assert api._fCertVerifyCertificateChainPolicy is not None


        chainPara = CERT_CHAIN_PARA()
        chainPara.cbSize = sizeof(CERT_CHAIN_PARA)
        pChainContext = PCCERT_CHAIN_CONTEXT()
        ok = api._fCertGetCertificateChain( None,
                                            self.pCertContext,
                                            None,
                                            None,
                                            byref(chainPara),
                                            api.CERT_CHAIN_CACHE_END_CERT | api.CERT_CHAIN_REVOCATION_CHECK_CHAIN,
                                            None,
                                            byref(pChainContext)
                                          )
        if not ok:
            raise api.Error()

        try:
            chainPolicyPara = CERT_CHAIN_POLICY_PARA()
            chainPolicyPara.cbSize = sizeof(CERT_CHAIN_POLICY_PARA)

            chainPolicyStatus = CERT_CHAIN_POLICY_STATUS()
            chainPolicyStatus.sbSize = sizeof(CERT_CHAIN_POLICY_STATUS)

            ok = api._fCertVerifyCertificateChainPolicy(api.CERT_CHAIN_POLICY_BASE,
                                                        pChainContext,
                                                        byref(chainPolicyPara),
                                                        byref(chainPolicyStatus))
            if not ok:
                raise api.Error()

            if chainPolicyStatus.dwError:
                raise api.Error(chainPolicyStatus.dwError)
        finally:
            if pChainContext:
                api._fCertFreeCertificateChain(pChainContext)

            pass


# ################################################################

# структуры для доступа к данным блобов
# https://cpdn.cryptopro.ru/content/csp40/html/struct___p_u_b_l_i_c_k_e_y_s_t_r_u_c.html
# Структура PUBLICKEYSTRUC, также известная, как структура BLOBHEADER, указывает тип ключевого блоба и алгоритм ключа, находящегося в нём. Экземпляр этой структуры находится в начале поля pbData каждого ключевого блоба.
class BLOBHEADER(Structure):
    _fields_ = (
                    ('bType',      BYTE),            # Тип ключевого блоба.( PUBLICKEYBLOB, PRIVATEKEYBLOB, SIMPLEBLOB )
                    ('bVersion',   BYTE),            # Номер версии формата ключевого блоба. В настоящий момент версия всегда должна быть равна 0x02
                    ('reserved',   WORD),            # пусто (для выравнивания?)
                    ('aiKeyAlgId', ALG_ID),          # Алгоритм ключа, содержащегося в ключевом блобе
               )
PUBLICKEYSTRUC = BLOBHEADER

# http://cpdn.cryptopro.ru/content/csp40/html/struct___c_r_y_p_t___p_u_b_k_e_y___i_n_f_o___h_e_a_d_e_r.html
# Структура CRYPT_PUBKEYPARAM содержит признак ключей по ГОСТ Р 34.10-2001.
class CRYPT_PUBKEYPARAM(Structure):
    _fields_ = (
                   ('Magic', DWORD),                 # Признак ключей по ГОСТ Р 34.10-2001 устанавливается в GR3410_1_MAGIC
                   ('BitLen', DWORD),                # Длина открытого ключа в битах.
               )

# https://cpdn.cryptopro.ru/content/csp40/html/struct___c_r_y_p_t___p_u_b_k_e_y___i_n_f_o___h_e_a_d_e_r.html
# Структура CRYPT_PUBKEY_INFO_HEADER содержит заголовок блоба открытого ключа или блоба ключевой пары по ГОСТ Р 34.10-2001.
class CRYPT_PUBKEY_INFO_HEADER(Structure):
    _fields_ = (
                  ('BlobHeader', BLOBHEADER),        # Общий заголовок ключевого блоба. Определяет его тип и алгоритм ключа находящегося в ключевом блобе. Для открытых ключей алгоритм ключа всегда, либо CALG_GR3410, либо CALG_GR3410EL
                  ('KeyParam',   CRYPT_PUBKEYPARAM), # Основной признак и длина ключей ГОСТ Р 34.10-94 и ГОСТ Р 34.10-2001
               )

# https://cpdn.cryptopro.ru/content/csp36/html/struct___c_r_y_p_t___p_u_b_l_i_c_k_e_y_b_l_o_b.html
#typedef struct _CRYPT_PUBLICKEYBLOB {
#  CRYPT_PUBKEY_INFO_HEADER tPublicKeyParam;      // Общий заголовок ключевого блоба типа PUBLICKEYBLOB "КриптоПро CSP".
#  BYTE bASN1GostR3410_94_PublicKeyParameters[1]; // Содержит ASN1 структуру в DER кодировке, определяющую параметры открытого ключа, как описано типами GostR3410-2001-PublicKeyParameters и GostR3410-94-PublicKeyParameters CPPK [RFC 4491] и CPALGS [RFC 4357].
#  BYTE bPublicKey[1];                            // Содержит открытый ключ в сетевом представлении (ASN1 DER) как описано типами GostR3410-2001-PublicKey и GostR3410-94-PublicKey CPPK [RFC 4491]. Длина массива равна tPublicKeyParam.KeyParam.BitLen/8
#} CRYPT_PUBLICKEYBLOB, *PCRYPT_PUBLICKEYBLOB;
#

class CPPublicKeyBlob:
    VERSION = 0x20

    def __init__(self, api):
        self.api = api
        self.keyAlgId = None
        self.bitLen   = None
        self.paramSetBytes   = None
        self.publicKeyBytes  = None


    def decode(self, blobBytes):
        pBlobBytes = c_char_p(blobBytes)
        pHeader    = cast( pBlobBytes, POINTER(CRYPT_PUBKEY_INFO_HEADER) )
        assert pHeader
        header = pHeader.contents

        assert header.BlobHeader.bType == self.api.PUBLICKEYBLOB
        assert header.BlobHeader.bVersion == self.VERSION
        assert header.KeyParam.Magic == self.api.GR3410_1_MAGIC
#        assert pHeader.content.KeyParam.BitLen == 512

        keyAlgId = header.BlobHeader.aiKeyAlgId
        bitLen   = header.KeyParam.BitLen

        pBytes = cast( pBlobBytes, c_void_p )
        publicKeyLen    = bitLen//8
        publicKeyOffset = len(blobBytes) - publicKeyLen

        paramSetOffset  = sizeof(CRYPT_PUBKEY_INFO_HEADER)
        paramSetLen     = publicKeyOffset - paramSetOffset

        assert publicKeyOffset > 0
        assert paramSetLen >= 0
        self.paramSetBytes   = string_at( pBytes.value + paramSetOffset,  paramSetLen )
        self.publicKeyBytes  = string_at( pBytes.value + publicKeyOffset, publicKeyLen )
        self.keyAlgId = keyAlgId
        self.bitLen   = bitLen


    def encode(self):
        assert self.keyAlgId
#        assert self.bitLen == 512
        assert self.paramSetBytes
        assert self.publicKeyBytes
        assert self.bitLen
        assert len(self.publicKeyBytes) == self.bitLen//8

        paramSetOffset  = sizeof(CRYPT_PUBKEY_INFO_HEADER)
        paramSetLen     = len(self.paramSetBytes)
        publicKeyOffset = paramSetOffset+paramSetLen
        publicKeyLen    = len(self.publicKeyBytes)

        buffer = create_string_buffer(publicKeyOffset + publicKeyLen)
        pHeader = cast(buffer, POINTER(CRYPT_PUBKEY_INFO_HEADER))
        header = pHeader.contents
        header.BlobHeader.bType      = self.api.PUBLICKEYBLOB
        header.BlobHeader.bVersion   = self.VERSION
        header.BlobHeader.aiKeyAlgId = self.keyAlgId
        header.KeyParam.Magic        = self.api.GR3410_1_MAGIC
        header.KeyParam.BitLen       = self.bitLen

        paramSetLen     = len(self.paramSetBytes)

        memmove(addressof(buffer) + paramSetOffset,  self.paramSetBytes, paramSetLen)
        memmove(addressof(buffer) + publicKeyOffset, self.publicKeyBytes, publicKeyLen)

        return buffer.raw



# https://cpdn.cryptopro.ru/content/csp40/html/struct___c_r_y_p_t___s_i_m_p_l_e_b_l_o_b___h_e_a_d_e_r.html
class CRYPT_SIMPLEBLOB_HEADER(Structure):
    _fields_ = (
                    ('BlobHeader',        BLOBHEADER), # Общий заголовок ключевого блоба. Определяет алгоритм ключа находящегося в ключевом блобе.
                    ('Magic',             DWORD),      # Признак ключей по ГОСТ 28147-89 или мастер ключей TLS, устанавливается в G28147_MAGIC
                    ('EncryptKeyAlgId',   ALG_ID),     # Определяет алгоритм экспорта ключа. Этот алгоритм является параметром ключа экспорта
               )

# https://cpdn.cryptopro.ru/content/csp40/html/struct___c_r_y_p_t___s_i_m_p_l_e_b_l_o_b.html
# Псевдоструктура (т. е. недоопределенная структура) CRYPT_SIMPLEBLOB полностью описывает ключевой блоб типа SIMPLEBLOB для ключей "КриптоПро CSP".
# я ещё обрезал bEncryptionParamSet
class CRYPT_SIMPLEBLOB_FP(Structure):
    SEANCE_VECTOR_LEN =  8 # Длина в байтах вектора инициализации алгоритма
    G28147_KEYLEN     = 32 # Длина в байтах ключа ГОСТ 28147-89
    EXPORT_IMIT_SIZE  =  4 # Длина в байтах имитовставки при импорте/экспорте

    _fields_ = (
                    ('tSimpleBlobHeader', CRYPT_SIMPLEBLOB_HEADER), # Общий заголовок ключевого блоба типа SIMPLEBLOB "КриптоПро CSP"
                    ('bSV',               BYTE*SEANCE_VECTOR_LEN),  # Вектор инициализации для алгоритма CALG_PRO_EXPORT
                    ('bEncryptedKey',     BYTE*G28147_KEYLEN),      # Зашифрованный ключ ГОСТ 28147-89
                    ('bMacKey',           BYTE*EXPORT_IMIT_SIZE),   # Имитовставка по ГОСТ 28147-89 на ключ. Рассчитывается до зашифрования и проверяется после расшифрования
                    #BYTE bEncryptionParamSet[1];                   # Содержит ASN1 структуру в DER кодировке, определяющую параметры алгоритма шифрования ГОСТ 28147-89
               )

class CPSimpleBlob:
    VERSION = 0x20

    def __init__(self, api):
        self.api = api
        self.keyAlgId = None
        self.encryptKeyAlgId = None
        self.sv = None
        self.encryptedKey = None
        self.macKey = None
        self.encryptionParamSet = None


    def decode(self, blobBytes):
        pBlobBytes = c_char_p(blobBytes)
        pHeader    = cast( pBlobBytes, POINTER(CRYPT_SIMPLEBLOB_FP) )
        pBytes     = cast( pBlobBytes, c_void_p )
        assert pHeader
        header = pHeader.contents

        assert header.tSimpleBlobHeader.BlobHeader.bType == self.api.SIMPLEBLOB
        assert header.tSimpleBlobHeader.BlobHeader.bVersion == self.VERSION
        assert header.tSimpleBlobHeader.Magic == self.api.G28147_MAGIC

        keyAlgId        = header.tSimpleBlobHeader.BlobHeader.aiKeyAlgId
        encryptKeyAlgId = header.tSimpleBlobHeader.EncryptKeyAlgId
        sv              = string_at( pBytes.value + CRYPT_SIMPLEBLOB_FP.bSV.offset, CRYPT_SIMPLEBLOB_FP.bSV.size )
        encryptedKey    = string_at( pBytes.value + CRYPT_SIMPLEBLOB_FP.bEncryptedKey.offset, CRYPT_SIMPLEBLOB_FP.bEncryptedKey.size )
        macKey          = string_at( pBytes.value + CRYPT_SIMPLEBLOB_FP.bMacKey.offset, CRYPT_SIMPLEBLOB_FP.bMacKey.size )

        encryptionParamSetOffset  = sizeof(header)
        encryptionParamSetLen     = len(blobBytes) - encryptionParamSetOffset

        assert encryptionParamSetLen>0

        self.keyAlgId        = keyAlgId
        self.encryptKeyAlgId = encryptKeyAlgId
        self.sv              = sv
        self.encryptedKey    = encryptedKey
        self.macKey          = macKey
        self.encryptionParamSet = string_at( pBytes.value + encryptionParamSetOffset, encryptionParamSetLen )


    def encode(self):
        assert self.keyAlgId
        assert self.encryptKeyAlgId

        assert self.sv and len(self.sv) == CRYPT_SIMPLEBLOB_FP.bSV.size
        assert self.encryptedKey and len(self.encryptedKey) == CRYPT_SIMPLEBLOB_FP.bEncryptedKey.size
        assert self.macKey and len(self.macKey) == CRYPT_SIMPLEBLOB_FP.bMacKey.size
        assert self.encryptionParamSet

        encryptionParamSetOffset  = sizeof(CRYPT_SIMPLEBLOB_FP)
        encryptionParamSetLen     = len(self.encryptionParamSet)

        buffer = create_string_buffer(encryptionParamSetOffset  + encryptionParamSetLen)

        pHeader = cast(buffer, POINTER(CRYPT_SIMPLEBLOB_FP))
        header = pHeader.contents

        header.tSimpleBlobHeader.BlobHeader.bType      = self.api.SIMPLEBLOB
        header.tSimpleBlobHeader.BlobHeader.bVersion   = self.VERSION
        header.tSimpleBlobHeader.BlobHeader.aiKeyAlgId = self.keyAlgId
        header.tSimpleBlobHeader.Magic                 = self.api.G28147_MAGIC
        header.tSimpleBlobHeader.EncryptKeyAlgId       = self.encryptKeyAlgId

        memmove( byref(buffer, CRYPT_SIMPLEBLOB_FP.bSV.offset),           self.sv,           CRYPT_SIMPLEBLOB_FP.bSV.size)
        memmove( byref(buffer, CRYPT_SIMPLEBLOB_FP.bEncryptedKey.offset), self.encryptedKey, CRYPT_SIMPLEBLOB_FP.bEncryptedKey.size)
        memmove( byref(buffer, CRYPT_SIMPLEBLOB_FP.bMacKey.offset),       self.macKey,       CRYPT_SIMPLEBLOB_FP.bMacKey.size)

        encryptionParamSetOffset  = sizeof(header)
        encryptionParamSetLen     = len(self.encryptionParamSet)

        memmove( byref(buffer, encryptionParamSetOffset),  self.encryptionParamSet, encryptionParamSetLen)

        return buffer.raw

