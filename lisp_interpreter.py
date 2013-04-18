#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lisp_lexer import lisp_lexer
from lisp_parser import lisp_parser
from lisp_errors import LispError, LispParseError
from lisp import _Namespace, _Fvals, nil, t

from pprint import pprint


def lisp_interpreter(_in=input, out=print):
    _Namespace.clear()
    _Fvals.clear()

    _Namespace['nil'] = nil
    _Namespace['t'] = t
    
    i = 1

    while True:
        try:
            ls = lisp_parser.parse(_in('[{}]> '.format(i)), lexer=lisp_lexer)
        except LispParseError as err:
            out(repr(err))
            continue

        for expr in ls:
            # print('< ', repr(expr))
            try:
                v = expr.eval()
                # out(v)
            except (LispError, RuntimeError) as err:
                print('  Error: ' + repr(err))
                continue

            yield v

            i += 1
