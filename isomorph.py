from math import factorial
from graph import *
from graph_io import *
from collections import Counter
from fast_col_ref import color_refinement
import sys
from basicpermutationgroup import *


def is_unbalanced(A, B):
    a = Counter([v.color for v in A.vertices])
    b = Counter([v.color for v in B.vertices])
    return not a == b


def is_bijective(A, B):
    a = Counter([v.color for v in A.vertices])
    b = Counter([v.color for v in B.vertices])
    return a == b and len(a) == len(A.vertices) and len(b) == len(B.vertices)


"""
TODO: Maintain a passed list (?)
TODO: verify on bigger graphs
"""


def colour_twins(A: "Graph", B: "Graph"):
    true_twins_a, false_twins_a = A.twins()
    true_twins_b, false_twins_b = B.twins()
    twins_a = true_twins_a + false_twins_a
    for twina in twins_a:
        for twinb in true_twins_b + false_twins_b:
            if [d.color for d in twina[0].neighbours] == [d.color for d in twinb[0].neighbours]:
                twina[0].color = A.max_color + 1
                twinb[0].color = B.max_color + 1
                break
            else:
                continue
        continue
    res = set()
    print("A is connected: ", A.is_connected())
    if A.is_connected():
        print("Im connected!")
        return factorial(len(twins_a))
    else:
        print("Im not connected!")
        for twin in twins_a:
            res.add(twin[0])
            res.add(twin[1])
        print(res)
        return 2 ** len(res)


def membership_test(H: "list", f: "permutation"):
    if f.istrivial():
        return True
    alpha = FindNonTrivialOrbit(H)
    orbit, transversal = Orbit(H, alpha, True)
    im = f.__getitem__(alpha)
    if im not in orbit:
        return False
    else:
        u = next(v for v in transversal if v.__getitem__(alpha) == im)
        if u.istrivial():
            return False
        else:
            return membership_test(Stabilizer(H, alpha), -u * f)


def cardinality_generating_set(H: "list"):
    """"
    Given a generating set for the Aut(G) group, this method returns the cardinality of this generating set
    that is, the number of automorphisms there actually are in the graph
    :param H: the generating set
    """

    alpha = FindNonTrivialOrbit(H)
    if alpha is not None:
        length_orbit = Orbit(H, alpha, False).__len__()
        stab = Stabilizer(H, alpha)
        return length_orbit * cardinality_generating_set(stab)
    else:
        return 1


def count_isomorphisms(X: "Graph", Y: "Graph", count_isomorphs=True):
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
    # for v in A.vertices:
    #     v.colornum = v.color
    # with open('colored1.dot', 'w') as f:
    #     write_dot(A, f)

    twin_count = colour_twins(A, B)

    # for v in A.vertices:
    #     v.colornum = v.color
    # with open('colored2.dot', 'w') as g:
    #     write_dot(A, g)

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
    print("Num: ", num, "twin_count: ", twin_count)
    return num * twin_count


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
