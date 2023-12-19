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

# Process the input. It's a sequence of instructions for digging a trench. Each line has a direction,
# a distance, and a hex color code.
input_lines = input_text.split('\n')
num_steps = len(input_lines)
dirs = []
distances = []
colors = []
for line in input_lines:
	m = re.match(r'([UDLR]) (\d+) \(#([0-9a-f]+)\)', line)
	dirs.append(m[1])
	distances.append(int(m[2]))
	colors.append(m[3])

# Part 1: After digging out the trench and its interior, how many tiles of lava can it hold? Finding
# the interior is a bit trickier than on day 10 since we don't have an easy way of telling which way
# the trench points. We'll have to find an interior point and fill in from there. Let's draw the
# trench first.
def delta_direction(direction: str):
	if direction == 'U':   return (0, 1)
	elif direction == 'D': return (0, -1)
	elif direction == 'L': return (-1, 0)
	else:                  return (1, 0)

dug_tiles = set()
dug_tiles.add((0, 0))
locx = 0
locy = 0
for s in range(num_steps):
	dx, dy = delta_direction(dirs[s])
	for dist in range(1, distances[s]+1):
		dug_tiles.add((locx + dist*dx, locy + dist*dy))
	locx += dist*dx
	locy += dist*dy
minx = min(dt[0] for dt in dug_tiles)
maxx = max(dt[0] for dt in dug_tiles)
miny = min(dt[1] for dt in dug_tiles)
maxy = max(dt[1] for dt in dug_tiles)

def print_grid(tiles: set, minx: int, maxx: int, miny: int, maxy: int):
	for y in range(maxy, miny-1, -1):
		for x in range(minx, maxx+1):
			print('#' if (x,y) in tiles else '.', end='')
		print()

# Okay, it looks like there's always at least a one-tile gap between trench tiles. Both the example
# and my input start by going right, so I'll just start with tile (1, -1) and expand outward. Making
# a fully general solution wouldn't be hard, but I'm in a hurry today.
tile_queue = [(1, -1)]
while len(tile_queue) > 0:
	(tx, ty) = tile_queue.pop()
	if (tx, ty) in dug_tiles:
		continue
	
	dug_tiles.add((tx, ty))
	for new_tile in ((tx+1, ty), (tx-1, ty), (tx, ty+1), (tx, ty-1)):
		if new_tile not in dug_tiles and new_tile not in tile_queue:
			tile_queue.insert(0, new_tile)

print(f"Part 1: The size of the lagoon is: {len(dug_tiles)}")

# Part 2: The color codes were the real instructions all along! The first five hex digits give the
# distance and the last encodes the direction (0=R, 1=D, 2=L, 3=U). The lengths are now impossibly
# large, and the example produces a lagoon with an area of ~950 billion. We'll probably have to find
# bounding boxes or something. Ugh.
new_dirs = []
new_dists = []
for color in colors:
	new_dists.append(int(color[:5], 16))
	if color[5] == '0':
		new_dirs.append('R')
	elif color[5] == '1':
		new_dirs.append('D')
	elif color[5] == '2':
		new_dirs.append('L')
	else:
		new_dirs.append('U')



