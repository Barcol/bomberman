import sys
import random

import pygame

from bomb import Bomb
from explosions import Explosion
from obstacle import Obstacle


def check_keydown_events(event, game_settings, screen, character, bombs):
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


def place_bomb(game_settings, screen, character, bombs):
    if len(bombs) < character.bombs_allowed:
        new_bomb = Bomb(game_settings, screen, character)
        bombs.add(new_bomb)


def check_keyup_events(event, character):
    if event.key == pygame.K_RIGHT:
        character.moving_right = False
    if event.key == pygame.K_LEFT:
        character.moving_left = False
    if event.key == pygame.K_UP:
        character.moving_up = False
    if event.key == pygame.K_DOWN:
        character.moving_down = False


def set_character_movement(character, up, right, down, left):
    character.moving_up = up
    character.moving_right = right
    character.moving_down = down
    character.moving_left = left


def detect_last_choice(character):
    if not (character.moving_left or character.moving_right):
        latest_choice = 0
    elif character.moving_right:
        latest_choice = 1
    else:
        latest_choice = 2
    if not(character.moving_up or character.moving_down):
        latest_choice_y = 3
    elif character.moving_down:
        latest_choice_y = 4
    else:
        latest_choice_y = 5
    return latest_choice, latest_choice_y


def check_joystick_axis_events(axis_x, axis_y, character, latest_choice, latest_choice_y):
    if (axis_x < 0.4) and (axis_x > -0.4) and (latest_choice != 0):
        set_character_movement(character, character.moving_up, False, character.moving_down, False)
    if axis_x > 0.4 and (latest_choice != 1):
        set_character_movement(character, character.moving_up, True, character.moving_down, False)
    if axis_x < -0.4 and (latest_choice != 2):
        set_character_movement(character, character.moving_up, False, character.moving_down, True)
    if (axis_y < 0.4) and (axis_y > -0.4) and (latest_choice_y != 3):
        set_character_movement(character, False, character.moving_right, False, character.moving_left)
    if axis_y > 0.4 and (latest_choice_y != 4):
        set_character_movement(character, False, character.moving_right, True, character.moving_left)
    if axis_y < - 0.4 and (latest_choice_y != 5):
        set_character_movement(character, True, character.moving_right, False, character.moving_left)
    return detect_last_choice(character)


def check_joystick_events(character, joystick, latest_choice, latest_choice_y):
    return check_joystick_axis_events(joystick.get_axis(0), joystick.get_axis(1), character, latest_choice,
                                      latest_choice_y)


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


def kill_yout_heroes(explosions, character, character2):
    for explosion in explosions:
        if pygame.sprite.collide_rect(explosion, character):
            character.die()
        if pygame.sprite.collide_rect(explosion, character2):
            character2.die()


def place_a_treasure(drop_x, drop_y, game_settings, screen, treasures):
    if random.randint(0, 10) < 5:
        treasure = Obstacle(game_settings, screen, "treasure.bmp")
        treasure.rect.x = drop_x
        treasure.rect.y = drop_y
        treasures.add(treasure)


def player_collected_treasure(character, treasures):
    for treasure in treasures:
        if pygame.sprite.collide_rect(character, treasure):
            treasures.remove(treasure)
            type_of_upgrade(character)


def type_of_upgrade(character):
    guess = random.randint(0, 3)
    if guess == 0:
        character.character_speed += 0.4
    if guess in (1, 2):
        character.explosion_size += 25
    if guess == 3:
        character.bombs_allowed += 1


def update_bombs(bombs, game_settings, screen, explosions, obstacles, treasures):
    bombs.update()
    drop = []
    for bomb in bombs.copy():
        if bomb.lifetime < 1:
            explosions.add(Explosion(bomb.character.explosion_size, game_settings.explosion_width, screen, bomb))
            explosions.add(Explosion(game_settings.explosion_width, bomb.character.explosion_size, screen, bomb))
            destroyed_obstacles = pygame.sprite.groupcollide(explosions, obstacles, False, True)
            for ashes in destroyed_obstacles:
                drop.append(place_a_treasure(destroyed_obstacles[ashes][0].rect.x, destroyed_obstacles[ashes][0].rect.y,
                                             game_settings, screen, treasures))
            bombs.remove(bomb)
    for explosion in explosions:
        explosion.update()
        if explosion.lifetime < 0:
            explosions.remove(explosion)


def update_screen(game_settings, screen, character, obstacles, bombs, character2, bombs2, hard_obstacles, explosions,
                  treasures):
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
