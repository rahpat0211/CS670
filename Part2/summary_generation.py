from wsgiref.validate import validator

from defaults.weapons import *
from defaults.mansion import *
from defaults.characters import *
from defaults.solution import *

import pandas as pd
import os
import platform
import logging

def generate_summary(solution):
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
		"Character": solution.get('character'),
		"Weapon":    solution.get('weapon'),
		"Room":      solution.get('room')},
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