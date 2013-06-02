#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ply.lex as lex


reserved = {
   'nil' : 'NIL'
}

# List of token names.
tokens = [
    'SYMBOL',
    'INT',
    'STRING'
] + list(reserved.values())

literals = [ ',', '#', "'", '(', ')', '.' ]  # le point est bizarre en lisp



# A string containing ignored characters (spaces and tabs)
t_ignore_SPACE = r'\s+'
t_ignore_COMMENT = r';.*'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n'
    t.lexer.lineno += len(t.value)

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_SYMBOL(t):
    r'[^0-9 ",#()\'.;][^ :;",()\'\n]*'
    t.type = reserved.get(t.value, 'SYMBOL')    # Check for reserved words
    return t

# Error handling rule
def t_error(t):
    raise RuntimeError("Illegal character '%s' at line %d" % (t.value[0], t.lexer.lineno))

# Build the lexer
lisp_lexer = lex.lex()
