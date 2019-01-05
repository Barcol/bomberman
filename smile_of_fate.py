import random
from obstacle import Obstacle
import pygame
from character import Character
from pygame.sprite import Group
from pygame import Surface
from settings import Settings


class SmileOfFate:
    def __init__(self, game_settings):
        self.game_settings = game_settings

    def type_of_upgrade(self, character: Character):
        guess = random.randint(0, 3)
        if guess == 0:
            character.character_speed += self.game_settings.character_speed_boost
        if guess in (1, 2):
            character.explosion_size += self.game_settings.explosion_boost
        if guess == 3:
            character.bombs_allowed += self.game_settings.bombs_allowed_boost

    def place_a_treasure(self, drop_x: int, drop_y: int, game_settings: Settings, screen: Surface, treasures: Group):
        if random.randint(0, 10) < 5:
            treasure = Obstacle(game_settings, screen, "treasure.bmp")
            treasure.rect.x = drop_x
            treasure.rect.y = drop_y
            treasures.add(treasure)

    def player_collected_treasure(self, character, treasures):
        for treasure in treasures:
            if pygame.sprite.collide_rect(character, treasure):
                treasures.remove(treasure)
                self.type_of_upgrade(character)
