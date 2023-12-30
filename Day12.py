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
# combinations instead of billions. The internet suggests using the size of the gaps between the
# groups as a variable. Let's try a recursive solution using that. Turns out I need memorization
# (I refuse to call it "memoization") to get usable performance.
memo = {}
def count_valid_combos(rem_rec: str, rem_groups: tuple, depth: int):
	key = (rem_rec, rem_groups, depth)
	if key in memo:
		return memo[key]

	if len(rem_groups) == 0:
		return 0 if '#' in rem_rec else 1
	else:
		valid_gaps = []
		for gap in range(0 if (depth == 0 or len(rem_groups) == 0) else 1, 100):
			doable = len(rem_rec) >= gap and '#' not in rem_rec[:gap]
			if doable:
				valid_gaps.append(gap)

		valid_combos = 0
		for gap in valid_gaps:
			gap_rec = rem_rec[gap:]
			doable = len(gap_rec) >= rem_groups[0] and '.' not in gap_rec[:rem_groups[0]]
			if doable:
				valid_combos += count_valid_combos(gap_rec[rem_groups[0]:], rem_groups[1:], depth + 1)
		memo[key] = valid_combos
		return valid_combos

# Might as well redo part 1 here; it runs much faster
total_valid_combos = 0
for n in range(len(records)):
	total_valid_combos += count_valid_combos(records[n], tuple(group_sizes[n]), 0)
print(f"Part 1: The total count of valid arrangements is: {total_valid_combos}")

# Let's finish this off. Takes about 3 seconds to run.
total_valid_combos = 0
for n in range(len(records)):
	new_record = records[n] + '?' + records[n] + '?' + records[n] + '?' + records[n] + '?' + records[n]
	new_group_sizes = group_sizes[n] * 5
	total_valid_combos += count_valid_combos(new_record, tuple(new_group_sizes), 0)
print(f"Part 2: The total count of valid arrangements is: {total_valid_combos}")
