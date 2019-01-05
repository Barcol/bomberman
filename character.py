import pygame
from typing import Tuple
from settings import Settings
from pygame import Surface
from pygame.sprite import Group


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

    def update(self, obstacles: Group, hard_obstacles: Group):
        if self.moving_right and (self.rect.right < self.screen_rect.right) and self.alive:
            if self.collision_check(obstacles, hard_obstacles):
                self.center += self.character_speed
            else:
                self.center -= 2 * self.character_speed
                self.moving_right = False
        if self.moving_left and (self.rect.left > self.screen_rect.left) and self.alive:
            if self.collision_check(obstacles, hard_obstacles):
                self.center -= self.character_speed
            else:
                self.center += 2 * self.character_speed
                self.moving_left = False
        if self.moving_up and (self.rect.top > self.screen_rect.top) and self.alive:
            if self.collision_check(obstacles, hard_obstacles):
                self.center_height -= self.character_speed
            else:
                self.center_height += 2 * self.character_speed
                self.moving_up = False
        if self.moving_down and (self.rect.bottom < self.screen_rect.bottom) and self.alive:
            if self.collision_check(obstacles, hard_obstacles):
                self.center_height += self.character_speed
            else:
                self.center_height -= 2 * self.character_speed
                self.moving_down = False

        self.rect.centerx = self.center
        self.rect.centery = self.center_height

    def collision_check(self, obstacles: Group, hard_obstacles: Group) -> bool:
        for obstacle in obstacles:
            if pygame.sprite.collide_rect(obstacle, self):
                return False
        for obstacle in hard_obstacles:
            if pygame.sprite.collide_rect(obstacle, self):
                return False
        return True

    def blitme(self):
        self.screen.blit(self.image, self.rect)
