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
##    описание общей части CryptoAPI, первая часть функций
##
#############################################################################

from collections import namedtuple
from ctypes import Structure, c_uint, c_void_p, POINTER

from wintypes import PDWORD, CHAR, DWORD, ULONG_PTR, CAPIFUNCTYPE, LPWSTR, PBYTE, BOOL, LPSTR

# типы данных, специфические для этого API
ALG_ID     = c_uint

HCRYPTPROV = ULONG_PTR
HCRYPTKEY  = ULONG_PTR
HCRYPTHASH = ULONG_PTR

PULONG_PTR  = POINTER(ULONG_PTR)
PHCRYPTPROV = PULONG_PTR
PHCRYPTKEY  = PULONG_PTR
PHCRYPTHASH = PULONG_PTR

#############################################################################
#
# CAPI 1.0
#
#############################################################################

class PROV_ENUMALGS(Structure):
    _fields_ = (
                 ('aiAlgid',       ALG_ID  ),
                 ('dwBitLen',      DWORD   ),
                 ('dwNameLen',     DWORD   ),
                 ('szName',        CHAR*20 ),
               )

class PROV_ENUMALGS_EX(Structure):
    _fields_ = (
                 ('aiAlgid',       ALG_ID  ),
                 ('dwDefaultLen',  DWORD   ),
                 ('dwMinLen',      DWORD   ),
                 ('dwMaxLen',      DWORD   ),
                 ('dwProtocols',   DWORD   ),
                 ('dwNameLen',     DWORD   ),
                 ('szName',        CHAR*20 ),
                 ('dwLongNameLen', DWORD   ),
                 ('szLongName',    CHAR*40 ),
               )


# https://msdn.microsoft.com/en-us/library/aa379930(v=vs.85).aspx
ftCryptEnumProviderTypesA= CAPIFUNCTYPE(BOOL,   # result
                                        DWORD,  # _In_    DWORD  dwIndex,      // Index of the next provider type to be enumerated.
                                        PDWORD, # _In_    DWORD  *pdwReserved, // Reserved for future use and must be NULL.
                                        DWORD,  # _In_    DWORD  dwFlags,      // Reserved for future use and must be zero.
                                        PDWORD, # _Out_   DWORD  *pdwProvType, // Address of the DWORD value designating the enumerated provider type.
                                        LPSTR,  # _Out_   LPSTR  pszTypeName,  // A pointer to a buffer that receives the data from the enumerated provider type.
                                        PDWORD  # _Inout_ DWORD  *pcbTypeName  // A pointer to a DWORD value specifying the size, in bytes, of the buffer pointed to by the pszTypeName parameter. When the function returns, the DWORD value contains the number of bytes stored in the buffer.
                                       )
ftCryptEnumProviderTypesW= CAPIFUNCTYPE(BOOL,   # result
                                        DWORD,  # _In_    DWORD  dwIndex,      // Index of the next provider type to be enumerated.
                                        PDWORD, # _In_    DWORD  *pdwReserved, // Reserved for future use and must be NULL.
                                        DWORD,  # _In_    DWORD  dwFlags,      // Reserved for future use and must be zero.
                                        PDWORD, # _Out_   DWORD  *pdwProvType, // Address of the DWORD value designating the enumerated provider type.
                                        LPWSTR, # _Out_   LPTSTR pszTypeName,  // A pointer to a buffer that receives the data from the enumerated provider type.
                                        PDWORD  # _Inout_ DWORD  *pcbTypeName  // A pointer to a DWORD value specifying the size, in bytes, of the buffer pointed to by the pszTypeName parameter. When the function returns, the DWORD value contains the number of bytes stored in the buffer.
                                       )
# Error codes&escriptions:
#e: ERROR_NO_MORE_ITEMS     There are no more items to enumerate.
#e: ERROR_NOT_ENOUGH_MEMORY The operating system ran out of memory.
#e: NTE_BAD_FLAGS           The dwFlags parameter has an unrecognized value.
#e: NTE_FAIL                Something was wrong with the type registration.


# https://msdn.microsoft.com/en-us/library/aa379929(v=vs.85).aspx
ftCryptEnumProvidersA    = CAPIFUNCTYPE(BOOL,   # result
                                        DWORD,  # _In_    DWORD  dwIndex,      // Index of the next provider to be enumerated.
                                        PDWORD, # _In_    DWORD  *pdwReserved, // Reserved for future use and must be NULL.
                                        DWORD,  # _In_    DWORD  dwFlags,      // Reserved for future use and must be zero.
                                        PDWORD, # _Out_   DWORD  *pdwProvType, // Address of the DWORD value designating the type of the enumerated provider.
                                        LPSTR,  # _Out_   LPSTR  pszProvName,  // A pointer to a buffer that receives the data from the enumerated provider. This is a string including the terminating null character.
                                        PDWORD  # _Inout_ DWORD  *pcbProvName  // A pointer to a DWORD value specifying the size, in bytes, of the buffer pointed to by the pszProvName parameter. When the function returns, the DWORD value contains the number of bytes stored in the buffer.
                                       )
ftCryptEnumProvidersW    = CAPIFUNCTYPE(BOOL,   # result
                                        DWORD,  # _In_    DWORD  dwIndex,      // Index of the next provider to be enumerated.
                                        PDWORD, # _In_    DWORD  *pdwReserved, // Reserved for future use and must be NULL.
                                        DWORD,  # _In_    DWORD  dwFlags,      // Reserved for future use and must be zero.
                                        PDWORD, # _Out_   DWORD  *pdwProvType, // Address of the DWORD value designating the type of the enumerated provider.
                                        LPWSTR, # _Out_   LPTSTR pszProvName,  // A pointer to a buffer that receives the data from the enumerated provider. This is a string including the terminating null character.
                                        PDWORD  # _Inout_ DWORD  *pcbProvName  // A pointer to a DWORD value specifying the size, in bytes, of the buffer pointed to by the pszProvName parameter. When the function returns, the DWORD value contains the number of bytes stored in the buffer.
                                       )
# Error codes&escriptions:
#e: ERROR_MORE_DATA         The pszProvName buffer was not large enough to hold the provider name.
#e: ERROR_NO_MORE_ITEMS     There are no more items to enumerate.
#e: ERROR_NOT_ENOUGH_MEMORY The operating system ran out of memory.
#e: NTE_BAD_FLAGS           The dwFlags parameter has an unrecognized value.
#e: NTE_FAIL                Something was wrong with the type registration.


# https://msdn.microsoft.com/en-us/library/aa379945(v=vs.85).aspx
ftCryptGetDefaultProviderA=CAPIFUNCTYPE(BOOL,   # result
                                        DWORD,  # _In_    DWORD  dwProvType,   // The provider type for which the default CSP name is to be found.
                                        PDWORD, # _In_    DWORD  *pdwReserved, // This parameter is reserved for future use and must be NULL.
                                        DWORD,  # _In_    DWORD  dwFlags,      // The following flag values are defined: CRYPT_USER_DEFAULT, CRYPT_MACHINE_DEFAULT
                                        LPSTR,  # _Out_   LPSTR pszProvName,   // A pointer to a null-terminated character string buffer to receive the name of the default CSP.
                                        PDWORD  # _Inout_ DWORD  *pcbProvName  // A pointer to a DWORD value that specifies the size, in bytes, of the buffer pointed to by the pszProvName parameter. When the function returns, the DWORD value contains the number of bytes stored or to be stored in the buffer.
                                       )
ftCryptGetDefaultProviderW=CAPIFUNCTYPE(BOOL,   # result
                                        DWORD,  # _In_    DWORD  dwProvType,   // The provider type for which the default CSP name is to be found.
                                        PDWORD, # _In_    DWORD  *pdwReserved, // This parameter is reserved for future use and must be NULL.
                                        DWORD,  # _In_    DWORD  dwFlags,      // The following flag values are defined: CRYPT_USER_DEFAULT, CRYPT_MACHINE_DEFAULT
                                        LPWSTR, # _Out_   LPTSTR pszProvName,  // A pointer to a null-terminated character string buffer to receive the name of the default CSP.
                                        PDWORD  # _Inout_ DWORD  *pcbProvName  // A pointer to a DWORD value that specifies the size, in bytes, of the buffer pointed to by the pszProvName parameter. When the function returns, the DWORD value contains the number of bytes stored or to be stored in the buffer.
                                       )
# Error codes&escriptions:
#e: ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e: ERROR_MORE_DATA         The buffer for the name is not large enough.
#e: ERROR_NOT_ENOUGH_MEMORY The operating system ran out of memory.
#e: NTE_BAD_FLAGS           The dwFlags parameter has an unrecognized value.
#e: NTE_PROV_TYPE_NOT_DEF   Provider type not defined


# https://msdn.microsoft.com/en-us/library/aa379886(v=vs.85).aspx
ftCryptAcquireContext =    CAPIFUNCTYPE(BOOL,        # result
                                        PHCRYPTPROV, # _Out_ HCRYPTPROV *phProv,     // A pointer to a handle of a CSP.
                                        LPWSTR,      # _In_  LPCTSTR    pszContainer,// The key container name.
                                        LPWSTR,      # _In_  LPCTSTR    pszProvider, // A null-terminated string that contains the name of the CSP to be used.
                                        DWORD,       # _In_  DWORD      dwProvType,  // Specifies the type of provider to acquire.
                                        DWORD        # _In_  DWORD      dwFlags      // see docs :)
                                       )
# Error codes&escriptions:
#e: ERROR_BUSY              Some CSPs set this error if the CRYPT_DELETEKEYSET flag value is set and another thread or process is using this key container.
#e: ERROR_FILE_NOT_FOUND    The profile of the user is not loaded and cannot be found. This happens when the application impersonates a user, for example, the IUSR_ComputerName account.
#e: ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e: ERROR_NOT_ENOUGH_MEMORY The operating system ran out of memory during the operation.
#e: NTE_BAD_FLAGS           The dwFlags parameter has a value that is not valid.
#e: NTE_BAD_KEY_STATE       The user password has changed since the private keys were encrypted.
#e: NTE_BAD_KEYSET          The key container could not be opened. A common cause of this error is that the key container does not exist. To create a key container, call CryptAcquireContext using the CRYPT_NEWKEYSET flag. This error code can also indicate that access to an existing key container is denied. Access rights to the container can be granted by the key set creator by using CryptSetProvParam.
#e: NTE_BAD_KEYSET_PARAM    The pszContainer or pszProvider parameter is set to a value that is not valid.
#e: NTE_BAD_PROV_TYPE       The value of the dwProvType parameter is out of range. All provider types must be from 1 through 999, inclusive.
#e: NTE_BAD_SIGNATURE       The provider DLL signature could not be verified. Either the DLL or the digital signature has been tampered with.
#e: NTE_EXISTS              The dwFlags parameter is CRYPT_NEWKEYSET, but the key container already exists.
#e: NTE_KEYSET_ENTRY_BAD    The pszContainer key container was found but is corrupt.
#e: NTE_KEYSET_NOT_DEF      The requested provider does not exist.
#e: NTE_NO_MEMORY           The CSP ran out of memory during the operation.
#e: NTE_PROV_DLL_NOT_FOUND  The provider DLL file does not exist or is not on the current path.
#e: NTE_PROV_TYPE_ENTRY_BAD The provider type specified by dwProvType is corrupt. This error can relate to either the user default CSP list or the computer default CSP list.
#e: NTE_PROV_TYPE_NO_MATCH  The provider type specified by dwProvType does not match the provider type found. Note that this error can only occur when pszProvider specifies an actual CSP name.
#e: NTE_PROV_TYPE_NOT_DEF   No entry exists for the provider type specified by dwProvType.
#e: NTE_PROVIDER_DLL_FAIL   The provider DLL file could not be loaded or failed to initialize.
#e: NTE_SIGNATURE_FILE_BAD  An error occurred while loading the DLL file image, prior to verifying its signature.


# https://msdn.microsoft.com/en-us/library/aa380268(v=vs.85).aspx
ftCryptReleaseContext =    CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTPROV,  # _In_ HCRYPTPROV hProv,        // Handle of a cryptographic service provider (CSP) created by a call to CryptAcquireContext.
                                        DWORD        # _In_ DWORD      dwFlags       // Reserved for future use and must be zero.
                                       )
#e: ERROR_BUSY              The CSP context specified by hProv is currently being used by another process.
#e: ERROR_INVALID_HANDLE    One of the parameters specifies a handle that is not valid.
#e: ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e: NTE_BAD_FLAGS           The dwFlags parameter is nonzero.
#e: NTE_BAD_UID             The hProv parameter does not contain a valid context handle.


# https://msdn.microsoft.com/en-us/library/aa380196(v=vs.85).aspx
ftCryptGetProvParam =      CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTPROV,  # _In_ HCRYPTPROV hProv,        // A handle of the CSP target of the query. This handle must have been created by using the CryptAcquireContext function.
                                        DWORD,       # _In_    DWORD      dwParam,   // The nature of the query. The following queries are defined... ( see docs! )
                                        PBYTE,       # _Out_   BYTE       *pbData,   // A pointer to a buffer to receive the data. The form of this data varies depending on the value of dwParam. When dwParam is set to PP_USE_HARDWARE_RNG, pbData must be set to NULL.
                                        PDWORD,      # _Inout_ DWORD      *pdwDataLen,// A pointer to a DWORD value that specifies the size, in bytes, of the buffer pointed to by the pbData parameter.
                                        DWORD        # _In_    DWORD      dwFlags    // ...
                                       )
#e: ERROR_INVALID_HANDLE    One of the parameters specifies a handle that is not valid.
#e: ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e: ERROR_MORE_DATA         If the buffer specified by the pbData parameter is not large enough to hold the returned data, the function sets the ERROR_MORE_DATA code and stores the required buffer size, in bytes, in the variable pointed to by pdwDataLen.
#e: ERROR_NO_MORE_ITEMS     The end of the enumeration list has been reached. No valid data has been placed in the pbData buffer. This error code is returned only when dwParam equals PP_ENUMALGS or PP_ENUMCONTAINERS.
#e: NTE_BAD_FLAGS           The dwFlags parameter specifies a flag that is not valid.
#e: NTE_BAD_TYPE            The dwParam parameter specifies an unknown value number.
#e: NTE_BAD_UID             The CSP context specified by hProv is not valid.


# https://msdn.microsoft.com/en-us/library/aa380276(v=vs.85).aspx
ftCryptSetProvParam =      CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTPROV,  # _In_ HCRYPTPROV hProv,        // A handle of the CSP target of the query. This handle must have been created by using the CryptAcquireContext function.
                                        DWORD,       # _In_    DWORD      dwParam,   // The nature of the query. The following queries are defined... ( see docs! )
                                        PBYTE,       # _Out_   BYTE       *pbData,   // A pointer to a buffer initialized with the value to be set before calling CryptSetKeyParam. The form of this data varies depending on the value of dwParam.
                                        DWORD        # _In_    DWORD      dwFlags    // ...
                                       )
#e: ERROR_BUSY              The CSP context is currently being used by another process.
#e: ERROR_INVALID_HANDLE    One of the parameters specifies a handle that is not valid.
#e: ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e: NTE_BAD_FLAGS           The dwFlags parameter is nonzero, or the pbData buffer contains a value that is not valid.
#e: NTE_BAD_TYPE            The dwParam parameter specifies an unknown parameter.
#e: NTE_BAD_UID             The CSP context that was specified when the hKey key was created cannot be found.
#e: NTE_FAIL                The function failed in some unexpected way.
#e: NTE_FIXEDPARAMETER      Some CSPs have hard-coded P, Q, and G values. If this is the case, then using KP_P, KP_Q, and KP_G for the value of dwParam causes this error.

# https://msdn.microsoft.com/en-us/library/aa379942(v=vs.85).aspx
ftCryptGenRandom =         CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTPROV,  # _In_    HCRYPTPROV hProv,       # Handle of a cryptographic service provider (CSP) created by a call to CryptAcquireContext.
                                        DWORD,       # _In_    DWORD      dwLen,       # Number of bytes of random data to be generated.
                                        PBYTE        # _Inout_ BYTE       *pbBuffer    # Buffer to receive the returned data. This buffer must be at least dwLen bytes in length.
                                       )
#e ERROR_INVALID_HANDLE    One of the parameters specifies a handle that is not valid.
#e ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e NTE_BAD_UID             The hProv parameter does not contain a valid context handle.
#e NTE_FAIL                The function failed in some unexpected way.

# https://msdn.microsoft.com/en-us/library/aa379941(v=vs.85).aspx
ftCryptGenKey =            CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTPROV,  # _In_  HCRYPTPROV hProv,       // A handle to a cryptographic service provider (CSP) created by a call to CryptAcquireContext.
                                        ALG_ID,      # _In_  ALG_ID     Algid,       // An ALG_ID value that identifies the algorithm for which the key is to be generated. Values for this parameter vary depending on the CSP used.
                                        DWORD,       # _In_  DWORD      dwFlags,     // Specifies the type of key generated. [TL;DR - TL;DC]
                                        PHCRYPTKEY   # _Out_ HCRYPTKEY  *phKey       // Address to which the function copies the handle of the newly generated key.
                                       )
#e: ERROR_INVALID_HANDLE    One of the parameters specifies a handle that is not valid.
#e: ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e: NTE_BAD_ALGID           The Algid parameter specifies an algorithm that this CSP does not support.
#e: NTE_BAD_FLAGS           The dwFlags parameter contains a value that is not valid.
#e: NTE_BAD_UID             The hProv parameter does not contain a valid context handle.
#e: NTE_FAIL                The function failed in some unexpected way.
#e: NTE_SILENT_CONTEXT      The provider could not perform the action because the context was acquired as silent.

# https://msdn.microsoft.com/en-us/library/aa379920(v=vs.85).aspx
ftCryptDuplicateKey =      CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTKEY,   # _In_  HCRYPTKEY hKey,         // A handle to the key to be duplicated.
                                        c_void_p,    # _In_  DWORD     *pdwReserved, // Reserved for future use and must be NULL.
                                        DWORD,       # _In_  DWORD     dwFlags,      // Reserved for future use and must be zero.
                                        PHCRYPTKEY   # _Out_ HCRYPTKEY  *phKey       // Address of the handle to the duplicated key. When you have finished using the key, release the handle by calling the CryptDestroyKey function.
                                       )
#e: ERROR_CALL_NOT_IMPLEMENTED Because this is a new function, existing CSPs might not implement it. This error is returned if the CSP does not support this function.
#e: ERROR_INVALID_PARAMETER    One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e: NTE_BAD_KEY                A handle to the original key is not valid.


# https://msdn.microsoft.com/en-us/library/aa380199(v=vs.85).aspx
ftCryptGetUserKey =        CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTPROV,  # _In_  HCRYPTPROV hProv,       // HCRYPTPROV handle of a cryptographic service provider (CSP) created by a call to CryptAcquireContext.
                                        DWORD,       # _In_  DWORD      dwKeySpec,   // Identifies the private key to use from the key container. It can be AT_KEYEXCHANGE or AT_SIGNATURE.
                                        PHCRYPTKEY   # _Out_ HCRYPTKEY  *phUserKey   // A pointer to the HCRYPTKEY handle of the retrieved keys. When you have finished using the key, delete the handle by calling the CryptDestroyKey function.
                                       )
#e: ERROR_INVALID_HANDLE    One of the parameters specifies a handle that is not valid.
#e: ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e: NTE_BAD_KEY             The dwKeySpec parameter contains a value that is not valid.
#e: NTE_BAD_UID             The hProv parameter does not contain a valid context handle.
#e: NTE_NO_KEY              The key requested by the dwKeySpec parameter does not exist.


# https://msdn.microsoft.com/en-us/library/aa380207(v=vs.85).aspx
ftCryptImportKey =         CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTPROV,  # _In_  HCRYPTPROV hProv,       // The handle of a CSP obtained with the CryptAcquireContext function.
                                        PBYTE,       # _In_  BYTE       *pbData,     // A BYTE array that contains a PUBLICKEYSTRUC BLOB header followed by the encrypted key. This key BLOB is created by the CryptExportKey function, either in this application or by another application possibly running on a different computer.
                                        DWORD,       # _In_  DWORD      dwDataLen,   // Contains the length, in bytes, of the key BLOB.
                                        HCRYPTKEY,   # _In_  HCRYPTKEY  hPubKey,     // A handle to the cryptographic key that decrypts the key stored in pbData.
                                        DWORD,       # _In_  DWORD      dwFlags,     // Currently used only when a public/private key pair in the form of a PRIVATEKEYBLOB is imported into the CSP.
                                        PHCRYPTKEY   # _Out_ HCRYPTKEY  *phKey       // A pointer to a HCRYPTKEY value that receives the handle of the imported key.
                                       )
#e: ERROR_BUSY              Some CSPs set this error if a private key is imported into a container while another thread or process is using this key.
#e: ERROR_INVALID_HANDLE    One of the parameters specifies a handle that is not valid.
#e: ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e: NTE_BAD_ALGID           The simple key BLOB to be imported is not encrypted with the expected key exchange algorithm.
#e: NTE_BAD_DATA            Either the algorithm that works with the public key to be imported is not supported by this CSP, or an attempt was made to import a session key that was encrypted with something other than one of your public keys.
#e: NTE_BAD_FLAGS           The dwFlags parameter specified is not valid.
#e: NTE_BAD_TYPE            The key BLOB type is not supported by this CSP and is possibly not valid.
#e: NTE_BAD_UID             The hProv parameter does not contain a valid context handle.
#e: NTE_BAD_VER             The version number of the key BLOB does not match the CSP version. This usually indicates that the CSP needs to be upgraded.


# https://msdn.microsoft.com/en-us/library/windows/desktop/aa379949(v=vs.85).aspx
ftCryptGetKeyParam =       CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTKEY,   # _In_ HCRYPTKEY hKey           // The handle of the key being queried.
                                        DWORD,       # _In_    DWORD     dwParam,    // KP*
                                        PBYTE,       # _Out_   BYTE      *pbData,    // A pointer to a buffer that receives the data. The form of this data depends on the value of dwParam.
                                        PDWORD,      # _Inout_ DWORD     *pdwDataLen,// A pointer to a DWORD value that, on entry, contains the size, in bytes, of the buffer pointed to by the pbData parameter. When the function returns, the DWORD value contains the number of bytes stored in the buffer.
                                        DWORD        # _In_    DWORD     dwFlags     // This parameter is reserved for future use and must be set to zero.
                                       )
#e: ERROR_INVALID_HANDLE    One of the parameters specifies a handle that is not valid.
#e: ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e: ERROR_MORE_DATA         If the buffer specified by the pbData parameter is not large enough to hold the returned data, the function sets the ERROR_MORE_DATA code and stores the required buffer size, in bytes, in the variable pointed to by pdwDataLen.
#e: NTE_BAD_FLAGS           The dwFlags parameter is nonzero.
#e: NTE_BAD_KEY             The key specified by the hKey parameter is not valid.
#e: NTE_NO_KEY              The key specified by the hKey parameter is not valid.
#e: NTE_BAD_TYPE            The dwParam parameter specifies an unknown value number.
#e: NTE_BAD_UID             The CSP context that was specified when the key was created cannot be found.


# https://msdn.microsoft.com/en-us/library/aa380272(v=vs.85).aspx
ftCryptSetKeyParam =       CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTKEY,   # _In_       HCRYPTKEY hKey,
                                        DWORD,       # _In_       DWORD     dwParam,
                                        PBYTE,       # _In_ const BYTE      *pbData,
                                        DWORD        # _In_       DWORD     dwFlags
                                       )
#e: ERROR_BUSY              The CSP context is currently being used by another process.
#e: ERROR_INVALID_HANDLE    One of the parameters specifies a handle that is not valid.
#e: ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e: NTE_BAD_FLAGS           The dwFlags parameter is nonzero, or the pbData buffer contains a value that is not valid.
#e: NTE_BAD_TYPE            The dwParam parameter specifies an unknown parameter.
#e: NTE_BAD_UID             The CSP context that was specified when the hKey key was created cannot be found.
#e: NTE_FAIL                The function failed in some unexpected way.
#e: NTE_FIXEDPARAMETER      Some CSPs have hard-coded P, Q, and G values. If this is the case, then using KP_P, KP_Q, and KP_G for the value of dwParam causes this error.


#https://msdn.microsoft.com/en-us/library/aa379931(v=vs.85).aspx
ftCryptExportKey =         CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTKEY,   # _In_ HCRYPTKEY hKey           // A handle to the key to be exported.
                                        HCRYPTKEY,   # _In_ HCRYPTKEY hExpKey,       // A handle to a cryptographic key of the destination user. The key data within the exported key BLOB is encrypted using this key. This ensures that only the destination user is able to make use of the key BLOB. Both hExpKey and hKey must come from the same CSP.
                                        DWORD,       # _In_    DWORD     dwBlobType, // Specifies the type of key BLOB to be exported in pbData.
                                        DWORD,       # _In_    DWORD     dwFlags,    // Specifies additional options for the function. This parameter can be zero or a combination of one or more of the following values.
                                        PBYTE,       # _Out_   BYTE      *pbData,    // A pointer to a buffer that receives the key BLOB data.
                                        PDWORD       # _Inout_ DWORD     *pdwDataLen // A pointer to a DWORD value that, on entry, contains the size, in bytes, of the buffer pointed to by the pbData parameter. When the function returns, this value contains the number of bytes stored in the buffer.
                                       )
#e: ERROR_INVALID_HANDLE    One of the parameters specifies a handle that is not valid.
#e: ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e: ERROR_MORE_DATA         If the buffer specified by the pbData parameter is not large enough to hold the returned data, the function sets the ERROR_MORE_DATA code and stores the required buffer size, in bytes, in the variable pointed to by pdwDataLen.
#e: NTE_BAD_DATA            Either the algorithm that works with the public key to be exported is not supported by this CSP, or an attempt was made to export a session key that was encrypted with something other than one of your public keys.
#e: NTE_BAD_FLAGS           The dwFlags parameter is nonzero.
#e: NTE_BAD_KEY             One or both of the keys specified by hKey and hExpKey are not valid.
#e: NTE_BAD_KEY_STATE       You do not have permission to export the key. That is, when the hKey key was created, the CRYPT_EXPORTABLE flag was not specified.
#e: NTE_BAD_PUBLIC_KEY      The key BLOB type specified by dwBlobType is PUBLICKEYBLOB, but hExpKey does not contain a public key handle.
#e: NTE_BAD_TYPE            The dwBlobType parameter specifies an unknown BLOB type.
#e: NTE_BAD_UID             The CSP context that was specified when the hKey key was created cannot be found.
#e: NTE_NO_KEY              A session key is being exported, and the hExpKey parameter does not specify a public key.


# https://msdn.microsoft.com/en-us/library/aa379918(v=vs.85).aspx
ftCryptDestroyKey =        CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTKEY    # _In_ HCRYPTKEY hKey           // The handle of the key to be destroyed.
                                       )
#e: ERROR_BUSY              The key object specified by hKey is currently being used and cannot be destroyed.
#e: ERROR_INVALID_HANDLE    The hKey parameter specifies a handle that is not valid.
#e: ERROR_INVALID_PARAMETER The hKey parameter contains a value that is not valid.
#e: NTE_BAD_KEY             The hKey parameter does not contain a valid handle to a key.
#e: NTE_BAD_UID             The CSP context that was specified when the key was created cannot be found.


# https://msdn.microsoft.com/en-us/library/aa379908(v=vs.85).aspx
ftCryptCreateHash =        CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTPROV,  # _In_ HCRYPTPROV hProv,        // A handle to a CSP created by a call to CryptAcquireContext.
                                        ALG_ID,      # _In_  ALG_ID                  // Algid, An ALG_ID value that identifies the hash algorithm to use.
                                        HCRYPTKEY,   # _In_  HCRYPTKEY  hKey,        // If the type of hash algorithm is a keyed hash, such as the Hash-Based Message Authentication Code (HMAC) or Message Authentication Code (MAC) algorithm, the key for the hash is passed in this parameter. For nonkeyed algorithms, this parameter must be set to zero.
                                        DWORD,       # _In_  DWORD      dwFlags,     // must be 0
                                        PHCRYPTHASH  # _Out_ HCRYPTHASH *phHash      // The address to which the function copies a handle to the new hash object. When you have finished using the hash object, release the handle by calling the CryptDestroyHash function.
                                       )
#e: ERROR_INVALID_HANDLE    One of the parameters specifies a handle that is not valid.
#e: ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e: ERROR_NOT_ENOUGH_MEMORY The operating system ran out of memory during the operation.
#e: NTE_BAD_ALGID           The Algid parameter specifies an algorithm that this CSP does not support.
#e: NTE_BAD_FLAGS           The dwFlags parameter is nonzero.
#e: NTE_BAD_KEY             A keyed hash algorithm, such as CALG_MAC, is specified by Algid, and the hKey parameter is either zero or it specifies a key handle that is not valid. This error code is also returned if the key is to a stream cipher or if the cipher mode is anything other than CBC.
#e: NTE_NO_MEMORY           The CSP ran out of memory during the operation.


# https://msdn.microsoft.com/en-us/library/aa379919(v=vs.85).aspx
ftCryptDuplicateHash =     CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTHASH,  # _In_  HCRYPTHASH hHash,
                                        PDWORD,      #  _In_  DWORD      *pdwReserved,
                                        DWORD,       #  _In_  DWORD      dwFlags,
                                        PHCRYPTHASH  #  _Out_ HCRYPTHASH *phHash
                                       )
#e: ERROR_CALL_NOT_IMPLEMENTED Because this is a new function, existing CSPs cannot implement it. This error is returned if the CSP does not support this function.
#e: ERROR_INVALID_PARAMETER    One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e: NTE_BAD_HASH               A handle to the original hash is not valid.


# https://msdn.microsoft.com/en-us/library/aa380202(v=vs.85).aspx
ftCryptHashData =          CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTHASH,  # _In_ HCRYPTHASH hHash,        // Handle of the hash object.
                                        PBYTE,       # _In_ BYTE       *pbData,      // A pointer to a buffer that contains the data to be added to the hash object.
                                        DWORD,       # _In_ DWORD      dwDataLen,    // Number of bytes of data to be added. This must be zero if the CRYPT_USERDATA flag is set.
                                        DWORD        # _In_ DWORD      dwFlags       // must be 0
                                       )
#e: ERROR_INVALID_HANDLE    One of the parameters specifies a handle that is not valid.
#e: ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e: NTE_BAD_ALGID           The hHash handle specifies an algorithm that this CSP does not support.
#e: NTE_BAD_FLAGS           The dwFlags parameter contains a value that is not valid.
#e: NTE_BAD_HASH            The hash object specified by the hHash parameter is not valid.
#e: NTE_BAD_HASH_STATE      An attempt was made to add data to a hash object that is already marked "finished."
#e: NTE_BAD_KEY             A keyed hash algorithm is being used, but the session key is no longer valid. This error is generated if the session key is destroyed before the hashing operation is complete.
#e: NTE_BAD_LEN             The CSP does not ignore the CRYPT_USERDATA flag, the flag is set, and the dwDataLen parameter has a nonzero value.
#e: NTE_BAD_UID             The CSP context that was specified when the hash object was created cannot be found.
#e: NTE_FAIL                The function failed in some unexpected way.
#e: NTE_NO_MEMORY           The CSP ran out of memory during the operation.


# https://msdn.microsoft.com/en-us/library/aa379947(v=vs.85).aspx
ftCryptGetHashParam =      CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTHASH,  # _In_    HCRYPTHASH hHash,     // Handle of the hash object to be queried
                                        DWORD,       # _In_    DWORD      dwParam,   // Query type.
                                        PBYTE,       # _Out_   BYTE       *pbData,   // A pointer to a buffer that receives the specified value data. The form of this data varies, depending on the value number. This parameter can be NULL to determine the memory size required.
                                        PDWORD,      # _Inout_ DWORD      *pdwDataLen, // A pointer to a DWORD value specifying the size, in bytes, of the pbData buffer.
                                        DWORD        # _In_    DWORD      dwFlags    // Reserved for future use and must be zero.
                                       )
#e: ERROR_INVALID_HANDLE    One of the parameters specifies a handle that is not valid.
#e: ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e: ERROR_MORE_DATA         If the buffer specified by the pbData parameter is not large enough to hold the returned data, the function sets the ERROR_MORE_DATA code and stores the required buffer size, in bytes, in the variable pointed to by pdwDataLen.
#e: NTE_BAD_FLAGS           The dwFlags parameter is nonzero.
#e: NTE_BAD_HASH            The hash object specified by the hHash parameter is not valid.
#e: NTE_BAD_TYPE            The dwParam parameter specifies an unknown value number.
#e: NTE_BAD_UID             The CSP context that was specified when the hash was created cannot be found.


# https://msdn.microsoft.com/en-us/library/aa380280(v=vs.85).aspx
ftCryptSignHash =          CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTHASH,  # _In_    HCRYPTHASH hHash,     // Handle of the hash object to be signed.
                                        DWORD,       # _In_    DWORD      dwKeySpec, // Identifies the private key to use from the provider's container. It can be AT_KEYEXCHANGE or AT_SIGNATURE.
                                        LPWSTR,      # _In_    LPCTSTR    sDescription, // This parameter is no longer used and must be set to NULL.
                                        DWORD,       # _In_    DWORD      dwFlags,      // The following flag values are defined: CRYPT_NOHASHOID, CRYPT_TYPE2_FORMAT, CRYPT_X931_FORMAT
                                        PBYTE,       # _Out_   BYTE       *pbSignature, // A pointer to a buffer receiving the signature data, NULL for size uery
                                        PDWORD       # _Inout_ DWORD      *pdwSigLen // A pointer to a DWORD value that specifies the size, in bytes, of the pbSignature buffer. When the function returns, the DWORD value contains the number of bytes stored in the buffer.
                                       )
#e: ERROR_INVALID_HANDLE    One of the parameters specifies a handle that is not valid.
#e: ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e: ERROR_MORE_DATA         The buffer specified by the pbSignature parameter is not large enough to hold the returned data. The required buffer size, in bytes, is in the pdwSigLenDWORD value.
#e: NTE_BAD_ALGID           The hHash handle specifies an algorithm that this CSP does not support, or the dwKeySpec parameter has an incorrect value.
#e: NTE_BAD_FLAGS           The dwFlags parameter is nonzero.
#e: NTE_BAD_HASH            The hash object specified by the hHash parameter is not valid.
#e: NTE_BAD_UID             The CSP context that was specified when the hash object was created cannot be found.
#e: NTE_NO_KEY              The private key specified by dwKeySpec does not exist.
#e: NTE_NO_MEMORY           The CSP ran out of memory during the operation.


# https://msdn.microsoft.com/en-us/library/aa381097(v=vs.85).aspx
ftCryptVerifySignature =   CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTHASH,  # _In_ HCRYPTHASH hHas    h,    // A handle to the hash object to verify
                                        PBYTE,       # _In_ BYTE       *pbSignature, // The address of the signature data to be verified.
                                        DWORD,       # _In_ DWORD      dwSigLen,     // The number of bytes in the pbSignature signature data.
                                        HCRYPTKEY,   # _In_ HCRYPTKEY  hPubKey,      // A handle to the public key to use to authenticate the signature. This public key must belong to the key pair that was originally used to create the digital signature.
                                        LPWSTR,      # _In_ LPCTSTR    sDescription, // This parameter should no longer be used and must be set to NULL.
                                        DWORD        # _In_ DWORD      dwFlags       // As CryptSignHash.dwFlags
                                       )
#e: ERROR_INVALID_HANDLE    One of the parameters specifies a handle that is not valid.
#e: ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e: NTE_BAD_FLAGS           The dwFlags parameter is nonzero.
#e: NTE_BAD_HASH            The hash object specified by the hHash parameter is not valid.
#e: NTE_BAD_KEY             The hPubKey parameter does not contain a handle to a valid public key.
#e: NTE_BAD_SIGNATURE       The signature was not valid. This might be because the data itself has changed, the description string did not match, or the wrong public key was specified by hPubKey. This error can also be returned if the hashing or signature algorithms do not match the ones used to create the signature.
#e: NTE_BAD_UID             The cryptographic service provider (CSP) context that was specified when the hash object was created cannot be found.
#e: NTE_NO_MEMORY           The CSP ran out of memory during the operation.


# https://msdn.microsoft.com/en-us/library/aa379917(v=vs.85).aspx
ftCryptDestroyHash =       CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTHASH   # _In_ HCRYPTHASH hHash         // Handle of the hash object.
                                       )
#e: ERROR_BUSY              The hash object specified by hHash is currently being used and cannot be destroyed.
#e: ERROR_INVALID_HANDLE    The hHash parameter specifies a handle that is not valid.
#e: ERROR_INVALID_PARAMETER The hHash parameter contains a value that is not valid.
#e: NTE_BAD_ALGID           The hHash handle specifies an algorithm that this CSP does not support.
#e: NTE_BAD_HASH            The hash object specified by the hHash parameter is not valid.
#e: NTE_BAD_UID             The CSP context that was specified when the hash object was created cannot be found.


# https://msdn.microsoft.com/en-us/library/aa379924(v=vs.85).aspx
ftCryptEncrypt =           CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTKEY,   # _In_    HCRYPTKEY  hKey,        # A handle to the encryption key.
                                        HCRYPTHASH,  # _In_    HCRYPTHASH hHash,       # A handle to a hash object... If no hash is to be done, this parameter must be NULL.
                                        BOOL,        # _In_    BOOL       Final,       # A Boolean value that specifies whether this is the last section in a series being encrypted. Final is set to TRUE for the last or only block and to FALSE if there are more blocks to be encrypted. For more information, see Remarks.
                                        DWORD,       # _In_    DWORD      dwFlags,     # Usualy 0
                                        PBYTE,       # _Inout_ BYTE       *pbData,     # A pointer to a buffer that contains the plaintext to be encrypted. The plaintext in this buffer is overwritten with the ciphertext created by this function.
                                        PDWORD,      # _Inout_ DWORD      *pdwDataLen, # A pointer to a DWORD value that, on entry, contains the length, in bytes, of the plaintext in the pbData buffer. On exit, this DWORD contains the length, in bytes, of the ciphertext written to the pbData buffer.
                                        DWORD,       # _In_    DWORD      dwBufLen     # Specifies the total size, in bytes, of the input pbData buffer.
                                       )
#e ERROR_INVALID_HANDLE    One of the parameters specifies a handle that is not valid.
#e ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e NTE_BAD_ALGID           The hKey session key specifies an algorithm that this CSP does not support.
#e NTE_BAD_DATA            The data to be encrypted is not valid. For example, when a block cipher is used and the Final flag is FALSE, the value specified by pdwDataLen must be a multiple of the block size.
#e NTE_BAD_FLAGS           The dwFlags parameter is nonzero.
#e NTE_BAD_HASH            The hHash parameter contains a handle that is not valid.
#e NTE_BAD_HASH_STATE      An attempt was made to add data to a hash object that is already marked "finished."
#e NTE_BAD_KEY             The hKey parameter does not contain a valid handle to a key.
#e NTE_BAD_LEN             The size of the output buffer is too small to hold the generated ciphertext.
#e NTE_BAD_UID             The CSP context that was specified when the key was created cannot be found.
#e NTE_DOUBLE_ENCRYPT      The application attempted to encrypt the same data twice.
#e NTE_FAIL                The function failed in some unexpected way.
#e NTE_NO_MEMORY           The CSP ran out of memory during the operation.


#https://msdn.microsoft.com/en-us/library/aa379913(v=vs.85).aspx
ftCryptDecrypt =           CAPIFUNCTYPE(BOOL,        # result
                                        HCRYPTKEY,   # _In_    HCRYPTKEY  hKey,        # A handle to the key to use for the decryption.
                                        HCRYPTHASH,  # _In_    HCRYPTHASH hHash,       # A handle to a hash object... If no hash is to be done, this parameter must be NULL.
                                        BOOL,        # _In_    BOOL       Final,       # A Boolean value that specifies whether this is the last section in a series being decrypted. This value is TRUE if this is the last or only block. If this is not the last block, this value is FALSE. For more information, see Remarks.
                                        DWORD,       # _In_    DWORD      dwFlags,     # Usualy 0
                                        PBYTE,       # _Inout_ BYTE       *pbData,     # A pointer to a buffer that contains the data to be decrypted. After the decryption has been performed, the plaintext is placed back into this same buffer.
                                        PDWORD       # _Inout_ DWORD      *pdwDataLen, # A pointer to a DWORD value that indicates the length of the pbData buffer. Before calling this function, the calling application sets the DWORD value to the number of bytes to be decrypted. Upon return, the DWORD value contains the number of bytes of the decrypted plaintext.
                                       )
#e ERROR_INVALID_HANDLE    One of the parameters specifies a handle that is not valid.
#e ERROR_INVALID_PARAMETER One of the parameters contains a value that is not valid. This is most often a pointer that is not valid.
#e NTE_BAD_ALGID           The hKey session key specifies an algorithm that this CSP does not support.
#e NTE_BAD_DATA            The data to be decrypted is not valid. For example, when a block cipher is used and the Final flag is FALSE, the value specified by pdwDataLen must be a multiple of the block size. This error can also be returned when the padding is found to be not valid.
#e NTE_BAD_FLAGS           The dwFlags parameter is nonzero.
#e NTE_BAD_HASH            The hHash parameter contains a handle that is not valid.
#e NTE_BAD_KEY             The hKey parameter does not contain a valid handle to a key.
#e NTE_BAD_LEN             The size of the output buffer is too small to hold the generated plaintext.
#e NTE_BAD_UID             The CSP context that was specified when the key was created cannot be found.
#e NTE_DOUBLE_ENCRYPT      The application attempted to decrypt the same data twice.
#e NTE_FAIL                The function failed in some unexpected way.


# для удобства просмотра результатов CryptEnumProviderTypes:
ProviderTypeDescr = namedtuple('ProviderTypeDescr', ('type', 'name'))
ProviderDescr     = namedtuple('ProviderDescr',     ('type', 'name'))
AlgDescr          = namedtuple('AlgDescr',          ('algId', 'name', 'bitLen'))
AlgDescrEx        = namedtuple('AlgDescrEx',        ('algId', 'name', 'longName', 'defaultLen', 'minLen', 'maxLen', 'protocols'))

