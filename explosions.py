import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    def __init__(self, x, y, screen, bomb):
        super(Explosion, self).__init__()
        self.bomb = bomb
        self.screen = screen
        self.rect = pygame.Rect(0, 0, x, y)
        self.rect.centerx = bomb.rect.centerx
        self.rect.centery = bomb.rect.centery
