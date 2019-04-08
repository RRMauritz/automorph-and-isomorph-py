from graph_adj import *
from graph_io_adj import *
from collections import Counter
from fast_col_ref import color_refinement
import sys
from graph_lib import *


def is_isomorph(X: "Graph", Y: "Graph"):
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

    #twin_count = colour_twins(A, B)

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
        if is_isomorph(A, B):
            return True
        # Change color back so another vertex can get colored
        u.change_color(old_u_color)
    return False


if __name__ == "__main__":
    if len(sys.argv) > 3:
        with open(sys.argv[1]) as f:
            graph_list = load_graph_list(f)

        A = graph_list[int(sys.argv[2])]
        B = graph_list[int(sys.argv[3])]
        print(is_isomorph(A, B))
