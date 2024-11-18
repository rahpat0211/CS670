class Character:
	"""
	Initialize the characters with a name and a starting position
	"""
	def __init__(self, name, starting_position):
		self.name = name
		self.position = starting_position
	
	def move_spaces(self, new_position):
		self.position = new_position


# Characters and their positions

characters = [
	Character("Miss Scarlet", "Kitchen"),
	Character("Colonel Mustard", "Ballroom"),
	Character("Mrs. White", "Conservatory"),
	Character("Mr. Green", "Dining Room"),
	Character("Mrs. Peacock", "Lounge"),
	Character("Professor Plum", "Hall"),
	Character("Mrs. Pink", "Study Room"),
	Character("Mrs. Red", "Library"),
	Character("Mrs. Yellow", "Billiard Room")
]


