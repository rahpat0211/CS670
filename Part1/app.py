from wsgiref.validate import validator

from defaults.weapons import *
from defaults.mansion import *
from defaults.characters import *
from defaults.solution import *

import pandas as pd
import os
import platform
import logging

class ClueGame:
	def __init__(self):
		self.solution = gather_solution()
		self.selected_character = ''
		self.selected_room = ''
		self.selected_weapon = ''
	
	def summary_generation(self):
		character_sheet = pd.DataFrame(columns=["Character Name", "Starting Position"])
		mansion_sheet = pd.DataFrame(columns=["Rooms"])
		weapons_sheet = pd.DataFrame(columns=["Weapons"])
		solution_sheet = pd.DataFrame(columns=["Character", "Weapon", "Room"])
		
		for character in characters:
			character_sheet = character_sheet._append({
				"Character Name": character.name,
				"Starting Position": character.position},
			               ignore_index=True)
		
		for room in Mansion().get_rooms():
			mansion_sheet = mansion_sheet._append({"Rooms": room}, ignore_index=True)
		
		for tools in list(weapons.values()):
			weapons_sheet = weapons_sheet._append({"Weapons": tools}, ignore_index=True)
		
		solution_sheet = solution_sheet._append({
			"Character": self.solution.get('character'),
			"Weapon": self.solution.get('weapon'),
			"Room": self.solution.get('room')},
			ignore_index=True)

		file_name = os.path.join("Layout","Game_Set_Up.xlsx")
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
		info = {character.name: character.position for character in characters}
		
		while True:  # Loop until a valid character is selected
			selected_character = input(f"Please choose a character from this list: {list(info.keys())}: ")
			
			if selected_character in list(info.keys()):
				selected_room = info.get(selected_character)
				print(f"You have selected: {selected_character}")
				print(f"Starting Room: {selected_room}")
				
				self.selected_character = selected_character  # Return the selected character
				self.selected_room = selected_room
				return
			else:
				print(f"Sorry, '{selected_character}' is not a valid character. Please try again.")
	
	def character_movements(self):
		def move_room():
			while True:
				selected_room = input(f"Select a room you would like to move to: {Mansion().get_rooms()}")
				if selected_room in Mansion().get_rooms():
					print(f"You have selected: {selected_room}")
					self.selected_room = selected_room
					return
				else:
					print(f"Sorry, '{selected_room}' is not a valid room. Please try again.")
		
		def make_suggestion():
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
						return "character"
					elif self.solution['weapon'] != weapon:
						print("Wrong Weapon.")
						return "weapon"
					elif self.solution['room'] != room:
						print("Wrong Room.")
						return "room"
			
			def validator(question, actual):
				while True:
					resp = input(question)
					if resp in actual:
						return resp
					else:
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
				
				# Provide hints on the second, third, and fourth attempts
				if attempt == 2:
					print(f"HINT: The correct Character is '{self.solution['character']}'.")
				elif attempt == 3:
					print(f"HINT: The correct Weapon is '{self.solution['weapon']}'.")
				elif attempt == 4:
					print(f"HINT: The correct Room is '{self.solution['room']}'.")
				
				print("Let's start over with your suggestions.")
				attempt += 1
			
			if attempt > 5:
				print("You've exhausted all attempts. Please try again later.")
		
		# Main loop for player movement
		while True:
			movement = int(input(f"Enter 1 for Suggestion or Enter 2 for new room: "))
			if movement in [1, 2]:
				if movement == 2:
					move_room()  # Assuming move_room is defined elsewhere
				else:
					make_suggestion()  # Call the suggestion function
					return  # Exit the loop after making a suggestion
		
	
				
def clue_game_handler():
	clue = ClueGame()
	clue.summary_generation()
	clue.character_selection()
	clue.character_movements()

clue_game_handler()