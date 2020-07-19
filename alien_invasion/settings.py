class Settings:
	"""A class to store all settings for alien invasion"""

	def __init__(self):
		"""Initialize the game's static settings"""
		# Screen settings
		self.screen_width = 800
		self.screen_height = 1200
		self.bg_color = (230,230,230)

		# Ship settings
		self.ship_limit = 3
		self.shield = True

		# Bullet settings for ship
		self.bullet_width = 3
		self.bullet_height = 20
		self.bullet_color = (0,0,255)
		self.bullet_allowed = 5

		# Alien settings
		self.fleet_drop_speed = 10

		# Bullet settings for aliens
		self.bullet_alien_width = 3
		self.bullet_alien_height = 20
		self.bullet_alien_color = (255,0,0)

		# How quickly the game speeds up
		self.speedup_scale = 1.2

		# How quickly the alien point values increase
		self.score_scale = 1.15

		self.initialize_dynamic_settings_easy()
		self.alien_bullet_allowed = 0

	def initialize_dynamic_settings_easy(self):
		"""Initialize settings that change throughout the game"""
		self.ship_speed = 3
		self.bullet_speed = 5.0
		self.bullet_alien_speed = 2.0
		self.alien_bullet_allowed = 4
		self.alien_speed = 2.0

		# Scoring
		self.alien_points = 50

		# fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1

	def initialize_dynamic_settings_medium(self):
		"""Initialize settings that change throughout the game"""
		self.ship_speed = 2.5
		self.bullet_speed = 3.0
		self.bullet_alien_speed = 3.0
		self.alien_bullet_allowed = 5
		self.alien_speed = 2.5

		# Scoring
		self.alien_points = 75

		# fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1

	def initialize_dynamic_settings_hard(self):
		"""Initialize settings that change throughout the game"""
		self.ship_speed = 3
		self.bullet_speed = 2.0
		self.bullet_alien_speed = 5.0
		self.alien_bullet_allowed = 6
		self.alien_speed = 3.0

		# Scoring
		self.alien_points = 100

		# fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1

	def increase_speed(self):
		"""Increase speed settings and alien point values"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.bullet_alien_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale

		self.alien_points = int(self.alien_points*self.score_scale)