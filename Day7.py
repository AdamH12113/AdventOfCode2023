import re, sys, math
from functools import cmp_to_key

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

# Process the input. Each line is one Camel Cards hand and a numerical bid
input_lines = input_text.split('\n')
hands = {}
for line in input_lines:
	s = line.split(' ')
	hands[s[0]] = int(s[1])

# Part 1: Sort the hands according to strength. If the rank of a hand is its order in this list,
# what is the sum of the products of each hand's rank and bid? Our main goal here is to implement
# a comparison function for hands. I have a feeling this is going to need to be efficient for part
# 2, but let's worry about that later.
def count_cards(hand: str):
	counts = {}
	for card in hand:
		if card in counts:
			counts[card] += 1
		else:
			counts[card] = 1
	return counts

# Hand type strength stored as a number from 0 to 6, where 0 is high card and 6 is five of a kind.
def find_hand_type(hand: str):
	card_counts = count_cards(hand)
	count_nums = list(card_counts.values())
	max_same_card = max(count_nums)
	if max_same_card == 5:
		return 6             # Five of a kind
	elif max_same_card == 4:
		return 5             # Four of a kind
	elif max_same_card == 3:
		if 2 in count_nums:
			return 4         # Full house
		else:
			return 3         # Three of a kind
	elif max_same_card == 2:
		if count_nums == [2,2,1] or count_nums == [2,1,2] or count_nums == [1,2,2]:
			return 2         # Two pairs
		else:
			return 1         # One pair
	else:
		return 0             # High card

# Returns 1 if hand1 has a higher card than hand2, -1 if the reverse, or 0 if they're equal.
# (The hands will never actually be equal, but it's a very easily case to handle.)
def compare_hand_values(hand1: str, hand2: str):
	face_card_values = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
	for c in range(len(hand1)):
		card1_value = int(hand1[c]) if hand1[c].isdigit() else face_card_values[hand1[c]]
		card2_value = int(hand2[c]) if hand2[c].isdigit() else face_card_values[hand2[c]]
		if card1_value > card2_value:
			return 1
		elif card2_value > card1_value:
			return -1
	return 0

# Returns 1 if hand1 beats hand2, -1 if hand2 beats hand1, or 0 if they're a tie (i.e. identical)
def compare_hands(hand1: str, hand2: str):
	hand1_type = find_hand_type(hand1)
	hand2_type = find_hand_type(hand2)
	if hand1_type != hand2_type:
		return 1 if hand1_type > hand2_type else -1
	else:
		return compare_hand_values(hand1, hand2)

sorted_hands = sorted(list(hands), key=cmp_to_key(compare_hands))
total_winnings = sum((h + 1) * hands[sorted_hands[h]] for h in range(len(sorted_hands)))
print(f"Part 1: The total winnings are: {total_winnings}")

# Part 2: J cards are now jokers, which act as wild cards for determining the hand type but have
# lowest possible card values. For the hand type, we can add the joker count to the highest card
# count in the rest of the hand. (We have to handle the case of an all-joker hand, of course!)
def find_joker_hand_type(hand: str):
	# We remove the joker count from the rest of the card counts to minimze changes to the rest
	# of the function.
	card_counts = count_cards(hand)
	if 'J' in card_counts:
		joker_count = card_counts['J']
		del card_counts['J']
	else:
		joker_count = 0
	
	# Special case for a hand containing only jokers
	if joker_count == 5:
		return 6                # Five of a kind
	
	# Add the jokers to the highest card count
	max_same_card = max(card_counts.values())
	for card in card_counts:
		if card_counts[card] == max_same_card:
			card_counts[card] += joker_count
			max_same_card += joker_count
			break
	count_nums = list(card_counts.values())
	
	if max_same_card == 5:
		return 6                # Five of a kind
	elif max_same_card == 4:
		return 5                # Four of a kind
	elif max_same_card == 3:
		if 2 in count_nums:
			return 4         # Full house
		else:
			return 3         # Three of a kind
	elif max_same_card == 2:
		# A joker always turns one pair into three of a kind, so the count numbers for two pairs
		# are unchanged.
		if count_nums == [2,2,1] or count_nums == [2,1,2] or count_nums == [1,2,2]:
			return 2         # Two pairs
		else:
			return 1         # One pair
	else:
		return 0             # High card

# This is just a simple change to the look-up table
def compare_joker_hand_values(hand1: str, hand2: str):
	face_card_values = {'J': 1, 'T': 10, 'Q': 12, 'K': 13, 'A': 14}
	for c in range(len(hand1)):
		card1_value = int(hand1[c]) if hand1[c].isdigit() else face_card_values[hand1[c]]
		card2_value = int(hand2[c]) if hand2[c].isdigit() else face_card_values[hand2[c]]
		if card1_value > card2_value:
			return 1
		elif card2_value > card1_value:
			return -1
	return 0

# Unchanged from part 1 except for function calls. Could've monkey-patched, I guess.
def compare_joker_hands(hand1: str, hand2: str):
	hand1_type = find_joker_hand_type(hand1)
	hand2_type = find_joker_hand_type(hand2)
	if hand1_type != hand2_type:
		return 1 if hand1_type > hand2_type else -1
	else:
		return compare_joker_hand_values(hand1, hand2)

sorted_hands = sorted(list(hands), key=cmp_to_key(compare_joker_hands))
total_winnings = sum((h + 1) * hands[sorted_hands[h]] for h in range(len(sorted_hands)))
print(f"Part 2: The total winnings are: {total_winnings}")
