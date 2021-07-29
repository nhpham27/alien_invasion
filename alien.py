import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to manage an alien in a fleet"""
    def __init__(self, ai_game):
        """Inilializa the alien"""
        super().__init__()
        self.screen = ai_game.screen

        # load alien image and create a rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # put the alien in top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store alien's position as decimal value
        self.x = float(self.rect.x)

        