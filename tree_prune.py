from permv2 import *
from collections import deque, Counter
from graph_adj import *
from fast_col_ref import color_refinement
from isomorph import membership_test, cardinality_generating_set
import sys
from graph_io_adj import load_graph_list


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
                if (u.index, v.index) not in root.mapping and (
                        v.index, u.index) not in root.mapping:
                    root.mapping.append((v.index, u.index))

            # Generate cycles and permutation from current mapping
            cycles = cycles_from_mapping(root.mapping)
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

        new_mapping = root.mapping.copy()
        new_mapping.append((v.index, u.index))
        new_node = tree_node(root, mapping=new_mapping)
        if create_level(new_node, A, B, gen_set) and not root.is_trivial():
            return True

        # Add child
        root.add_child(new_node)

        u.change_color(old_u_color)

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


def count_automorphs(graph: "Graph", dot_tree=False):
    # Create root of tree
    root = tree_node(None)
    gen_set = list()
    color_refinement(graph)
    create_level(root, graph, graph, gen_set)
    if dot_tree:
        root.print_tree()
    return gen_set


def is_unbalanced(A, B):
    return not sorted(A.colors) == sorted(B.colors)


def is_bijective(A, B):
    a = sorted(A.colors)
    b = sorted(B.colors)
    return a == b and len(set(a)) == A.size and len(set(b)) == B.size


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
            return "[Root]"
        reduced_m = [m for m in self.mapping if m[0] != m[1]]
        if reduced_m:
            return "{}".format(reduced_m)

        else:
            return "trivial"

    def print_tree(self):
        verts = dict()
        edges = list()

        # Recursive sub function for printing
        def rec_print_tree(node: "tree_node", v: "Dict", e: "List", i=[0]):
            v[node] = i[0]

            for c in node.children:
                i[0] += 1
                rec_print_tree(c, v, e, i)
                e.append([v[node], v[c]])

        rec_print_tree(self, verts, edges)

        G = Graph(directed=False)
        vertices = {i: Vertex(G, label=v.__str__()) for v, i in verts.items()}
        for v in vertices.values():
            G.add_vertex(v)

        for e in edges:
            G.add_edge(Edge(vertices[e[0]], vertices[e[1]]))

        with open('colored.dot', 'w') as f:
            write_dot(G, f)
            print("Wrote tree to 'colored.dot'")


if __name__ == "__main__":
    #print("Counting automorphs")
    with open(sys.argv[1]) as f:
        G = load_graph_list(f)
    #sys.setrecursionlimit(10000)
    gen_set = count_automorphs(
        G[int(sys.argv[2])], dot_tree=(len(sys.argv) > 3))
    #print("Gen_set: ", gen_set)
    print("Automorphs: ", cardinality_generating_set(gen_set))
