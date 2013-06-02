#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lisp_lexer import lisp_lexer
from lisp_parser import lisp_parser
from lisp import _Namespace, nil


progs = [
"""
()
""",
"""
(a b c)
""",
"""
"a b"
""",
"""
12
""",
"""
(a b . c)
""",
"""
(a b . (c))
""",
"""
(a b (c) d)
""",
"""
(a b . nil)
""",
"""
(nil)
""",
"""
'a
""",
"""
'1
""",
"""
'(a b)
""",
"""
(+ 1 2)
""",
"""
(/ 5 0)
""",
"""
(defun fibo (n)
  (if (or (= n 0) (= n 1))
    n
    (+ (fibo (- n 1)) (fibo (- n 2))) ) )
(fibo 0)
(fibo 1)
(fibo 5)
(fibo 10)
(fibo)
(fibo 1 2)
""",
"""
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
""",
"""
((lambda (x) ((lambda (y) (cons x y)) 'y)) 'x) ;; ok
((lambda (a) ((lambda (b) (list a b)) (+ 2 a))) 1) ;; ok
(((lambda (a) (lambda (b) (list a b))) 1) 2)  ;; ok
(lambda (x) (+ 1 x))
""",
"""
(setq lst '((A (D) B) (E (H G) . I) E F))
(rplacd (cdr (car (cdr (car (cdr lst))))) (car (cdr lst)))
lst
""",
"""
(setq lst '(((G E (F) A I B D)) (E . H)))
(rplacd (cdr lst) (cdr (cdr (car (car lst)))))
lst
""",
"""
(setq lst '(E ((A B F D) . D) (H G) (I)))
(rplacd (cdr (cdr (cdr lst))) (cdr lst))
lst
""",
"""
(setq lst '(((F) E ((E) H I . G) (B . A) D)))
(rplacd (car (car (cdr (cdr (car lst))))) (cdr (cdr (car lst))))
lst
""",
"""
(setq lst '(I ((A) F H B . D) (D (G)) E))
(rplacd (car (car (cdr lst))) (cdr (cdr (cdr (car (cdr lst))))))
lst
"""
]

# (defmacro pop (a) (list 'prog1 (list 'car 'a) (list 'setq 'a (list 'cdr 'a))))



for i, prgm in enumerate(progs):
    _Namespace.clear()
    _Namespace['nil'] = nil

    print('TEST N. {}'.format(i))
    ret = lisp_parser.parse(prgm, lexer=lisp_lexer)
    for e in ret:
        try:
            print('> {}'.format(e))
            print(e.eval())
        except Exception as err:
            print('Error: ' + repr(err))
            in_ = input('continue ?')
            if 'n' in in_: raise err
            continue
