from graph_io import *
from color_refinement import color_refinement
import sys

# Use color_refinement on one graph and print the .dot file
with open(sys.argv[1]) as f:
    G = load_graph(f)

color_refinement(G)

with open('colored.dot', 'w') as f:
    write_dot(G, f)
