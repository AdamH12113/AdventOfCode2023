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

# Process the input. Each line has a history consisting of a list of numbers separated by spaces.
input_lines = input_text.split('\n')
histories = [[int(n) for n in re.findall(r'\-?\d+', line)] for line in input_lines]

# Part 1: Extrapolate the next value in each history by (essentially) computing derivatives until
# I get zeros, then adding another zero to the end of the final derivative and extrapolating upward
# from there. What is the sum of these extrapolated values?
def compute_derivative(sequence: [int]):
	derivative = []
	for n in range(1, len(sequence)):
		derivative.append(sequence[n] - sequence[n-1])
	return derivative

next_values = []
for history in histories:
	derivatives = [history]
	while True:
		derivatives.append(compute_derivative(derivatives[-1]))
		if all(n == 0 for n in derivatives[-1]):
			break
	derivatives[-1].append(0)
	for n in range(len(derivatives)-2, -1, -1):
		derivatives[n].append(derivatives[n][-1] + derivatives[n+1][-1])
	next_values.append(derivatives[0][-1])

print(f"Part 1: The sum of the extrapolated values is {sum(next_values)}")

# Part 2: Using a similar process to the above, extrapolate the previous values in the histories and
# find their sum.
next_values = []
for history in histories:
	derivatives = [history]
	while True:
		derivatives.append(compute_derivative(derivatives[-1]))
		if all(n == 0 for n in derivatives[-1]):
			break
	derivatives[-1].insert(0, 0)
	for n in range(len(derivatives)-2, -1, -1):
		derivatives[n].insert(0, derivatives[n][0] - derivatives[n+1][0])
	next_values.append(derivatives[0][0])

print(f"Part 2: The sum of the extrapolated values is {sum(next_values)}")

