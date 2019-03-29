from permv2 import *
from collections import deque, Counter
from graph import *
from fast_col_ref import color_refinement
from isomorph import membership_test, cardinality_generating_set
import sys
from graph_io import *
from random import randint


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


def is_unbalanced(A, B):
    a = Counter([v.color for v in A.vertices])
    b = Counter([v.color for v in B.vertices])
    return not a == b


def is_bijective(A, B):
    a = Counter([v.color for v in A.vertices])
    b = Counter([v.color for v in B.vertices])
    return a == b and len(a) == len(A.vertices) and len(b) == len(B.vertices)


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
            # Create a list of untrivial mappings which are the cycles
            cycles = [[c[0], c[1]] for c in root.mapping if c[0] != c[1]]
            # Create the permutation
            perm = permutation(len(A.vertices), cycles)

            # Test if the permutation is already a member
            if len(gen_set) == 0 or not membership_test(gen_set, perm):
            # TODO replace random choice with membership_test when it works
            #if randint(0, 1) < 0.5:
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

    for u in [k for k in B.vertices if k.color == ref_c_class]:
        old_u_color = u.color
        u.color = v.color

        new_mapping = root.mapping.copy()
        new_mapping.append((v.label, u.label))
        new_node = tree_node(root, mapping=new_mapping)
        if create_level(new_node, A, B, gen_set) and not root.is_trivial():
            return True

        # Add child
        root.add_child(new_node)

        u.color = old_u_color

    return False


def count_isomorphs(graph: "Graph"):
    # Create root of tree
    root = tree_node(None)
    gen_set = list()
    create_level(root, graph, graph, gen_set)
    return gen_set


if __name__ == "__main__":
    print("Counting automorphs")
    with open(sys.argv[1]) as f:
        G = load_graph(f, read_list=True)
    gen_set = count_isomorphs(G[0][int(sys.argv[2])])
    print("Gen_set: ", gen_set)
    print("Automorphs: ", cardinality_generating_set(gen_set))
