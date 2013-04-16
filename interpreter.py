#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from lisp_interpreter import lisp_interpreter
from internal_repr import *

#~ try:
    #~ from lisp_graph import plot_graph as plot
#~ except:
from pprint import pprint as plot


for e in lisp_interpreter():
    print(e)
    G = GraphExpr.from_lsp_obj(e)
    r, g = G.root, G.graph
    plot((r, g))
    print(G.to_lsp_obj())
