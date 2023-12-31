import re, sys, math

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

# Process the input. The first line has a list of left and right instructions on it, while the
# remaining lines describe a binary tree-like structure.
input_lines = input_text.split('\n')
instructions = input_lines[0]
tree = {}
for line in input_lines[2:]:
	nodes = re.findall(r'[A-Z0-9]+', line)
	tree[nodes[0]] = (nodes[1], nodes[2])

# Part 1: How many steps does it take to get from node AAA to node ZZZ?

step = 0
node = 'AAA'
while True:
	next_instruction = instructions[step % len(instructions)]
	choice = 0 if next_instruction == 'L' else 1
	node = tree[node][choice]
	step += 1
	if node == 'ZZZ':
		break

print(f"Part 1: The number of steps needed to reach ZZZ is: {step}")

# Part 2: Now we have to start at every node whose name ends with A, step through the tree along
# each path simultaneously, and stop only when every path hits a node whose name ends with Z at the
# same time. This will probably take a *very* long time, but I'm guessing the paths will cycle
# through Z nodes at regular intervals. If I can find what those intervals are, I can compute a
# least common multiple for the solution. 
nodes = [node for node in tree if node[2] == 'A']
z_times = [0] * len(nodes)
step = 0
while True:
	next_instruction = instructions[step % len(instructions)]
	choice = 0 if next_instruction == 'L' else 1;
	for n in range(len(nodes)):
		nodes[n] = tree[nodes[n]][choice]
	step += 1
	
	# Turns out that the first cycle is as long as the rest, so I don't even have to wait for the
	# process to stabilize.
	for n in range(len(nodes)):
		if nodes[n][2] == 'Z':
			z_times[n] = step
	if all(zt != 0 for zt in z_times):
		break

needed_steps = math.lcm(*z_times)
print(f"Part 2: The number of steps needed for all paths to reach a node ending in Z is: {needed_steps}")
