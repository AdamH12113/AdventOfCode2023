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

# Process the input. Plot twist: it's *multiple* 2-D grids! Each grid gives a pattern of ash ('.')
# and rocks ('#').
grids_text = input_text.split('\n\n')
grids = [grid_text.split('\n') for grid_text in grids_text]

# Part 1: Each grid is symmetric across a single vertical line (between columns) or horizontal line
# (between rows). Find the line of symmetry. The actual answer is an elaborate formula I'll give later.
def compare_rows(grid: list, y1: int, y2: int):
	for x in range(len(grid[0])):
		if grid[y1][x] != grid[y2][x]:
			return False
	return True

def compare_cols(grid: list, x1: int, x2: int):
	for y in range(len(grid)):
		if grid[y][x1] != grid[y][x2]:
			return False
	return True

# The x coordinate here refers to the column immediately to the right of the line of symmetry
def check_horizontal_symmetry(grid: list, xs: int):
	dist = min(xs, len(grid[0]) - xs)
	for r in range(1, dist + 1):
		if not compare_cols(grid, xs - r, xs + r - 1):
			return False
	return True

# The y coordinate here refers to the column immediately below the line of symmetry
def check_vertical_symmetry(grid: list, ys: int):
	dist = min(ys, len(grid) - ys)
	for r in range(1, dist + 1):
		if not compare_rows(grid, ys - r, ys + r - 1):
			return False
	return True

# The numerical answer we're supposed to get is either the number of columns to the left of a
# line of horizontal symmetry or 100 times the number of rows above a line of vertical symmetry.
def find_symmetry(grid: list):
	for x in range(1, len(grid[0])):
		if check_horizontal_symmetry(grid, x):
			return x
	
	for y in range(1, len(grid)):
		if check_vertical_symmetry(grid, y):
			return 100*y
	return 0

result = sum(find_symmetry(grid) for grid in grids)
print(f"Part 1: The summarized value is: {result}")

# Part 2: Every mirror now has a smudge -- an error that flips a single value from '#' to '.' or
# vice-versa. Fixing the error creates a different line of symmetry. Repeat the above process, but
# find the new lines of symmetry by fixing the smudges. The grids are fairly small, so I think we
# should be able to try flipping one symbol at a time. The tricky part is that the old line of
# symmetry may still be valid, and we have to ignore them.
def find_selective_symmetry(grid: list, reject_symmetry: int = 0):
	for x in range(1, len(grid[0])):
		if x != reject_symmetry % 100 and check_horizontal_symmetry(grid, x):
			return x
	
	for y in range(1, len(grid)):
		if y != reject_symmetry // 100 and check_vertical_symmetry(grid, y):
			return 100*y
	return 0

def find_new_symmetry(grid: list):
	g = [list(s) for s in grid]
	old_symmetry = find_symmetry(g)

	for x in range(len(g[0])):
		for y in range(len(g)):
			c = g[y][x]
			g[y][x] = '.' if c == '#' else '#'
			
			symmetry = find_selective_symmetry(g, old_symmetry)
			if symmetry > 0:
				return symmetry
			g[y][x] = c

result = sum(find_new_symmetry(grid) for grid in grids)
print(f"Part 2: The summarized value is: {result}")






