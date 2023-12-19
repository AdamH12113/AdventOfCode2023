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

# Process the input. Each line consists of A) a sequence of characters representing springs that
# are operational ('.'), damaged ('#'), or in an unknown state ('?'); and B) a list of numbers
# giving the size of each contiguous group of damaged springs.
input_lines = input_text.split('\n')
records = [line.split(' ')[0] for line in input_lines]
group_sizes = [[int(n) for n in line.split(' ')[1].split(',')] for line in input_lines]

# Part 1: For each record, find the number of possible arrangements of damaged springs that could
# produce the given group sizes. What is the sum of those counts? It looks like there aren't any
# more than about 16 unknown springs per group, so I think brute force will suffice for part 1. No
# sense in trying to optimize until part 2 is visible.
def record_combinations(record: str):
	num_unknown = sum(1 for s in record if s == '?')
	unknown_positions = [n for n in range(len(record)) if record[n] == '?']

	for c in range(2**num_unknown):
		combo = list(record)
		for n in range(num_unknown):
			combo[unknown_positions[n]] = '#' if c & (1 << n) else '.'
		yield ''.join(combo)

def matches_groups(record: str, groups: list):
	damaged_sets = [len(c) for c in filter(None, record.split('.'))]
	if len(damaged_sets) != len(groups):
		return False
	return all(damaged_sets[n] == groups[n] for n in range(max(len(groups), len(damaged_sets))))

def count_valid_combinations(record: str, groups: list):
	num_valid_combos = 0
	for combo in record_combinations(record):
		if matches_groups(combo, groups):
			num_valid_combos += 1
	return num_valid_combos

#total_valid_combos = sum(count_valid_combinations(records[n], group_sizes[n]) for n in range(len(records)))
#print(f"Part 1: The total count of valid arrangements is: {total_valid_combos}")

# Part 2: Replace each record and group size list with five concatenated copies of itself. Yeah,
# I had a feeling... Well, there's no way we're going to iterate over 60 bits of possibilities, so
# we need a log(n) algorithm. That's a lot to ask from a poor EE... maybe some sort of greedy search
# where we handle one group of ?s at a time? Still a lot, but at least it maxes out a millions of
# combinations instead of billions.




for n in range(len(records)):
	new_record = records[n] + '?' + records[n] + '?' + records[n] + '?' + records[n] + '?' + records[n]
	new_group_sizes = group_sizes[n] * 5
