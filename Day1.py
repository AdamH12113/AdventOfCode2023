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

# Process the input. It's just lines of text.
input_lines = input_text.split('\n')

# Part 1: What is the sum of all of the calibration values? The calibration value for a line
# is the combination of the first and last numerical digit in the line. Note that there may only be
# one digit!
input_line_digits = [re.findall(r'\d', line) for line in input_lines]
calibration_values = [int(digits[0] + digits[-1]) for digits in input_line_digits if len(digits) >= 1]
print(f"Part 1: The sum of the calibration values is: {sum(calibration_values)}")

# Part 2: In addition to numerical digits, we can now have numbers spelled out ("one", "two", etc.).
# What is the sum of the calibration values now? Since a spelled-out number will never contain a digit,
# we can tokenize the lines into digits and strings of letters. Tokenization is done via REs using a
# modified method from: https://stackoverflow.com/a/70979561/5220760
number_match = r'(?=(\d|zero|one|two|three|four|five|six|seven|eight|nine))'
input_line_numbers = [re.findall(number_match, line) for line in input_lines]

number_lookup = {'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}
calibration_strings = [number_lookup.get(numbers[0], numbers[0]) + number_lookup.get(numbers[-1], numbers[-1]) for numbers in input_line_numbers]
calibration_values = [int(cal_str) for cal_str in calibration_strings]
print(f"Part 2: The sum of the calibration values is: {sum(calibration_values)}")
