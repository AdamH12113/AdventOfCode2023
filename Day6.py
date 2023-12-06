import re, sys, math

# Read the input
try:
	day_num = int(re.findall(r'\d+', __file__)[-1])
	filename_base = 'Example' if '--example' in sys.argv else 'Input'
	filename = filename_base + str(day_num) + '.txt'
	with open(filename, 'rt') as f:
		input_text = f.read()[:-1]
except Exception as e:
	print(f"Error reading input: [{exception.__class__.__name__}] {exception}")

# Process the input. There's a list of times on one line and a list of distances on the other line.
input_lines = input_text.split('\n')
times = [int(n) for n in re.findall(r'\d+', input_lines[0])]
distances = [int(n) for n in re.findall(r'\d+', input_lines[1])]

# Part 1: Holding down the button on the boat increases its speed by 1 mm/ms/ms. How many different
# lengths of time (in integer milliseconds) can we hold down the button in each race and still beat
# the distance record? What is the product of those counts?

# This can be solved mathematically. If the total race time is T and the time to hold the button is h,
# then the distance traveled will be h * (T - h). If the distance record is R, then to win, we must
# satisfy:
#
#   h * (T - h) > R
#
# This gives two crossover points, the roots of the polynomial:
#
#   -h^2 + Th - R = 0
#   h = (-T +/- sqrt(T^2 - 4*-1*-R))/(2*-1)
#   h = T/2 +/- sqrt(T^2 - 4*R)/2
#
# Rounding the first root up and the second root down to the nearest integer gives us the shortest
# and longest times we can hold the button and still win. Note that we do have to *beat* the record,
# so if the root is an integer we need to round up anyway!
win_count_product = 1
for race in range(len(times)):
	T = times[race]
	R = distances[race]
	low_root = T/2 - math.sqrt(T*T - 4*R)/2
	high_root = T/2 + math.sqrt(T*T - 4*R)/2
	min_time = math.floor(low_root + 1)
	max_time = math.ceil(high_root - 1)
	win_count_product *= max_time - min_time + 1
print(f"Part 1: The product of the numbers of ways we can win is: {win_count_product}")

# Part 2: Concatenate the times and distances to produce a single race with huge values. How many
# ways are there to beat the record? We can use the same solution as above.
T = int(''.join(re.findall(r'\d+', input_lines[0])))
R = int(''.join(re.findall(r'\d+', input_lines[1])))
low_root = T/2 - math.sqrt(T*T - 4*R)/2
high_root = T/2 + math.sqrt(T*T - 4*R)/2
min_time = math.floor(low_root + 1)
max_time = math.ceil(high_root - 1)
print(f"Part 2: The number of ways we can win is: {max_time - min_time + 1}")
