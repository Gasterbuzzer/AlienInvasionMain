class Settings:
	"""A class to store all settings for Alien Invasion."""

	def __init__(self, game):
		"""Initialize the game's settings."""

		# Screen Settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)

		self.game = game

		# Ship Settings
		self.ship_limit = 3

		# Bullet Settings
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 3

		# How quickly the game speeds up.
		self.speedup_scale = 1.2
		self.score_scale = 1.5
		self.fleet_drop_speed = 7 # Original value: 7

		self.initialize_dynamic_settings()

		self.LEVEL_DEFAULT = 1
		self.SHIP_SPEED_DEFAULT = 1.5
		self.BULLET_SPEED_DEFAULT = 1.7
		self.ALIEN_SPEED_DEFAULT = 0.5
		self.ALIEN_POINTS_DEFAULT = 50

	def initialize_dynamic_settings(self):
		self.level = 1
		self.ship_speed = 1.5
		self.bullet_speed = 1.7

		self.alien_points = 50

		#Alien Stuff
		self.alien_speed = 0.5

		# fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1

	def increase_speed(self):
		"""Increase speed settings."""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed = self.alien_speed * self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)

		self.level += 1
		self.game.sb.prep_level()
		#print(f"New level! Level {self.level} now has {self.alien_points} points for aliens!")

	def increase_level(self):
		self.level += 1
		self.game.sb.prep_level()

		# Default values for calculations
		self.ship_speed = self.SHIP_SPEED_DEFAULT
		self.bullet_speed = self.BULLET_SPEED_DEFAULT
		self.alien_speed = self.ALIEN_SPEED_DEFAULT
		self.fleet_direction = 1
		self.alien_points = self.ALIEN_POINTS_DEFAULT

		for number in range(0, self.level):
			self.ship_speed *= self.speedup_scale
			self.bullet_speed *= self.speedup_scale
			self.alien_speed *= self.speedup_scale
			self.alien_points = int(self.alien_points * self.score_scale)

	def decrease_level(self):
		self.level -= 1
		self.game.sb.prep_level()

		# Default values for calculations
		self.ship_speed = self.SHIP_SPEED_DEFAULT
		self.bullet_speed = self.BULLET_SPEED_DEFAULT
		self.alien_speed = self.ALIEN_SPEED_DEFAULT
		self.fleet_direction = 1
		self.alien_points = self.ALIEN_POINTS_DEFAULT

		for number in range(0, self.level):
			self.ship_speed *= self.speedup_scale
			self.bullet_speed *= self.speedup_scale
			self.alien_speed *= self.speedup_scale
			self.alien_points = int(self.alien_points * self.score_scale)
