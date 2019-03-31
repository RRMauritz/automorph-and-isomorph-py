from permv2 import *
from collections import deque, Counter
from graph import *
from fast_col_ref import color_refinement
from isomorph import membership_test, cardinality_generating_set
import sys
from graph_io import load_graph


def create_level(root: "tree_node", A: "Graph", B: "Graph", gen_set: "List"):
    U = A + B
    color_refinement(U, reset_colors=False)
    A, B = U.split_disjoint()

    # Check if tree is unbalanced or bijective
    if is_unbalanced(A, B):
        return False
    elif is_bijective(A, B):
        if root.is_trivial():
            return False
        else:
            # Find the mappings induced by color refinement
            is_mapped = set([x for sl in root.mapping for x in sl])
            for v in A.vertices:
                if v in is_mapped:
                    continue
                u = next((x for x in B.vertices if x.color == v.color))
                if (u.label, v.label) not in root.mapping and (
                        v.label, u.label) not in root.mapping:
                    root.mapping.append((v.label, u.label))

            # Generate cycles and permutation from current mapping
            cycles = cycles_from_mapping(root.mapping)
            perm = permutation(len(A.vertices), cycles)

            # Test if the permutation is already a member
            if len(gen_set) == 0 or not membership_test(gen_set, perm):
                gen_set.append(perm)
                # Return True which means return to the latest trivial node
                return True
            return False

    c_classes = [
        c for c, n in Counter([v.color for v in A.vertices]).items() if n >= 2
    ]

    ref_c_class = max(c_classes)

    col_verts = [v for v in A.vertices if v.color == ref_c_class]

    v = col_verts[0]

    v.color = A.max_color + 1
    v.color_num = v.color

    for u in [k for k in B.vertices if k.color == ref_c_class]:
        old_u_color = u.color
        u.color = v.color
        u.color_num = v.color_num

        new_mapping = root.mapping.copy()
        new_mapping.append((v.label, u.label))
        new_node = tree_node(root, mapping=new_mapping)
        if create_level(new_node, A, B, gen_set) and not root.is_trivial():
            return True

        # Add child
        root.add_child(new_node)

        u.color_num = old_u_color
        u.color = old_u_color

    return False


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


def count_automorphs(graph: "Graph"):
    # Create root of tree
    root = tree_node(None)
    gen_set = list()
    color_refinement(graph)
    create_level(root, graph, graph, gen_set)
    return gen_set


def is_unbalanced(A, B):
    a = Counter([v.color for v in A.vertices])
    b = Counter([v.color for v in B.vertices])
    return not a == b


def is_bijective(A, B):
    a = Counter([v.color for v in A.vertices])
    b = Counter([v.color for v in B.vertices])
    return a == b and len(a) == len(A.vertices) and len(b) == len(B.vertices)


class tree_node:
    def __init__(self, parent: "tree_node", mapping: "List" = list()):
        # Parent node
        self.parent = parent
        if parent:
            self.level = parent.level + 1
        else:
            self.level = 0
        # List of children
        self.children = list()
        self.mapping = mapping
        self.trivial = all(m[0] == m[1] for m in mapping)

    def add_child(self, child: "tree_node"):
        self.children.append(child)

    def is_trivial(self):
        return self.trivial

    def prune_except(self, child: "tree_node"):
        # Drop everything except that one child
        self.children = [c for c in self.children if c == child]

    def prune(self):
        # Drop everything
        self.children = list()

    def __str__(self):
        if self.level == 0:
            return "[Root of Tree]"
        return "{}{}".format("\t" * (self.level - 1), self.mapping)

    def print_tree(self):
        S = deque()
        S.append(self)

        while S:
            v = S.pop()
            print(v)
            for w in v.children:
                S.append(w)


if __name__ == "__main__":
    print("Counting automorphs")
    with open(sys.argv[1]) as f:
        G = load_graph(f, read_list=True)
    gen_set = count_automorphs(G[0][int(sys.argv[2])])
    #print("Gen_set: ", gen_set)
    print("Automorphs: ", cardinality_generating_set(gen_set))
