# Import the required libraries after following steps 1 and 2 from RahulPatel_Readme.md

from wsgiref.validate import validator

from defaults.weapons import *
from defaults.mansion import *
from defaults.characters import *
from defaults.solution import *

import pandas as pd
import os
import platform
import logging

# ----------------------------------------------------------------------------------------------------------------------

class ClueGame:
	def __init__(self):
		self.solution = gather_solution() # Generate a dictionary format of the solution
		
		# Set the following to an empty string for the initial selection for the character
		self.selected_character = ''
		self.selected_room = ''
		self.selected_weapon = ''
	
	def summary_generation(self):
		"""
		Generation of a xlsx file that consists of the overall Game Layout. Including a generated solution.
		Don't need to run this if you don't want to see the solution.
		Comment out clue.summary_generation() in clue_game_handler() if you wish to skip this.
		"""
		
		# Directory Validation to store the file
		layout_directory = "Layout"
		if not os.path.exists(layout_directory):
			os.makedirs(layout_directory)
			logging.info(f"Created directory: {layout_directory}")
		
		# Create an empty dataframe for each sheet by creating the columns
		character_sheet = pd.DataFrame(columns=["Character Name", "Starting Position"])
		mansion_sheet = pd.DataFrame(columns=["Rooms"])
		weapons_sheet = pd.DataFrame(columns=["Weapons"])
		solution_sheet = pd.DataFrame(columns=["Character", "Weapon", "Room"])
		
		
		# Population of the Character Sheet
		for character in characters:
			character_sheet = character_sheet._append({
				"Character Name":    character.name,
				"Starting Position": character.position},
				ignore_index=True)
		
		# Population of the Mansion Sheet
		for room in Mansion().get_rooms():
			mansion_sheet = mansion_sheet._append({"Rooms": room}, ignore_index=True)
		
		# Population of the Weapons Sheet
		for tools in list(weapons.values()):
			weapons_sheet = weapons_sheet._append({"Weapons": tools}, ignore_index=True)
		
		# Population of the Solution Sheet
		solution_sheet = solution_sheet._append({
			"Character": self.solution.get('character'),
			"Weapon":    self.solution.get('weapon'),
			"Room":      self.solution.get('room')},
			ignore_index=True)
		
		# Initialize the file name by joining the file name with the parent directory
		file_name = os.path.join(layout_directory, "Game_Set_Up.xlsx")
		try:
			with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
				character_sheet.to_excel(writer, sheet_name='Character Definition', index=False)
				mansion_sheet.to_excel(writer, sheet_name='Mansion Layout', index=False)
				weapons_sheet.to_excel(writer, sheet_name='Weapon Definition', index=False)
				solution_sheet.to_excel(writer, sheet_name='Solution Selection', index=False)
		except PermissionError as PE:
			logging.error(f"Please close the file {file_name} before proceeding")
			exit(1)
		
		print("Opening Game Layout in new window")
		
		# Automatically open the Excel file
		if platform.system() == "Windows":
			os.startfile(file_name)
		elif platform.system() == "Darwin":  # macOS
			os.system(f"open {file_name}")
		else:  # Linux
			os.system(f"xdg-open {file_name}")
	
	def character_selection(self):
		"""
		Selection of a character from a list.
		Validation to ensure the character input is in the list
		Retry mechanism for any typos
		"""
		
		# Dictionary of available characters and their starting position
		info = {character.name: character.position for character in characters}
		
		while True:  # Loop until a valid character is selected
			selected_character = input(f"Please choose a character from this list: {list(info.keys())}: ")
			
			# Validator to ensure character selection is valid
			if selected_character in list(info.keys()):
				selected_room = info.get(selected_character)
				print(f"You have selected: {selected_character}")
				print(f"Starting Room: {selected_room}")
				
				self.selected_character = selected_character  # Return the selected character
				self.selected_room = selected_room
				return
			else:
				# Retrial of character selection if choice is not valid
				print(f"Sorry, '{selected_character}' is not a valid character. Please try again.")
	
	def character_movements(self):
		"""
		Process for the user to choice between moving to rooms or making a suggestion
		Validation for each prompt input
		Retry mechanism for any typos
		"""
		
		def move_room():
			# Moving to a different room
			while True:
				selected_room = input(f"Select a room you would like to move to: {Mansion().get_rooms()}: ")
				
				# Validation check to ensure room selected is within the list
				if selected_room in Mansion().get_rooms():
					print(f"You have selected: {selected_room}")
					self.selected_room = selected_room
					return
				else:
					# Retrial of room selection if choice is not valid
					print(f"Sorry, '{selected_room}' is not a valid room. Please try again.")
		
		def make_suggestion():
			# Making a suggestion based on user inputs of a character, weapon and room
			
			# Information to valid on
			info = {character.name: character.position for character in characters}
			weapon_list = list(weapons.values())
			rooms = Mansion().get_rooms()
			
			def valid_suggestion(character, weapon, room):
				# Check if all parameters match the solution
				if self.solution['character'] == character and \
						self.solution['weapon'] == weapon and \
						self.solution['room'] == room:
					print("Congratulations! Your suggestion is correct!")
					return True
				else:
					# Provide hints based on which parameter is incorrect
					if self.solution['character'] != character:
						print("Wrong Character.")
					if self.solution['weapon'] != weapon:
						print("Wrong Weapon.")
					if self.solution['room'] != room:
						print("Wrong Room.")
					return False
			
			def validator(question, actual):
				# Ensure the input matches that of the validated information
				while True:
					resp = input(question)
					if resp in actual:
						return resp
					else:
						# Retrial of input if the choice is not valid
						print(f"Sorry, your input does not match the records in the system. Please try again.")
			
			attempt = 1
			while attempt <= 5:
				# Get initial suggestions
				target_character = validator(f"Suggest a Character: {list(info.keys())}: ", info)
				target_weapon = validator(f"Suggest a Weapon: {weapon_list}: ", weapon_list)
				target_room = validator(f"Suggest a Room: {rooms}: ", rooms)
				
				# Check the suggestion validity
				result = valid_suggestion(target_character, target_weapon, target_room)
				
				if result is True:
					break  # Correct suggestion, exit the loop
				
				# Ask the user if they want to change rooms or continue retrying the suggestion
				choice = input("Would you like to (1) retry suggestion or (2) change room? Enter 1 or 2: ")
				if choice == '2':
					move_room()  # Call the move room function
					return  # Exit the suggestion loop since the user chose to change rooms
				elif choice == '1':
					# Provide a hint before retrying
					if attempt == 1:
						print("Let's try again! Remember to consider your previous guesses.")
					elif attempt == 2:
						print(f"HINT: The correct Character is '{self.solution['character']}'.")
					elif attempt == 3:
						print(f"HINT: The correct Weapon is '{self.solution['weapon']}'.")
					elif attempt == 4:
						print(f"HINT: The correct Room is '{self.solution['room']}'.")
					
					attempt += 1  # Increment the attempt count
				else:
					print("Invalid input. Please enter 1 or 2.")
				
				print("Let's start over with your suggestions.")
			
			if attempt > 5:
				print("You've exhausted all attempts. Please try again later.")
		
		# Main loop for player movement
		while True:
			movement = input("Enter 1 for Suggestion or Enter 2 for new room: ")
			if movement == '1':
				make_suggestion()  # Call the suggestion function
			elif movement == '2':
				move_room()  # Call the move room function
			else:
				print("Invalid input. Please enter 1 or 2.")
		
	
				
def clue_game_handler():
	"""
	Main handler of the Clue Game.
	Initialization of the main class
	Calling class methods
	
	Please comment line 231 if you don't want to download the Game Layout nor Solution
	"""
	clue = ClueGame()
	clue.summary_generation()
	clue.character_selection()
	clue.character_movements()

clue_game_handler()