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

# Process the input. There's an initial list of seeds along with a collection of multi-line maps.
# The maps all have names but they're basically an order, so we don't need to worry about them.
input_blocks = input_text.split('\n\n')
seeds = [int(n) for n in re.findall(r'\d+', input_blocks[0])]

print(input_lines)
