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

# Process the input. Each line is a pair of 3-D (!!) coordinates separated by a tilde, which
# represent the endpoints of a single rectangular brick.
input_lines = input_text.split('\n')

class Coord:
	def __init__(self, x: int, y: int, z: int):
		self.x = x
		self.y = y
		self.z = z

	def __add__(self, coord):
		return Coord(self.x + coord.x, self.y + coord.y, self.z + coord.z)
	
	def __sub__(self, coord):
		return Coord(self.x - coord.x, self.y - coord.y, self.z - coord.z)
	
	def __mul__(self, scalar: int):
		return Coord(scalar * self.x, scalar * self.y, scalar * self.z)
	def __rmul__(self, scalar: int):
		return Coord(scalar * self.x, scalar * self.y, scalar * self.z)
	
	def __str__(self):
		return f"{self.x}, {self.y},{self.z:3}"
	def __repr__(self):
		return f"Coord({self.x},{self.y},{self.z})"

down = Coord(0, 0, -1)

class Brick:
	def __init__(self, coord_text: str):
		tilde = coord_text.index('~')
		self.c1 = Coord(*(int(n) for n in coord_text[:tilde].split(',')))
		self.c2 = Coord(*(int(n) for n in coord_text[tilde+1:].split(',')))
		diff = self.c2 - self.c1
		self.length = abs(diff.x + diff.y + diff.z) + 1
		if (diff.x < 0) or (diff.y < 0) or (diff.z < 0):
			c = self.c1
			self.c1 = self.c2
			self.c2 = c
		if diff.x != 0:
			self.direction = Coord(1, 0, 0)
		elif diff.y != 0:
			self.direction = Coord(0, 1, 0)
		else:
			self.direction = Coord(0, 0, 1)
		self.below = []
		self.above = []
	
	def move_down(self):
		self.c1.z -= 1
		self.c2.z -= 1
	
	def coord_range(self):
		return [self.c1 + n*self.direction for n in range(self.length)]
	
	def __contains__(self, coord: Coord):
		return coord.x >= self.c1.x and coord.x <= self.c2.x and coord.y >= self.c1.y and \
		       coord.y <= self.c2.y and coord.z >= self.c1.z and coord.z <= self.c2.z
	
	def __str__(self):
		return f"{self.c1.x},{self.c1.y},{self.c1.z}-{self.c2.x},{self.c2.y},{self.c2.z} {self.below} {self.above}"

bricks = {n: Brick(input_lines[n]) for n in range(len(input_lines))}
x_size = max(max(b.c1.x, b.c2.x) for b in bricks.values())
y_size = max(max(b.c1.y, b.c2.y) for b in bricks.values())

# Part 1: How many bricks could be disintigrated without causing another brick to fall? Bricks can
# be supported even on the very end, so this is ultimately about which bricks are touching each
# other, not balance. The bricks are still in the air, so we need to figure out where they all end
# up first. Let's start by sorting the bricks by height.
sorted_ids = sorted(bricks.keys(), key=lambda id: min(bricks[id].c1.z, bricks[id].c2.z))
fallen_ids = []
n = 0

for id in sorted_ids:
	print(n, id)
	n += 1
	brick = bricks[id]
	supported = False
	while not supported and brick.c1.z > 0:
		for c in brick.coord_range():
			below = c + down
			for id2 in fallen_ids:
				if bricks[id2].c2.z < below.z:
					continue
				if below in bricks[id2]:
					supported = True
					if id2 not in brick.below:
						brick.below.append(id2)
						bricks[id2].above.append(id)
		if not supported:
			brick.move_down()
	fallen_ids.append(id)

num_disintegrable = 0
for id in fallen_ids:
	disintegrable = True
	for ba_id in bricks[id].above:
		if len(bricks[ba_id].below) == 1:
			disintegrable = False
	if disintegrable:
		num_disintegrable += 1
print(f"Part 1: The number of disintegrable blocks is: {num_disintegrable}")



