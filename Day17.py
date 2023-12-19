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

# Process the input. It's a 2-D grid consisting of digits that give a cost for entering that tile.
input_lines = input_text.split('\n')
#input_lines = input_lines[:2]
grid = [[int(d) for d in line] for line in input_lines]
y_size = len(grid)
x_size = len(grid[0])

def print_grid(grid: list):
	print('\n'.join(''.join(str(g) for g in grid_line) for grid_line in grid))


# Part 1: Find the lowest-cost path through the grid without moving more than three consecutive
# steps in any direction. Time for a breadth-first search! (I'm surprised its taken this long to
# need one, honestly.) Since the search state is a bit more complicated than just coordinates, I'm
# going to take this opportunity to experiment with named tuples.
Coord = namedtuple('Coord', ['x', 'y'])
State = namedtuple('State', ['coord', 'dir', 'dirsteps', 'loss'])
up = Coord(0, -1)
down = Coord(0, 1)
left = Coord(-1, 0)
right = Coord(1, 0)

def add_coords(a: Coord, b: Coord):
	return Coord(a.x + b.x, a.y + b.y)

# Start with zero steps in the current direction as a hack to handle the first tile
visited = {}
next_steps = [State(Coord(0, 0), right, 0, 0)]

def print_costs():
	for y in range(y_size):
		for x in range(x_size):
			c = Coord(x, y)
			cost = visited[c] if c in visited else 0
			print(f"{cost: 4}", end='')
		print()
	print()


while len(next_steps) > 0:
	# Update the minimum loss for the current location
	loc, direction, dirsteps, loss = next_steps.pop()
	if loc not in visited or visited[loc] > loss:
		visited[loc] = loss
		#print(len(next_steps), len(visited))
	else:
		continue

	# Which ways can we physically move?
	can_move_left = loc.x > 0 and not (direction == right or (direction == left and dirsteps >= 3))
	can_move_right = loc.x < x_size - 1 and not (direction == left or (direction == right and dirsteps >= 3))
	can_move_up = loc.y > 0 and not (direction == down or (direction == up and dirsteps >= 3))
	can_move_down = loc.y < y_size - 1 and not (direction == up or (direction == down and dirsteps >= 3))

	# Add possible steps to the queue if it looks like we've found a lower-loss path
	if can_move_left:
		new_coord = add_coords(loc, left)
		new_loss = loss + grid[new_coord.y][new_coord.x]
		new_dirsteps = (dirsteps + 1) if direction == left else 1
		if new_coord not in visited or visited[new_coord] > new_loss:
			new_state = State(new_coord, left, new_dirsteps, new_loss)
			next_steps.insert(0, new_state)

	if can_move_right:
		new_coord = add_coords(loc, right)
		new_loss = loss + grid[new_coord.y][new_coord.x]
		new_dirsteps = (dirsteps + 1) if direction == right else 1
		if new_coord not in visited or visited[new_coord] > new_loss:
			new_state = State(new_coord, right, new_dirsteps, new_loss)
			next_steps.insert(0, new_state)

	if can_move_up:
		new_coord = add_coords(loc, up)
		new_loss = loss + grid[new_coord.y][new_coord.x]
		new_dirsteps = (dirsteps + 1) if direction == up else 1
		if new_coord not in visited or visited[new_coord] > new_loss:
			new_state = State(new_coord, up, new_dirsteps, new_loss)
			next_steps.insert(0, new_state)

	if can_move_down:
		new_coord = add_coords(loc, down)
		new_loss = loss + grid[new_coord.y][new_coord.x]
		new_dirsteps = (dirsteps + 1) if direction == down else 1
		if new_coord not in visited or visited[new_coord] > new_loss:
			new_state = State(new_coord, down, new_dirsteps, new_loss)
			next_steps.insert(0, new_state)

#min_loss = min(visited[c, d] for (c, d) in visited.keys() if c.x == x_size - 1 and c.y == y_size - 1)
min_loss = visited[Coord(x_size - 1, y_size - 1)]
print(f"Part 1: The minimum heat loss to reach the end of the path is: {min_loss}")


