import re, sys

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

# Process the input. There's an initial list of seeds along with a collection of multi-line maps.
# The maps all have names but they're basically an order, so we don't need to worry about them.
input_blocks = input_text.split('\n\n')
seeds = [int(n) for n in re.findall(r'\d+', input_blocks[0])]

maps = []
for block in range(1, len(input_blocks)):
	maps.append([])
	lines = input_blocks[block].split('\n')[1:]
	for line in lines:
		nums = [int(n) for n in re.findall(r'\d+', line)]
		maps[block - 1].append({'dest': nums[0], 'src': nums[1], 'range': nums[2]})

def do_mapping(value, maps):
	for map in maps:
		if value >= map['src'] and value <= map['src'] + map['range']:
			return map['dest'] + (value - map['src'])
	return value

mapped_values = seeds
for vmap in maps:
	mfunc = lambda value: do_mapping(value, vmap)
	mapped_values = list(map(mfunc, mapped_values))
print(f"Part 1: The lowest location value is: {min(mapped_values)}")

# Part 2: The seed numbers now describe ranges. Each pair of numbers represents a starting value
# and a range. The real input represents billions of seeds. This cannot be brute-forced.











