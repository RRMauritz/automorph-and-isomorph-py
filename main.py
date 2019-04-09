from is_iso import is_iso
from count_aut import count_aut
from graph_io_adj import load_graph_list
from graph_lib import cycles_from_mapping
import itertools as it
import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    iso = group.add_argument_group()
    aut = group.add_argument_group()

    iso.add_argument("-i", "--iso", action="store_true")
    iso.add_argument("-g", "--graph", nargs="*", type=int)
    aut.add_argument("-a", "--aut", action="store_true")
    parser.add_argument("path")
    args = parser.parse_args()
    print(args)
    if args.aut:
        with open(args.path) as f:
            G = load_graph_list(f)
        if args.graph:
            G = [g for i, g in enumerate(G) if i in args.graph]

        if args.graph:
            zipper = args.graph
        else:
            zipper = range(len(G))
        for i, g in zip(zipper, G):
            print("[{}] {}".format(i, count_aut(g)))
    elif args.iso:
        with open(args.path) as f:
            G = load_graph_list(f)

        if args.graph:
            G = [g for i, g in enumerate(G) if i in args.graph]

        pairs = list()
        passed = set()

        if args.graph:
            zipper = args.graph
        else:
            zipper = range(len(G))
        for (i, a), (j, b) in it.product(zip(zipper, G), zip(zipper, G)):
            if i == j or i in passed or j in passed:
                continue

            if is_iso(a, b):
                pairs.append([i, j])
                passed.add(j)

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

        for c in cycles:
            print(c)

        for i in single:
            print("[{}]".format(i))
