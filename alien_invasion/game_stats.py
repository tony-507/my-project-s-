class GameStats:
	"""Track statistics for alien invasion"""

	def __init__(self,ai_game):
		"""Initialize statistics"""
		self.settings = ai_game.settings
		self.reset_stats()

		# Start game in an inactive state
		self.game_active = False

		#High score should never be reset
		f = open("high_score.txt","r")
		self.high_score = int(float(f.read()))
		f.close()

	def reset_stats(self):
		"""Initialize statistics that can change during the game."""
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1