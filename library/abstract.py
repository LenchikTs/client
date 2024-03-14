# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from functools import update_wrapper

def abstract(f):
    def wrapper(*args, **kwargs):
        raise NotImplementedError('Abstract method is called')

    return update_wrapper(wrapper, f)


# ##################################################

if __name__ == '__main__':

    class CTest:
        def m1(self):
            ":)"
            print 'hello from m1'

        @abstract
        def m2(self):
            ";)"
            print 'hello from m2'

    t = CTest()

    print t.m1.__doc__
    t.m1()

    print t.m2.__doc__
    t.m2()
