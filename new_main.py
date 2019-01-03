import pygame
from pygame.sprite import Group

import game_functions as gf
from character import Character
from settings import Settings
from joystick import Joystick


def run_game():
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption("BOMBERMAN")
    character = Character(game_settings, screen, (0, 0))
    character2 = Character(game_settings, screen, (1, 1))
    bombs = Group()
    bombs2 = Group()
    obstacles = Group()
    hard_obstacles = Group()
    explosions = Group()
    treasures = Group()
    gf.create_obstacles(game_settings, screen, obstacles)
    gf.create_hard_obstacles(game_settings, screen, hard_obstacles)
    joystick = Joystick()
    latest_choices = (0, 0)
    while True:
        pygame.event.pump()
        gf.check_events(game_settings, screen, character, bombs, character2, bombs2)
        character.update(obstacles, hard_obstacles)
        if joystick.is_joystick():
            latest_choices = gf.check_joystick_events(character2, joystick.is_joystick(), latest_choices[0],
                                                      latest_choices[1])
        character2.update(obstacles, hard_obstacles)
        gf.update_bombs(bombs, game_settings, screen, explosions, obstacles, treasures)
        gf.update_bombs(bombs2, game_settings, screen, explosions, obstacles, treasures)
        gf.kill_yout_heroes(explosions, character, character2)
        gf.player_collected_treasure(character, treasures)
        gf.player_collected_treasure(character2, treasures)
        gf.update_screen(game_settings, screen, character, obstacles, bombs, character2, bombs2, hard_obstacles,
                         explosions, treasures)

if __name__ == "__main__":
    run_game()
