import re, sys, copy
from dataclasses import dataclass
from typing_extensions import Self

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
# bounding boxes or something. Ugh. Doing some Googling (since this is apparently the Advent of
# Googling for Algorithms this year) turns up something called the shoelace formula, which involves
# adding determinants of 2x2 matrices constructed from pairs of coordinates moving clockwise around
# the perimeter. Let's give it a try!
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

# After doing day 24, I switched to dataclasses for coordinates. This code is originally from there.
@dataclass
class Vector:
	x: int
	y: int
	
	def __add__(self, v: Self) -> Self:
		return type(self)(self.x + v.x, self.y + v.y)

	def __sub__(self, v: Self) -> Self:
		return type(self)(self.x - v.x, self.y - v.y)
	
	def __neg__(self) -> Self:
		return type(self)(-self.x, -self.y)
	
	def __mul__(self, c: int) -> Self:
		return type(self)(c * self.x, c * self.y)
	
	def __rmul__(self, c: int) -> Self:
		return self * c
	
	def __str__(self) -> str:
		return f"({self.x},{self.y})"

up = Vector(0, 1)
down = Vector(0, -1)
left = Vector(-1, 0)
right = Vector(1, 0)
start = Vector(0, 0)

# Let's convert the color-encoded directions to vectors
directions = []
perimeter = 0
for color in colors:
	new_dist = int(color[:5], 16)
	if color[5] == '0':
		new_dir = right
	elif color[5] == '1':
		new_dir = down
	elif color[5] == '2':
		new_dir = left
	else:
		new_dir = up
	perimeter += new_dist
	directions.append(new_dist * new_dir)

# The directions seem to be in clockwise order. We want our coordinates to be in counter-clockwise
# order for the algorithm.
coords = [start]
for d in reversed(directions):
	c = coords[-1]
	coords.append(c + d)

# Time to tie some shoelaces!
def det2x2(v1: Vector, v2: Vector):
	return (v1.x * v2.y) - (v2.x * v1.y)

area = 0
for n in range(len(coords) - 1):
	area += det2x2(coords[n], coords[n+1])
area = area // 2

# The area doesn't include the perimeter, which has a nonzero width. Curiously, it seems to be
# missing *half* the perimeter. I'm not sure how that works, but I'm not going to complain. (There's
# also an off-by-one, just for fun.)
print(f"Part 2: The size of the much larger lagoon is: {area + perimeter//2 + 1}")
