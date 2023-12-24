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

# Process the input. We have a description of a digital machine, with each line describing the
# outputs of a flip-flop module ('%'), a conjunction module ('&'), or the broadcaster ('broadcaster').
# We need to know how many inputs each conjunction module has, so the processing is a bit complicated.
# We have to keep track of high and low pulses. Let's use True and False for those.
input_lines = input_text.split('\n')

class Broadcast:
	def __init__(self, targets: list):
		self.targets = targets

	def receive_pulse(self, input_name: str, state: bool) -> bool:
		return state

	def __str__(self):
		return f"Broadcaster -> {self.targets}"

class FlipFlop:
	def __init__(self, name: str, targets: list):
		self.name = name
		self.targets = targets
		self.state = False

	def receive_pulse(self, input_name: str, state: bool) -> bool:
		if state:
			return None
		else:
			self.state = not self.state
			return self.state

	def __str__(self):
		return f"FlipFlop {self.name} -> {self.targets}"

class Conjunction:
	def __init__(self, name: str, targets: list):
		self.name = name
		self.targets = targets
		self.inputs = {}

	def add_input(self, input_name: str):
		self.inputs[input_name] = False

	def receive_pulse(self, input_name: str, state: bool) -> bool:
		self.inputs[input_name] = state
		return not all(self.inputs.values())

	def __str__(self):
		return f"Conjunction {list(self.inputs)} -> {self.name} -> {self.targets}"

modules = {}
for line in input_lines:
	module_text, targets_text = line.split(' -> ')
	targets = targets_text.split(', ')
	if module_text[0] == '%':
		name = module_text[1:]
		modules[name] = FlipFlop(name, targets)
	elif module_text[0] == '&':
		name = module_text[1:]
		modules[name] = Conjunction(name, targets)
	else:
		modules[module_text] = Broadcast(targets)

conjunction_names = [m for m in modules if type(modules[m]) is Conjunction]
for cn in conjunction_names:
	for m in modules:
		if cn in modules[m].targets:
			modules[cn].add_input(m)

# Part 1: Press the button 1000 times, delivering 1000 low pulses to the broadcaster. What is the
# product of the total number of low and high pulses sent in the system as a result? Note that the
# low pulses from the button to the broadcaster do count.
TargetedPulse = namedtuple('TargetedPulse', ['pulse', 'source', 'target'])

def push_button(modules: dict):
	event_queue = [TargetedPulse(False, 'button', 'broadcaster')]
	high_count = 0
	low_count = 0

	while len(event_queue) > 0:
		pulse, source, target = event_queue.pop()
		if pulse:
			high_count += 1
		else:
			low_count += 1

		# Handle output modules
		if target not in modules:
			continue

		next_pulse = modules[target].receive_pulse(source, pulse)
		#print(f"{source} {pulse} -> {target} becomes {next_pulse}")
		if next_pulse is not None:
			for t in modules[target].targets:
				event_queue.insert(0, TargetedPulse(next_pulse, target, t))

	return high_count, low_count

total_high = 0
total_low = 0
test_modules = copy.deepcopy(modules)
for pushes in range(1000):
	hc, lc = push_button(test_modules)
	total_high += hc
	total_low += lc
print(f"Part 1: There were {total_high} high pulses and {total_low} low pulses for a product of: {total_high * total_low}")

# Part 2: Attach a module named rx. What is the fewest number of button presses required to deliver
# a single low pulse to rx?
class Receiver:
	def __init__(self, name: str):
		self.name = name
		self.activated = False

	def receive_pulse(self, input_name: str, state: bool) -> bool:
		if state == False:
			self.activated = True
		return None

	def __str__(self):
		return f"Receiver {self.name}: {self.activated}"

TargetedPulse = namedtuple('TargetedPulse', ['pulse', 'source', 'targets'])

def push_button(modules: dict, num_pushes: int):
	event_queue = [TargetedPulse(False, 'button', ['broadcaster'])]

	while len(event_queue) > 0:
		pulse, source, targets = event_queue.pop()

		for target in targets:
			# Handle output modules
			if target not in modules:
				continue

			# rx is fed by a single conjunction module called &lx
			if target == 'lx' and pulse == True:
				print(target, pulse, source, num_pushes)

			next_pulse = modules[target].receive_pulse(source, pulse)
			if next_pulse is not None:
				event_queue.insert(0, TargetedPulse(next_pulse, target, modules[target].targets))

# Our target module rx will only get a low pulse when &lx gets high pulses on each of its inputs on
# the same button press. By inspecting the console output, I found that &lx's input modules produce
# high pulses at the following intervals:
#   &cl: 3733
#   &lb: 3911
#   &rp: 4091
#   &nj: 4093
#
# The least common multiple of these intervals is the answer: 244465191362269
modules['rx'] = Receiver('rx')
for pushes in range(1, 13000):
	push_button(modules, pushes)
