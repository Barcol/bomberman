import sys
import pygame
import math
from bomberman.bomb import Bomb
from bomberman.obstacle import Obstacle
from bomberman.explosions import Explosion


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
    if len(bombs) < game_settings.bombs_allowed:
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
            create_obstacle(game_settings, screen, obstacles, obstacle_number, 1 + (2 * row_number), obstacle_width, "hard_obstacle.bmp")


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


def check_joystick_axis_events(axis_x, axis_y, character):
    if (axis_x < 0.4) and (axis_x > -0.4):
        character.moving_right = False
        character.moving_left = False
    if axis_x > 0.4:
        character.moving_right = True
        character.moving_left = False
    if axis_x < -0.4:
        character.moving_left = True
        character.moving_right = False
    if (axis_y < 0.4) and (axis_y > -0.4):
        character.moving_up = False
        character.moving_down = False
    if axis_y > 0.4:
        character.moving_up = False
        character.moving_down = True
    if axis_y < - 0.4:
        character.moving_down = False
        character.moving_up = True


def check_joystick_events(character, joystick):
    check_joystick_axis_events(joystick.get_axis(0), joystick.get_axis(1), character)


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


def update_bombs(bombs, game_settings, screen, explosions, obstacles):
    bombs.update()
    for bomb in bombs.copy():
        if bomb.lifetime < 1:
            explosions.add(Explosion(game_settings.explosion_size_x, 20, screen, bomb))
            explosions.add(Explosion(20, game_settings.explosion_size_y, screen, bomb))
            pygame.sprite.groupcollide(explosions, obstacles, True, True)
            bombs.remove(bomb)


def update_screen(game_settings, screen, character, obstacles, bombs, character2, bombs2, hard_obstacles):
    screen.fill(game_settings.bg_color)
    for bomb in bombs.sprites():
        bomb.draw_bomb()
    for bomb in bombs2.sprites():
        bomb.draw_bomb()
    character.blitme()
    character2.blitme()
    obstacles.draw(screen)
    hard_obstacles.draw(screen)
    pygame.display.flip()
