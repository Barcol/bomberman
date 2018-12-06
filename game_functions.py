import sys
import pygame
from bomberman.bomb import Bomb
from bomberman.obstacle import Obstacle


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
    available_space_y = (game_settings.screen_height)
    number_rows = int(available_space_y / (2 * obstacle_height))
    return number_rows


def place_bomb(game_settings, screen, character, bombs):
    if len(bombs) < game_settings.bombs_allowed:
        new_bomb = Bomb(game_settings, screen, character)
        bombs.add(new_bomb)


def get_number_obstacles_x(game_settings, obstacle_width):
    available_space_x = game_settings.screen_width - 2 * obstacle_width
    number_obstacles_x = int(available_space_x/(2*obstacle_width))
    return number_obstacles_x


def create_obstacle(game_settings, screen, obstacles, obstacle_number, row_number):
    obstacle = Obstacle(game_settings, screen)
    obstacle_width = obstacle.rect.width
    obstacle.x = obstacle_width + 2 * obstacle_width * obstacle_number
    obstacle.rect.x = obstacle.x
    obstacle.rect.y = obstacle.rect.height + 2 * obstacle.rect.height * row_number
    obstacles.add(obstacle)


def create_obstacles(game_settings, screen, character, obstacles):
    obstacle = Obstacle(game_settings, screen)
    obstacle_width = obstacle.rect.width
    number_obstacles_x = get_number_obstacles_x(game_settings, obstacle_width)
    number_rows = get_number_rows(game_settings, obstacle.rect.height)
    for row_number in range(number_rows):
        for obstacle_number in range(number_obstacles_x):
            create_obstacle(game_settings, screen, obstacles, obstacle_number, row_number)


def check_keyup_events(event, character):
    if event.key == pygame.K_RIGHT:
        character.moving_right = False
    if event.key == pygame.K_LEFT:
        character.moving_left = False
    if event.key == pygame.K_UP:
        character.moving_up = False
    if event.key == pygame.K_DOWN:
        character.moving_down = False


def check_events(game_settings, screen, character, bombs):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, character, bombs)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, character)


def update_bombs(bombs):
    bombs.update()
    for bomb in bombs.copy():
        if bomb.lifetime < 1:
            bombs.remove(bomb)


def update_screen(game_settings, screen, character, obstacles, bombs):
    screen.fill(game_settings.bg_color)
    for bomb in bombs.sprites():
        bomb.draw_bomb()
    character.blitme()
    obstacles.draw(screen)
    pygame.display.flip()
