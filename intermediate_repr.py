#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from operator import itemgetter

from lisp_lexer import lisp_lexer
from lisp_parser import lisp_parser
from lisp import Cons, consp, atom


# from pprint import pprint

value = itemgetter(0)
children = itemgetter(1)


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
            if value(internal) is None:
                id_car, id_cdr = children(internal)
                obj = Cons(rec_build(id_car), rec_build(id_cdr))
            else:
                obj = lisp_parser.parse(value(internal), lexer=lisp_lexer)[0] # bof
            visited[uid] = obj
            return obj
        return rec_build(self.root)

    @staticmethod
    def from_lsp_obj(obj):
        visited = {}
        def rec_build(obj):
            uid = id(obj)
            if uid not in visited:
                if consp(obj):
                    visited[uid] = None, [id(obj.car), id(obj.cdr)]
                    if id(obj.car) not in visited:
                        rec_build(obj.car)
                    if id(obj.cdr) not in visited:
                        rec_build(obj.cdr)
                else:
                    visited[uid] = repr(obj), []
            # print(uid) ; pprint(visited); input('continuer ?')
            return uid
        return GraphExpr(rec_build(obj), visited)
