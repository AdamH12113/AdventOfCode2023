import re, sys, copy
from collections import namedtuple

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

# Process the input. We have a collection of "workflows" (instructions for routing parts) and a
# collection of part ratings. Each part is rated in four categories, "x", "m", "a", and "s".
(workflow_lines, ratings_lines) = (t.split('\n') for t in input_text.split('\n\n'))

Rating = namedtuple('Rating', ['x', 'm', 'a', 's'])
ratings = []
for line in ratings_lines:
	m = re.match(r'{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}', line)
	ratings.append(Rating(int(m[1]), int(m[2]), int(m[3]), int(m[4])))

# Just for fun, let's use functional programming!
workflows = {}
for line in workflow_lines:
	bkt = line.index('{')
	name = line[:bkt]
	instructions = line[bkt+1:-1].split(',')
	inst_funcs = []
	for inst in instructions[:-1]:
		stat = inst[0]
		oper = inst[1]
		level = int(re.findall(r'\d+', inst)[0])
		target = inst[inst.index(':')+1:]
		
		# Turns out Python is really picky about the way it captures values for closures. To avoid
		# overwriting values used by existing lambdas, we need to create extra parameters with
		# default values and bind our values to those defaults. Yeesh.
		if oper == '<':
			inst_funcs.append(lambda rating, target=target, stat=stat, level=level: target if rating.__getattribute__(stat) < level else None)
		elif oper == '>':
			inst_funcs.append(lambda rating, target=target, stat=stat, level=level: target if rating.__getattribute__(stat) > level else None)
	inst_funcs.append(lambda rating, target=instructions[-1]: target)
	workflows[name] = inst_funcs

# Part 1: Run each part through the workflows until it is either accepted or rejected. What is the
# sum of the ratings of all of the accepted parts?
def do_workflow(workflow: list, rating: Rating):
	for f in workflow:
		result = f(rating)
		if result is not None:
			return result
	raise ValueError(f"Bad result for rating {rating}")

def score(rating: Rating):
	return rating.x + rating.m + rating.a + rating.s

sum_scores = 0
for rating in ratings:
	wf = 'in'
	while wf != 'A' and wf != 'R':
		wf = do_workflow(workflows[wf], rating)
	if wf == 'A':
		sum_scores += score(rating)
print(f"Part 1: The sum of the ratings of the accepted parts is: {sum_scores}")

# Part 2: Forget the part list. Each of the four ratings can have a value between 1 and 4000. How
# many combinations of ratings will be accepted? Sheesh, I was hoping for an easy puzzle today...
# Time for some recursion! We'll need to reprocess the rules, too, since the functional approach is
# (not unexpectedly) entirely wrong for this part.
Rule = namedtuple('Rule', ['stat', 'oper', 'level', 'target'])
workflows: dict[str, Rule] = {}
for line in workflow_lines:
	bkt = line.index('{')
	name = line[:bkt]
	instructions = line[bkt+1:-1].split(',')
	inst_rules = []
	for inst in instructions[:-1]:
		stat = inst[0]
		oper = inst[1]
		level = int(re.findall(r'\d+', inst)[0])
		target = inst[inst.index(':')+1:]
		inst_rules.append(Rule(stat, oper, level, target))
	inst_rules.append(Rule('', 'default', '', instructions[-1]))
	workflows[name] = inst_rules

# Each rule affects one stat and only ever shrinks its range (i.e. never splits it into two ranges).
# This makes the ranges fairly easy to represent.
Range = namedtuple('Range', ['low', 'high'])
Ranges = namedtuple('Ranges', ['x', 'm', 'a', 's'])

def range_size(range: Range):
	return 1 + range.high - range.low

def ranges_combos(ranges: Ranges):
	return range_size(ranges.x) * range_size(ranges.m) * range_size(ranges.a) * range_size(ranges.s)

def split_range(range: Range, oper: str, level: int):
	if oper == '<':
		if range.low >= level:
			return None, range
		elif range.high < level:
			return range, None
		else:
			return Range(range.low, level - 1), Range(level, range.high)
	else:
		if range.high <= level:
			return None, range
		elif range.low > level:
			return range, None
		else:
			return Range(level + 1, range.high), Range(range.low, level)

def update_ranges(stat: str, new_range: Range, ranges: Ranges):
	return Ranges(
		x = ranges.x if stat != 'x' else new_range,
		m = ranges.m if stat != 'm' else new_range,
		a = ranges.a if stat != 'a' else new_range,
		s = ranges.s if stat != 's' else new_range)

def count_valid_combos(workflow: str, ranges: Ranges):
	if workflow == 'A':
		return ranges_combos(ranges)
	elif workflow == 'R':
		return 0
	else:
		valid_combos = 0
		for rule in workflows[workflow]:
			if rule.oper == 'default':
				valid_combos += count_valid_combos(rule.target, ranges)
			else:
				stat_range = ranges.__getattribute__(rule.stat)
				in_range, out_range = split_range(stat_range, rule.oper, rule.level)
				if in_range is not None:
					valid_combos += count_valid_combos(rule.target, update_ranges(rule.stat, in_range, ranges))
				if out_range is None:
					break
				else:
					ranges = update_ranges(rule.stat, out_range, ranges)
		return valid_combos

start_ranges = Ranges(Range(1, 4000), Range(1, 4000), Range(1, 4000), Range(1, 4000))
num_valid_combos = count_valid_combos('in', start_ranges)
print(f"Part 2: The number of accepted rating combinations is: {num_valid_combos}")
