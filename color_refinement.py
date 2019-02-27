from graph import *
from collections import Counter


def color_refinement(G: "Graph"):
    # Initialize colors for every vertex
    colors = {v: v.degree for v in G.vertices}
    last_color = max([c for k, c in colors])
    colors_old = {}

    while not colors == colors_old:
        # Store last iteration
        colors_old = colors.copy()

        # Create coloring of vertices
        # Iterate over all vertices
        for u in G.vertices:
            for v in G.vertices:
                # Skip if vertices are the same
                if u is v:
                    continue

                # Check if colors were the same previously
                if colors_old[u] == colors_old.get[v]:
                    u_color_neighborhood = Counter(
                        [colors_old[k] for k in u.neighbors])
                    v_color_neighborhood = Counter(
                        [colors_old[k] for k in v.neighbors])

                    if u_color_neighborhood == v_color_neighborhood:
                        last_color += 1
                        colors[u], colors[v] = last_color
                    else:
                        last_color += 1
                        colors[u] = last_color
                        last_color += 1
                        colors[v] = last_color

    return colors
