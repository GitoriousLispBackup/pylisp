#!/usr/bin/env python3


from igraph import *
from collections import OrderedDict, deque


def set_layers(uid, g, layers, level=0):
    layers[uid] = level
    for adj in g[uid][1]:
        if adj not in layers: # check circularity
            set_layers(adj, g, layers, level + 1)
    return layers

def set_graph(g):
    """
    suppress nil object from the grah,
    for having pleasant plotting
    """
    nils = set(uid for uid, internal in g.items() if internal.repr == 'nil')
    return {uid : (internal.repr if internal.typ == '#atom' else internal.typ, list(set(internal.children)-nils)) for uid, internal in g.items() if uid not in nils}

from pprint import pprint

def get_dfs(root, g):
    ret = OrderedDict()
    def rec_traversal(uid):
        ret[uid] = g[uid]
        for next_uid in g[uid][1]:
            if next_uid not in ret:
                rec_traversal(next_uid)
    rec_traversal(root)
    return ret

def get_bfs(root, g):
    ret = OrderedDict()
    fifo = deque([root])
    while fifo:
        uid = fifo.popleft()
        ret[uid] = g[uid]
        for next_uid in g[uid][1]:
            if next_uid not in ret:
                fifo.append(next_uid)
    return ret
  

def plot_graph(lsp_graph):
    root, g = lsp_graph.root, lsp_graph.graph
    
    g = set_graph(g)
    g = get_bfs(root, g)
    pprint((root, g))
    
    layers = set_layers(root, g, {})
    print(layers)

    eqv = dict(zip(g.keys(), range(len(g))))

    G = Graph() # ; print(G)
    G.add_vertices(len(g)) # ; print(G)

    for uid, (_, adjlst) in g.items():
        for e in adjlst:
            G.add_edges((eqv[uid], eqv[e]))
    print(G)

    G.vs["name"] = [obj for obj, _ in g.values()]  # list(map(str, g.keys())) # 
    _layers = [layers[uid] for uid in g.keys()]

    layout = G.layout_sugiyama() # ; print(layout)  _layers

    visual_style = {}
    visual_style["vertex_label"] = [name if name != '#cons' else '' for name in G.vs["name"]]
    visual_style["vertex_color"] = [{'#cons' : 'red'}.get(label, 'blue') for label in G.vs["name"]]
    visual_style["layout"] = layout
    visual_style["bbox"] = 600, 400
    visual_style["margin"] = 30

    plot(G, **visual_style)

