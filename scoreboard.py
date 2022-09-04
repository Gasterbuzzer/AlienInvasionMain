import pygame.font

class Scoreboard:

	def __init__(self, game):

		self.screen = game.screen
		self.screen_rect = self.screen.get_rect()
		self.Settings = game.Settings
		self.Stats = game.Stats

		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)

		self.prep_score()

	def prep_score(self):
		"""Turn the score into a rendered image."""
		rounded_score = round(self.stats.score, -1)
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color, self.Settings.bg_color)

		# Display the score at the top right of the screen. The true statement is for antialisasing.
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def show_score(self):
		"""Draw score to the screen."""
		self.screen.blit(self.score_image, self.score_rect)
