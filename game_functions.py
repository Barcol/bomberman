import math
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


def get_number_rows(game_settings, obstacle_height):
    available_space_y = game_settings.screen_height
    number_rows = int(available_space_y / obstacle_height)
    return number_rows


def place_bomb(game_settings, screen, character, bombs):
    if len(bombs) < character.bombs_allowed:
        new_bomb = Bomb(game_settings, screen, character)
        bombs.add(new_bomb)


def get_number_obstacles_x(game_settings, obstacle_width, tabulator):
    available_space_x = game_settings.screen_width - obstacle_width
    number_obstacles_x = int(math.ceil(available_space_x/(2 * obstacle_width)))
    if not tabulator:
        number_obstacles_x += 1
    return number_obstacles_x


def create_obstacle(game_settings, screen, obstacles, obstacle_number, row_number, tabulator, spirit):
    obstacle = Obstacle(game_settings, screen, spirit)
    obstacle_width = obstacle.rect.width
    obstacle.x = tabulator + 2 * obstacle_width * obstacle_number
    obstacle.rect.x = obstacle.x
    obstacle.rect.y = obstacle.rect.height * row_number
    obstacles.add(obstacle)


def create_hard_obstacles(game_settings, screen, obstacles):
    obstacle = Obstacle(game_settings, screen, "hard_obstacle.bmp")
    obstacle_width = obstacle.rect.width
    number_rows = get_number_rows(game_settings, obstacle.rect.height)
    for row_number in range(math.floor(number_rows/2)):
        for obstacle_number in range(get_number_obstacles_x(game_settings, obstacle_width, 0) - 1):
            create_obstacle(game_settings, screen, obstacles, obstacle_number, 1 + (2 * row_number), obstacle_width,
                            "hard_obstacle.bmp")


def create_obstacles(game_settings, screen, obstacles):
    obstacle = Obstacle(game_settings, screen, "obstacle.bmp")
    obstacle_width = obstacle.rect.width
    number_rows = get_number_rows(game_settings, obstacle.rect.height)
    for row_number in range(number_rows):
        if (row_number % 2) != 0:
            tabulator = 0
        else:
            tabulator = obstacle.rect.height
        for obstacle_number in range(get_number_obstacles_x(game_settings, obstacle_width, tabulator)):
            if (row_number == 0) or (row_number == 1):
                obstacle_number += 1
            if (row_number == number_rows - 1) or (row_number == (number_rows - 2)):
                obstacle_number -= 1
            create_obstacle(game_settings, screen, obstacles, obstacle_number, row_number, tabulator, "obstacle.bmp")


def check_keyup_events(event, character):
    if event.key == pygame.K_RIGHT:
        character.moving_right = False
    if event.key == pygame.K_LEFT:
        character.moving_left = False
    if event.key == pygame.K_UP:
        character.moving_up = False
    if event.key == pygame.K_DOWN:
        character.moving_down = False


def check_joystick_axis_events(axis_x, axis_y, character, latest_choice, latest_choice_y):
    if (axis_x < 0.4) and (axis_x > -0.4) and (latest_choice != 0):
        character.moving_right = False
        character.moving_left = False
        latest_choice = 0
    if axis_x > 0.4 and (latest_choice != 1):
        character.moving_right = True
        character.moving_left = False
        latest_choice = 1
    if axis_x < -0.4 and (latest_choice != 2):
        character.moving_left = True
        character.moving_right = False
        latest_choice = 2
    if (axis_y < 0.4) and (axis_y > -0.4) and (latest_choice_y != 3):
        character.moving_up = False
        character.moving_down = False
        latest_choice_y = 3
    if axis_y > 0.4 and (latest_choice_y != 4):
        character.moving_up = False
        character.moving_down = True
        latest_choice_y = 4
    if axis_y < - 0.4 and (latest_choice_y != 5):
        character.moving_down = False
        character.moving_up = True
        latest_choice_y = 5
    return latest_choice, latest_choice_y


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
        print("speed bonus!")
        character.character_speed += 0.4
    if guess in (1, 2):
        character.explosion_size += 25
        print("attack bonus!")
    if guess == 3:
        print("bomb number bonus!")
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
