import pygame
from pygame.sprite import Group

from src.character import Character
from src.settings import Settings


class Screen:
    def __init__(self, game_settings):
        self.screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))

    def update_screen(self, game_settings: Settings, character: Character, obstacles: Group, bombs: Group,
                      character2: Character, bombs2: Group, hard_obstacles: Group, explosions: Group, treasures: Group):
        self.screen.fill(game_settings.bg_color)
        for bomb in bombs.sprites():
            bomb.draw_bomb()
        for bomb in bombs2.sprites():
            bomb.draw_bomb()
        character.blitme()
        character2.blitme()
        obstacles.draw(self.screen)
        for explosion in explosions.sprites():
            explosion.drawme()
        hard_obstacles.draw(self.screen)
        treasures.draw(self.screen)
        pygame.display.flip()
