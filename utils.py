from reliability.Reliability_testing import two_proportion_test


def get_a(deck):
	return round(deck['wr'] * deck['matches'] * 0.0001)

def get_win_lose(deck_one, deck_two):
	if deck_one['wr'] > deck_two['wr']:
		win, lose = deck_one['name'], deck_two['name']
	elif deck_one['wr'] == deck_two['wr']:
		if deck_one['matches'] > deck_two['matches']:
			win, lose = deck_one['name'], deck_two['name']
		else:
			win, lose = deck_two['name'], deck_one['name']
	else:
		win, lose = deck_two['name'], deck_one['name']
	return win, lose
	
def check_reliable(deck_one, deck_two):
	reliable = "non-significant"
	ci = 0.99
	while reliable != "significant" and ci > 0.5:
		result = two_proportion_test(
			sample_1_trials=deck_one['matches'],
			sample_1_successes=get_a(deck_one),
			sample_2_trials=deck_two['matches'],
			sample_2_successes=get_a(deck_two),
			CI=ci,
			print_results=False
		)
		reliable = result[2]
		ci -= 0.01
	win, lose = get_win_lose(deck_one, deck_two)
	return win, lose, ci*100
	
def validate_deck(deck):
	if deck['wr'] < 0:
		return False
	if deck['matches'] < 0:
		return False
	return True