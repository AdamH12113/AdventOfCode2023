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

# Process the input. Each line is a single numbered scratchcard listing winning numbers followed by
# numbers we have.
input_lines = input_text.split('\n')
num_games = len(input_lines)
winning_numbers = []
numbers_we_have = []
for line in input_lines:
	winning_numbers_text = line.split(': ')[1].split(' |')[0]
	numbers_we_have_text = line.split(' |')[1]
	winning_numbers_list = [int(n) for n in re.findall(r'\d+', winning_numbers_text)]
	numbers_we_have_list = [int(n) for n in re.findall(r'\d+', numbers_we_have_text)]
	winning_numbers.append(winning_numbers_list)
	numbers_we_have.append(numbers_we_have_list)

# Part 1: Find how many winning numbers we have in each game. The score for each game is one for
# the first winning number and doubles for each extra winning number. What is the total point score?
total_score = 0
for game in range(num_games):
	num_matches = sum(1 for n in numbers_we_have[game] if n in winning_numbers[game])
	total_score += int(2**(num_matches - 1))
print(f"Part 1: The total point value of the cards is: {total_score}")

# Part 2: Winning numbers now cause us to win copies of scratchcards. The number of matches gives
# the number of copies, and copies from from the cards further down the list. How many total
# scratchcards do we end up with? This looks simple but the number of cards to process grows
# quadratically, so we need to save our results.
cards_won_cache = {}

def count_cards_won(card: int) -> int:
	if card in cards_won_cache:
		return cards_won_cache[card]

	num_wins = 0
	num_matches = sum(1 for n in numbers_we_have[card] if n in winning_numbers[card])
	num_wins += num_matches
	for n in range(card + 1, card + 1 + num_matches):
		num_wins += cards_won_cache[n] if n in cards_won_cache else count_cards_won(n)
	cards_won_cache[card] = num_wins
	return num_wins

card_queue = list(reversed(range(num_games)))
total_cards_won = sum(count_cards_won(card) for card in card_queue)
print(f"Part 2: The number of scratchcards we end up with is: {total_cards_won + num_games}")
