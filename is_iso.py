from graph_adj import *
from graph_io_adj import *
from collections import Counter
from fast_col_ref import color_refinement
import sys
from graph_lib import *


def is_isomorph(X: "Graph", Y: "Graph", firstcall: "bool" = True):
    # If the number of vertices or edges is different they cannot be
    # isomorphic
    if not len(X.vertices) == len(Y.vertices) or not len(X.edges) == len(
            Y.edges):
        return 0

    # Create disjoint union
    U = X + Y
    # Apply color refinement
    color_refinement(U, reset_colors=False)
    # Split the union up again
    A, B = U.split_disjoint()
    if firstcall:
        for v in B.vertices:
            print("Label for v: ", v.i, " for v: ", v)
            print("Neigh: ", B.neighbors[v.i])
            print("Adj. matrix: ", B.adj_matrix)
        colour_twins(A, B)

    # Check for unbalancy and bijectivity for early recursion exit
    if is_unbalanced(A, B):
        return False
    elif is_bijective(A, B):
        return True

    # Get all color classes with size >= 2 in both graphs
    color_classes = [{
        "color": c,
        "n": n,
        "degree": A.degree_of_color(c)
    } for c, n in Counter([v.color for v in A.vertices]).items() if n >= 2]

    ##################################
    #### Selection of color class ####
    ##################################
    # Select color by number of vertices
    ref_c_class = max(color_classes, key=lambda c: c["n"])

    # Select color by number of vertices and degree
    # ref_c_class = max(color_classes, key=lambda c: (c["n"], c["degree"]))

    # Select first color
    # ref_c_class = color_classes[0]

    # Select color by degree
    # ref_c_class = min(color_classes, key=lambda c: c["degree"])

    # All vertices in A of that color
    ref_c = ref_c_class["color"]
    color_vertices = [v for v in A.vertices if v.color == ref_c]

    # Choose a vertice
    v = color_vertices[0]

    # Create a new color for it
    v.change_color(A.max_color + 1)

    num = 0
    for u in [k for k in B.vertices if k.color == ref_c]:
        # Save old color
        old_u_color = u.color
        # Make the vertices the same color
        u.change_color(v.color)
        # Recursion step
        if is_isomorph(A, B, False):
            return True
        # Change color back so another vertex can get colored
        u.change_color(old_u_color)
    return False


def tree_isomorphism(X: "Graph", centerx, Y: "Graph", centery):
    if len(centerx) == 1 and len(centery) == 1:
        return AHU(X, centerx[0], Y, centery[0])
    elif len(centerx) == 2 and len(centery) == 2:
        return AHU(X, centerx[0], Y, centery[0]) or AHU(
            X, centerx[1], Y, centery[0])
    else:
        return False


if __name__ == "__main__":
    if len(sys.argv) > 3:
        with open(sys.argv[1]) as f:
            graph_list = load_graph_list(f)

        A = graph_list[int(sys.argv[2])]
        B = graph_list[int(sys.argv[3])]
        a_tree = A.is_tree()
        b_tree = B.is_tree()
        if a_tree and b_tree:
            print(tree_isomorphism(A, A.find_center(), B, B.find_center()))
        elif a_tree and not b_tree or not a_tree and b_tree:
            print(False)
        else:
            print(is_isomorph(A, B))
