import re, sys, copy

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

# Process the input. It's a 2-D grid consisting of mirrors ('/' and '\'), splitter ('|' and '-'),
# and empty space ('.').
grid = [list(line) for line in input_text.split('\n')]
y_size = len(grid)
x_size = len(grid[0])

def print_grid(grid: list):
	print('\n' + '\n'.join(''.join(g) for g in grid))

# Part 1: Light reflects off of mirrors at a 90-degree angle, and is split into two 90-degree beams
# when it hits a splitter perpendicularly. How many tiles have a beam of light passing through them
# ("energized")?
def print_energized(tiles: list):
	out = []
	for y in range(y_size):
		out.append([])
		for x in range(x_size):
			out[y].append('#' if tiles[y][x] else '.')
	print('\n' + '\n'.join(''.join(g) for g in out))

# An unexpected bit of trickiness -- the light can travel in loops! We need to mark which splitters
# have been used already.
def follow_light_beam(x: int, y: int, direction: tuple, energized: list, splitter_used: list):
	while True:
		if x < 0 or x >= x_size or y < 0 or y >= y_size:
			break

		energized[y][x] = True
		tile = grid[y][x]
		if tile == '/':
			direction = (-direction[1], -direction[0])
		elif tile == '\\':
			direction = (direction[1], direction[0])
		elif tile == '|' and (direction == (1, 0) or direction == (-1, 0)):
			if not splitter_used[y][x]:
				splitter_used[y][x] = True
				follow_light_beam(x, y - 1, (0, -1), energized, splitter_used)
				follow_light_beam(x, y + 1, (0, 1), energized, splitter_used)
			break
		elif tile == '-' and (direction == (0, 1) or direction == (0, -1)):
			if not splitter_used[y][x]:
				splitter_used[y][x] = True
				follow_light_beam(x - 1, y, (-1, 0), energized, splitter_used)
				follow_light_beam(x + 1, y, (1, 0), energized, splitter_used)
			break
		
		x += direction[0]
		y += direction[1]

energized_tiles = [[False for x in range(x_size)] for y in range(y_size)]
splitter_used = [[False for x in range(x_size)] for y in range(y_size)]
follow_light_beam(0, 0, (1, 0), energized_tiles, splitter_used)
num_energized = sum(energized_tiles[y][x] for y in range(y_size) for x in range(x_size))
print(f"Part 1: The number of energized tiles is: {num_energized}")

# Part 2: We can make the light enter from any location on any edge. For the choice that produces
# the most energized tiles, how many tiles are energized?
def run_one_configuration(x: int, y: int, direction: tuple):
	energized_tiles = [[False for x in range(x_size)] for y in range(y_size)]
	splitter_used = [[False for x in range(x_size)] for y in range(y_size)]
	follow_light_beam(x, y, direction, energized_tiles, splitter_used)
	num_energized = sum(energized_tiles[y][x] for y in range(y_size) for x in range(x_size))
	return num_energized

max_energized = 0
for x in range(x_size):
	energized = run_one_configuration(x, 0, (0, 1))
	max_energized = max(max_energized, energized)
	energized = run_one_configuration(x, y_size - 1, (0, -1))
	max_energized = max(max_energized, energized)

for y in range(y_size):
	energized = run_one_configuration(0, y, (1, 0))
	max_energized = max(max_energized, energized)
	energized = run_one_configuration(x_size - 1, y, (-1, 0))
	max_energized = max(max_energized, energized)
	
print(f"Part 2: The maximum possible number of energized tiles is: {max_energized}")










