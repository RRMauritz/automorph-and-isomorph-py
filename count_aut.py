from sys import argv
from math import factorial
import itertools as it
from permv2 import *
from collections import deque, Counter
from graph_adj import *
from fast_col_ref import color_refinement
from graph_lib import is_unbalanced, is_bijective, cycles_from_mapping, membership_test, cardinality_generating_set
from is_iso import tree_isomorphism


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
            # if root.is_trivial():
            return False
        else:
            # Find the mappings induced by color refinement
            for v in A.vertices:
                u = next((x for x in B.vertices if x.color == v.color))
                if (u.i, v.i) not in mapping and (v.i, u.i) not in mapping:
                    mapping.append((v.i, u.i))

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
        new_mapping.append((v.i, u.i))
        trivial = False
        if v.i == u.i and is_trivial:
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
<<<<<<< HEAD
    return cardinality_generating_set(gen_set)
=======
    return gen_set
>>>>>>> Rutger


def tree_count_aut(G: "Graph", root: "Vertex"):
    if G.size == 1 or G.size == 2:
        return 1

    _, _, lvl = G.graph_search(root)

    # Get subroots
    subroots = [r for r in G.vertices if lvl[r.i] == lvl[root.i] + 1]
    # Get subtrees
    subtrees = [G.induced_subtree(r, root) for r in subroots]
    classes = {s: 1 for s in subtrees}

    passed = set()
    for tree1, tree2 in it.product(subtrees, subtrees):
        if tree1 == tree2 or tree1 in passed or tree2 in passed:
            continue

        if tree_isomorphism(tree1, [tree1.vertices[0]], tree2,
                            [tree2.vertices[0]]):
            if classes[tree1] != 1:
                passed.add(tree2)
                classes[tree1] += 1
            elif classes[tree2] != 1:
                passed.add(tree1)
                classes[tree2] += 1
            else:
                passed.add(tree2)
                classes[tree1] += 1

    prod = 1
    for stree, v in classes.items():
        if stree in passed:
            continue
        rec_tree_count = tree_count_aut(stree, stree.vertices[0])
        prod *= factorial(v) * pow(rec_tree_count, v)
    return prod


def count_aut(G: "Graph") -> bool:
    if G.is_tree():
        return tree_count_aut(G, G.find_center()[0])
    else:
        return count_automorphs(G)


if __name__ == "__main__":
    from graph_io_adj import load_graph_list
    with open(argv[1]) as f:
        G = load_graph_list(f)[int(argv[2])]

    print(count_aut(G))
