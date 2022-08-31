import pygame

class Ship:
	"""A class to manage the ship."""

	def __init__(self, ai_game):
		"""Initialize the ship and set its starting postiion."""
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()
		self.Settings = ai_game.Settings

		# Load the ship image and its rect.
		self.image = pygame.image.load("images/ship.bmp")
		self.rect = self.image.get_rect()

		# Start each new ship at the bottom center of the screen.
		self.rect.midbottom = self.screen_rect.midbottom

		#Store a decimal value for the ship's horizontal position.
		self.x = float(self.rect.x)

		#Movement
		self.moving_right = False
		self.moving_left = False

	def update_pos(self):
		"""Update Ships position"""
		if self.moving_right == True and self.rect.right < self.screen_rect.right:
			self.x += self.Settings.ship_speed
		if self.moving_left == True and self.rect.left > 0:
			self.x -= self.Settings.ship_speed

		self.rect.x = self.x

	def blitme(self):
		"""Draw the ship at its current location."""
		self.screen.blit(self.image, self.rect)




class Heart:
	"""A class to manage a heart."""
	def __init__(self, ai_game):
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()

		# Load heart and its rect
		self.image = pygame.image.load("images/heart.bmp")
		self.rect = self.image.get_rect()

		#Start heart at center

		self.rect.x = 275
		self.rect.y = 100

	def blitme(self):
		"""Draw heart on screen"""
		self.screen.blit(self.image, self.rect)