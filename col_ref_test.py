import time
from is_iso import *
from graph_io_adj import *
from permv2 import *
from fast_col_ref import color_refinement
from count_aut import *
import sys

with open('graphs/examplegraph4.gr') as f:
    Graphs = read_graph_list(f)
G1 = Graphs[0]
G2 = Graphs[0]
start = time.time()
for i in range(1):
    is_isomorph(G1,G2)
print("Elapsed time:", time.time() - start)
with open('colored.dot', 'w') as f:
    write_dot(G1, f)
