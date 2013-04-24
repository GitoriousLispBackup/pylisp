#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lisp_lexer import lisp_lexer
from lisp_parser import lisp_parser


prgm1 = """
()
"""

prgm2 = """
(a b c)
"""

prgm3 = """
"a b"
"""

prgm4 = """
12
"""

prgm5 = """
(a b . c)
"""

prgm6 = """
(a b . (c))
"""

prgm7 = """
(a b (c) d)
"""

prgm8 = """
(a b . nil)
"""

prgm9 = """
(nil)
"""

prgm10 = """
'a
"""

prgm11 = """
'1
"""

prgm12 = """
'(a b)
"""

prgm13 = """
(+ 1 2)
"""

prgm14 = """
(defun fibo (n) (if (or (= n 0) (= n 1)) n (+ (fibo (- n 1)) (fibo (- n 2)))))
(fibo 0)
(fibo 1)
(fibo 5)
(fibo 10)
(fibo)
(fibo 1 2)
"""

prgm15 = """
(defun append (l1 l2)
  (if (not l1)
    l2
    (cons
      (car l1)
      (append (cdr l1) l2) ) ) )
(append '(1 2 3) '(4 5 6))
(append nil '(1 2))
(setq a '(8 9))
(setq b '(a b))
(append b a)
"""

prgm16 = """
((lambda (x) ((lambda (y) (cons x y)) 'y)) 'x) ;; ok
((lambda (a) ((lambda (b) (list a b)) (+ 2 a))) 1) ;; ok
(((lambda (a) (lambda (b) (list a b))) 1) 2)  ;; ok
(lambda (x) (+ 1 x))
"""

# (defmacro pop (a) (list 'prog1 (list 'car 'a) (list 'setq 'a (list 'cdr 'a))))

# prgm1, prgm2, prgm3, prgm4, prgm5, prgm6, prgm7, prgm8, prgm9, prgm10, prgm11, prgm12, 
progs = [
    prgm1, prgm2, prgm3, prgm4, prgm5, prgm6, prgm7, prgm8, prgm9, prgm10, prgm11, prgm12,
    prgm13, prgm14, prgm15, prgm16
]

i = 1
for prgm in progs:
    #print(prgm)
    ret = lisp_parser.parse(prgm, lexer=lisp_lexer)
    for e in ret:
        try:
            print('[{}]>'.format(i), e)
            print(e.eval())
        except Exception as err:
            print(repr(err))
            continue
        i += 1
