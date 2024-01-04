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
# garden plots can the elf reach? The first thing we need to do is handle the infinite grid with
# modulus indexing. The example has 81 plots, 39 of which can be reached in an odd number of steps
# and 42 of which can be reached in an even number of steps. The input has 14781 plots, of which
# 7421 are odd and 7450 are even.
grid_range = 3
min_x = -grid_range * x_size
max_x = (grid_range + 1) * x_size - 1
min_y = -grid_range * y_size
max_y = (grid_range + 1) * y_size - 1

def mcoord(x: int, y: int) -> Coord:
	return Coord(x % x_size, y % y_size)

def print_grids(grid_range: int, visited: dict, what: str = 'dist'):
	num_in = 0
	for y in range(min_y, max_y + 1):
		for x in range(min_x, max_x + 1):
			#mc = mcoord(x, y)
			mc = Coord(x, y)
			if mc in visited:
				if what == 'dist':
					print(f"{visited[mc]:3} ", end='')
				else:
					print(f"{abs(x):2}{abs(y):2}", end='')
			else:
				print('████', end='')
		print()

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
		mc = mcoord(new_loc.x, new_loc.y)
		if new_loc.y >= min_y and new_loc.y <= max_y and new_loc.x >= min_x and new_loc.x <= max_x:
			if grid[mc.y][mc.x] != '#' and (new_loc not in visited or visited[new_loc] > new_dist):
				queue.insert(0, State(new_loc, new_dist))

# After playing with this, it looks like the number of steps it takes to get to a plot has a pattern
# where each copy of the grid adds 11 to the step count (in the example). The real input's copies
# are 131 steps apart. The example grid is 11x11, and the input is 131x131, so that explains that.
# To determine whether the elf can reach a plot, we only care if it takes an odd or even number of
# steps to get there. The parity of the grid flips when we cross between adjacent copies. So for
# grids that are fully within range, we can just add a known count. The tricky part is the grids
# around the edges. In principle, we could iterate over all grids within range and count the reachable
# plots for each one. But even for the real input that's 200000x200000 grids, which is too many.
# Maybe we should take a hint from the description and try computing a bunch of different distances
# to see if there's a pattern. But trying that doesn't get me a usable pattern I can find, so let's
# try doing it the hard way! First, I need a way to get the distance for any coordinate.
grid_step = 11 if '--example' in sys.argv else 131

# The pattern seems to kick in three grids away from the start, but there are some complications.
# If we go in a straight line from the start, then even after a long distance the next grid to the
# side isn't 11 or 131 steps away. So we need to handle these stripes separately.
def base_coord(x: int, y: int) -> Coord:
	xc = x
	if x >= x_size * (grid_range + 1):
		x = (x % x_size) + (x_size * grid_range)
	elif x < -x_size * grid_range:
		# Negative modulus division in Python is a little weird
		x = (x % -x_size) - (x_size * (grid_range - 1))

	if y >= y_size * (grid_range + 1):
		y = (y % y_size) + (y_size * grid_range)
	elif y < -y_size * grid_range:
		# Negative modulus division in Python is a little weird
		y = (y % -y_size) - (y_size * (grid_range - 1))

	return Coord(x, y)

def dist(x: int, y: int) -> int:
	bc = base_coord(x, y)
	if bc not in visited:
		return None
	extra_x_grids = abs(x - bc.x) / x_size
	extra_y_grids = abs(y - bc.y) / y_size
	return visited[bc] + extra_x_grids*grid_step + extra_y_grids*grid_step

# We need to know how many plots are in even- and odd-numbered grids for optimization
even_grid_count = sum(1 for c in visited if c.x in range(0, x_size) and c.y in range(0, y_size) and visited[c] % 2 == 0)
odd_grid_count = sum(1 for c in visited if c.x in range(0, x_size) and c.y in range(0, y_size) and visited[c] % 2 == 1)

def grid_in_range(gx: int, gy: int, num_steps: int):
	xmin = gx * x_size
	ymin = gy * y_size
	xmax = xmin + x_size - 1
	ymax = ymin + y_size - 1
	corners = (Coord(xmin, ymin), Coord(xmin, ymax), Coord(xmax, ymin), Coord(xmax, ymax))
	corners_in = sum(1 for c in corners if dist(c.x, c.y) <= num_steps)
	if corners_in == 0 and not (gx == 0 and gy == 0):
		return False
	elif corners_in == 4:
		return True
	else:
		return None

def reachable_plots_in_grid(gx: int, gy: int, num_steps: int, force: bool = False):
	# The zero coordinates are forcibly calculated as a workaround for some edge case I
	# don't want to spend time on.
	gir = grid_in_range(gx, gy, num_steps)
	if gir == True and not force and not (gx == 0 or gy == 0):
		return even_grid_count if (gx + gy) % 2 == 0 else odd_grid_count
	elif gir == False and not force:
		return 0
	else:
		reachable = 0
		for x in range(gx*x_size, (gx+1)*x_size):
			for y in range(gy*y_size, (gy+1)*y_size):
				d = dist(x, y)
				if d is not None and d <= num_steps and d % 2 == num_steps % 2:
					reachable += 1
		return reachable

# Okay, after noodling at this the plan is to divide the reachable area into horizontal slices. Each
# slice will have two end grids (which we have to check individually) and a bunch of fully-in-range
# grids in between, which we can handle by multiplying.
def gymax_for_maxdist(max_dist: int):
	return (max_dist // y_size) + 3

def gxmax_for_maxdist_and_gy(max_dist: int, gy: int):
	return (max_dist // x_size) - abs(gy) + 3

max_dist = 26501365
manual_range = 3

print('Starting sweep...')
total = 0
gymax = gymax_for_maxdist(max_dist)
for gy in range(-gymax, gymax + 1):
	if gy % 10 == 0:
		print(gy)
	gxmax = gxmax_for_maxdist_and_gy(max_dist, gy)
	if gxmax == 0:
		total += reachable_plots_in_grid(0, gy, max_dist)
	elif gxmax <= manual_range:
		for gx in range(-gxmax, gxmax + 1):
			total += reachable_plots_in_grid(gx, gy, max_dist)
	else:
		gx = -gxmax
		while gx < -manual_range:
			c = reachable_plots_in_grid(gx, gy, max_dist)
			if c == even_grid_count:
				remx = abs(gx - -manual_range)
				total += (remx//2) * odd_grid_count
				total += (remx//2 + remx % 2) * even_grid_count
				break
			elif c == odd_grid_count:
				remx = abs(gx - -manual_range)
				total += (remx//2 + remx % 2) * odd_grid_count
				total += (remx//2) * even_grid_count
				break
			else:
				total += c
				gx += 1

		total += sum(reachable_plots_in_grid(gx, gy, max_dist) for gx in range(-manual_range, manual_range + 1))

		gx = gxmax
		while gx > manual_range:
			c = reachable_plots_in_grid(gx, gy, max_dist)
			if c == even_grid_count:
				remx = abs(gx - manual_range)
				total += (remx//2) * odd_grid_count
				total += (remx//2 + remx % 2) * even_grid_count
				break
			elif c == odd_grid_count:
				remx = abs(gx - manual_range)
				total += (remx//2 + remx % 2) * odd_grid_count
				total += (remx//2) * even_grid_count
				break
			else:
				total += c
				gx -= 1

print(f"Part 2: The number of reachable plots is: {total}")

# This code takes about 12 hours to run. I get 608603011371992. The actual answer is 608603023105276,
# so I am off by about 19 parts per billion. There is probably a small error somewhere in the code,
# but I am not going to bother finding it. Looking online, I see mainly solutions that rely heavily
# on assumptions about the real input that do not seem to apply to the example, and are definitely
# not found anywhere in the problem description. Perhaps this is the sort of thing they have to do
# to keep ChatGPT off the leaderboards, but I am not competing for the leaderboards so I do not find
# this sort of thing very fun. (Not to complain about the free puzzles, mind you! I love the Advent
# of Code.)
#
# After several days of effort, I declare defeat for this puzzle. I used someone else's code to get
# the answer so I could see the pretty animation on the web page.
