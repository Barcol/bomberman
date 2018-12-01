import pygame
from bomberman.settings import Settings
from bomberman.character import Character
import bomberman.game_functions as gf
from pygame.sprite import Group
from bomberman.obstacle import Obstacle


def run_game():
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption("BOMBERMAN")
    character = Character(game_settings, screen)
    bombs = Group()
    obstacle = Obstacle(game_settings, screen)

    while True:
        gf.check_events(game_settings, screen, character, bombs)
        character.update()
        gf.update_bombs(bombs)
        gf.update_screen(game_settings, screen, character, obstacle, bombs)


run_game()
