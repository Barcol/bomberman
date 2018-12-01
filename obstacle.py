import pygame
from pygame.sprite import Sprite


class Obstacle(Sprite):
    def __init__(self, game_settings, screen):
        super(Obstacle, self).__init__()
        self.screen = screen
        self.game_settings = game_settings

        self.image = pygame.image.load("obstacle.bmp")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)