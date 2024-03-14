# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import __future__
import keyword
import operator
import re
import symtable

from library.Utils            import exceptionToUnicode

__all__ = ( 'isIdentifier',
            'functions',
            'checkExpr',
            'buildMapWhatdepends',
            'buildExecutionPlan',
          )



def avg(vs):
    cnt = 0
    s   = 0.0
    for v in vs:
        if v is not None:
            cnt += 1
            s += v
    return s/cnt if cnt else 0


def search_(required, dictOrPairs, isEqual, default=None):
   if hasattr(dictOrPairs, 'iteritems'):
       pairs = dictOrPairs.iteritems()
   elif hasattr(dictOrPairs, 'items'):
       pairs = dictOrPairs.items()
   else:
       pairs = dictOrPairs

   for key, val in pairs:
       if isEqual(required, key):
           return val
   return default


def search(required, dictOrPairs, default=None):
    return search_(required, dictOrPairs, operator.eq, default)


def searchStart(required, dictOrPairs, default=None):
    def isEqual(required, key):
        if required is None:
            required = ''
        elif isinstance(required, unicode):
            pass
        else:
            required = unicode(required)
        return required.startswith(key)
    return search_(required, dictOrPairs, isEqual, default)


def searchEnd(required, dictOrPairs, default=None):
    def isEqual(required, key):
        if required is None:
            required = ''
        elif isinstance(required, unicode):
            pass
        else:
            required = unicode(required)
        return required.endswith(key)
    return search_(required, dictOrPairs, isEqual, default)


def searchIn(required, dictOrPairs, default=None):
    def isEqual(required, key):
        if required is None:
            required = ''
        elif isinstance(required, unicode):
            pass
        else:
            required = unicode(required)
        return key in required
    return search_(required, dictOrPairs, isEqual, default)


def searchMatch(required, dictOrPairs, default=None):
    def isEqual(required, key):
        if required is None:
            required = ''
        elif isinstance(required, unicode):
            pass
        else:
            required = unicode(required)
        return re.match(key, required, re.DOTALL|re.UNICODE)
    return search_(required, dictOrPairs, isEqual, default)


def searchRange(required, dictOrPairs, default=None):
    def isEqual(required, key):
        return key[0] <= required < key[1]
    return search_(required, dictOrPairs, isEqual, default)


functions = {
              # константы

              'None'    : None,
              'False'   : False,
              'True'    : True,

              # типы
              'bool'    : bool,
              'dict'    : dict,
              'float'   : float,
              'int'     : int,
              'list'    : list,
              'set'     : set,
              'str'     : str,
              'tuple'   : tuple,
              'unicode' : unicode,
              'range'   : range,
              'xrange'  : xrange,

              # встроенные функции
              'abs'     : abs,
              'all'     : all,
              'any'     : any,
              'len'     : len,
              'max'     : max,
              'min'     : min,
              'reversed': reversed,
              'round'   : round,
              'sorted'  : sorted,
              'sum'     : sum,

              # наши функции
              'avg'         : avg,
              'search'      : search,
              'searchStart' : searchStart,
              'searchEnd'   : searchEnd,
              'searchIn'    : searchIn,
              'searchMatch' : searchMatch,
              'searchRange' : searchRange,
            }


def isIdentifier(v):
    return (     bool(re.match('[A-Za-z_][A-Za-z_0-9]*', v))
             and not keyword.iskeyword(v)
             and v not in functions
           )


def compileAndDetermineDependeces(var, expr, variables, fs=None):
    fs = fs or functions
    filename = '<def_%s>' % var
    co = compile(expr, filename, 'eval', __future__.division.compiler_flag|__future__.unicode_literals.compiler_flag)
    depends = []
    symTable = symtable.symtable(expr.encode('utf-8'), filename, 'eval')
    for name in symTable.get_identifiers():
        if name in fs:
            pass
        elif variables is None or name in variables:
            depends.append(name)
        else:
            raise Exception(u'«%s» не является именем переменной или функции' % name)
    return co, depends


def buildMapWhatdepends(mapDepends):
    # преобразование отображения переменная->список_влияющих_переменных
    # в отображение переменная->список_зависимых_переменных
    # в результат добавляется None->список_константных_переменных
    result = {}
    for var, depends in mapDepends.iteritems():
        if depends:
            for var2 in depends:
                result.setdefault(var2, []).append(var)
        else:
            result.setdefault(None, []).append(var)
    return result


def buildExecutionPlan(initialVar, mapWhatDepends):
    # Фантазия на тему алгоритма Тарьяна
    # белый:  0
    # серый:  1
    # чёрный: 2
    vars = set()
    for var, whatDepends in mapWhatDepends.iteritems():
        vars.add(var)
        vars.update(whatDepends)
    color     = dict( (var,0) for var in vars )
    revPlan   = []

    def explore(var, path):
        if color[var] == 2: # чёрный
            return
        if color[var] == 1: # серый
            loop = path[path.index(var):]
            raise Exception(u'Обнаружен цикл ' +  u' → '.join(u'«%s»' % v for v in loop))
        if var in mapWhatDepends:
            color[var] = 1 # серый
            for depVar in mapWhatDepends[var]:
                explore(depVar, path + [depVar])
        revPlan.append(var)
        color[var] = 2 # чёрный

    explore(initialVar, [initialVar])
    return revPlan[-2::-1]

### Удалить -

def checkExpr(expr, variables, fs=None):
    fs = fs or functions
    try:
        filename = '<line>'
        co = compile(expr, filename, 'eval', __future__.division.compiler_flag|__future__.unicode_literals.compiler_flag)
        symTable = symtable.symtable(expr.encode('utf-8'), filename, 'eval')
        for name in symTable.get_identifiers():
            if name in variables or name in fs:
                pass
            else:
                return False, u'«%s» не является именем переменной или функции' % name
        return True, ''
    except Exception as e:
        return False, exceptionToUnicode(e)


