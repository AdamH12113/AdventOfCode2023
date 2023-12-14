import re, sys

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

# Process the input. It's a 2-D grid describing the layout of connected pipe segments.
input_lines = input_text.split('\n')
x_size = len(input_lines[0])
y_size = len(input_lines)

# Transposing the grid solely because I like writing the x coordinate first
grid = [[input_lines[y][x] for y in range(y_size)] for x in range(x_size)]
for x in range(x_size):
	for y in range(y_size):
		if grid[x][y] == 'S':
			start = (x, y)

# Part 1: The cell containing 'S' is the starting position of an animal in a large, continuous loop
# of pipe. We need to find the distance to the farther pipe segment in that loop as measured along
# the loop in either direction. First, we need to find what directions we can go from the start
# since that pipe segment is covered by the 'S', and replace the 'S' with a proper tile.
def replace_start_tile(x: int, y: int):
	start_dirs = []
	if x > 0:
		p = grid[x-1][y]
		if p == '-' or p == 'L' or p == 'F':
			start_dirs.append((-1, 0))
	if x < x_size - 1:
		p = grid[x+1][y]
		if p == '-' or p == 'J' or p == '7':
			start_dirs.append((1, 0))
	if y > 0:
		p = grid[x][y-1]
		if p == '|' or p == '7' or p == 'F':
			start_dirs.append((0, -1))
	if y < y_size - 1:
		p = grid[x][y+1]
		if p == '|' or p == 'L' or p == 'J':
			start_dirs.append((0, 1))
			
	if (-1, 0) in start_dirs and (1, 0) in start_dirs:
		grid[x][y] = '-'
	elif (0, -1) in start_dirs and (0, 1) in start_dirs:
		grid[x][y] = '|'
	elif (0, -1) in start_dirs and (1, 0) in start_dirs:
		grid[x][y] = 'L'
	elif (-1, 0) in start_dirs and (0, -1) in start_dirs:
		grid[x][y] = 'J'
	elif (-1, 0) in start_dirs and (0, 1) in start_dirs:
		grid[x][y] = '7'
	else:
		grid[x][y] = 'F'
	

def get_dirs_from_segment(seg: str):
	if seg == '|':  return ((0, -1), (0, 1))
	if seg == '-':  return ((-1, 0), (1, 0))
	if seg == 'L':  return ((1, 0), (0, -1))
	if seg == 'J':  return ((-1, 0), (0, -1))
	if seg == '7':  return ((-1, 0), (0, 1))
	if seg == 'F':  return ((1, 0), (0, 1))
	raise ValueError(f"Bad segment {seg}")
	

# Now we can iterate along the pipe to find all the distances
replace_start_tile(start[0], start[1])
visited = {}
queue = [(start[0], start[1], 0)]

# Mediocre redundant implementation because I'm tired
while len(queue) > 0:
	x, y, dist = queue.pop()
	if (x, y) not in visited or visited[(x, y)] > dist:
		visited[(x, y)] = dist

	dist += 1
	next_dirs = get_dirs_from_segment(grid[x][y])
	for ndir in next_dirs:
		nx = x + ndir[0]
		ny = y + ndir[1]
		if (nx, ny) not in visited or visited[(nx, ny)] > dist:
			queue.insert(0, (nx, ny, dist))

print(f"Part 1: The farthest distance from the starting position is: {max(visited.values())}")

# Part 2: Find the number of tiles enclosed by the loop. We already have all the tiles in the loop
# from part 1, so here's my clever plan: I observe from the examples that tiles inside the loop can
# only reach the edge of the map by passing through an *odd* number of *perpendicular* pipe segments
# in the loop. But the way the map is encoded makes this tricky to use -- looking at a corner by
# itself doesn't tell us anything; we have to know about the next corner too. For example, if we're
# moving horizontally, then we can squeeze by LJ or F7 but L7 or FJ counts as an actual boundary.
# So we have to remember the last corner we saw.
def is_inside_loop(tx: int, ty: int):
	if (tx, ty) in visited:
		return False
	pipes_crossed = 0
	last_corner = None
	
	# We can move in any direction. Might as well go right.
	for x in range(tx+1, x_size):
		if (x, ty) not in visited:
			continue
		seg = grid[x][ty]
		if seg == '|':
			pipes_crossed += 1
		elif seg == 'L' or seg == 'F':
			last_corner = seg
		elif seg == '7':
			if last_corner == 'L':
				pipes_crossed += 1
			last_corner = None
		elif seg == 'J':
			if last_corner == 'F':
				pipes_crossed += 1
			last_corner = None
	return (pipes_crossed % 2) == 1

num_enclosed_tiles = 0
for x in range(1, x_size-1):
	for y in range(1, y_size-1):
		if is_inside_loop(x, y):
			num_enclosed_tiles += 1
print(f"Part 2: The number of enclosed tiles is: {num_enclosed_tiles}")
