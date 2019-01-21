import sys

import pygame

from bomb import Bomb
from explosions import Explosion
from settings import Settings
from pygame import Surface
from character import Character
from pygame.sprite import Group
from pygame.event import EventType
from typing import Tuple, Union
from pygame.joystick import Joystick
from smile_of_fate import SmileOfFate


def check_keydown_events(event: EventType, game_settings: Settings, screen: Surface, character: Character,
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
        place_bomb(game_settings, screen, character, bombs)
    elif event.key == pygame.K_q:
        sys.exit()


def place_bomb(game_settings: Settings, screen: Surface, character: Character, bombs: Group):
    if len(bombs) < character.bombs_allowed:
        new_bomb = Bomb(game_settings, screen, character)
        bombs.add(new_bomb)


def check_keyup_events(event: EventType, character: Character):
    if event.key == pygame.K_RIGHT:
        character.moving_right = False
    if event.key == pygame.K_LEFT:
        character.moving_left = False
    if event.key == pygame.K_UP:
        character.moving_up = False
    if event.key == pygame.K_DOWN:
        character.moving_down = False


def set_character_movement(character: Character, positive: bool, negative: bool, direction: str):
    if direction == "vertical":
        character.moving_down = positive
        character.moving_up = negative
    if direction == "horizontal":
        character.moving_right = positive
        character.moving_left = negative


def check_joystick_axis(axis: float, character: Character, latest_choice: int, direction: str):
    if (axis < 0.4) and (axis > -0.4) and (latest_choice != 0):
        set_character_movement(character, False, False, direction)
        latest_choice = 0
    if axis > 0.4 and (latest_choice != 1):
        set_character_movement(character, True, False, direction)
        latest_choice = 1
    if axis < -0.4 and (latest_choice != 2):
        set_character_movement(character, False, True, direction)
        latest_choice = 2
    return latest_choice


def check_joystick_events(character: Character, joystick: Union[Joystick, bool], latest_choices: Tuple):
    return (check_joystick_axis(joystick.get_axis(0), character, latest_choices[0], "horizontal"),
            check_joystick_axis(joystick.get_axis(1), character, latest_choices[1], "vertical"))


def check_events(game_settings, screen, character, bombs, character2, bombs2):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, character, bombs)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, character)
        elif event.type == pygame.JOYBUTTONDOWN:
            place_bomb(game_settings, screen, character2, bombs2)


def kill_yout_heroes(explosions: Group, character: Character, character2: Character):
    for explosion in explosions:
        if pygame.sprite.collide_rect(explosion, character):
            character.die()
        if pygame.sprite.collide_rect(explosion, character2):
            character2.die()


def update_bombs(bombs: Group, game_settings: Settings, screen: Surface, explosions: Group, obstacles: Group,
                 treasures: Group, smile_of_fate: SmileOfFate):
    bombs.update()
    drop = []
    for bomb in bombs.copy():
        if bomb.lifetime < 1:
            explosions.add(Explosion(bomb.character.explosion_size, game_settings.explosion_width, screen, bomb))
            explosions.add(Explosion(game_settings.explosion_width, bomb.character.explosion_size, screen, bomb))
            destroyed_obstacles = pygame.sprite.groupcollide(explosions, obstacles, False, True)
            for ashes in destroyed_obstacles:
                drop.append(smile_of_fate.place_a_treasure(destroyed_obstacles[ashes][0].rect.x,
                                                           destroyed_obstacles[ashes][0].rect.y,
                                                           game_settings, screen, treasures))
            bombs.remove(bomb)
    for explosion in explosions:
        explosion.update()
        if explosion.lifetime < 0:
            explosions.remove(explosion)


def update_screen(game_settings: Settings, screen: Surface, character: Character, obstacles: Group, bombs: Group,
                  character2: Character, bombs2: Group, hard_obstacles: Group, explosions: Group, treasures: Group):
    screen.fill(game_settings.bg_color)
    for bomb in bombs.sprites():
        bomb.draw_bomb()
    for bomb in bombs2.sprites():
        bomb.draw_bomb()
    character.blitme()
    character2.blitme()
    obstacles.draw(screen)
    for explosion in explosions.sprites():
        explosion.drawme()
    hard_obstacles.draw(screen)
    treasures.draw(screen)
    pygame.display.flip()
