from grap import *
from collections import Counter
from color_refinement import color_refinement


def count_isomorphisms(X: "Graph", Y: "Graph"):
    # If the number of vertices or edges is different they cannot be
    # isomophic
    if not len(X.vertices) == len(Y.vertices) or not len(X.edges) == len(
            Y.edges):
        return 0

    # Create disjoint union
    U = X + Y
    # Apply color refinement
    color_refinement(U)
    # Split the union up again
    A, B = U.split_disjoint()

    # Check for unbalancy and bijectivity for early recursion exit
    if is_unbalanced(A, B):
        return 0
    elif is_bijective(A, B):
        return 1

    # Get the number of occurences for each color
    colors = Counter([v.label for v in A.vertices])
    # Get a color class where the number of occurences is larger than
    # or equal to 2
    # This color occurs at least twice in both graphs A and B because
    # they are not unbalanced
    color_class = next([c for c, n in colors if n >= 2])
    # Get a vertice that belongs to the color class
    v = next([v for v in A.vertices if v.color == color_class])

    v.color = max_color(A) + 1
    num = 0
    for u in [v for v in B.vertices if v.color == color_class]:
        # Save old color
        old_u_color = u.color
        # Make the vertices the same color
        u.color = v.color
        # Recursion step
        num += count_isomorphisms(A + x, B + u)
        # Change color back so another vertex can get colored
        u.color = old_u_color
    return num

