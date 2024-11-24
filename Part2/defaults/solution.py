import random

from defaults.characters import *
from defaults.mansion import *
from defaults.weapons import *


class Solution:
	_instance = None
	
	def __new__(cls):
		if cls._instance is None:
			cls._instance = super(Solution, cls).__new__(cls)
			cls._instance._initialize()
		return cls._instance
	
	def _initialize(self):
		self.character = random.choice(characters).name
		self.weapon = random.choice(list(weapons.values()))
		self.room = random.choice(Mansion().get_rooms())


def gather_solution():
	solution = Solution()
	return {
		"character": solution.character,
		"weapon":    solution.weapon,
		"room":      solution.room
	}
