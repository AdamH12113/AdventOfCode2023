import re, sys, copy
from typing_extensions import Self
from dataclasses import dataclass

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

# Process the input. Each line contains a hailstone's 3-D position and velocity separated by an @.
# In the problem text, we're also given a "test area", a range of x and y coordinates to use.
# Apparently a lot of people don't like named tuples, and frankly I'm getting tired of their
# limitations for representing coordinates, so I'm going to try the more popular dataclasses for
# this puzzle.
input_lines = input_text.split('\n')
if '--example' in sys.argv:
	test_area_min = 7
	test_area_max = 27
else:
	test_area_min = 200000000000000
	test_area_max = 400000000000000

@dataclass
class Vector:
	x: float
	y: float
	z: float
	
	def __add__(self, v: Self) -> Self:
		return type(self)(self.x + v.x, self.y + v.y, self.z + v.z)

	def __sub__(self, v: Self) -> Self:
		return type(self)(self.x - v.x, self.y - v.y, self.z - v.z)
	
	def __neg__(self) -> Self:
		return type(self)(-self.x, -self.y, -self.z)
	
	def __mul__(self, c: float) -> Self:
		return type(self)(c * self.x, c * self.y, c * self.z)
	
	def __rmul__(self, c: float) -> Self:
		return self * c
	
	def __truediv__(self, v: Self) -> Self:
		qx = (self.x / v.x) if v.x != 0 else 0
		qy = (self.y / v.y) if v.y != 0 else 0
		qz = (self.z / v.z) if v.z != 0 else 0
		return type(self)(qx, qy, qz)
	
	def __str__(self) -> str:
		return f"({self.x},{self.y},{self.z})"

positions = []
velocities = []
for line in input_lines:
	nums = re.findall(r'(\-?\d+)', line)
	positions.append(Vector(float(nums[0]), float(nums[1]), float(nums[2])))
	velocities.append(Vector(float(nums[3]), float(nums[4]), float(nums[5])))

# Part 1: Looking at the 2-D x-y plane *only*, find where the hailstones intersect. How many
# intersections are within the test area?
flat_pos = [Vector(p.x, p.y, 0) for p in positions]
flat_vel = [Vector(v.x, v.y, 0) for v in velocities]

# Time for some algebra. The equation for a hailstone's 2-D path is:
#   m = v.y / v.x
#   (y - p.y) = m(x - p.x)
#   -> y = m*x - m*p.x + p.y
#
#   m1*x - m1*x1 + y1 = m2*x - m2*x2 + y2
#   (m1 - m2)*x = m1*x1 - m2*x2 + y2 - y1
#   x = (m1*x1 - m2*x2 + y2 - y1) / (m1 - m2)
#
# Conveniently, none of the velocity components is ever zero.
def find_2d_intersection(p1: Vector, v1: Vector, p2: Vector, v2: Vector) -> Vector:
	m1 = v1.y / v1.x
	m2 = v2.y / v2.x
	if m1 == m2:
		return None
	x = (m1*p1.x - m2*p2.x + p2.y - p1.y) / (m1 - m2)
	y = m1*(x - p1.x) + p1.y
	return Vector(x, y, 0)

# To count as a valid hit, the two hailstone paths have to cross inside the target area *and* in the
# future of *both* hailstones.
num_valid_hits = 0
for h1 in range(len(positions) - 1):
	for h2 in range(h1 + 1, len(positions)):
		intersection = find_2d_intersection(positions[h1], velocities[h1], positions[h2], velocities[h2])
		if intersection is None:
			print(positions[h1], positions[h2], 'no intersection')
			continue
		
		dt1 = (intersection.x - positions[h1].x) / velocities[h1].x
		dt2 = (intersection.x - positions[h2].x) / velocities[h2].x
		print(positions[h2], positions[h2], intersection, dt1, dt2)
		if dt1 > 0 and dt2 > 0 and intersection.x >= test_area_min and intersection.x <= test_area_max and \
		              intersection.y >= test_area_min and intersection.y <= test_area_max:
			num_valid_hits += 1
print(f"Part 1: The number of intersections in the target area is: {num_valid_hits}")

# Part 2: We want to throw a rock from an arbitrary position with an arbitrary velocity and hit
# every hailstone as it falls. Find the position and velocity required to do this, then find the
# sum of the x, y, and z coordinates of the position? Collisions don't affect the rock's motion,
# so the hailstone paths must all intersect with some line, but how on earth do I find it?




