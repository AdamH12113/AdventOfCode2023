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

# Process the input. Each line is a single numbered game consisting of multiple sets of colored
# cube quantities delimited by commas (for the quantities) and semicolons (for the sets).
def round_text_to_tuple(round_text: str):
	red_match = re.search(r'(\d+) red', round_text)
	red = int(red_match[1]) if red_match else 0
	green_match = re.search(r'(\d+) green', round_text)
	green = int(green_match[1]) if green_match else 0
	blue_match = re.search(r'(\d+) blue', round_text)
	blue = int(blue_match[1]) if blue_match else 0
	return (red, green, blue)


input_lines = input_text.split('\n')
games = []
for line in input_lines:
	rounds_text = line.split(':')[1].split('; ')
	rounds = [round_text_to_tuple(round) for round in rounds_text]
	games.append(rounds)

# Part 1: Which games would have been possible if the bag had been loaded with only 12 red cubes,
# 13 green cubes, and 14 blue cubes? What is the sum of the ID numbers of those games?
sum_ids = 0
for n in range(len(games)):
	fail = False
	for round in games[n]:
		if round[0] > 12 or round[1] > 13 or round[2] > 14:
			fail = True
	if not fail:
		sum_ids += n + 1
print(f"Part 1: The sum of the IDs of the valid games is: {sum_ids}")

# Part 2: What is the fewest number of cubes of each color that could have produced each game?
# If the "power" of a set of cubes is defined as the product of the minimum red, green, and blue
# cubes, what is the sum of the powers of each game?
sum_powers = 0
for game in games:
	max_red = max(round[0] for round in game)
	max_green = max(round[1] for round in game)
	max_blue = max(round[2] for round in game)
	power = max_red * max_green * max_blue
	sum_powers += power
print(f"Part 2: The sum of the power of each game is: {sum_powers}")

