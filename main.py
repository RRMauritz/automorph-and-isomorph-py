#!/bin/python
from is_iso import is_iso
from count_aut import count_aut
from graph_io_adj import load_graph_list
from graph_lib import cycles_from_mapping
import itertools as it
import sys
import argparse


def print_help():
    print(
        "Usage: python main.py graphs/graph.grl [--iso | --aut] {--graph 0 1 3 ...}"
    )
    print("[--iso]   Evaluate equivalence classes.")
    print("[--aut]   Count automorphisms of graphs.")
    print("{--graph} Indicate the indices of the graphs to be parsed.")
    print("          If not specified every graph is parsed.")
    print("{-af}     Calculate automorphs first and the compare the")
    print("          ones with equal amount for isomorphism.")
    print("{-v}      Enable verbose mode for more logs.")


def equivalence_classes(args, graph_list=None):
    with open(args.path) as f:
        G = load_graph_list(f)

    if graph_list == None:
        graph_list = args.graph

    if graph_list:
        G = [g for i, g in enumerate(G) if i in graph_list]

    if graph_list:
        zipper = sorted(graph_list)
    else:
        zipper = range(len(G))

    if args.verbose:
        print("Calculating equivalence classes for graphs", list(zipper))

    pairs = list()
    passed = set()
    non_iso = {i: set() for i in zipper}

    for (i, a), (j, b) in it.combinations(zip(zipper, G), 2):
        if i == j or i in passed or j in passed:
            continue

        if args.verbose:
            print("Checking for isomorphism between {} and {}".format(i, j))
        if any(j in sl for sl in pairs):
            pairs_with_j = [p for p in pairs if j in p]
            other = set()
            for p in pairs_with_j:
                if p[0] != j:
                    other.add(p[0])
                else:
                    other.add(p[1])

            not_iso = False
            for o in other:
                if o in non_iso[i]:
                    if args.verbose:
                        print(
                            "{} is isomorphic with {} which is non isomorphic with {} so skipping"
                            .format(j, o, i))
                    not_iso = True
                    break
            if not_iso:
                continue
        if is_iso(a, b):
            if args.verbose:
                print("{} and {} are isomorphic".format(i, j))
            pairs.append([i, j])
            passed.add(i)

            for x in non_iso[j]:
                non_iso[i].add(x)
            non_iso[j] = non_iso[i]
        else:
            non_iso[i].add(j)
            non_iso[j].add(i)

    cycles = cycles_from_mapping(pairs)
    single = set()
    for i in zipper:
        found = True
        for c in cycles:
            if i in c:
                found = False
                break
        if found:
            single.add(i)

    eq_classes = list()
    for c in cycles:
        eq_classes.append(sorted(c))
    for i in single:
        eq_classes.append([i])
    return eq_classes


def automorphs(args, graph_list=None):
    if graph_list == None:
        graph_list = args.graph
    with open(args.path) as f:
        G = load_graph_list(f)
    if graph_list:
        G = [g for i, g in enumerate(G) if i in graph_list]

    if graph_list:
        zipper = sorted(graph_list)
    else:
        zipper = range(len(G))

    automorphs = dict()
    for i, g in zip(zipper, G):
        if args.verbose:
            print("Calculating automorph for graph [{}]".format(i))
        automorphs[i] = count_aut(g)

    return automorphs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    iso = parser.add_argument_group()
    aut = parser.add_argument_group()

    iso.add_argument("-i",
                     "--iso",
                     action="store_true",
                     help="Determine isomorphism equivalence classes")
    iso.add_argument("-g", "--graph", nargs="*", type=int)
    aut.add_argument("-a",
                     "--aut",
                     action="store_true",
                     help="Calculate number of automorphisms")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("path")
    parser.add_argument("-af", "--autfirst", action="store_true")
    try:
        args = parser.parse_args()
    except:
        print_help()
        parser.exit()

    if args.iso and args.aut or not args.iso and not args.aut:
        # Old version, iso first then aut
        if not args.autfirst:
            eq_classes = equivalence_classes(args)
            automorphs = automorphs(args, [c[0] for c in eq_classes])
            for c in eq_classes:
                print("{} {}".format(
                    c, [v for k, v in automorphs.items() if k in c][0]))
        # New version, only do iso check on graphs
        # that have the same number of automorphs
        else:
            inv_autom = dict()
            for k, v in automorphs(args).items():
                inv_autom[v] = inv_autom.get(v, list())
                inv_autom[v].append(k)
            for k, v in inv_autom.items():
                eq_classes = equivalence_classes(args, v)
                for c in eq_classes:
                    print("{} {}".format(c, k))

    elif args.aut:
        for k, v in automorphs(args).items():
            print("[{}] {}".format(k, v))
    elif args.iso:
        for c in equivalence_classes(args):
            print(c)
