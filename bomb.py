import pygame
from pygame.sprite import Sprite
from settings import Settings
from pygame import Surface
from character import Character


class Bomb(Sprite):
    def __init__(self, game_settings: Settings, screen: Surface, character: Character):
        super(Bomb, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, game_settings.bomb_width, game_settings.bomb_height)
        self.rect.centerx = character.rect.centerx
        self.rect.top = character.rect.centery
        self.lifetime = 100
        self.character = character
        self.color = game_settings.bomb_color
        self.speed_factor = game_settings.bomb_speed_factor

    def update(self):
        self.lifetime -= self.speed_factor

    def draw_bomb(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
