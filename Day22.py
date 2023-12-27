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
		self.below = set()
		self.above = set()
	
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

# After getting stuck on part 2 I became desperate for a faster way of doing part 1. Tracking which
# bricks end at which z coordinates turned out to be the key to optimizing the distressingly-nested
# loops below.
z_max = max(b.c2.z for b in bricks.values())
z_index = {z: set() for z in range(z_max)}

for id in sorted_ids:
	brick = bricks[id]
	supported = False
	while not supported and brick.c1.z > 0:
		crange = [brick.c1] if brick.direction.z == 1 else brick.coord_range()
		ids_to_check = z_index[brick.c1.z - 1]
		for id2 in ids_to_check:
			for c in crange:
				below = c + down
				if below in bricks[id2]:
					supported = True
					brick.below.add(id2)
					bricks[id2].above.add(id)
		if not supported:
			brick.move_down()
	z_index[brick.c2.z].add(id)

num_disintegrable = 0
for id in sorted_ids:
	disintegrable = True
	for ba_id in bricks[id].above:
		if len(bricks[ba_id].below) == 1:
			disintegrable = False
	if disintegrable:
		num_disintegrable += 1
print(f"Part 1: The number of disintegrable blocks is: {num_disintegrable}")

# Part 2: For each brick, determine how many other bricks would fall if that brick were
# disintegrated. What is the sum of those counts? Superficially, this seems like something where
# we could start from the top and keep track of results, but the interconnected nature of the
# bricks makes this tricky. I wonder if we could go from the top down? We could iterate downward
# through all possible paths and see if they converge at a single brick. Such a brick is apparently
# called a "dominator" in graph theory. It looks like all the ways of solving this problem are
# somewhat difficult to implement. Since the vast majority of bricks are only supported by one
# brick below, I'm going to do something easier but inefficient.
sorted_fallen_ids = sorted(bricks.keys(), key=lambda id: bricks[id].c1.z)
for id in sorted_fallen_ids:
	if bricks[id].c1.z > 0:
		first_nonzero_id = id
		break

sum_additional_destroyed_bricks = 0
for n in range(len(sorted_fallen_ids)):
	id = sorted_fallen_ids[n]
	destroyed = set()
	destroyed.add(id)
	not_on_ground = filter(lambda id: bricks[id].c1.z > 0, sorted_fallen_ids)
	
	for id2 in not_on_ground:
		if all(b in destroyed for b in bricks[id2].below):
			destroyed.add(id2)
	sum_additional_destroyed_bricks += len(destroyed) - 1

print(f"Part 2: The sum of the number of additional falling bricks is: {sum_additional_destroyed_bricks}")

