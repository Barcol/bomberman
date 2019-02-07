import sys
from typing import Tuple, Union

import pygame
from pygame import Surface
from pygame.event import EventType
from pygame.joystick import Joystick
from pygame.sprite import Group

from bomb import Bomb
from character import Character
from settings import Settings


class Controller:
    def __init__(self):
        pass

    def check_keydown_events(self, event: EventType, game_settings: Settings, screen: Surface, character: Character,
                             bombs: Group):
        if event.key == pygame.K_RIGHT:
            character.moving_right = True
        if event.key == pygame.K_LEFT:
            character.moving_left = True
        if event.key == pygame.K_UP:
            character.moving_up = True
        if event.key == pygame.K_DOWN:
            character.moving_down = True
        if event.key == pygame.K_SPACE:
            self.place_bomb(game_settings, screen, character, bombs)
        elif event.key == pygame.K_q:
            sys.exit()

    @staticmethod
    def place_bomb(game_settings: Settings, screen: Surface, character: Character, bombs: Group):
        if len(bombs) < character.bombs_allowed:
            new_bomb = Bomb(game_settings, screen, character)
            bombs.add(new_bomb)

    @staticmethod
    def check_keyup_events(event: EventType, character: Character):
        if event.key == pygame.K_RIGHT:
            character.moving_right = False
        if event.key == pygame.K_LEFT:
            character.moving_left = False
        if event.key == pygame.K_UP:
            character.moving_up = False
        if event.key == pygame.K_DOWN:
            character.moving_down = False

    @staticmethod
    def set_character_movement(character: Character, positive: bool, negative: bool, direction: str):
        if direction == "vertical":
            character.moving_down = positive
            character.moving_up = negative
        if direction == "horizontal":
            character.moving_right = positive
            character.moving_left = negative

    def check_joystick_axis(self, axis: float, character: Character, latest_choice: int, direction: str):
        if (axis < 0.4) and (axis > -0.4) and (latest_choice != 0):
            self.set_character_movement(character, False, False, direction)
            latest_choice = 0
        if axis > 0.4 and (latest_choice != 1):
            self.set_character_movement(character, True, False, direction)
            latest_choice = 1
        if axis < -0.4 and (latest_choice != 2):
            self.set_character_movement(character, False, True, direction)
            latest_choice = 2
        return latest_choice

    def check_joystick_events(self, character: Character, joystick: Union[Joystick, bool], latest_choices: Tuple):
        return (self.check_joystick_axis(joystick.get_axis(0), character, latest_choices[0], "horizontal"),
                self.check_joystick_axis(joystick.get_axis(1), character, latest_choices[1], "vertical"))

    def check_events(self, game_settings, screen, character, bombs, character2, bombs2):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event, game_settings, screen, character, bombs)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event, character)
            elif event.type == pygame.JOYBUTTONDOWN:
                self.place_bomb(game_settings, screen, character2, bombs2)
