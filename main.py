from is_iso import is_iso
from count_aut import count_aut
from graph_io_adj import load_graph_list
from graph_lib import cycles_from_mapping
import itertools as it
import sys

if __name__ == "__main__":
    if sys.argv[1] == "-a" or sys.argv[1] == "--aut":
        with open(sys.argv[2]) as f:
            G = load_graph_list(f)

        handle_list = False
        if len(sys.argv) >= 4:
            if sys.argv[3] == "-l" or sys.argv[3] == "--list":
                handle_list = True
            else:
                x = sys.argv[3]
                G = G[int(sys.argv[3])]
        else:
            G = G[0]
            x = 0

        if handle_list:
            for i, g in enumerate(G):
                print("[{}] {}".format(i, count_aut(g)))
        else:
            print("[{}] {}".format(x, count_aut(G)))
    elif sys.argv[1] == "-i" or sys.argv[1] == "--iso":
        with open(sys.argv[2]) as f:
            G = load_graph_list(f)

        handle_two = False
        if len(sys.argv) >= 5:
            G = [G[int(sys.argv[3])], G[int(sys.argv[4])]]
            handle_two = True

        if handle_two:
            if is_iso(G[0], G[1]):
                print("[{}] and [{}] are isomorphic".format(
                    sys.argv[3], sys.argv[4]))
            else:
                print("[{}] and [{}] are not isomorphic".format(
                    sys.argv[3], sys.argv[4]))
        else:
            pairs = list()
            passed = set()

            for (i, a), (j, b) in it.product(enumerate(G), enumerate(G)):
                if i == j or i in passed or j in passed:
                    continue

                if is_iso(a, b):
                    pairs.append([i, j])
                    passed.add(j)

            cycles = cycles_from_mapping(pairs)
            
            for c in cycles:
                print(c)
