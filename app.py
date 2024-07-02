from flask import Flask, render_template, request, url_for, flash
from utils import check_reliable, validate_deck
import secrets


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route("/")
def index():
    return render_template('index.html')
	
@app.route("/deck_touch", methods=('GET', 'POST'))
def deck_touch():
	if request.method == 'POST':
		name_one = request.form['name1'] if request.form['name1'] else "Deck 1"
		matches_one = int(request.form['matches1'])
		wr_one = int(request.form['wr1'])
		name_two = request.form['name2'] if request.form['name2'] else "Deck 2"
		matches_two = int(request.form['matches2'])
		wr_two = int(request.form['wr2'])
		deck_one = {'name': name_one, 'matches': matches_one, 'wr': wr_one}
		deck_two = {'name': name_two, 'matches': matches_two, 'wr': wr_two}
		if validate_deck(deck_one) and validate_deck(deck_one):
			win, lose, error = check_reliable(deck_one, deck_two)
			if int(error) == 49:
				msg = f"Nope, can't be sure of anything."
			else:
				msg = f"Sure, {win} looks better than {lose}... but there is a {round(100-error,2)}% chance you're wrong."
		else:
			msg = "Bad input"
		flash(msg)
		
	return render_template('deck_touch.html')
	
@app.route("/two_tap", methods=('GET', 'POST'))
def two_tap():
	if request.method == 'POST':
		...
	
	return render_template('two_tap.html')
