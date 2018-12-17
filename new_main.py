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
    character = Character(game_settings, screen, (0, 0))
    bombs = Group()
    bombs2 = Group()
    obstacles = Group()
    hard_obstacles = Group()
    explosions = Group()
    gf.create_obstacles(game_settings, screen, obstacles)
    gf.create_hard_obstacles(game_settings, screen, hard_obstacles)
    pygame.joystick.init()
    pygame.joystick.Joystick(0).init()
    joystick = pygame.joystick.Joystick(0)
    character2 = Character(game_settings, screen, (1, 1))
    while True:
        pygame.event.pump()
        gf.check_events(game_settings, screen, character, bombs, character2, bombs2)
        character.update()
        gf.check_joystick_events(character2, joystick)
        character2.update()
        gf.update_bombs(bombs, game_settings, screen, explosions, obstacles)
        gf.update_bombs(bombs2, game_settings, screen, explosions, obstacles)
        gf.update_screen(game_settings, screen, character, obstacles, bombs, character2, bombs2, hard_obstacles, explosions)


run_game()
