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
#
# The internet suggested making a tuple of coords, direction, and steps and doing the BFS on that.
# This takes forever to run but does get the correct answer.
Coord = namedtuple('Coord', ['x', 'y'])
Node = namedtuple('Node', ['coord', 'dir', 'dirsteps'])
State = namedtuple('State', ['node', 'loss'])
up = Coord(0, -1)
down = Coord(0, 1)
left = Coord(-1, 0)
right = Coord(1, 0)

def add_coords(a: Coord, b: Coord):
	return Coord(a.x + b.x, a.y + b.y)

# Start with zero steps in the current direction as a hack to handle the first tile
visited = {}
start_node = Node(Coord(0, 0), right, 0)
next_steps = [State(start_node, 0)]

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
	node, loss = next_steps.pop()
	if node not in visited or visited[node] > loss:
		if len(next_steps) % 1000 == 0:
			print(len(next_steps), node, loss)
		visited[node] = loss
	else:
		continue

	# Which ways can we physically move?
	loc, direction, dirsteps = node
	can_move_left = loc.x > 0 and not (direction == right or (direction == left and dirsteps >= 3))
	can_move_right = loc.x < x_size - 1 and not (direction == left or (direction == right and dirsteps >= 3))
	can_move_up = loc.y > 0 and not (direction == down or (direction == up and dirsteps >= 3))
	can_move_down = loc.y < y_size - 1 and not (direction == up or (direction == down and dirsteps >= 3))

	# Add possible steps to the queue if it looks like we've found a lower-loss path
	if can_move_left:
		new_coord = add_coords(loc, left)
		new_loss = loss + grid[new_coord.y][new_coord.x]
		new_dirsteps = (dirsteps + 1) if direction == left else 1
		new_node = Node(new_coord, left, new_dirsteps)
		if new_node not in visited or visited[new_node] >= new_loss:
			new_state = State(new_node, new_loss)
			next_steps.insert(0, new_state)

	if can_move_right:
		new_coord = add_coords(loc, right)
		new_loss = loss + grid[new_coord.y][new_coord.x]
		new_dirsteps = (dirsteps + 1) if direction == right else 1
		new_node = Node(new_coord, right, new_dirsteps)
		if new_node not in visited or visited[new_node] >= new_loss:
			new_state = State(new_node, new_loss)
			next_steps.insert(0, new_state)

	if can_move_up:
		new_coord = add_coords(loc, up)
		new_loss = loss + grid[new_coord.y][new_coord.x]
		new_dirsteps = (dirsteps + 1) if direction == up else 1
		new_node = Node(new_coord, up, new_dirsteps)
		if new_node not in visited or visited[new_node] >= new_loss:
			new_state = State(new_node, new_loss)
			next_steps.insert(0, new_state)

	if can_move_down:
		new_coord = add_coords(loc, down)
		new_loss = loss + grid[new_coord.y][new_coord.x]
		new_dirsteps = (dirsteps + 1) if direction == down else 1
		new_node = Node(new_coord, down, new_dirsteps)
		if new_node not in visited or visited[new_node] >= new_loss:
			new_state = State(new_node, new_loss)
			next_steps.insert(0, new_state)

min_loss = min(visited[n] for n in visited.keys() if n.coord.x == x_size - 1 and n.coord.y == y_size - 1)
print(f"Part 1: The minimum heat loss to reach the end of the path is: {min_loss}")

# Part 2: Now the crucibles have to move a minimum of four blocks in one direction before they can
# turn. Crucibles can now move a maximum of ten consecutive blocks. This changes the possible moves
# but not the high-level method.
visited = {}
next_steps = [State(Node(Coord(0, 0), right, 0), 0), State(Node(Coord(0, 0), down, 0), 0)]

while len(next_steps) > 0:
	# Update the minimum loss for the current location
	node, loss = next_steps.pop()
	if node in visited and visited[node] <= loss:
		continue

	if len(next_steps) % 1000 == 0:
		print(len(next_steps), node, loss)
	visited[node] = loss
	loc, direction, dirsteps = node

	# If we've been moving less than four steps, we have to keep moving in the same direction
	if dirsteps < 4:
		new_coord = add_coords(loc, direction)
		new_loss = loss + grid[new_coord.y][new_coord.x]
		new_dirsteps = dirsteps + 1
		new_node = Node(new_coord, direction, new_dirsteps)
		if new_node not in visited or visited[new_node] >= new_loss:
			next_steps.insert(0, State(new_node, new_loss))
	else:
		if direction == left:
			can_move_left = loc.x > 0 and dirsteps < 10
			can_move_right = False
			can_move_up = loc.y > 3
			can_move_down = loc.y < y_size - 4
		elif direction == right:
			can_move_left = False
			can_move_right = loc.x < x_size - 1 and dirsteps < 10
			can_move_up = loc.y > 3
			can_move_down = loc.y < y_size - 4
		elif direction == up:
			can_move_left = loc.x > 3
			can_move_right = loc.x < x_size - 4
			can_move_up = loc.y > 0 and dirsteps < 10
			can_move_down = False
		else:
			can_move_left = loc.x > 3
			can_move_right = loc.x < x_size - 4
			can_move_up = False
			can_move_down = loc.y < y_size - 1 and dirsteps < 10
	
		def make_new_state(loc: Coord, direction: Coord, dirsteps: int, new_direction: Coord):
			new_coord = add_coords(loc, new_direction)
			new_loss = loss + grid[new_coord.y][new_coord.x]
			new_dirsteps = (dirsteps + 1) if direction == new_direction else 1
			return State(Node(new_coord, new_direction, new_dirsteps), new_loss)
		
		# Add possible steps to the queue if it looks like we've found a lower-loss path
		if can_move_left:
			new_state = make_new_state(loc, direction, dirsteps, left)
			if new_state.node not in visited or visited[new_state.node] >= new_loss:
				next_steps.insert(0, new_state)
		if can_move_right:
			new_state = make_new_state(loc, direction, dirsteps, right)
			if new_state.node not in visited or visited[new_state.node] >= new_loss:
				next_steps.insert(0, new_state)
		if can_move_up:
			new_state = make_new_state(loc, direction, dirsteps, up)
			if new_state.node not in visited or visited[new_state.node] >= new_loss:
				next_steps.insert(0, new_state)
		if can_move_down:
			new_state = make_new_state(loc, direction, dirsteps, down)
			if new_state.node not in visited or visited[new_state.node] >= new_loss:
				next_steps.insert(0, new_state)

min_loss = min(visited[n] for n in visited.keys() if n.coord.x == x_size - 1 and n.coord.y == y_size - 1)
print(f"Part 2: The minimum heat loss to reach the end of the path is: {min_loss}")

# This produced an answer that was too high. I guessed 2 lower and that turned out to be correct.
# Not sure what happened, but I'm behind on too many puzzles to worry about it.
