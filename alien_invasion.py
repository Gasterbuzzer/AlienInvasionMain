import sys

import pygame

from settings import Settings
from ship import Ship, Heart
from bullet import Bullet
from alien import Alien

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
		self.ship_height = self.Ship.rect.height
		self.Heart = Heart(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()	

		alien = Alien(self)
		self.alien_width = alien.rect.width
		self.alien_height = alien.rect.height

		self._create_fleet()

	def run_game(self):
		"""Start the main loop for the game."""
		while True:
			self._check_events()
			self._update_movement_player()
			self._update_bullets()
			self._update_aliens()
			self._update_screen()
			

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

		self.aliens.draw(self.screen)

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
		"""Create Bullets on top of Ship, maximum of three"""
		if len(self.bullets) < self.Settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Update position of bullets and delete offscreen ones"""
		# Update bullet positions.
		self.bullets.update()
		
		# Get rid of bullets when not visible.
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)
				print(len(self.bullets))

		self._check_collion_bullet_alien()

	def _check_collion_bullet_alien(self):
		# Check for collision if bullets hit aliens.
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

		if not self.aliens:
			# Destroy all bullets and create a new fleet.
			self.bullets.empty()
			self._create_fleet()

	def _create_fleet(self):
		self.avalable_space_x = self.Settings.screen_width - (4 * self.alien_width)
		self.number_aliens_x = self.avalable_space_x // (2 * self.alien_width)
		self.avalable_space_y = self.Settings.screen_height - (4 * self.alien_height) - self.ship_height
		self.number_rows = self.avalable_space_y // (2 * self.alien_height)
		# Create a row of aliens:
		for row in range(0, self.number_rows):
			for alien_i in range(0, self.number_aliens_x):
				self._create_alien(alien_i, row)

	def _create_alien(self, alien_number, row_number):
		alien = Alien(self)
		alien.x = self.alien_width + ((2 * self.alien_width) * alien_number)
		alien.rect.x = alien.x
		alien.rect.y = self.alien_height + ((2 * alien.rect.height) * row_number)
		self.aliens.add(alien)

	def _update_aliens(self):
		self._check_fleet_edges()
		self.aliens.update()

	def _check_fleet_edges(self):
		"""Respond if any aliens have reached an edge."""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Drop the entire fleet and change the fleet's direction."""
		for alien in self.aliens.sprites():
			alien.rect.y += self.Settings.fleet_drop_speed
		self.Settings.fleet_direction *= -1

if __name__ == "__main__":
	# Make a game instance, and run the game.
	ai = AlienInvasion()
	ai.run_game()