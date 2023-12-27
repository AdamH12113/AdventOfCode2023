import re, sys, copy
from typing_extensions import Self
import networkx as nx
#import matplotlib.pyplot as plt

# Read the input
try:
	day_num = int(re.findall(r'\d+', __file__)[-1])
	filename_base = 'Example' if '--example' in sys.argv else 'Input'
	filename = filename_base + str(day_num) + '.txt'
	with open(filename, 'rt') as f:
		input_text = f.read()[:-1]
except Exception as e:
	print(f"Error reading input: [{e.__class__.__name__}] {e}")
	exit()

# Process the input. Each line describes connections ("wires" between named components. Wires are
# bidirectional. Time for more graphs, I guess.
input_lines = input_text.split('\n')
nodes: set[str] = set()
edges: set[tuple[str, str]] = set()
for line in input_lines:
	c1 = line[:line.index(':')]
	nodes.add(c1)
	for c2 in line.split(' ')[1:]:
		nodes.add(c2)
		if c1 < c2:
			edges.add((c1, c2))
		else:
			edges.add((c2, c1))

# Part 1: Removing three wires will separate the components into two unconnected groups. Find
# the three wires and separate the groups. What is the product of the sizes of the two groups?
# In order for this to work, each component must have a minimum of four connections to other
# components. Unfortunately, despite a fair bit of reading about things like "minimum cuts",
# I am not confident in my ability to programmatically identify the three wires, so I'm going
# to use a graph library to do it. :-(
G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
min_cut_edges = nx.minimum_edge_cut(G)
print(min_cut_edges)
for edge in min_cut_edges:
	G.remove_edge(edge[0], edge[1])
size_product = 1
for cc in nx.connected_components(G):
	size_product *= len(cc)
print(f"Part 1: The product of the disconnect group sizes is: {size_product}")
