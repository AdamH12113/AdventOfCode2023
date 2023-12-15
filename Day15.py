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

# Process the input. It's a sequence of small strings ("steps") separated by commas on one line.
steps = input_text.split(',')

# Part 1: To hash a string, start with a value of zero, then, for each character:
#   1. Add the ASCII code of that character to the current value.
#   2. Multiply the current value by 17.
#   3. Set the current value to itself modulo 256.
# What is the sum of the hash values of each step?
def hash_step(step: str):
	val = 0
	for c in step:
		val += ord(c)
		val = (val * 17) % 256
	return val

result = sum(hash_step(step) for step in steps)
print(f"Part 1: The sum of the results is {result}")

# Part 2: We now have an elaborate procedure for putting labeled lenses in boxes using the steps in
# the input. There are 256 boxes, and the hash value of a label tells us which box it's targeting.
# Each box has slots for multiple lenses of different focal lengths. Our two basic operations are
# inserting and removing lenses.
boxes = [[] for n in range(256)]     # Note that [[]] * 256 would copy by reference

# We'll encode the lenses as tuples containing the label and focal length
def find_lens_in_box(box: list, label: str):
	for n in range(len(box)):
		if box[n][0] == label:
			return n
	return -1

def add_lens(box: list, label: str, focal_length: int):
	current_location = find_lens_in_box(box, label)
	if current_location == -1:
		box.append((label, focal_length))
	else:
		box[current_location] = (label, focal_length)

def remove_lens(box: list, label: str):
	current_location = find_lens_in_box(box, label)
	if current_location != -1:
		del box[current_location]

def do_step(boxes: list, step: str):
	parts = re.split(r'[\-\=]', step)
	label = parts[0]
	focal_length = int(parts[1]) if len(parts[1]) > 0 else 0
	box_num = hash_step(label)

	if '-' in step:
		remove_lens(boxes[box_num], label)
	else:
		add_lens(boxes[box_num], label, focal_length)

# Carry out the steps
for step in steps:
	do_step(boxes, step)

# The focusing power of a lens is defined as the product of (1 + box number), (1 + lens slot number),
# and the focal length of the lens. What is the sum of the focusing powers of all of the lenses?
total_focusing_power = 0
for box_num in range(len(boxes)):
	for slot in range(len(boxes[box_num])):
		fp = (1 + box_num) * (1 + slot) * boxes[box_num][slot][1]
		total_focusing_power += fp

print(f"Part 2: The total focusing power is: {total_focusing_power}")


