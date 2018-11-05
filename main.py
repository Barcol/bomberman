import sys
import pygame

pygame.init()

size = width, height = 1280, 640
speed = [1, 0]
black = 58, 125, 241

print(isinstance(size, tuple))

screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()

print(type(ball))
print(type(ballrect))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            speed[1] -= 1
        if event.type == pygame.KEYUP:
            speed[1] += 1
        if event.type == pygame.MOUSEBUTTONUP:
            speed[0] -= 1
        #if event.type == pygame.KEYUP:
        #    speed[0] += 1

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
