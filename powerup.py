import pygame
from pygame.sprite import Sprite

class Powerup(Sprite):

	def __init__(self, game):
		super().__init__()

		self.screen = game.screen
		self.screen_rect = self.screen.get_rect()

		self.image = pygame.image.load("images/powerup.bmp")
		self.rect = self.image.get_rect()

		self.Settings = game.Settings


	def update(self):
		self.rect.y += 1

	def check_top(self):
		if self.rect.top >= self.screen_rect.bottom:
			return True