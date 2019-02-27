from graph import *
from collections import Counter
from graph_io import load_graph, write_dot
from itertools import product


def color_refinement(G: "Graph"):
    # Initialize colors for every vertex
    #colors = {v: 0 for v in G.vertices}
    colors = {v: v.degree for v in G.vertices}
    last_color = max([c for k, c in colors.items()])
    colors_old = {}
    c_map = {}

    while not colors == colors_old:
        # Store last iteration
        colors_old = colors.copy()

        # Create coloring of vertices
        # Iterate over all vertices
        for u, v in product(G.vertices, G.vertices):
            # Check if colors were the same previously
            if colors_old[u] == colors_old[v]:
                # Get the colors of the neighbourhood
                u_neighbours = Counter([colors_old[k] for k in u.neighbours])
                v_neighbours = Counter([colors_old[k] for k in v.neighbours])

                if u_neighbours == v_neighbours:
                    # If the neighbourhood color is not defined, add it to the dict
                    if frozenset(u_neighbours.items()) not in c_map.keys():
                        c_map[frozenset(u_neighbours.items())] = colors_old[u]

                    # Assign colors
                    colors[u] = c_map[frozenset(u_neighbours.items())]
                    colors[v] = c_map[frozenset(v_neighbours.items())]
                else:
                    # If the two nodes don't share the same neighbourhood
                    # Make a new color for one of them
                    last_color += 1
                    c_map[frozenset(v_neighbours.items())] = last_color

    # Make labels the color number and make graph colorful
    for v in G.vertices:
        v.label = colors[v]
        v.colornum = v.label

    return G


# Load graph
with open('./colorref_smallexample_4_16.grl') as f:
    G = load_graph(f)

# Apply function
K = color_refinement(G)

# Write the dot file
with open('colored.dot', 'w') as f:
    write_dot(K, f)
