from math import factorial
from graph_adj import *
from collections import Counter
from basicpermutationgroup import *


def is_unbalanced(A, B):
    return not sorted(A.colors) == sorted(B.colors)


def is_bijective(A, B):
    a = sorted(A.colors)
    b = sorted(B.colors)
    return a == b and len(set(a)) == A.size and len(set(b)) == B.size


def colour_twins(A: "Graph", B: "Graph"):
    true_twins_a, false_twins_a = A.twins()
    true_twins_b, false_twins_b = B.twins()
    twins_a = true_twins_a + false_twins_a
    for twina in twins_a:
        for twinb in true_twins_b + false_twins_b:
            if [d.color for d in twina[0].neighbors] == [
                    d.color for d in twinb[0].neighbors
            ]:
                twina[0].change_color(A.max_color + 1)
                twinb[0].change_color(B.max_color + 1)
                break
            else:
                continue
        continue
    res = set()
    if A.is_connected():
        return factorial(len(twins_a))
    else:
        for twin in twins_a:
            res.add(twin[0])
            res.add(twin[1])
        return 2**len(res)


def membership_test(H: "list", f: "permutation"):
    alpha = FindNonTrivialOrbit(H)
    if alpha is None:
        return False
    if f.istrivial():
        return True
    orbit, transversal = Orbit(H, alpha, True)
    beta = f.__getitem__(alpha)
    u = [v for v in transversal if v.__getitem__(alpha) == beta]
    if not u:
        return False
    u = u[0]
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


def construct_genset(H: "list", f):
    if not membership_test(H, f):
        H.append(f)
    return H


def cycles_from_mapping(mapping: "List"):
    cycles = list()
    # This creates a cycle representation of the mapping
    for c in [[c[0], c[1]] for c in mapping if c[0] != c[1]]:
        if not cycles:
            cycles.append(c)
            continue
        append = [x for x in cycles if x[-1] == c[0]]
        prepend = [x for x in cycles if x[0] == c[-1]]

        if append and prepend:
            append = append[0]
            prepend = prepend[0]
            if append == prepend:
                i = cycles.index(append)
                cycles[i] = append[:-1] + c[:-1]
            else:
                i = cycles.index(append)
                cycles[i] = append[:-1] + c[:-1] + prepend
                cycles.remove(prepend)
        elif append:
            append = append[0]
            i = cycles.index(append)
            cycles[i] = append[:-1] + c
            if cycles[i][0] == cycles[i][-1]:
                cycles[i] = cycles[i][:-1]
        elif prepend:
            prepend = prepend[0]
            j = cycles.index(prepend)
            cycles[j] = c[:-1] + prepend
            if cycles[j][0] == cycles[j][-1]:
                cycles[j] = cycles[j][:-1]
        else:
            cycles.append(c)
    return cycles


def AHU(X: "Graph", centerx: "Vertex", Y: "Graph", centery: "Vertex"):
    _, _, dx = X.graph_search(centerx)
    _, _, dy = Y.graph_search(centery)
    level_vertsX = {}
    # dictionary with key = level, value = list of vertices corresponding to that level
    level_vertsY = {}
    labelx = {}  # canonical representation of a vertex
    labely = {}
    canonx = {}  # canonical representation of level
    canony = {}

    max_levelX = max(dx.values())  # depth of the tree
    max_levelY = max(dy.values())

    for lx, ly in zip(range(0, max_levelX + 1), range(0, max_levelY + 1)):
        z1 = [v for v in dx.keys()
              if dx[v] == lx]  # gather all vertices at particular level lx
        z2 = [v for v in dy.keys() if dy[v] == ly]
        level_vertsX[lx] = z1
        level_vertsY[ly] = z2

    if max_levelX != max_levelY:  # if the trees have different depths then obviously no isomorphism
        return False

    leavesx = [
        v.i for v in X.vertices if v.degree == 1
    ]  # leaves: all vertices with degree one (no children themselves)
    leavesy = [v.i for v in Y.vertices if v.degree == 1]
    if len(leavesy) != len(leavesx):
        return False
    for vx, vy in zip(leavesx, leavesy):  # all leaves get label 1
        labelx[vx] = 1
        labely[vy] = 1

    for lx, ly in zip(
            range(max_levelX - 1, -1, -1), range(max_levelY - 1, -1, -1)):
        for vx, vy in zip(level_vertsX[lx], level_vertsY[ly]):
            # iterate over the children of particular vertex vx/vy in layer lx/ly
            vx = Vertex(X, vx)
            vy = Vertex(Y, vy)
            if vx.degree > 1:
                # if vx.degree == 1 -> leave -> already a label -> skip labeling
                labelx[vx.i] = [
                    labelx[c] for c in level_vertsX[lx + 1]
                    if vx.is_adjacent(Vertex(Y, c))
                ]  # list of the labels of the children
            if vy.degree > 1:
                labely[vy.i] = [
                    labely[c] for c in level_vertsY[ly + 1]
                    if vy.is_adjacent(Vertex(Y, c))
                ]  # list of the labels of the children

        canonx[lx] = [labelx[v] for v in level_vertsX[lx]
                      ]  # canonical representation for the layer
        canony[ly] = [labely[v] for v in level_vertsY[ly]
                      ]  # canonical representation for the layer
        #print("Level:", lx)
        #print(" X:", canonx[lx])
        #print(" Y:", canony[ly])
        i = 0
        for x, y in zip(canonx[lx], canony[ly]):
            if isinstance(x, list):
                x.sort(
                )  # sort the label of a vertex if it is a list, we do this since we can't otherwise sort the canonical representation of the level (ints & lists)
                canonx[lx][i] = int(''.join(map(str,
                                                x)))  # convert list to int
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

    if labelx[centerx.i] == labely[centery.i]:
        return True
    else:
        return False
