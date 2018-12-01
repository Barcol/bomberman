import pygame

class Character():
    def __init__(self, game_settings, screen):
        self.screen = screen
        self.image = pygame.image.load('player.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.game_settings = game_settings

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)
        self.center_height = float(self.rect.centery)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False


    def update(self):
        if self.moving_right and (self.rect.right < self.screen_rect.right):
            self.center += self.game_settings.character_speed
        if self.moving_left and (self.rect.left > self.screen_rect.left):
            self.center -= self.game_settings.character_speed
        if self.moving_up and (self.rect.top > self.screen_rect.top):
            self.center_height -= self.game_settings.character_speed
        if self.moving_down and (self.rect.bottom < self.screen_rect.bottom):
            self.center_height += self.game_settings.character_speed

        self.rect.centerx = self.center
        self.rect.centery = self.center_height

    def blitme(self):
        self.screen.blit(self.image, self.rect)