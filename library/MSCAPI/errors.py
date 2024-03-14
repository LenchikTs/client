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
##    ошибки; в windows это вроде бы не очень нужно, но нужно в других ОС
##
#############################################################################

from ctypes import c_void_p

from .wintypes import CAPIFUNCTYPE, DWORD, LPSTR, LPWSTR

NO_ERROR                        =          0 # 
ERROR_FILE_NOT_FOUND            =          2 # The system cannot find the file specified
ERROR_INVALID_HANDLE            =          6 # The handle is invalid
ERROR_NOT_ENOUGH_MEMORY         =          8 # Not enough storage is available to process this command
ERROR_INVALID_PARAMETER         =         87 # The parameter is incorrect
ERROR_CALL_NOT_IMPLEMENTED      =        120 # This function is not supported on this system
ERROR_BUSY                      =        170 # The requested resource is in use
ERROR_MORE_DATA                 =        234 # More data is available
ERROR_NO_MORE_ITEMS             =        259 # No more data is available

E_NOTIMPL                       = 0x80004001 # Not implemented
E_INVALIDARG                    = 0x80070057 # Invalid argument

NTE_BAD_UID                     = 0x80090001 # Bad UID
NTE_BAD_HASH                    = 0x80090002 # Bad Hash
NTE_BAD_KEY                     = 0x80090003 # Bad Key
NTE_BAD_LEN                     = 0x80090004 # Bad Length
NTE_BAD_DATA                    = 0x80090005 # Bad Data
NTE_BAD_SIGNATURE               = 0x80090006 # Invalid Signature
NTE_BAD_VER                     = 0x80090007 # Bad Version of provider
NTE_BAD_ALGID                   = 0x80090008 # Invalid algorithm specified
NTE_BAD_FLAGS                   = 0x80090009 # Invalid flags specified
NTE_BAD_TYPE                    = 0x8009000A # Invalid type specified
NTE_BAD_KEY_STATE               = 0x8009000B # Key not valid for use in specified state
NTE_BAD_HASH_STATE              = 0x8009000C # Hash not valid for use in specified state
NTE_NO_KEY                      = 0x8009000D # Key does not exist
NTE_NO_MEMORY                   = 0x8009000E # Insufficient memory available for the operation
NTE_EXISTS                      = 0x8009000F # Object already exists
NTE_PERM                        = 0x80090010 # Access denied
NTE_NOT_FOUND                   = 0x80090011 # Object was not found
NTE_DOUBLE_ENCRYPT              = 0x80090012 # Data already encrypted
NTE_BAD_PROVIDER                = 0x80090013 # Invalid provider specified
NTE_BAD_PROV_TYPE               = 0x80090014 # Invalid provider type specified
NTE_BAD_PUBLIC_KEY              = 0x80090015 # Provider's public key is invalid
NTE_BAD_KEYSET                  = 0x80090016 # Keyset does not exist
NTE_PROV_TYPE_NOT_DEF           = 0x80090017 # Provider type not defined
NTE_PROV_TYPE_ENTRY_BAD         = 0x80090018 # Provider type as registered is invalid
NTE_KEYSET_NOT_DEF              = 0x80090019 # The keyset is not defined
NTE_KEYSET_ENTRY_BAD            = 0x8009001A # Keyset as registered is invalid
NTE_PROV_TYPE_NO_MATCH          = 0x8009001B # Provider type does not match registered value
NTE_SIGNATURE_FILE_BAD          = 0x8009001C # The digital signature file is corrupt
NTE_PROVIDER_DLL_FAIL           = 0x8009001D # Provider DLL failed to initialize correctly
NTE_PROV_DLL_NOT_FOUND          = 0x8009001E # Provider DLL could not be found
NTE_BAD_KEYSET_PARAM            = 0x8009001F # The Keyset parameter is invalid
NTE_FAIL                        = 0x80090020 # An internal error occurred
NTE_SYS_ERR                     = 0x80090021 # A base error occurred
NTE_SILENT_CONTEXT              = 0x80090022 # Provider could not perform the action since the context was acquired as silent
NTE_TOKEN_KEYSET_STORAGE_FULL   = 0x80090023 # The security token does not have storage space available for an additional container
NTE_TEMPORARY_PROFILE           = 0x80090024 # The profile for the user is a temporary profile
NTE_FIXEDPARAMETER              = 0x80090025 # The key parameters could not be set because the CSP uses fixed parameters
NTE_INVALID_PARAMETER           = 0x80090027 # The parameter is incorrect
NTE_NOT_SUPPORTED               = 0x80090029 # The requested operation is not supported
                                
CRYPT_E_MSG_ERROR               = 0x80091001 # An error occurred while performing an operation on a cryptographic message
CRYPT_E_UNKNOWN_ALGO            = 0x80091002 # Unknown cryptographic algorithm
CRYPT_E_OID_FORMAT              = 0x80091003 # The object identifier is poorly formatted
CRYPT_E_INVALID_MSG_TYPE        = 0x80091004 # Invalid cryptographic message type
CRYPT_E_UNEXPECTED_ENCODING     = 0x80091005 # Unexpected cryptographic message encoding
CRYPT_E_AUTH_ATTR_MISSING       = 0x80091006 # The cryptographic message does not contain an expected authenticated attribute
CRYPT_E_HASH_VALUE              = 0x80091007 # The hash value is not correct
CRYPT_E_INVALID_INDEX           = 0x80091008 # The index value is not valid
CRYPT_E_ALREADY_DECRYPTED       = 0x80091009 # The content of the cryptographic message has already been decrypted
CRYPT_E_NOT_DECRYPTED           = 0x8009100A # The content of the cryptographic message has not been decrypted yet
CRYPT_E_RECIPIENT_NOT_FOUND     = 0x8009100B # The enveloped-data message does not contain the specified recipient
CRYPT_E_CONTROL_TYPE            = 0x8009100C # Invalid control type
CRYPT_E_ISSUER_SERIALNUMBER     = 0x8009100D # Invalid issuer and/or serial number
CRYPT_E_SIGNER_NOT_FOUND        = 0x8009100E # Cannot find the original signer
CRYPT_E_ATTRIBUTES_MISSING      = 0x8009100F # The cryptographic message does not contain all of the requested attributes
CRYPT_E_STREAM_MSG_NOT_READY    = 0x80091010 # The streamed cryptographic message is not ready to return data
CRYPT_E_STREAM_INSUFFICIENT_DATA= 0x80091011 # The streamed cryptographic message requires more data to complete the decode operation
CRYPT_E_BAD_LEN                 = 0x80092001 # The length specified for the output data was insufficient
CRYPT_E_BAD_ENCODE              = 0x80092002 # An error occurred during encode or decode operation
CRYPT_E_FILE_ERROR              = 0x80092003 # An error occurred while reading or writing to a file
CRYPT_E_NOT_FOUND               = 0x80092004 # Cannot find object or property
CRYPT_E_EXISTS                  = 0x80092005 # The object or property already exists
CRYPT_E_NO_PROVIDER             = 0x80092006 # No provider was specified for the store or object
CRYPT_E_SELF_SIGNED             = 0x80092007 # The specified certificate is self signed
CRYPT_E_DELETED_PREV            = 0x80092008 # The previous certificate or CRL context was deleted
CRYPT_E_NO_MATCH                = 0x80092009 # Cannot find the requested object
CRYPT_E_UNEXPECTED_MSG_TYPE     = 0x8009200A # The certificate does not have a property that references a private key
CRYPT_E_NO_KEY_PROPERTY         = 0x8009200B # Cannot find the certificate and private key for decryption
CRYPT_E_NO_DECRYPT_CERT         = 0x8009200C # Cannot find the certificate and private key to use for decryption
CRYPT_E_BAD_MSG                 = 0x8009200D # Not a cryptographic message or the cryptographic message is not formatted correctly
CRYPT_E_NO_SIGNER               = 0x8009200E # The signed cryptographic message does not have a signer for the specified signer index
CRYPT_E_PENDING_CLOSE           = 0x8009200F # Final closure is pending until additional frees or closes
CRYPT_E_REVOKED                 = 0x80092010 # The certificate is revoked
CRYPT_E_NO_REVOCATION_DLL       = 0x80092011 # No Dll or exported function was found to verify revocation
CRYPT_E_NO_REVOCATION_CHECK     = 0x80092012 # The revocation function was unable to check revocation for the certificate
CRYPT_E_REVOCATION_OFFLINE      = 0x80092013 # The revocation function was unable to check revocation because the revocation server was offline
CRYPT_E_NOT_IN_REVOCATION_DATABASE = 0x80092014 # The certificate is not in the revocation server's database
CRYPT_E_INVALID_NUMERIC_STRING  = 0x80092020 # The string contains a non-numeric character
CRYPT_E_INVALID_PRINTABLE_STRING= 0x80092021 # The string contains a non-printable character
CRYPT_E_INVALID_IA5_STRING      = 0x80092022 # The string contains a character not in the 7 bit ASCII character set
CRYPT_E_INVALID_X500_STRING     = 0x80092023 # The string contains an invalid X500 name attribute key, oid, value or delimiter
CRYPT_E_NOT_CHAR_STRING         = 0x80092024 # The dwValueType for the CERT_NAME_VALUE is not one of the character strings.  Most likely it is either a CERT_RDN_ENCODED_BLOB or CERT_TDN_OCTED_STRING
CRYPT_E_FILERESIZED             = 0x80092025 # The Put operation can not continue.  The file needs to be resized.  However, there is already a signature present.  A complete signing operation must be done
CRYPT_E_SECURITY_SETTINGS       = 0x80092026 # The cryptographic operation failed due to a local security option setting
CRYPT_E_NO_VERIFY_USAGE_DLL     = 0x80092027 # No DLL or exported function was found to verify subject usage
CRYPT_E_NO_VERIFY_USAGE_CHECK   = 0x80092028 # The called function was unable to do a usage check on the subject
CRYPT_E_VERIFY_USAGE_OFFLINE    = 0x80092029 # Since the server was offline, the called function was unable to complete the usage check
CRYPT_E_NOT_IN_CTL              = 0x8009202A # The subject was not found in a Certificate Trust List (CTL)
CRYPT_E_NO_TRUSTED_SIGNER       = 0x8009202B # None of the signers of the cryptographic message or certificate trust list is trusted
CRYPT_E_MISSING_PUBKEY_PARA     = 0x8009202C # The public key's algorithm parameters are missing

# https://www.hresult.info/FACILITY_SCARD:
#SCARD_F_INTERNAL_ERROR          = 0x80100001 # An internal consistency check failed
#SCARD_E_CANCELLED               = 0x80100002 # The action was cancelled by an SCardCancel request.
#SCARD_E_INVALID_HANDLE          = 0x80100003 # The supplied handle was invalid
#SCARD_E_INVALID_PARAMETER       = 0x80100004 # One or more of the supplied parameters could not be properly interpreted.
#SCARD_E_INVALID_TARGET          = 0x80100005 # Registry startup information is missing or invalid. 
#SCARD_E_NO_MEMORY               = 0x80100006 # Not enough memory available to complete this command.
#SCARD_F_WAITED_TOO_LONG         = 0x80100007 # An internal consistency timer has expired.
#SCARD_E_INSUFFICIENT_BUFFER     = 0x80100008 # 
#SCARD_E_UNKNOWN_READER          = 0x80100009
#SCARD_E_TIMEOUT                 = 0x8010000A
#SCARD_E_SHARING_VIOLATION       = 0x8010000B
#SCARD_E_NO_SMARTCARD            = 0x8010000C
#SCARD_E_UNKNOWN_CARD            = 0x8010000D
#SCARD_E_CANT_DISPOSE            = 0x8010000E
#SCARD_E_PROTO_MISMATCH          = 0x8010000F
SCARD_E_NOT_READY               = 0x80100010 # The reader or smart card is not ready to accept commands.
#SCARD_E_INVALID_VALUE           = 0x80100011
#SCARD_E_SYSTEM_CANCELLED        = 0x80100012
#SCARD_F_COMM_ERROR              = 0x80100013
#SCARD_F_UNKNOWN_ERROR           = 0x80100014
#SCARD_E_INVALID_ATR             = 0x80100015
#SCARD_E_NOT_TRANSACTED          = 0x80100016
SCARD_E_READER_UNAVAILABLE      = 0x80100017 # The specified reader is not currently available for use. 
#SCARD_P_SHUTDOWN                = 0x80100018
#SCARD_E_PCI_TOO_SMALL           = 0x80100019
#SCARD_E_READER_UNSUPPORTED      = 0x8010001A
#SCARD_E_DUPLICATE_READER        = 0x8010001B
#SCARD_E_CARD_UNSUPPORTED        = 0x8010001C
#SCARD_E_NO_SERVICE              = 0x8010001D
SCARD_E_SERVICE_STOPPED         = 0x8010001E # The Smart Card Resource Manager has shut down. 
#SCARD_E_UNEXPECTED              = 0x8010001F
#SCARD_E_ICC_INSTALLATION        = 0x80100020
#SCARD_E_ICC_CREATEORDER         = 0x80100021
#SCARD_E_UNSUPPORTED_FEATURE     = 0x80100022
#SCARD_E_DIR_NOT_FOUND           = 0x80100023
#SCARD_E_FILE_NOT_FOUND          = 0x80100024
#SCARD_E_NO_DIR                  = 0x80100025
#SCARD_E_NO_FILE                 = 0x80100026
#SCARD_E_NO_ACCESS               = 0x80100027
#SCARD_E_WRITE_TOO_MANY          = 0x80100028
#SCARD_E_BAD_SEEK                = 0x80100029
SCARD_E_INVALID_CHV             = 0x8010002A # The supplied PIN is incorrect. 
#SCARD_E_UNKNOWN_RES_MNG         = 0x8010002B
#SCARD_E_NO_SUCH_CERTIFICATE     = 0x8010002C
SCARD_E_CERTIFICATE_UNAVAILABLE = 0x8010002D # The requested certificate could not be obtained.
SCARD_E_NO_READERS_AVAILABLE    = 0x8010002E # Cannot find a smart card reader
#SCARD_E_COMM_DATA_LOST          = 0x8010002F
SCARD_E_NO_KEY_CONTAINER        = 0x80100030 # The requested key container does not exist on the smart card
#SCARD_E_SERVER_TOO_BUSY         = 0x80100031
#SCARD_E_PIN_CACHE_EXPIRED       = 0x80100032
#SCARD_E_NO_PIN_CACHE            = 0x80100033
#SCARD_E_READ_ONLY_CARD          = 0x80100034
#SCARD_W_UNSUPPORTED_CARD        = 0x80100065
#SCARD_W_UNRESPONSIVE_CARD       = 0x80100066
#SCARD_W_UNPOWERED_CARD          = 0x80100067
#SCARD_W_RESET_CARD              = 0x80100068
#SCARD_W_REMOVED_CARD            = 0x80100069
#SCARD_W_SECURITY_VIOLATION      = 0x8010006A
SCARD_W_WRONG_CHV               = 0x8010006B # The card cannot be accessed because the wrong PIN was presented.
SCARD_W_CHV_BLOCKED             = 0x8010006C # The card cannot be accessed because the maximum number of PIN entry attempts has been reached.
#SCARD_W_EOF                     = 0x8010006D
SCARD_W_CANCELLED_BY_USER       = 0x8010006E # The action was cancelled by the user.
#SCARD_W_CARD_NOT_AUTHENTICATED  = 0x8010006F
#SCARD_W_CACHE_ITEM_NOT_FOUND    = 0x80100070
#SCARD_W_CACHE_ITEM_STALE        = 0x80100071
#SCARD_W_CACHE_ITEM_TOO_BIG      = 0x80100072




############################################

ftGetLastError  =          CAPIFUNCTYPE(DWORD,        # result
                                       )


ftSetLastError  =          CAPIFUNCTYPE(None,         # result
                                        DWORD         #  _In_ DWORD dwErrCode
                                       )

# XxxW обычно предпочтительнее чем XxxA,
# но в КриптоПро для linux - только FormatMessageA под именем FormatMessage,
# и я не знаю как получить сообщение на русском языке (и пытаться не буду).
# в ViPNet для linux и в windows - обе.

ftFormatMessageA =         CAPIFUNCTYPE(DWORD,        # result
                                        DWORD,        #  _In_     DWORD   dwFlags,
                                        c_void_p,     #  _In_opt_ LPCVOID lpSource,
                                        DWORD,        #  _In_     DWORD   dwMessageId,
                                        DWORD,        #  _In_     DWORD   dwLanguageId,
                                        LPSTR,        #  _Out_    LPTSTR  lpBuffer,
                                        DWORD,        #  _In_     DWORD   nSize,
                                        c_void_p      #  _In_opt_ va_list *Arguments
                                       )

ftFormatMessageW =         CAPIFUNCTYPE(DWORD,        # result
                                        DWORD,        #  _In_     DWORD   dwFlags,
                                        c_void_p,     #  _In_opt_ LPCVOID lpSource,
                                        DWORD,        #  _In_     DWORD   dwMessageId,
                                        DWORD,        #  _In_     DWORD   dwLanguageId,
                                        LPWSTR,       #  _Out_    LPTSTR  lpBuffer,
                                        DWORD,        #  _In_     DWORD   nSize,
                                        c_void_p      #  _In_opt_ va_list *Arguments
                                       )
#


class MSCAPIError(Exception):
    u'Аналог сообщения windows: код + текст'
    def __init__(self, code, message):
        Exception.__init__(self, message)
        self.code = code


def findErrorName(errorCode):
    u'Поиск названия ошибки по коду, findErrorName(0x80004001) -> "E_NOTIMPL"'
    for (n, v) in globals().iteritems():
        if isinstance(v, (int, long)) and v == errorCode:
            return n
    return None
