from graph import *
from graph_io import *
from collections import Counter
from color_refinement import color_refinement
from copy import deepcopy


def is_unbalanced(A, B):
    a = Counter([v.color for v in A.vertices])
    b = Counter([v.color for v in B.vertices])
    return not a == b


def is_bijective(A, B):
    a = Counter([v.color for v in A.vertices])
    b = Counter([v.color for v in B.vertices])
    return a == b and len(a) == len(A.vertices) and len(b) == len(B.vertices)


def count_isomorphisms(X: "Graph", Y: "Graph"):
    # If the number of vertices or edges is different they cannot be
    # isomophic
    if not len(X.vertices) == len(Y.vertices) or not len(X.edges) == len(
            Y.edges):
        return 0

    # Create disjoint union
    U = X + Y
    # Apply color refinement
    color_refinement(U, False)
    # Split the union up again
    A, B = U.split_disjoint()

    # Check for unbalancy and bijectivity for early recursion exit
    if is_unbalanced(A, B):
        print("unbalanced")
        return 0
    elif is_bijective(A, B):
        print("bijective")
        return 1

    # Get the number of occurences for each color
    colors = Counter([v.color for v in A.vertices])
    # Get a color class where the number of occurences is larger than
    # or equal to 2
    # This color occurs at least twice in both graphs A and B because
    # they are not unbalanced
    color_class = [c for c, n in colors.items() if n >= 2][0]
    # Get a vertice that belongs to the color class
    v = [v for v in A.vertices if v.color == color_class][0]

    v.color = A.max_color + 1
    v.colornum = v.color
    with open('colored.dot', 'w') as f:
        write_dot(A + B, f)

    num = 0
    for u in [k for k in B.vertices if k.color == color_class]:
        # Save old color
        old_u_color = u.color
        # Make the vertices the same color
        u.color = v.color
        u.colornum = v.colornum
        # Recursion step
        num += count_isomorphisms(A, B)
        # Change color back so another vertex can get colored
        u.color = old_u_color
        u.colornum = old_u_color
    return num

with open('./colorref_smallexample_4_16.grl') as f:
    graph_list = load_graph(f, read_list=True)

A = graph_list[0][0]
B = graph_list[0][1]
U = A + B
color_refinement(U)
with open('colored.dot', 'w') as f:
    write_dot(U, f)
print(count_isomorphisms(A, B))
