from graph import *
from graph_io import load_graph, write_dot
from collections import Counter


def color_refinement(graph: "Graph"):
    vert = graph.vertices

    colors = {v: v.degree for v in vert}    # initialization
    last_color = max([c for k, c in colors.items()])
    colors_old = {}

    while not colors == colors_old:
        colors_old = colors.copy()  # old color set

        # create coloring of vertices

        for u in vert:
            for v in vert:
                if u == v:
                    continue
                if colors_old[u] == colors_old[v]:
                    u_color_neighbourhood = Counter([colors_old[k] for k in u.neighbours])
                    v_color_neighbourhood = Counter([colors_old[k] for k in v.neighbours])
                    if u_color_neighbourhood == v_color_neighbourhood:
                        last_color += 1
                        colors[u] = last_color
                        colors[v] = last_color
                    else:
                        last_color += 1
                        colors[u] = last_color
                        last_color += 1
                        colors[v] = last_color
    for v in vert:
        v.label = colors[v]
        v.colornum = v.label
    return graph


with open('examplegraph2.gr') as f:
    G = load_graph(f)

K = color_refinement(G)

with open('coloured.dot', 'w') as f:
    write_dot(K,f)


















