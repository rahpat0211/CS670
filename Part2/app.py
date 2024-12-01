import os
import json
import logging
from flask import Flask, render_template, request, session, jsonify
from summary_generation import *

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Secret key for session management

# Define the path for the session file
SESSION_FILE = 'session_data.json'


# Function to delete the session file if it exists
def delete_session_file():
	"""
	Deletes the session data file if it exists.
	Useful for clearing stale session data when starting the application.
	"""
	if os.path.exists(SESSION_FILE):
		os.remove(SESSION_FILE)
		logger.info(f"{SESSION_FILE} has been deleted.")


# Call the function to delete the session file at the start
delete_session_file()

solution = gather_solution()  # Initial solution for the game


# Load session data from a file
def load_session():
	"""
	Loads and returns session data from a file if it exists, otherwise returns an empty dictionary.
	"""
	if os.path.exists(SESSION_FILE):
		with open(SESSION_FILE, 'r') as f:
			return json.load(f)
	return {}


# Save session data to a file
def save_session():
	"""
	Saves the current session data to a file for persistence between requests.
	"""
	with open(SESSION_FILE, 'w') as f:
		json.dump(session, f)


@app.route('/refresh-session', methods=['POST'])
def refresh_session():
	"""
	Endpoint to refresh the session, clearing existing data and setting new defaults.
	Responds with a success message in JSON format.
	"""
	session.clear()
	session['new_game'] = 'value'  # Example of setting new session data
	return jsonify({'message': 'Session refreshed successfully.'})


@app.before_request
def initialize_session():
	"""
	Hook to initialize session variables before handling requests.
	Loads session data and sets default values for suggestions, deductions, and attempts.
	"""
	session_data = load_session()
	session['suggestions'] = session_data.get('suggestions', [])
	session['deductions'] = session_data.get('deductions', [])
	session['attempts'] = session_data.get('attempts', 0)


@app.after_request
def after_request(response):
	"""
	Hook to save session data after handling requests.
	Ensures session changes persist across requests.
	"""
	save_session()
	return response


@app.route('/')
def home():
	"""
	Renders the home page of the application, displaying all available characters.
	"""
	all_characters = [character.name for character in characters]
	return render_template('index.html', characters=all_characters)


@app.route('/download-layout', methods=['POST'])
def download_layout():
	"""
	Endpoint to generate and respond with a summary of the solution in JSON format.
	"""
	summary = generate_summary(solution)
	return jsonify(summary=summary)


@app.route('/select-character', methods=['POST'])
def select_character():
	"""
	Endpoint to select a character and store it in the session.
	Renders a template indicating the selected character.
	"""
	selected_character = request.form['character']
	session['selected_character'] = selected_character
	return render_template('select_character.html', character=selected_character)


@app.route('/choose-room', methods=['GET', 'POST'])
def choose_room():
	"""
	Handles the process of selecting a room, either displaying available rooms or processing the selection.
	Stores the selected room in the session.
	"""
	rooms = Mansion().get_rooms()
	selected_character = session.get('selected_character', None)
	
	if request.method == 'POST':
		selected_room = request.form['room']
		session['refute_room'] = selected_room
		weapon = weapons.get(selected_room)
		return render_template('room_selected.html', room=selected_room, character=selected_character,
		                       weapon=weapon)
	
	return render_template('choose_room.html', rooms=rooms)


@app.route('/make-suggestion', methods=['GET'])
def make_suggestion():
	"""
	Displays the suggestion form, allowing the user to select characters, rooms, and weapons.
	"""
	rooms = Mansion().get_rooms()
	all_weapons = list(weapons.values())
	all_characters = [character.name for character in characters]
	return render_template('suggestion.html', characters=all_characters, rooms=rooms, weapons=all_weapons)


@app.route('/submit-suggestion', methods=['POST'])
def submit_suggestion():
	"""
	Processes a submitted suggestion, checks if it matches the solution, and provides feedback including hints.
	"""
	global solution
	character = request.form['character']
	room = request.form['room']
	weapon = request.form['weapon']
	
	suggestion = {'character': character, 'room': room, 'weapon': weapon}
	session['suggestions'].append(suggestion)
	
	if character == solution['character'] and room == solution['room'] and weapon == solution['weapon']:
		message = "Congratulations! Your suggestion is correct."
		correct = True
		session.pop('attempts', None)  # Clear attempts on success
		
		session.clear()
		solution = gather_solution(reinitialize=True)
	
	else:
		attempts = session.get('attempts', 0) + 1
		session['attempts'] = attempts
		logger.info(attempts)
		
		hints = [
			"Hint 1: The correct character is " + solution['character'] + ".",
			"Hint 2: The correct weapon is " + solution['weapon'] + ".",
			"Hint 3: The correct room is " + solution['room'] + "."
		]
		
		if attempts >= 2:
			hint_index = attempts - 2  # Start giving hints from the 2nd retry
			if hint_index < len(hints):
				message = f"Sorry, your suggestion is incorrect. Here is a hint: {hints[hint_index]}"
			else:
				message = "Sorry, your suggestion is incorrect. No more hints available."
		else:
			message = "Sorry, your suggestion is incorrect. Please try again."
		
		correct = False
	
	return jsonify(message=message, correct=correct)


@app.route('/refute-suggestion', methods=['POST'])
def refute_suggestion():
	"""
	Processes a refutation attempt by checking the player's cards against the suggestion,
	returning whether a matching card is held.
	"""
	data = request.get_json()
	suggestion = data['suggestion']
	
	# Get the current player's cards
	player_cards = get_player_cards()  # This function should return the player's cards
	
	matching_card = None
	
	if suggestion['character'] == player_cards['character']:
		matching_card = player_cards['character']
	elif suggestion['room'] == player_cards['room']:
		matching_card = player_cards['room']
	elif suggestion['weapon'] == player_cards['weapon']:
		matching_card = player_cards['weapon']
	
	if matching_card:
		return jsonify(message=f"You refuted the suggestion with: {matching_card}")
	else:
		return jsonify(message="No player currently holds a card that matches the solution.")


@app.route('/save-deductions', methods=['POST'])
def save_deductions():
	"""
	Endpoint to save user deductions to the session.
	Responds with a success message or prompts the user to provide deductions.
	"""
	data = request.json
	deductions = data.get('deductions', '')
	logger.info("Received deductions:", deductions)
	
	if 'deductions' not in session:
		session['deductions'] = []  # Initialize if not present
	
	if deductions:
		session['deductions'].append(deductions)
		session.modified = True  # Mark session as modified
		logger.info("Deductions saved:", session['deductions'])
		return jsonify(message="Deductions saved successfully.")
	else:
		return jsonify(message="No deductions provided.")


@app.route('/view-deductions', methods=['GET'])
def view_deductions():
	"""
	Endpoint to view saved deductions from the session.
	Returns the deductions in JSON format.
	"""
	deductions = session.get('deductions', [])
	logger.info("Deductions being viewed:", deductions)  # Log deductions being viewed
	return jsonify(deductions=deductions)


@app.route('/clear-deductions', methods=['POST'])
def clear_deductions():
	"""
	Endpoint to clear all saved deductions from the session.
	"""
	session.pop('deductions', None)  # Remove deductions from the session
	return jsonify(message="Deductions cleared successfully.")


@app.route('/add-deduction', methods=['POST'])
def add_deduction():
	"""
	Adds a new deduction to the session after cleaning it.
	"""
	data = request.get_json()
	deduction_value = data.get('deduction')
	
	if deduction_value:
		deduction_value = deduction_value.replace("Sorry, your suggestion is incorrect. Here is a hint:", "").strip()
	
	logger.info("Deduction value received:", deduction_value)
	
	if 'deductions' not in session:
		session['deductions'] = []
	
	session['deductions'].append(deduction_value)
	session.modified = True
	
	return jsonify({'message': 'Deduction added successfully!', 'deductions': session['deductions']})


refute_click_count = 0


def get_player_cards():
	"""
	Simulates getting player cards for refutation.
	Ensures player has at least one correct card.
	"""
	global refute_click_count
	characters_copy = characters.copy()
	rooms = session.get('refute_room', None)
	rooms_copy = list(Mansion().get_rooms())
	weapons_copy = list(weapons.values())
	
	if solution['character'] in characters_copy:
		characters_copy.remove(solution['character'])
	if solution['weapon'] in weapons_copy:
		weapons_copy.remove(solution['weapon'])
	
	refute_click_count += 1
	
	player_cards = {'character': solution['character'], 'room': rooms if rooms else None, 'weapon': solution['weapon']}
	
	return player_cards


@app.route('/get-player-cards', methods=['GET'])
def get_player_cards_endpoint():
	"""
	Endpoint to fetch player cards related to the active game session.
	"""
	player_cards = get_player_cards()
	logger.info(player_cards)  # Debugging line to see what is returned
	return jsonify(cards=player_cards)  # Return the player cards as a JSON object


if __name__ == '__main__':
	if os.path.exists('session_data.json'):
		os.remove('session_data.json')
	app.run(debug=True)
