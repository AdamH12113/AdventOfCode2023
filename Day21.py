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

# Process the input. It's a 2-D grid consisting of garden plots ('.'), rocks ('#'), and a starting
# position on a garden plot ('S').
input_lines = input_text.split('\n')
grid = [list(line) for line in input_lines]
y_size = len(grid)
x_size = len(grid[0])

Coord = namedtuple('Coord', ['x', 'y'])
for x in range(x_size):
	for y in range(y_size):
		if grid[y][x] == 'S':
			start = Coord(x, y)
			grid[y][x] = '.'

def print_grid(grid: list):
	for y in range(y_size):
		for x in range(x_size):
			print(grid[y][x], end='')
		print()

up = Coord(0, -1)
down = Coord(0, 1)
left = Coord(-1, 0)
right = Coord(1, 0)

def add_coords(c1: Coord, c2: Coord):
	return Coord(c1.x + c2.x, c1.y + c2.y)

# Part 1: How many garden plots could a wandering elf reach in exactly 64 steps? It looks like any
# plot an even number of steps away is accessible. Regardless, the first step is to find the distances
# to each plot from the starting point.
State = namedtuple('State', ['coord', 'dist'])
visited = {}
queue = [State(start, 0)]
while len(queue) > 0:
	loc, dist = queue.pop()
	if loc in visited and visited[loc] <= dist:
		continue
	visited[loc] = dist
	new_dist = dist + 1
	
	# Add adjacent nodes to queue
	for direction in (up, down, left, right):
		new_loc = add_coords(loc, direction)
		if new_loc.y >= 0 and new_loc.y <= y_size - 1 and new_loc.x >= 0 and new_loc.x <= x_size - 1 and \
		   grid[new_loc.y][new_loc.x] != '#' and (new_loc not in visited or visited[new_loc] > new_dist):
			queue.insert(0, State(new_loc, new_dist))

max_steps = 64
reachable_plots = 0
for x in range(x_size):
	for y in range(y_size):
		c = Coord(x, y)
		if c in visited and visited[c] % 2 == 0 and visited[c] <= max_steps:
			reachable_plots += 1
print(f"Part 1: The number of reachable plots is: {reachable_plots}")

# Part 2: The elf now needs to travel 26501365 steps on an infinitely-repeating grid. How many
# garden plots can the elf reach?