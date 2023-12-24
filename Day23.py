import re, sys, copy
from collections import namedtuple

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

# Process the input. It's a 2-D grid describing a maze. The tiles can be walls ('#'), paths ('.'),
# and one-way downhill slopes ('^', 'v', '<', '>').
input_lines = input_text.split('\n')
grid = input_lines
x_size = len(input_lines[0])
y_size = len(input_lines)

# The starting and ending points are always next to the corners and can be hard-coded.
Coord = namedtuple('Coord', ['x', 'y'])
start = Coord(1, 0)
end = Coord(x_size - 2, y_size - 1)
up = Coord(0, -1)
down = Coord(0, 1)
left = Coord(-1, 0)
right = Coord(1, 0)

def add_coords(c1: Coord, c2: Coord) -> Coord:
	return Coord(c1.x + c2.x, c1.y + c2.y)

# Part 1: What is the length of the longest path from the start to the end? Doing a *longest* path
# search is a bit unusual, but the real limitation is that we can't step on the same tile twice.
# This makes it hard (impossible?) to do a BFS. We'll have to do a DFS instead. The optimal way to
# do this is to build a weighted digraph.
def is_intersection(x: int, y: int) -> bool:
	if x > 0 and x < x_size - 1 and y > 0 and y < y_size - 1 and grid[y][x] == '.':
		num_exits = (grid[y-1][x] != '#') + (grid[y+1][x] != '#') + (grid[y][x-1] != '#') + (grid[y][x+1] != '#')
		if num_exits == 1:
			print('Dead end:', x, y)
		return num_exits > 2
	return False

def print_grid():
	for y in range(y_size):
		for x in range(x_size):
			if is_intersection(x, y):
				print('X', end='')
			else:
				print(grid[y][x], end='')
		print()

nodes = [Coord(x, y) for x in range(x_size) for y in range(y_size) if is_intersection(x, y)]
nodes.append(start)
nodes.append(end)

# Now for the edges. We need a convenient way to measure the distance along a path. There aren't any
# simple dead ends, but there are one-way paths, so we have to account for that. Luckily, the slopes
# are all right next to the intersections, so we don't have to worry about that for the length. And
# they all point downhill, so there are no loops in the graph!
def measure_length_to_next_node(node: Coord, direction: Coord):
	length = 0
	while True:
		node = add_coords(node, direction)
		length += 1
		if is_intersection(node.x, node.y) or node == end or node == start:
			return node, length

		for new_direction in (up, down, left, right):
			if new_direction != Coord(-1 * direction.x, -1 * direction.y):
				new_node = add_coords(node, new_direction)
				if grid[new_node.y][new_node.x] != '#':
					direction = new_direction
					break

def find_exits(node: Coord):
	exits = []
	for direction in (up, down, left, right):
		adj = add_coords(node, direction)
		if adj.x >= 0 and adj.x <= x_size - 1 and adj.y > 0 and adj.y <= y_size - 1:
			tile = grid[adj.y][adj.x]
			if tile == '.' or (tile == '^' and direction == up) or (tile == 'v' and direction == down) or \
			   (tile == '<' and direction == left) or (tile == '>' and direction == right):
				exits.append(direction)
	return exits

Edge = namedtuple('Edge', ['dest', 'dist'])
graph: dict[Coord, list[Edge]] = {}
for node in nodes:
	graph[node] = []
	for direction in find_exits(node):
		next_node, length = measure_length_to_next_node(node, direction)
		graph[node].append((next_node, length))

# Okay, now we can do the actual DFS
def find_longest_path(node: Coord):
	if node == end:
		return 0
	else:
		dists = []
		for next_node, dist in graph[node]:
			dists.append(dist + find_longest_path(next_node));
		return max(dists)

longest = find_longest_path(start)
print(f"Part 1: The longest possible path length is: {longest}")

# Part 2: We can now climb the slopes, so the graph now has loops. But since we can't step on the
# same tile twice, we can't visit intersections multiple times, so thankfully we don't have to solve
# some kind of Bridges of Koenigsburg problem. We do, however, have to keep track of which nodes
# we've visited already during the recursion.
def find_exits2(node: Coord):
	exits = []
	for direction in (up, down, left, right):
		adj = add_coords(node, direction)
		if adj.x >= 0 and adj.x <= x_size - 1 and adj.y > 0 and adj.y <= y_size - 1:
			tile = grid[adj.y][adj.x]
			if tile != '#':
				exits.append(direction)
	return exits

graph: dict[Coord, list[Edge]] = {}
for node in nodes:
	graph[node] = []
	for direction in find_exits2(node):
		next_node, length = measure_length_to_next_node(node, direction)
		graph[node].append((next_node, length))

def find_longest_path2(node: Coord, visited: list[Coord]):
	if node == end:
		return 0
	else:
		visited.append(node)
		dists = []
		for next_node, dist in graph[node]:
			if next_node not in visited:
				new_dist = find_longest_path2(next_node, visited)
				if new_dist != None:
					dists.append(dist + new_dist)
		del visited[-1]
		if len(dists) == 0:
			return None
		else:
			return max(dists)

# Takes about 45 seconds. Inefficient, but usable for a one-time run.
longest = find_longest_path2(start, [])
print(f"Part 2: The longest possible path length is: {longest}")
