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
## Биндинг к CryptoproCSP и ViPNetCSP средствами ctypes
##
#############################################################################

import os
import sys

from .cryptoProApi import CryptoProApi
from .vipnetApi    import ViPNetApi


if os.name == 'nt' or sys.platform == 'cygwin':
    from .winApiBinding import WinApiBindingMixin

    class CryptoProApiForWin(CryptoProApi, WinApiBindingMixin):
        def __init__(self, ansiEncoding = 'cp1251'):
            CryptoProApi.__init__(self, ansiEncoding)
            WinApiBindingMixin.__init__(self)


    class VipNetApiForWin(ViPNetApi, WinApiBindingMixin):
        def __init__(self, ansiEncoding = 'cp1251'):
            ViPNetApi.__init__(self, ansiEncoding)
            WinApiBindingMixin.__init__(self)


    def MSCApi(product='cryptopro', ansiEncoding = 'cp1251'):
        p = product.lower()
        if p == 'cryptopro':
            return CryptoProApiForWin(ansiEncoding)
        if p == 'vipnet':
            return VipNetApiForWin(ansiEncoding)
        raise NotImplementedError('Microsoft CryptoAPI for product %r is not implemented for windows' %product )

elif os.name == 'posix':
    from .posixCryptoProApiBinding import PosixCryptoProApiBindingMixin
    from .posixViPNetApiBinding    import PosixViPNetApiBindingMixin

    class CryptoProApiForPosix(CryptoProApi, PosixCryptoProApiBindingMixin):
        def __init__(self, ansiEncoding = 'cp1251'):
            CryptoProApi.__init__(self, ansiEncoding)
            PosixCryptoProApiBindingMixin.__init__(self)


    class ViPNetApiForPosix(ViPNetApi, PosixViPNetApiBindingMixin):
        def __init__(self, ansiEncoding = 'cp1251'):
            ViPNetApi.__init__(self, ansiEncoding)
            PosixViPNetApiBindingMixin.__init__(self)


    def MSCApi(product='cryptopro', ansiEncoding = 'cp1251'):
        p = product.lower()
        if p == 'cryptopro':
            return CryptoProApiForPosix(ansiEncoding)
        if p == 'vipnet':
            return ViPNetApiForPosix(ansiEncoding)
        raise NotImplementedError('Microsoft CryptoAPI for product %r is not implemented for posix' %product )

else:
    raise NotImplementedError('Microsoft CryptoAPI for this platfom not implemented')
