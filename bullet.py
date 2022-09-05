import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""A class to manage bullets fired from the ship"""

	def __init__(self, ai_game):
		"""Create a bullet object at the ship's current position."""
		super().__init__()
		self.screen = ai_game.screen
		self.Settings = ai_game.Settings
		self.color = ai_game.Settings.bullet_color

		# Create a bullet rect at (0, 0) and then set correct position.
		self.rect = pygame.Rect(0, 0, self.Settings.bullet_width, self.Settings.bullet_height)
		self.rect.midtop = ai_game.Ship.rect.midtop

		# Store the bullet's position as a decimal value.
		self.y = float(self.rect.y)


	def update(self):
		self.y -= self.Settings.bullet_speed

		self.rect.y = self.y

	def draw_bullets(self):
		pygame.draw.rect(self.screen, self.color, self.rect)

	def update_bullet(self):
		self.rect = pygame.Rect(0, 0, self.Settings.bullet_width, self.Settings.bullet_height)
