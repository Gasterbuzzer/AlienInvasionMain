import pygame

from pygame.sprite import Sprite
from settings import Settings

class Alien(Sprite):

	def __init__(self, game):
		super().__init__()
		self.screen = game.screen

		self.screen_rect = self.screen.get_rect()

		self.image = pygame.image.load("images/alien.bmp")
		self.rect = self.image.get_rect()

		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		self.x = float(self.rect.x)

		self.Settings = Settings()

	def update(self):
		"""Move the alien to the right."""
		self.x += (self.Settings.alien_speed * self.Settings.fleet_direction)
		self.rect.x = self.x

	def check_edges(self):
		"""Return True if alien is at edge of screen."""
		if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
			return True