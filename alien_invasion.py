import sys
from time import sleep
import json
from random import randint

import pygame

from settings import Settings
from ship import Ship, Heart
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from powerup import Powerup

class AlienInvasion:
	"""Overall class to manage game assets and behavior."""

	def __init__(self):
		"""Initialize the game, and create game resources."""
		pygame.init()
		self.Settings = Settings(self)

		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.Settings.screen_width = self.screen.get_rect().width
		self.Settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")
		self.screen_rect = self.screen.get_rect()

		self.Stats = GameStats(self)

		self.Ship = Ship(self)
		self.ship_height = self.Ship.rect.height
		self.Heart = Heart(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()	
		self.powerups = pygame.sprite.Group()

		alien = Alien(self)
		self.alien_width = alien.rect.width
		self.alien_height = alien.rect.height

		
		self.play_button = Button(self, "Play")
		self._create_buttons()

		self.sb = Scoreboard(self)

		self.load_highscore_file()

		self.last = pygame.time.get_ticks()
		self.now = pygame.time.get_ticks()
		self.cooldown_difference = self.now - self.last
		self.now_s = pygame.time.get_ticks()
		self.later_s = pygame.time.get_ticks() + 5_000
		self.powerup_active = False

	def run_game(self):
		"""Start the main loop for the game."""
		
		while True:
			self._check_events()

			if self.Stats.game_active:
				self._spawn_powerup()
				self._update_movement_player()
				self._update_bullets()
				self._update_aliens()
				self._update_pos_powerup()
				self._check_if_powerup_over()

			self._update_screen()

			if not self.Stats.game_active:
				self.play_button.draw_button()
				self.increase_difficulty_button.draw_button()
				self.decrease_difficulty_button.draw_button()


			pygame.display.flip()
			
	def _create_buttons(self):
		self.increase_difficulty_button = Button(self, "+Difficulty")
		self.increase_difficulty_button.move_button(250, -30)
		self.decrease_difficulty_button = Button(self, "-Difficulty")
		self.decrease_difficulty_button.move_button(250, 30)

	def load_highscore_file(self):
		try:
			with open("save.json", "r") as f:
				highscore = json.load(f)
				print("Save file loaded.")
		except FileNotFoundError:
			print("Error Loading Highscore: No save file found.")
		except json.decoder.JSONDecodeError:
			print("Error loading file: Save file is empty. Ignoring...")
		else:
			self.Stats.high_score = highscore
			self.sb.prep_high_score()
			print(f"Highscore applied as {self.Stats.high_score}.")

	def save_highscore_file(self):
		try:
			with open("save.json", "w") as f:
				json.dump(self.Stats.high_score, f)
				print(f"Saved highscore as {self.Stats.high_score}.")
		except FileNotFoundError:
			print("Error Loading Highscore: No save file found.")

	def _check_events(self):
		"""Watch for keyboard and mouse events."""
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self._close_game()
				elif event.type == pygame.KEYDOWN:
					self._check_keydown_events(event)
				elif event.type == pygame.KEYUP:
					self._check_keyup_events(event)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					mouse_pos = pygame.mouse.get_pos()
					self._check_play_button(mouse_pos)

	def _update_screen(self):
		self.screen.fill(self.Settings.bg_color)
		self.Ship.blitme()
		# self.Heart.blitme()
		
		# Make the most recently drawn screen visible
		for bullet in self.bullets.sprites():
			bullet.draw_bullets()

		self.aliens.draw(self.screen)
		self.powerups.draw(self.screen)
		self.sb.show_score()

	def _update_movement_player(self):
		self.Ship.update_pos()

	def _check_keydown_events(self, event):
		if event.key == pygame.K_RIGHT:
			#Move the ship to the right.
			self.Ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.Ship.moving_left = True
		elif event.key == pygame.K_q:
			self._close_game()
		elif event.key == pygame.K_SPACE and self.Stats.game_active:
			self._fire_bullet()
		elif event.key == pygame.K_p and not self.Stats.game_active:
			self._start_game()
		elif event.key == pygame.K_l:
			self._spawn_powerup()
			print(f"Current Time: {self.now_s} and future time {self.later_s}")
		elif event.key == pygame.K_n:
			print(f"Cooldown: {self.cooldown_difference} Current Time: {pygame.time.get_ticks()}")

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
				#print(len(self.bullets))

		self._check_collion_bullet_alien()

	def _check_collion_bullet_alien(self):
		# Check for collision if bullets hit aliens.
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

		if not self.aliens:
			# Destroy all bullets and create a new fleet.
			self._new_level()

		if collisions:
			for aliens in collisions.values():
				self.Stats.score += self.Settings.alien_points * len(aliens)
				self.sb.prep_score()
				self.sb.check_high_score()

	def _new_level(self):
		self.bullets.empty()
		self._create_fleet()
		self.Settings.increase_speed()

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

		if pygame.sprite.spritecollideany(self.Ship, self.aliens):
			self._ship_hit()

		self._check_alien_bottom()

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

	def _ship_hit(self):
		"""Respond??to the ship being hit by an alien."""
		# Decrement ships left.
		if self.Stats.ships_left > 0:
			self.Stats.ships_left -= 1
			self.sb.prep_ships()
			self.powerups.empty()

			self.aliens.empty()
			self.bullets.empty()

			self._create_fleet()
			self.Ship.center_ship()

			sleep(0.5)
		else:
			self.Stats.game_active = False
			self.Settings.level = 1
			self.powerups.empty()
			pygame.mouse.set_visible(True)

	def _check_alien_bottom(self):
		"""Check if alien hits bottom if screen."""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				self._ship_hit()
				break

	def _start_game(self):
		self.Stats.reset_stats()
		if self.Settings.level == 1:
			self.Settings.initialize_dynamic_settings()
			#print(f"Level Reset: {self.Settings.level}")
		self.Stats.game_active = True
		self.aliens.empty()
		self.bullets.empty()

		self._create_fleet()
		self.Ship.center_ship()
		self.sb.prep_score()
		pygame.mouse.set_visible(False)

	def _check_play_button(self, mouse_pos):
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		button_clicked_i_d = self.increase_difficulty_button.rect.collidepoint(mouse_pos)
		button_clicked_d_d = self.decrease_difficulty_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.Stats.game_active:
			self._start_game()
			self.sb.prep_level()
			self.sb.prep_ships()
			print("Start pressed.")
			print(f"Level: {self.Settings.level}.")
			self._create_fleet()
		if button_clicked_i_d and not self.Stats.game_active:
			self.Settings.increase_level()
			print("Level up pressed.")
			print(f"Level: {self.Settings.level}")
		if button_clicked_d_d and not self.Stats.game_active:
			self.Settings.decrease_level()
			print("Level down pressed.")

	def _close_game(self):
		self.save_highscore_file()
		sys.exit()

	def _update_pos_powerup(self):
		self.powerups.update()
		for powerup in self.powerups.sprites():
			if powerup.check_top():
				self.powerups.remove(powerup)

		if pygame.sprite.spritecollideany(self.Ship, self.powerups):
			self.powerups.empty()
			self._shotgun_active()

	def _spawn_powerup(self):
		self.now = pygame.time.get_ticks()

		self.cooldown_difference = self.now - self.last

		if self.cooldown_difference >= 10_000:
			powerup = Powerup(self)
			powerup.rect.y = 0
			powerup.rect.x = randint(0, self.screen_rect.right)
			self.powerups.add(powerup)
			self.last = pygame.time.get_ticks()

	def _shotgun_active(self):
		self.now_s = pygame.time.get_ticks()
		self.later_s = pygame.time.get_ticks() + 5_000

		self.Settings.bullet_width = 300
		self.powerup_active = True

	def _check_if_powerup_over(self):
		self.now_s = pygame.time.get_ticks()
		if self.now_s > self.later_s and self.powerup_active:
			self.Settings.bullet_width = 3
			self.powerup_active = False

if __name__ == "__main__":
	# Make a game instance, and run the game.
	ai = AlienInvasion()
	ai.run_game()