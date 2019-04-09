from math import factorial
from graph_adj import *
from basicpermutationgroup import *


def is_unbalanced(A, B):
    return not sorted(A.colors) == sorted(B.colors)


def is_bijective(A, B):
    a = sorted(A.colors)
    b = sorted(B.colors)
    return a == b and len(set(a)) == A.size and len(set(b)) == B.size


def colour_twins(A: "Graph", B: "Graph"):
    twins_a = A.true_twins() + A.false_twins()
    twins_b = B.true_twins() + B.false_twins()
    # print("True twins a:", true_twins_a)
    # print("False twins a:", false_twins_a)
    # print("True twins b:", true_twins_b)
    # print("False twins b:", false_twins_b)
    for twina in twins_a:
        for twinb in twins_b:
            if [d.color for d in twina[0].neighbors
                ] == [d.color for d in twinb[0].neighbors]:
                twina[0].change_color(A.max_color + 1)
                twinb[0].change_color(B.max_color + 1)
                break
            else:
                continue
        continue


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
    if X.size == 1 and Y.size == 1:
        return True
    if X.size != Y.size:
        return False

    _, _, dx = X.graph_search(centerx)
    _, _, dy = Y.graph_search(centery)
    # dictionary with key = level, value = list of vertices corresponding to that level
    level_vertsX = {}
    level_vertsY = {}
    labelx = {}  # canonical representation of a vertex
    labely = {}
    canonx = {}  # canonical representation of level
    canony = {}

    max_levelX = max(dx.values())  # depth of the tree
    max_levelY = max(dy.values())

    for lx, ly in zip(range(0, max_levelX + 1), range(0, max_levelY + 1)):
        # gather all vertices at particular level lx
        z1 = [v for v in dx.keys() if dx[v] == lx]
        z2 = [v for v in dy.keys() if dy[v] == ly]
        level_vertsX[lx] = z1
        level_vertsY[ly] = z2

    # if the trees have different depths then obviously no isomorphism
    if max_levelX != max_levelY:
        return False

    # leaves: all vertices with degree 1 (no children themselves)
    leavesx = [v.i for v in X.vertices if v.degree == 1]
    leavesy = [v.i for v in Y.vertices if v.degree == 1]
    if len(leavesy) != len(leavesx):
        return False
    for vx, vy in zip(leavesx, leavesy):  # all leaves get label 1
        labelx[vx] = 0
        labely[vy] = 0

    for lx, ly in zip(range(max_levelX, -1, -1),
                      range(max_levelY, -1, -1)):
        # if the cardinality of the levels differ -> no isomorphism
        if len(level_vertsX[lx]) != len(level_vertsY[ly]):
            return False
        for vx, vy in zip(level_vertsX[lx], level_vertsY[ly]):
            # iterate over the children of particular vertex vx/vy in layer lx/ly
            vx = Vertex(X, vx)
            vy = Vertex(Y, vy)
            if vx.degree > 1:
                # if vx.degree == 1 -> leave -> already a label -> skip labeling
                # list of the labels of the children
                labelx[vx.i] = int("".join(
                    map(
                        str,
                        sorted([
                            labelx[c] for c in level_vertsX[lx + 1]
                            if vx.is_adjacent(Vertex(X, c))
                        ]))))
            if vy.degree > 1:
                # list of the labels of the children
                labely[vy.i] = int("".join(
                    map(
                        str,
                        sorted([
                            labely[c] for c in level_vertsY[ly + 1]
                            if vy.is_adjacent(Vertex(Y, c))
                        ]))))

        # canonical representation for the layer
        canonx[lx] = [labelx[v] for v in level_vertsX[lx]]
        # canonical representation for the layer
        canony[ly] = [labely[v] for v in level_vertsY[ly]]

        if sorted(canonx[lx]) == sorted(canony[ly]):
            # Convert list
            mapping = dict()

            old_labelx = labelx.copy()
            old_labely = labely.copy()
            next_label = 1
            for vx, vy in zip(level_vertsX[lx], level_vertsY[ly]):
                if old_labelx[vx] not in mapping:
                    mapping[old_labelx[vx]] = next_label
                    next_label += 1

                if old_labely[vy] not in mapping:
                    mapping[old_labely[vy]] = next_label
                    next_label += 1

                labelx[vx] = mapping[old_labelx[vx]]
                labely[vy] = mapping[old_labely[vy]]
        else:
            return False

    if labelx[centerx.i] == labely[centery.i]:
        return True
    else:
        return False
