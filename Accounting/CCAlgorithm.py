# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2016-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import __future__


class CCCAlgorithm:
    u'Алгоритм вычисления значения коэффициента'

    builtins = {  'None'  : None,
                  'False' : False,
                  'True'  : True,

                  'int'   : int,
                  'long'  : long,
                  'float' : float,
                  'list'  : list,
                  'tuple' : tuple,

                  'abs'   : abs,
                  'cmp'   : cmp,
                  'max'   : max,
                  'min'   : min,
                  'round' : round,
                  'sum'   : sum,
               }

    def __init__(self, expr):
        if expr:
            self.lam = self.compile(expr)
        else:
            self.lam = None


    def __call__(self, k, duration, minDuration, maxDuration, avgDuration):
        if self.lam:
            return self.lam(k, duration, minDuration, maxDuration, avgDuration)
        else:
            return k


    @classmethod
    def compile(cls, expr):
        expr = unicode(expr).strip()
        if not expr:
            expr = 'k'
        lambdaExpr = 'lambda k, duration, minDuration, maxDuration, avgDuration: (' + expr + ')'
        codeObject = compile(lambdaExpr,
                             expr,
                             'eval',
                             __future__.division.compiler_flag)
        return eval(codeObject, {'__builtins__': cls.builtins})


    @classmethod
    def isOk(cls, expr):
        try:
            cls.compile(expr)
            return True
        except:
            return False
