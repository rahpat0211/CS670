import os
import json
from flask import Flask, render_template, request, session, jsonify

from defaults.mansion import *
from defaults.weapons import *
from defaults.characters import *
from defaults.solution import gather_solution
from summary_generation import *

app = Flask(__name__)
app.secret_key = 'niki0211'

# Define the path for the session file
SESSION_FILE = 'session_data.json'


# Function to delete the session file if it exists
def delete_session_file():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        print(f"{SESSION_FILE} has been deleted.")


# Call the function to delete the session file at the start
delete_session_file()

solution = gather_solution()


# Load session data from a file
def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            return json.load(f)
    return {}


# Save session data to a file
def save_session():
    with open(SESSION_FILE, 'w') as f:
        json.dump(session, f)


@app.route('/refresh-session', methods=['POST'])
def refresh_session():
    session.clear()  # Clear the current session
    # Optionally, set new session data here
    session['new_game'] = 'value'  # Example of setting new session data
    return jsonify({'message': 'Session refreshed successfully.'})


# Initialize session variables for suggestions and deductions
@app.before_request
def initialize_session():
    # Load existing session data
    session_data = load_session()
    
    # Initialize session variables
    session['suggestions'] = session_data.get('suggestions', [])
    session['deductions'] = session_data.get('deductions', [])
    session['attempts'] = session_data.get('attempts', 0)


@app.after_request
def after_request(response):
    # Save session data after each request
    save_session()
    return response


@app.route('/')
def home():
    print(solution)
    all_characters = [character.name for character in characters]
    return render_template('index.html', characters=all_characters)


@app.route('/download-layout', methods=['POST'])
def download_layout():
    summary = generate_summary(solution)
    return jsonify(summary=summary)


@app.route('/select-character', methods=['POST'])
def select_character():
    selected_character = request.form['character']
    session['selected_character'] = selected_character
    return render_template('select_character.html', character=selected_character)


@app.route('/choose-room', methods=['GET', 'POST'])
def choose_room():
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
    print(solution)
    rooms = Mansion().get_rooms()
    all_weapons = list(weapons.values())
    all_characters = [character.name for character in characters]
    return render_template('suggestion.html', characters=all_characters, rooms=rooms, weapons=all_weapons)


@app.route('/submit-suggestion', methods=['POST'])
def submit_suggestion():
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
        print(f"New Solution: {solution}")
        
    else:
        attempts = session.get('attempts', 0) + 1
        session['attempts'] = attempts
        print(attempts)
        
        # Prepare hints based on attempts
        hints = [
            "Hint 1: The correct character is " + solution['character'] + ".",
            "Hint 2: The correct weapon is " + solution['weapon'] + ".",
            "Hint 3: The correct room is " + solution['room'] + "."
        ]
        
        if attempts >= 2:
            # Provide a hint based on the number of attempts
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
    data = request.get_json()
    suggestion = data['suggestion']
    
    # Get the current player's cards
    player_cards = get_player_cards()  # This function should return the player's cards
    
    matching_card = None
    
    # Check if the player's cards match the suggestion
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
    data = request.json
    deductions = data.get('deductions', '')
    print("Received deductions:", deductions)

    if 'deductions' not in session:
        session['deductions'] = []  # Initialize if not present

    if deductions:
        session['deductions'].append(deductions)
        session.modified = True  # Mark session as modified
        print("Deductions saved:", session['deductions'])
        return jsonify(message="Deductions saved successfully.")
    else:
        return jsonify(message="No deductions provided.")

@app.route('/view-deductions', methods=['GET'])
def view_deductions():
    deductions = session.get('deductions', [])
    print("Deductions being viewed:", deductions)  # Log deductions being viewed
    return jsonify(deductions=deductions)

@app.route('/clear-deductions', methods=['POST'])
def clear_deductions():
    session.pop('deductions', None)  # Remove deductions from the session
    return jsonify(message="Deductions cleared successfully.")

@app.route('/add-deduction', methods=['POST'])
def add_deduction():
    data = request.get_json()
    deduction_value = data.get('deduction')

    # Strip out the specific phrase if it exists
    if deduction_value:
        deduction_value = deduction_value.replace("Sorry, your suggestion is incorrect. Here is a hint:", "").strip()

    # Log the cleaned deduction value
    print("Deduction value received:", deduction_value)

    # Initialize deductions if not already present
    if 'deductions' not in session:
        session['deductions'] = []

    # Add the cleaned deduction to the list
    session['deductions'].append(deduction_value)
    session.modified = True  # Mark session as modified

    # Return a valid JSON response with the updated deductions
    return jsonify({'message': 'Deduction added successfully!', 'deductions': session['deductions']})

refute_click_count = 0

def get_player_cards():
    global refute_click_count
    characters_copy = characters.copy()
    rooms = session.get('refute_room', None)
    rooms_copy = list(Mansion().get_rooms())
    weapons_copy = list(weapons.values())

    # Ensure at least one part of the solution is within the player's cards
    if solution['character'] in characters_copy:
        characters_copy.remove(solution['character'])
    if solution['weapon'] in weapons_copy:
        weapons_copy.remove(solution['weapon'])

    # Increment the click count
    refute_click_count += 1

    # Randomly select a character and weapon
    player_cards = {'character': solution['character'], 'room': rooms if rooms else None, 'weapon': solution['weapon']}
    
    return player_cards

@app.route('/get-player-cards', methods=['GET'])
def get_player_cards_endpoint():
    player_cards = get_player_cards()  # This function should return the player's cards
    print(player_cards)  # Debugging line to see what is returned
    return jsonify(cards=player_cards)  # Return the player cards as a JSON object

if __name__ == '__main__':
    if os.path.exists('session_data.json'):
        os.remove('session_data.json')
    app.run(debug=True)