import sys

import pygame

from settings import Settings
from ship import Ship, Heart
from bullet import Bullet

class AlienInvasion:
	"""Overall class to manage game assets and behavior."""

	def __init__(self):
		"""Initialize the game, and create game resources."""
		pygame.init()
		self.Settings = Settings()

		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.Settings.screen_width = self.screen.get_rect().width
		self.Settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		self.Ship = Ship(self)
		self.Heart = Heart(self)
		self.bullets = pygame.sprite.Group()

	def run_game(self):
		"""Start the main loop for the game."""
		while True:
			self._check_events()
			self._update_movement_player()
			self._update_screen()
			self.bullets.update()
			

	def _check_events(self):
		"""Watch for keyboard and mouse events."""
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					self._check_keydown_events(event)
				elif event.type == pygame.KEYUP:
					self._check_keyup_events(event)

	def _update_screen(self):
		self.screen.fill(self.Settings.bg_color)
		self.Ship.blitme()
		# self.Heart.blitme()
		# Make the most recently drawn screen visible
		for bullet in self.bullets.sprites():
			bullet.draw_bullets()
		pygame.display.flip()

	def _update_movement_player(self):
		self.Ship.update_pos()

	def _check_keydown_events(self, event):
		if event.key == pygame.K_RIGHT:
			#Move the ship to the right.
			self.Ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.Ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self, event):
		if event.key == pygame.K_RIGHT:
			self.Ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.Ship.moving_left = False

	def _fire_bullet(self):
		new_bullet = Bullet(self)
		self.bullets.add(new_bullet)



if __name__ == "__main__":
	# Make a game instance, and run the game.
	ai = AlienInvasion()
	ai.run_game()