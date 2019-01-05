import pygame
from pygame.sprite import Sprite
from pygame import Surface
from bomb import Bomb


class Explosion(Sprite):
    def __init__(self, x: int, y: int, screen: Surface, bomb: Bomb):
        super(Explosion, self).__init__()
        self.bomb = bomb
        self.screen = screen
        self.rect = pygame.Rect(0, 0, x, y)
        self.color = (249, 166, 2)
        self.rect.centerx = bomb.rect.centerx
        self.rect.centery = bomb.rect.centery
        self.lifetime = 60

    def drawme(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update(self):
        self.lifetime -= 1
