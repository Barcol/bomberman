from typing import Tuple

import pygame
from pygame import Surface
from pygame.sprite import Group

from settings import Settings


class Character:
    def __init__(self, game_settings: Settings, screen: Surface, coord: Tuple):
        self.screen = screen
        self.image = pygame.image.load("player.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.bombs_allowed = game_settings.bombs_allowed
        self.character_speed = game_settings.character_speed
        self.explosion_size = game_settings.explosion_size
        self.coord = coord
        if self.coord == (0, 0):
            self.rect.left = self.screen_rect.left
            self.rect.top = self.screen_rect.top
        elif self.coord == (1, 1):
            self.rect.right = self.screen_rect.right
            self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.center_height = float(self.rect.centery)
        self.center_copy = self.center
        self.center_height_copy = self.center_height
        self.alive = True
        self.safe_spot = ()
        self.undertextured_counter = 0
        self.moving_right, self.moving_left, self.moving_up, self.moving_down = (False, False, False, False)

    def reset_character_status(self):
        self.image = pygame.image.load("player.bmp")
        if self.coord == (0, 0):
            self.center = self.screen_rect.left + int(self.rect.width / 2)
            self.center_height = self.screen_rect.top + int(self.rect.height/2)
        elif self.coord == (1, 1):
            self.center = self.screen_rect.right - int(self.rect.width / 2)
            self.center_height = self.screen_rect.bottom - int(self.rect.height / 2)

    def die(self):
        self.image = pygame.image.load("dead_player.bmp")
        self.alive = False

    def step_horizontal_alternative(self, obstacles, hard_obstacles, positive_vector):
        self.center += self.character_speed * positive_vector
        if not self.collision_check(obstacles, hard_obstacles):
            self.rect.centerx = self.center

    def step_vertical_alternative(self, obstacles, hard_obstacles, positive_vector):
        self.center_height += self.character_speed * positive_vector
        if not self.collision_check(obstacles, hard_obstacles):
            self.rect.centery = self.center

    def step(self, obstacles, hard_obstacles):
        if self.moving_left and self.alive and (self.rect.left > self.screen_rect.left):
            self.step_horizontal_alternative(obstacles, hard_obstacles, -1)
        if self.moving_right and self.alive and (self.rect.right < self.screen_rect.right):
            self.step_horizontal_alternative(obstacles, hard_obstacles, 1)
        if self.moving_up and self.alive and (self.rect.top > self.screen_rect.top):
            self.step_vertical_alternative(obstacles, hard_obstacles, -1)
        if self.moving_down and self.alive and (self.rect.bottom < self.screen_rect.bottom):
            self.step_vertical_alternative(obstacles, hard_obstacles, 1)

    def update(self, obstacles: Group, hard_obstacles: Group):
        if not self.collision_check(obstacles, hard_obstacles):
            self.safe_spot = self.center, self.center_height
        else:
            self.undertextured_counter += 1
        if self.undertextured_counter < 1:
            self.step(obstacles, hard_obstacles)
        else:
            self.center, self.center_height = self.safe_spot
            self.undertextured_counter = 0
        self.rect.centerx = self.center
        self.rect.centery = self.center_height

    def collision_check(self, obstacles: Group, hard_obstacles: Group) -> bool:
        for obstacle in obstacles:
            if pygame.sprite.collide_rect(obstacle, self):
                return True
        for obstacle in hard_obstacles:
            if pygame.sprite.collide_rect(obstacle, self):
                return True
        return False

    def blitme(self):
        self.screen.blit(self.image, self.rect)
