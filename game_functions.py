from typing import List

import pygame
from pygame import Surface
from pygame.sprite import Group

from bomb import Bomb
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
            bomb_blow(bombs, game_settings, screen, explosions, obstacles, treasures, smile_of_fate, bomb, drop)
    for explosion in explosions:
        explosion.update()
        if explosion.lifetime < 0:
            explosions.remove(explosion)


def bomb_blow(bombs: Group, game_settings: Settings, screen: Surface, explosions: Group, obstacles: Group,
              treasures: Group, smile_of_fate: SmileOfFate, bomb: Bomb, drop: List):
    explosions.add(Explosion(bomb.character.explosion_size, game_settings.explosion_width, screen, bomb))
    explosions.add(Explosion(game_settings.explosion_width, bomb.character.explosion_size, screen, bomb))
    destroyed_obstacles = pygame.sprite.groupcollide(explosions, obstacles, False, True)
    for ashes in destroyed_obstacles:
        drop.append(smile_of_fate.place_a_treasure(destroyed_obstacles[ashes][0].rect.x,
                                                   destroyed_obstacles[ashes][0].rect.y,
                                                   game_settings, screen, treasures))
    bombs.remove(bomb)

