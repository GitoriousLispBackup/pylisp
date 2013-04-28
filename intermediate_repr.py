#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from operator import itemgetter

from lisp_lexer import lisp_lexer
from lisp_parser import lisp_parser
from lisp import Cons, Lambda, consp, atom



# from pprint import pprint

tag = itemgetter(0)
value = itemgetter(1)
children = itemgetter(2)


class GraphExpr:
    def __init__(self, root, graph):
        self.root = root
        self.graph = graph
    
    def to_lsp_obj(self):
        visited = {}
        def rec_build(uid):
            if uid in visited:
                return visited[uid]
            internal = self.graph[uid]
            if tag(internal) == '#cons':
                id_car, id_cdr = children(internal)
                obj = Cons(rec_build(id_car), rec_build(id_cdr))
            elif tag(internal) == '#lambda':
                s = value(internal)
                s = '(' + s[s.index(':') + 1:-1] + ')'
                obj = lisp_parser.parse(s, lexer=lisp_lexer)[0].eval()
            elif tag(internal) == '#atom':
                obj = lisp_parser.parse(value(internal), lexer=lisp_lexer)[0] # bof
            else:
                raise RuntimeError('Unkown value in tree')
            visited[uid] = obj
            return obj
        return rec_build(self.root)

    @staticmethod
    def from_lsp_obj(obj):
        visited = {}
        def rec_build(obj):
            uid = str(id(obj))
            if uid not in visited:
                if consp(obj):
                    visited[uid] = '#cons', None, [str(id(obj.car)), str(id(obj.cdr))]
                    if str(id(obj.car)) not in visited:
                        rec_build(obj.car)
                    if str(id(obj.cdr)) not in visited:
                        rec_build(obj.cdr)
                elif atom(obj):
                    visited[uid] = '#atom', repr(obj), []
                elif isinstance(obj, Lambda):
                    visited[uid] = '#lambda', repr(obj)[1:], []
                else:
                    raise RuntimeError('Unkown value in expr')
            # print(uid) ; pprint(visited); input('continuer ?')
            return uid
        return GraphExpr(rec_build(obj), visited)
