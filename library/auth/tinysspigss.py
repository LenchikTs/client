#-*- coding:utf-8 -*-
##
## Copyright (C) 2015-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## based on kerberos_sspi
## Copyright (c) 2012-2015 Norman Krämer. All rights reserved.
##
#############################################################################

from ctypes import create_string_buffer
from base64 import b64encode, b64decode

import sspi


def _sspi_spn_from_nt_service_name(nt_service_name):
    """
    create a service name consumable by sspi from the nt_service_name fromat used by krb,
    e.g. from http@somehost -> http/somehost
    """
    service = nt_service_name.replace("@", "/", 1)
    return service


"""
GSSAPI Function Result Codes:
    -1 : Error
    0  : GSSAPI step continuation (only returned by 'Step' function)
    1  : GSSAPI step complete, or function return OK

"""

# Some useful result codes
AUTH_GSS_CONTINUE     = 0
AUTH_GSS_COMPLETE     = 1

# Some useful gss flags
GSS_C_DELEG_FLAG      = sspi.ISC_REQ_DELEGATE
GSS_C_MUTUAL_FLAG     = sspi.ISC_REQ_MUTUAL_AUTH
GSS_C_REPLAY_FLAG     = sspi.ISC_REQ_REPLAY_DETECT
GSS_C_SEQUENCE_FLAG   = sspi.ISC_REQ_SEQUENCE_DETECT
GSS_C_CONF_FLAG       = sspi.ISC_REQ_CONFIDENTIALITY
GSS_C_INTEG_FLAG      = sspi.ISC_REQ_INTEGRITY

# leave the following undefined, so if someone relies on them they know that this package
# is not for them
#GSS_C_ANON_FLAG       = 0 
#GSS_C_PROT_READY_FLAG = 0 
#GSS_C_TRANS_FLAG      = 0 

#GSS_AUTH_P_NONE = 1
#GSS_AUTH_P_INTEGRITY = 2
#GSS_AUTH_P_PRIVACY = 4


def authGSSClientInit(service, gssflags=GSS_C_MUTUAL_FLAG|GSS_C_SEQUENCE_FLAG):
    """
    Initializes a context for GSSAPI client-side authentication with the given service principal.
    authGSSClientClean must be called after this function returns an OK result to dispose of
    the context once all GSSAPI operations are complete.

    @param service: a string containing the service principal in the form 'type@fqdn'
        (e.g. 'imap@mail.apple.com').
    @param gssflags: optional integer used to set GSS flags.
        (e.g.  GSS_C_DELEG_FLAG|GSS_C_MUTUAL_FLAG|GSS_C_SEQUENCE_FLAG will allow 
        for forwarding credentials to the remote host)
    @return: a tuple of (result, context) where result is the result code (see above) and
        context is an opaque value that will need to be passed to subsequent functions.
    """

    spn=_sspi_spn_from_nt_service_name(service)
    cred = sspi.SspiCredentials('Kerberos', sspi.SECPKG_CRED_OUTBOUND)

    context = {'cred':     cred,
               'ctx':      None,
#               'service':  service, 
               'spn':      spn,
               'gssflags': gssflags,
               'response': None
              }
    return AUTH_GSS_COMPLETE, context


def authGSSClientClean(context):
    """
    Destroys the context for GSSAPI client-side authentication. After this call the context
    object is invalid and should not be used again.

    @param context: the context object returned from authGSSClientInit.
    @return: a result code (see above).
    """
    if context['ctx'] is not None:
        context['ctx'].close()
    context['cred'].close()
    context['response'] = None

    return AUTH_GSS_COMPLETE


def authGSSClientStep(context, challenge):
    """
    Processes a single GSSAPI client-side step using the supplied server data.

    @param context: the context object returned from authGSSClientInit.
    @param challenge: a string containing the base64-encoded server data (which may be empty
        for the first step).
    @return: a result code (see above).
    """
    data = b64decode(challenge) if challenge else None
    outbuf = create_string_buffer(4096)
    if context['ctx'] is None:
        ctx, status, result_buffers = context['cred'].create_context(
            flags          = context['gssflags'],
            target_name    = context['spn'],
            byte_ordering  = 'network',
            input_buffers  = [(sspi.SECBUFFER_TOKEN, data)] if data else None,
            output_buffers = [(sspi.SECBUFFER_TOKEN, outbuf)]
            )
        context['ctx'] = ctx
    else:
        ctx = context['ctx']
        status, result_buffers = ctx.next(
            flags          = context['gssflags'],
            target_name    = context['spn'],
            byte_ordering  = 'network',
            input_buffers  = [(sspi.SECBUFFER_TOKEN, data)] if data else None,
            output_buffers = [(sspi.SECBUFFER_TOKEN, outbuf)]
            )

    context['response'] = result_buffers[0][1] if result_buffers else None
    return AUTH_GSS_COMPLETE if status == 0 else AUTH_GSS_CONTINUE


def authGSSClientResponse(context):
    """
    Get the client response from the last successful GSSAPI client-side step.

    @param context: the context object returned from authGSSClientInit.
    @return: a string containing the base64-encoded client data to be sent to the server.
    """
    data = context['response']
    return b64encode(data) if data else ''

