from permv2 import *
from collections import deque, Counter
from graph_adj import *
from fast_col_ref import color_refinement
from graph_io_adj import load_graph_list
from graph_lib import is_unbalanced, is_bijective, cycles_from_mapping, membership_test, cardinality_generating_set
from sys import setrecursionlimit, argv


def count_aut_rec(A: "Graph",
                  B: "Graph",
                  gen_set: "List",
                  mapping: "List" = list(),
                  is_trivial: "bool" = True):
    U = A + B
    color_refinement(U, reset_colors=False)
    A, B = U.split_disjoint()

    # Check if tree is unbalanced or bijective
    if is_unbalanced(A, B):
        return False
    elif is_bijective(A, B):
        if is_trivial:
            #if root.is_trivial():
            return False
        else:
            # Find the mappings induced by color refinement
            is_mapped = set([x for sl in mapping for x in sl])
            for v in A.vertices:
                if v in is_mapped:
                    continue
                u = next((x for x in B.vertices if x.color == v.color))
                if (u.index,
                        v.index) not in mapping and (v.index,
                                                     u.index) not in mapping:
                    mapping.append((v.index, u.index))

            # Generate cycles and permutation from current mapping
            cycles = cycles_from_mapping(mapping)
            perm = permutation(A.size, cycles)

            # Test if the permutation is already a member
            if len(gen_set) == 0 or not membership_test(gen_set, perm):
                gen_set.append(perm)
                # Return True which means return to the latest trivial node
                return True
            # If true, return
            # If automorph found that is already in the set still return to
            # trivial node instead of continuing
            # Otherwise use false
            return True

    c_classes = [
        c for c, n in Counter([v.color for v in A.vertices]).items() if n >= 2
    ]

    ref_c_class = max(
        c_classes, key=lambda c: len([v for v in A.vertices if v.color == c]))

    col_verts = [v for v in A.vertices if v.color == ref_c_class]

    v = col_verts[0]

    v.change_color(A.max_color + 1)

    for u in [k for k in B.vertices if k.color == ref_c_class]:
        old_u_color = u.color
        u.change_color(v.color)

        new_mapping = mapping.copy()
        new_mapping.append((v.index, u.index))
        trivial = False
        if v.index == u.index and is_trivial:
            trivial = True
        if count_aut_rec(A, B, gen_set, new_mapping,
                         trivial) and not is_trivial:
            return True

        u.change_color(old_u_color)

    return False


def count_automorphs(graph: "Graph"):
    gen_set = list()
    color_refinement(graph)
    count_aut_rec(graph, graph, gen_set)
    return gen_set


if __name__ == "__main__":
    #print("Counting automorphs")
    with open(argv[1]) as f:
        G = load_graph_list(f)
    #sys.setrecursionlimit(10000)
    gen_set = count_automorphs(G[int(argv[2])])
    #print("Gen_set: ", gen_set)
    print("Automorphs: ", cardinality_generating_set(gen_set))
