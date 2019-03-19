from graph import *
from graph_io import *
from collections import Counter
from fast_col_ref import color_refinement
import sys


def is_unbalanced(A, B):
    a = Counter([v.color for v in A.vertices])
    b = Counter([v.color for v in B.vertices])
    return not a == b


def is_bijective(A, B):
    a = Counter([v.color for v in A.vertices])
    b = Counter([v.color for v in B.vertices])
    return a == b and len(a) == len(A.vertices) and len(b) == len(B.vertices)


def count_isomorphisms(X: "Graph", Y: "Graph", count_isomorphs=True):
    # If the number of vertices or edges is different they cannot be
    # isomophic
    if not len(X.vertices) == len(Y.vertices) or not len(X.edges) == len(
            Y.edges):
        return 0

    # Create disjoint union
    U = X + Y
    # Apply color refinement
    color_refinement(U, reset_colors=False)
    # Split the union up again
    A, B = U.split_disjoint()

    # Check for unbalancy and bijectivity for early recursion exit
    if is_unbalanced(A, B):
        return 0
    elif is_bijective(A, B):
        if not count_isomorphs:
            print("Graphs are isomorphic")
            sys.exit(0)
        return 1

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
    #ref_c_class = max(color_classes, key=lambda c: (c["n"], c["degree"]))

    # Select first color
    #ref_c_class = color_classes[0]

    # Select color by degree
    #ref_c_class = min(color_classes, key=lambda c: c["degree"])

    # All vertices in A of that color
    ref_c = ref_c_class["color"]
    color_vertices = [v for v in A.vertices if v.color == ref_c]

    # Choose a vertice
    v = color_vertices[0]

    # Create a new color for it
    v.color = A.max_color + 1
    v.colornum = v.color

    num = 0
    for u in [k for k in B.vertices if k.color == ref_c]:
        # Save old color
        old_u_color = u.color
        # Make the vertices the same color
        u.color = v.color
        u.colornum = v.colornum
        # Recursion step
        num += count_isomorphisms(A, B, count_isomorphs=count_isomorphs)
        # Change color back so another vertex can get colored
        u.color = old_u_color
        u.colornum = old_u_color
    return num


if __name__ == "__main__":
    if len(sys.argv) > 3:
        with open(sys.argv[1]) as f:
            graph_list = load_graph(f, read_list=True)

        A = graph_list[0][int(sys.argv[2])]
        B = graph_list[0][int(sys.argv[3])]
        c_iso = True
        if len(sys.argv) > 4:
            print("Stopping after one automorph is found")
            c_iso = False

        print("Number of isomorphs: ",
              count_isomorphisms(A, B, count_isomorphs=c_iso))
    else:
        print("Need 3 arguments: %filename% %graph#1% %graph#2%")
        print("The graph numbers refer to the indexes in the list of graphs")
        print("Example: 'python isomorph.py graphs/torus24.grl 0 3'")
        print("Add an additional arbitrary argument to stop the process once")
        print("a single automorph has been found")
