import pygame

class Ship_shield:
	"""A class to manage the ship"""
	def __init__(self, ai_game):
		"""Initialize the ship and set its starting position"""
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()

		#Load the shield image and get its rect
		self.image = pygame.image.load('images/ship_shield.bmp')
		self.rect = self.image.get_rect()

		#Put the shield around the ship at the beginning of level
		self.rect.midbottom = self.screen_rect.midbottom

	def update(self,ship):
		"""Update the position of the shield"""
		self.rect.midbottom = ship.rect.midbottom

	def blitme(self):
		"""Draw the ship at its current location"""
		self.screen.blit(self.image,self.rect)