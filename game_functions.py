import pygame
from pygame import Surface
from pygame.sprite import Group

from character import Character
from explosions import Explosion
from settings import Settings
from smile_of_fate import SmileOfFate


def kill_your_heroes(explosions: Group, character: Character, character2: Character):
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
