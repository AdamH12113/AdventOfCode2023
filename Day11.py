import re, sys, copy

# Read the input
try:
	day_num = int(re.findall(r'\d+', __file__)[-1])
	filename_base = 'Example' if '--example' in sys.argv else 'Input'
	filename = filename_base + str(day_num) + '.txt'
	with open(filename, 'rt') as f:
		input_text = f.read()[:-1]
except Exception as e:
	print(f"Error reading input: [{exception.__class__.__name__}] {exception}")

# Process the input. It's a 2-D grid (deja vu!) giving the locations of galaxies. We're going to
# have to expand the grid, so I suspect a sparse representation will make part 2 easier.
input_lines = input_text.split('\n')
galaxies = []
x_size = len(input_lines[0])
y_size = len(input_lines)
for x in range(x_size):
	for y in range(y_size):
		if input_lines[y][x] == '#':
			galaxies.append((x, y))

# Part 1: Expand every empty row and column to be twice as wide. What is the sum of the lengths
# between each pair of galaxies? The only tricky part is inserting more space. We can do this by
# incrementing the coordinates of the galaxies, but we need to iterate backwards to prevent double-
# counting empty space.
def expand_universe(universe, expansion_amount=1):
	x_max = max(g[0] for g in universe)
	y_max = max(g[1] for g in universe)

	for x in range(x_max-1, 0 - 1, -1):
		galaxy_found = False
		for galaxy in universe:
			if galaxy[0] == x:
				galaxy_found = True
				break
		
		if not galaxy_found:
			for g in range(len(universe)):
				if universe[g][0] > x:
					universe[g] = (universe[g][0] + expansion_amount, universe[g][1])

	for y in range(y_max-1, 0 - 1, -1):
		galaxy_found = False
		for galaxy in universe:
			if galaxy[1] == y:
				galaxy_found = True
				break

		if not galaxy_found:
			for g in range(len(universe)):
				if universe[g][1] > y:
					universe[g] = (universe[g][0], universe[g][1] + expansion_amount)

universe = copy.deepcopy(galaxies)
expand_universe(universe)

# We're using Manhattan distance here
lengths = []
for g1 in range(len(universe) - 1):
	for g2 in range(g1+1, len(universe)):
		gal1 = universe[g1]
		gal2 = universe[g2]
		lengths.append(abs(gal1[0] - gal2[0]) + abs(gal1[1] - gal2[1]))
print(f"Part 1: The sum of the lengths between pairs of galaxies is: {sum(lengths)}")

# Part 2: Now each empty row and column expands one million times. This is handled in the
# above function.
universe = copy.deepcopy(galaxies)
expand_universe(universe, expansion_amount=999999)
lengths = []
for g1 in range(len(universe) - 1):
	for g2 in range(g1+1, len(universe)):
		gal1 = universe[g1]
		gal2 = universe[g2]
		lengths.append(abs(gal1[0] - gal2[0]) + abs(gal1[1] - gal2[1]))
print(f"Part 2: The sum of the lengths between pairs of galaxies is: {sum(lengths)}")
