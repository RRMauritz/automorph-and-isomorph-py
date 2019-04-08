from math import factorial
from graph import *
from graph_io import *
from collections import Counter
from fast_col_ref import color_refinement
import sys
from basicpermutationgroup import *
from itertools import product


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
    twins_b = true_twins_b + false_twins_b
    for twina in twins_a:
        for twinb in twins_b:
            # if the coloured neighbourhoods are the same:
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
        # print(res)
        return 2 ** len(res)


def membership_test(H: "list", f: "permutation"):
    alpha = FindNonTrivialOrbit(H)
    print("alpha:", alpha)
    if alpha is None:
        return False
    if f.istrivial():
        return True
    orbit, transversal = Orbit(H, alpha, True)
    beta = f.__getitem__(alpha)
    print("beta:", beta)
    u = [v for v in transversal if v.__getitem__(alpha) == beta]
    if not u:
        return False
    else:
        u = u[0]
        return membership_test(Stabilizer(H, alpha), -u * f)


def cardinality_generating_set(H: "list"):
    """"
    Given a generating set for the Aut(G) group, this method returns the cardinality of this generating set
    that is, the number of automorphisms there actually are in the graph
    :param H: the generating set
    """

    alpha = FindNonTrivialOrbit(H)
    print("Alpha:", alpha)
    if alpha is not None:
        length_orbit = Orbit(H, alpha, False).__len__()
        stab = Stabilizer(H, alpha)
        return length_orbit * cardinality_generating_set(stab)
    else:
        return 1


def canonical_representation(G: "Graph", root: "Vertex"):
    """"
    Returns the canonical representation of a graph, that is, for each of its vertices
    """
    _, _, dist = G.graph_search(root)
    level_verts = {}
    label = {}
    max_level = max(dist.values())
    for level in range(0, max_level + 1):
        z1 = [v for v in dist.keys() if dist[v] == level]
        level_verts[level] = z1

    leaves = [v for v in G.vertices if v.degree == 1]
    for v in leaves:
        label[v] = 1
    seperator = 3
    for level in range(max_level - 1, -1, -1):
        for v in level_verts[level]:
            if v.degree > 1:
                children = [label[c] for c in level_verts[level + 1] if
                            v.is_adjacent(c)]
                label[v] = str(seperator) + '2'.join(map(str, children)) + str(seperator)
        seperator += 1

    return label


def AHU(X: "Graph", centerx: "Vertex", Y: "Graph", centery: "Vertex"):
    """"
    Checks if two trees are isomorphic based on the AHU - method.
    :returns boolean and canonical representation of the tree
    """
    print("AHU X:", X)
    _, _, dx = X.graph_search(centerx)  # used for determining the levels
    _, _, dy = Y.graph_search(centery)
    level_vertsX = {}  # dictionary with key = level, value = list of vertices corresponding to that level
    level_vertsY = {}
    labelx = {}  # canonical representation of a vertex
    labely = {}
    canonx = {}  # canonical representation of level
    canony = {}

    max_levelX = max(dx.values())  # depth of the tree
    max_levelY = max(dy.values())

    for lx, ly in zip(range(0, max_levelX + 1), range(0, max_levelY + 1)):
        z1 = [v for v in dx.keys() if dx[v] == lx]  # gather all vertices at particular level lx
        z2 = [v for v in dy.keys() if dy[v] == ly]
        level_vertsX[lx] = z1
        level_vertsY[ly] = z2

    if max_levelX != max_levelY:  # if the trees have different depths then obviously no isomorphism
        return False

    leavesx = [v for v in X.vertices if v.degree == 1]  # leaves: all vertices with degree one (no children themselves)
    leavesy = [v for v in Y.vertices if v.degree == 1]
    if len(leavesy) != len(leavesx):
        return False
    for vx, vy in zip(leavesx, leavesy):  # all leaves get label 1
        labelx[vx] = 1
        labely[vy] = 1

    for lx, ly in zip(range(max_levelX - 1, -1, -1), range(max_levelY - 1, -1, -1)):
        for vx, vy in zip(level_vertsX[lx], level_vertsY[ly]):
            # iterate over the children of particular vertex vx/vy in layer lx/ly
            if vx.degree > 1:  # if vx.degree == 1 -> leave -> already a label -> skip labeling
                labelx[vx] = [labelx[c] for c in level_vertsX[lx + 1] if
                              vx.is_adjacent(c)]  # list of the labels of the children
            if vy.degree > 1:
                labely[vy] = [labely[c] for c in level_vertsY[ly + 1] if
                              vy.is_adjacent(c)]  # list of the labels of the children

        canonx[lx] = [labelx[v] for v in level_vertsX[lx]]  # canonical representation for the layer
        canony[ly] = [labely[v] for v in level_vertsY[ly]]  # canonical representation for the layer
        print("Level:", lx)
        print(" X:", canonx[lx])
        print(" Y:", canony[ly])
        i = 0
        for x, y in zip(canonx[lx], canony[ly]):
            if isinstance(x, list):
                x.sort()  # sort the label of a vertex if it is a list, we do this since we can't otherwise sort the canonical representation of the level (ints & lists)
                canonx[lx][i] = int(''.join(map(str, x)))  # convert list to int
            if isinstance(y, list):
                y.sort()
                canony[ly][i] = int(''.join(map(str, y)))
            i += 1

        if sorted(canonx[lx]) == sorted(canony[ly]):
            for v3, v4 in zip(level_vertsX[lx], level_vertsY[ly]):
                if isinstance(labelx[v3], list):
                    labelx[v3] = int(''.join(map(str, labelx[v3])))
                if isinstance(labely[v4], list):
                    labely[v4] = int(''.join(map(str, labely[v4])))

        else:
            return False

    if labelx[centerx] == labely[centery]:
        return True
    else:
        return False


def tree_isomorphism(X: "Graph", centerx, Y: "Graph", centery):
    print("X:", X)
    print("Y:", Y)
    if len(centerx) == 1 and len(centery) == 1:
        print("Check")
        return AHU(X, centerx[0], Y, centery[0])
    elif len(centerx) == 2 and len(centery) == 2:
        return AHU(X, centerx[0], Y, centery[0]) or AHU(X, centerx[1], Y, centery[0])
    else:
        return False


def tree_count_automorphism(G: "Graph", root: "Vertex"):
    # need to check if subgraphs are isomorphic
    classes = {}
    _, _, level = G.graph_search(root)  # determining the level-structure of the graph
    subroots = [c for c in G.vertices if level[c] == level[root] + 1]  # find the subroots
    passed = subroots
    for sr1, sr2 in product(subroots, subroots):  # construct a class dict with the corresponding multiplicities
        if sr1 != sr2 and (sr1 in passed and sr2 in passed):
            G1 = G.sub_tree(root, sr1)
            G2 = G.sub_tree(root, sr2)
            print("Subtree 1:", G1)
            print("Subtree 2:", G2)
            if tree_isomorphism(G1, [sr1], G2, [sr2]):  # if the subtrees are isomorphic
                print("Check")
                passed.remove(sr2)
                if sr1 in classes:
                    classes[sr1] += 1
                else:
                    classes[sr1] = 2
    skipped = [sr for sr in passed if sr not in classes]
    for sk in skipped:
        classes[sk] = 1

    return classes


def construct_genset(H: "list", f):
    if not membership_test(H, f):
        H.append(f)
    return H


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

    # twin_count = colour_twins(A, B)

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
    # print("Num: ", num, "twin_count: ", twin_count)
    return num  # *twin_count

# if len(sys.argv) > 3:
#     with open(sys.argv[1]) as f:
#         graph_list = load_graph(f, read_list=True)
#
#     A = graph_list[0][int(sys.argv[2])]
#     B = graph_list[0][int(sys.argv[3])]
#     c_iso = True
#     if len(sys.argv) > 4:
#         print("Stopping after one automorph is found")
#         c_iso = False
#
#     print("Number of isomorphs: ",
#           count_isomorphisms(A, B, count_isomorphs=c_iso))
# else:
#     print("Need 3 arguments: %filename% %graph#1% %graph#2%")
#     print("The graph numbers refer to the indexes in the list of graphs")
#     print("Example: 'python isomorph.py graphs/torus24.grl 0 3'")
#     print("Add an additional arbitrary argument to stop the process once")
#     print("a single automorph has been found")
