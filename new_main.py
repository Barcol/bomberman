import pygame
from bomberman.settings import Settings
from bomberman.character import Character
import bomberman.game_functions as gf
from pygame.sprite import Group


def run_game():
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption("BOMBERMAN")
    character = Character(game_settings, screen)
    bombs = Group()
    obstacles = Group()
    explosions = Group()
    gf.create_obstacles(game_settings, screen, obstacles)

    while True:
        gf.check_events(game_settings, screen, character, bombs)
        character.update()
        gf.update_bombs(bombs, game_settings, screen, explosions, obstacles)
        gf.update_screen(game_settings, screen, character, obstacles, bombs)


run_game()
