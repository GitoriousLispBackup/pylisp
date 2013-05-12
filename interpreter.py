#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from lisp_interpreter import lisp_interpreter
from intermediate_repr import *

#~ try:
    #~ from lisp_graph import plot_graph as plot
#~ except:
from pprint import pprint as plot

#~ import json

for e in lisp_interpreter():
    print(e)
    G = GraphExpr.from_lsp_obj(e)
    #~ dmp =json.dumps(G, default=lambda obj: obj.__dict__, indent=2, separators=(',', ': '))
    #~ tst = json.loads(dmp)
    #~ G = GraphExpr(**tst)
    plot((G.root, G.graph))
    print(G.to_lsp_obj())
