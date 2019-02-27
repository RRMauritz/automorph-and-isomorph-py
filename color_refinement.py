from graph import *
from collections import Counter

def color_refinement(graph: "Graph"):
    vertices = graph.vertices

    colors = {v: v.degree for v in vertices}    # initialization
    last_color = max([c for k, c in colors])
    colors_old = {}

    while not colors == colors_old:
        colors_old = colors.copy()  # old color set

        # create coloring of vertices

        for u in vertices:
            for v in vertices:
                if u == v:
                    continue
                if colors_old[u] == colors_old[v]:
                    u_color_neighbourhood = Counter([colors_old[k] for k in u.neighbours])
                    v_color_neighbourhood = Counter([colors_old[k] for k in v.neighbours])
                    if u_color_neighbourhood == v_color_neighbourhood:
                        last_color += 1
                        colors[u], colors[v] = last_color
                    else:
                        last_color += 1
                        colors[u] = last_color
                        last_color += 1
                        colors[v] = last_color
    return colors















