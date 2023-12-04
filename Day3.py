import re, sys

# Read the input
try:
	day_num = int(re.findall(r'\d+', __file__)[-1])
	filename_base = 'Example' if '--example' in sys.argv else 'Input'
	filename = filename_base + str(day_num) + '.txt'
	with open(filename, 'rt') as f:
		input_text = f.read()[:-1]
except Exception as e:
	print(f"Error reading input: [{exception.__class__.__name__}] {exception}")

# Process the input. It's a 2-D text grid containing (horizontal) numbers and punctuations marks,
# with periods used as spacers. We'll strip out the periods to make identifying punctuation easier.
input_lines = input_text.replace('.', ' ').split('\n')
schematic = input_lines
max_y = len(schematic) - 1
max_x = len(schematic[0]) - 1

# Part 1: If any number adjacent to a punctuation mark (even diagonally) is a part number, what is
# the sum of all of the part numbers? Let's find the coordinates, length, and bounding box of each
# number to aid in our search. Note that there *are* duplicate numbers in the real input!
all_numbers = []
for y in range(max_y + 1):
	for match in re.finditer(r'\d+', input_lines[y]):
		num = int(match[0])
		x = match.start()
		length = match.end() - x
		all_numbers.append({'number': num, 'x': x, 'y': y, 'len': length})

# Check the bounding box around the number for punctuation characters
def is_punctuation(x, y):
	if x >= 0 and x <= max_x and y >= 0 and y <= max_y:
		char = schematic[y][x]
		return not (char.isdigit() or char == ' ')
	else:
		return False

def has_adjacent_punctuation(number: dict):
	bbxi = number['x'] - 1
	bbxf = number['x'] + number['len']
	bbyi = number['y'] - 1
	bbyf = number['y'] + 1
	for y in (bbyi, bbyf):
		for x in range(bbxi, bbxf + 1):
			if is_punctuation(x, y):
				return True
	if is_punctuation(bbxi, number['y']):
		return True
	if is_punctuation(bbxf, number['y']):
		return True
	return False

sum_part_numbers = sum(number['number'] for number in all_numbers if has_adjacent_punctuation(number))
print(f"Part 1: The sum of the part numbers is: {sum_part_numbers}")

# Part 2: A gear is any * with exactly two adjacent numbers. If the "gear ratio" is the product of
# those two numbers, what is the sum of all gear ratios in the schematic? Time for more regexes!
def match_is_adjacent(match: re.Match, x):
	st = match.start()
	ed = match.end() - 1
	return (st >= x - 1 and st <= x + 1) or (ed >= x - 1 and ed <= x + 1)
	
def find_adjacent_numbers(x, y):
	nums = []
	if y >= 1:
		for match in re.finditer(r'\d+', input_lines[y-1]):
			if match_is_adjacent(match, x):
				nums.append(int(match[0]))
	if y < max_y:
		for match in re.finditer(r'\d+', input_lines[y+1]):
			if match_is_adjacent(match, x):
				nums.append(int(match[0]))
	for match in re.finditer(r'\d+', input_lines[y]):
		if match_is_adjacent(match, x):
			nums.append(int(match[0]))
	return nums

ratios = []
for y in range(max_y + 1):
	for x in range(max_x + 1):
		if schematic[y][x] == '*':
			adjacent = find_adjacent_numbers(x, y)
			if len(adjacent) == 2:
				ratios.append(adjacent[0] * adjacent[1])
print(f"Part 2: The sum of the gear ratios is: {sum(ratios)}")
