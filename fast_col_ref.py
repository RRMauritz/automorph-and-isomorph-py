from graph_adj import *
from collections import deque


def color_refinement(G: "Graph", reset_colors=True):
    # Assign colormap: Color -> [Vertices]
    color_classes = {}
    for v in G.vertices:
        key = v.degree
        #key = 0
        if not reset_colors:
            key = v.color

        if key in color_classes.keys():
            color_classes[key].add(v.i)
        else:
            color_classes[key] = set([v.i])

    # The set of neighbors for every vertice
    neighbors = {v.i: set([t.i for t in v.neighbors]) for v in G.vertices}

    #TODO color_classes going from 0 to n

    #TODO Choice of color_classes for initial queue
    #color_stack = deque([next(iter(color_classes.keys()))])
    color_stack = deque(
        sorted([k for k, _ in color_classes.items()],
               key=lambda c: len(color_classes[c])))

    while color_stack:
        # Choose the color class with the lowest amount of vertices
        color_class = color_stack[0]

        # The set of vertices on which the others are split on
        split_set = color_classes[color_class]
        n = len(split_set)

        # Get all other color classes and check them on number of neighbors
        # in the set of vertices that is being split
        # then define new partitions
        for cc, verts in color_classes.copy().items():
            # The D_n's for this color class cc
            D = [False] * (n + 1)
            for v in verts:
                nb = set(neighbors[v])
                nb = nb.intersection(split_set)
                i = len(nb)
                if not D[i]:
                    D[i] = set()
                D[i].add(v)

            # Clean up empty sets
            D = [d for d in D if d]

            # Split up cc into subpartitions from D
            first_iter = True
            for d in D:
                if first_iter:
                    color_classes[cc] = d
                    first_iter = False
                    continue

                new_color = max(color_classes.keys()) + 1
                color_classes[new_color] = d

                if cc in color_stack:
                    color_stack.append(new_color)
                else:
                    push_c = new_color
                    if len(color_classes[cc]) < len(color_classes[new_color]):
                        push_c = cc

                    for i, c in enumerate(color_stack):
                        if len(color_classes[push_c]) < len(color_classes[c]):
                            color_stack.insert(i, push_c)
                            break

        color_stack.remove(color_class)

    # Map label to vertice for easy color assignment
    verts = {v.i: v for v in G.vertices}
    for c, vs in color_classes.items():
        for v in vs:
            verts[v].change_color(c)
