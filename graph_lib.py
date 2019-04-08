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
