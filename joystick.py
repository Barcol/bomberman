import pygame


class Joystick:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count():
            pygame.joystick.Joystick(0).init()
            self.joystick = pygame.joystick.Joystick(0)
        else:
            self.joystick = None

    def is_joystick(self):
        return self.joystick
