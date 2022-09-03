class GameStats:
	"""Track statistics for Alien Invasion."""

	def __init__(self, game_instance):
		"""Initialize statistics."""
		self.Settings = game_instance.Settings
		self.reset_stats()

		self.game_active = True


	def reset_stats(self):
		"""Initialize statistics that can change during the game."""
		self.ships_left = self.Settings.ship_limit