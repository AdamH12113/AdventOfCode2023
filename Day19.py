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

# Part 1: Forget the part list. Each of the four ratings can have a value between 1 and 4000. How
# many combinations of ratings will be accepted? Sheesh, I was hoping for an easy puzzle today...








