class Mansion:
	def __init__(self):
		"""
		Initialize a list of rooms available throughout the mansion
		"""
		self.rooms = [
			"Kitchen",
			"Ballroom",
			"Conservatory",
			"Dining Room",
			"Lounge",
			"Hall",
			"Study Room",
			"Library",
			"Billiard Room"
		]
	
	# Return a string representation of the rooms in the mansion
	def __str__(self) -> str: return "Mansion Layout: " + ", ".join(self.rooms)
	
	# Return a list of all the rooms in the mansion
	def get_rooms(self) -> list: return self.rooms