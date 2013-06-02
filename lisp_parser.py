#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ply.yacc as yacc
from functools import reduce


from lisp import *


####################################################################


# Get the token map from the lexer.
from lisp_lexer import tokens
from lisp_errors import LispParseError


def p_source(p):
    """
    source : empty
           | lsource 
    """
    p[0] = [] if not p[1] else p[1]

def p_lsource(p):
    """
    lsource : expr
            | lsource expr
    """
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = p[1] + [p[2]]

def p_expr(p):
    """
    expr : atom
         | list
         | quote
    """
    #print('expr', p)
    p[0] = p[1]

def p_atom(p):
    """
    atom : nil
         | symbol
         | integer
         | string
         | array
    """
    #print('atom', p)
    p[0] = p[1]

def p_quote(p):
    """
    quote : "'" expr
    """
    #print('quote', p)
    p[0] = Cons(Symbol('quote'), Cons(p[2], nil))


def p_list(p):
    """
    list : '(' seq ')'
         | '(' seq '.' expr ')'
    """
    #print('list', p)
    p[0] = reduce(lambda x, y: Cons(y, x), reversed(p[2]), nil if len(p) == 4 else p[4])  ## bonne solution ?


def p_nil(p):
    """
    nil : NIL
         | '(' ')'
    """
    #print('nil', p)
    p[0] = nil


def p_seq(p):
    """
    seq : expr
        | seq expr
    """
    if len(p) == 2:
        #print('seq', p, [p[1]]); input("continuer ?")
        p[0] = [p[1]]
    else:
        #print('seq', p, p[1] + [p[2]]); input("continuer ?")
        p[0] = p[1] + [p[2]]

def p_empty(p):
    'empty :'
    #print('empty')
    pass

def p_array(p):
    """
    array : '#' '(' ')'
          | '#' '(' seq ')'
    """
    p[0] = Array(nil if len(p) == 3 else p[3])

def p_symbol(p):
    'symbol : SYMBOL'
    #print('atom', p)
    p[0] = Symbol(p[1])

def p_string(p):
    'string : STRING'
    #print('sring', p)
    p[0] = String(p[1])

def p_number(p):
    'integer : INT'
    #print('number', p)
    p[0] = Integer(p[1])
 

# Error rule for syntax errors
def p_error(p):
    raise LispParseError('\tline ' + repr(p) + '\nSyntax error in input !')


# Build the parser
lisp_parser = yacc.yacc()

