import sys
import pygame
from bomberman.bomb import Bomb


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
    if len(bombs) < game_settings.bombs_allowed:
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


def update_screen(game_settings, screen, character, obstacle, bombs):
    screen.fill(game_settings.bg_color)
    for bomb in bombs.sprites():
        bomb.draw_bomb()
    character.blitme()
    obstacle.blitme()
    pygame.display.flip()