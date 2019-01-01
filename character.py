import pygame


class Character:
    def __init__(self, game_settings, screen, coord):
        self.screen = screen
        self.image = pygame.image.load('player.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.game_settings = game_settings
        if coord == (0, 0):
            self.rect.left = self.screen_rect.left
            self.rect.top = self.screen_rect.top
        elif coord == (1, 1):
            self.rect.right = self.screen_rect.right
            self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)
        self.center_height = float(self.rect.centery)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self, obstacles, hard_obstacles):
        if self.moving_right and (self.rect.right < self.screen_rect.right):
            if self.collision_check(obstacles, hard_obstacles):
                self.center += self.game_settings.character_speed
            else:
                self.center -= 2 * self.game_settings.character_speed
                self.moving_right = False
        if self.moving_left and (self.rect.left > self.screen_rect.left):
            if self.collision_check(obstacles, hard_obstacles):
                self.center -= self.game_settings.character_speed
            else:
                self.center += 2 * self.game_settings.character_speed
                self.moving_left = False
        if self.moving_up and (self.rect.top > self.screen_rect.top):
            if self.collision_check(obstacles, hard_obstacles):
                self.center_height -= self.game_settings.character_speed
            else:
                self.center_height += 2 * self.game_settings.character_speed
                self.moving_up = False
        if self.moving_down and (self.rect.bottom < self.screen_rect.bottom):
            if self.collision_check(obstacles, hard_obstacles):
                self.center_height += self.game_settings.character_speed
            else:
                self.center_height -= 2 * self.game_settings.character_speed
                self.moving_down = False

        self.rect.centerx = self.center
        self.rect.centery = self.center_height

    def collision_check(self, obstacles, hard_obstacles):
        for obstacle in obstacles:
            if pygame.sprite.collide_rect(obstacle, self):
                return False
        for obstacle in hard_obstacles:
            if pygame.sprite.collide_rect(obstacle, self):
                return False
        return True

    def blitme(self):
        self.screen.blit(self.image, self.rect)
