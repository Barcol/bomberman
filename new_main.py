import pygame
from pygame.sprite import Group

from bombs_handler import BombsHandler
from character import Character
from controller import Controller
from joystick import Joystick
from obstacle_placer import ObstaclePlacer
from screen import Screen
from settings import Settings
from smile_of_fate import SmileOfFate


def run_game():
    pygame.init()
    game_settings = Settings()
    screen = Screen(game_settings)
    pygame.display.set_caption("BOMBERMAN")
    character = Character(game_settings, screen.screen, (0, 0))
    character2 = Character(game_settings, screen.screen, (1, 1))
    bombs_handler = BombsHandler(Group(), Group())
    obstacles = Group()
    hard_obstacles = Group()
    explosions = Group()
    treasures = Group()
    obstacle_placer = ObstaclePlacer()
    obstacle_placer.create_obstacles(game_settings, screen.screen, obstacles)
    obstacle_placer.create_hard_obstacles(game_settings, screen.screen, hard_obstacles)
    joystick = Joystick()
    smile_of_fate = SmileOfFate(game_settings)
    latest_choices = (0, 0)
    controller = Controller()
    while True:
        pygame.event.pump()
        controller.check_events(game_settings, screen.screen, character, bombs_handler.bombs[0], character2,
                                bombs_handler.bombs[1])
        character.update(obstacles, hard_obstacles)
        if joystick.is_joystick():
            latest_choices = controller.check_joystick_events(character2, joystick.is_joystick(), latest_choices)
        character2.update(obstacles, hard_obstacles)
        bombs_handler.update_bombs(bombs_handler.bombs[0], game_settings, screen.screen, explosions, obstacles,
                                   treasures, smile_of_fate)
        bombs_handler.update_bombs(bombs_handler.bombs[1], game_settings, screen.screen, explosions, obstacles,
                                   treasures, smile_of_fate)
        bombs_handler.kill_your_heroes(explosions, character, character2)
        if len(obstacles.sprites()) < 5:
            treasures.empty()
            character.reset_character_status()
            character2.reset_character_status()
            obstacle_placer.create_obstacles(game_settings, screen.screen, obstacles)
        smile_of_fate.player_collected_treasure(character, treasures)
        smile_of_fate.player_collected_treasure(character2, treasures)
        screen.update_screen(game_settings, character, obstacles, bombs_handler.bombs[0], character2,
                             bombs_handler.bombs[1], hard_obstacles, explosions, treasures)


if __name__ == "__main__":
    run_game()
