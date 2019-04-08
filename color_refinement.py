from graph import *
from collections import Counter
from graph_io import load_graph, write_dot
from itertools import product
from copy import deepcopy


def color_refinement(G: "Graph", reset_colors=True):
    # Initialize colors for every vertex
    colors = {}
    if reset_colors:
        colors = {v.label: v.degree for v in
                  G.vertices}  # dictionary where key = v.label and its corresponding value is the degree
    else:
        colors = {v.label: v.color for v in G.vertices}
    # Find the highest color value
    # last_color = max([c for k, c in colors.items()])
    # Stores version of color configuration from previous loop iteration
    colors_old = {}
    # Keeps track of colors used for certain neighbourhoods

    for v in G.vertices:
        v.colornum = colors[v.label]

    c_map = {}
    last_color = max([c for _, c in colors.items()])
    while not colors == colors_old:
        # Store last iteration
        colors_old = deepcopy(colors)

        # Create coloring of vertices
        # Iterate over all vertices
        for u, v in product(G.vertices, G.vertices):
            # Check if colors were the same previously
            if colors_old[u.label] == colors_old[v.label]:
                # Get the colors of the neighbourhood
                u_neighbours = Counter(
                    [colors_old[k.label] for k in u.neighbours])
                v_neighbours = Counter(
                    [colors_old[k.label] for k in v.neighbours])

                if u_neighbours == v_neighbours:
                    # If the neighbourhood color is not defined, add it to the dict
                    # And keep it the same
                    if frozenset(u_neighbours.items()) not in c_map.keys():
                        c_map[frozenset(
                            u_neighbours.items())] = colors_old[u.label]
                else:
                    # If the two nodes don't share the same neighbourhood
                    # Make a new color for one of them
                    if frozenset(u_neighbours.items()) not in c_map.keys():
                        last_color += 1
                        c_map[frozenset(u_neighbours.items())] = last_color
                    if frozenset(v_neighbours.items()) not in c_map.keys():
                        last_color += 1
                        c_map[frozenset(v_neighbours.items())] = last_color
                    # Only recolor if the vertices are different
                    if not u.label == v.label:
                        colors[v.label] = c_map[frozenset(
                            v_neighbours.items())]
                        colors[u.label] = c_map[frozenset(
                            u_neighbours.items())]
                        u.colornum = colors[u.label]
                        v.colornum = colors[v.label]

    # Make labels the color number and graph colorful
    for v in G.vertices:
        v.color = colors[v.label]
        v.colornum = v.color
    return colors
