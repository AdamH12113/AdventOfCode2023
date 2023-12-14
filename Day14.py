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

# Process the input. It's (sigh) another 2-D grid. The grid consists of empty space ('.'), cube-
# shaped rocks ('#', and rounded rocks ('O'). We're going to have to move rocks around, so let's
# same some time and convert the strings to lists right away.
grid = [list(line) for line in input_text.split('\n')]
y_size = len(grid)
x_size = len(grid[0])

def print_grid(grid: list):
	print('\n' + '\n'.join(''.join(g) for g in grid))

# Part 1: Tilt the platform so that all rounded rocks roll north (towards y=0). Find the total load
# on the support beams by calculating the distance from the bottom, with the bottommost row being 1.
def roll_rocks_north(grid: list):
	for x in range(x_size):
		northmost = 0
		for y in range(y_size):
			if grid[y][x] == '#':
				northmost = y + 1
			elif grid[y][x] == 'O':
				if y != northmost:
					grid[northmost][x] = 'O'
					grid[y][x] = '.'
				northmost += 1

def calculate_load(grid: list):
	load = 0
	for y in range(y_size):
		for x in range(x_size):
			if grid[y][x] == 'O':
				load += y_size - y
	return load

part1_grid = copy.deepcopy(grid)
roll_rocks_north(part1_grid)
load = calculate_load(part1_grid)
print(f"Part 1: The total load is: {load}")

# Part 2: A spin cycle involves tilting the platform north, then west, then south, then east. What
# is the total load after a billion cycles? I'm guessing there's going to be a repeating pattern.
def roll_rocks_south(grid: list):
	for x in range(x_size):
		southmost = y_size - 1
		for y in range(y_size - 1, -1, -1):
			if grid[y][x] == '#':
				southmost = y - 1
			elif grid[y][x] == 'O':
				if y != southmost:
					grid[southmost][x] = 'O'
					grid[y][x] = '.'
				southmost -= 1

def roll_rocks_west(grid: list):
	for y in range(y_size):
		westmost = 0
		for x in range(x_size):
			if grid[y][x] == '#':
				westmost = x + 1
			elif grid[y][x] == 'O':
				if x != westmost:
					grid[y][westmost] = 'O'
					grid[y][x] = '.'
				westmost += 1

def roll_rocks_east(grid: list):
	for y in range(y_size):
		eastmost = x_size - 1
		for x in range(x_size - 1, -1, -1):
			if grid[y][x] == '#':
				eastmost = x - 1
			elif grid[y][x] == 'O':
				if x != eastmost:
					grid[y][eastmost] = 'O'
					grid[y][x] = '.'
				eastmost -= 1

part2_grid = copy.deepcopy(grid)
for cycle in range(300):
	roll_rocks_north(part2_grid)
	roll_rocks_west(part2_grid)
	roll_rocks_south(part2_grid)
	roll_rocks_east(part2_grid)
	print(f"Cycle {cycle}: {calculate_load(part2_grid)}")

# I solved this part by running until I saw a repeating pattern, then using grep to find the pattern
# period and Excel to do a quick calculation of where in the pattern I needed to look to find the
# answer. Turns out the answer is 93742. I got this by looking at the repeating value 93827, which
# has a period of 51 cycles. Via arithmetic, the same value appears on cycle 999,999,960, which is
# 39 cycles before the end (counting from zero). 93742 is the value that appears 39 cycles after
# 93827, so that's the answer.
