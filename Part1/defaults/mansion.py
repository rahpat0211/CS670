class Mansion:
	def __init__(self):
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
	
	def __str__(self) -> str: return "Mansion Layout: " + ", ".join(self.rooms)
	
	def get_rooms(self) -> list: return self.rooms