from settings import*
from level import Level
import pygame, sys#2:22:11


#PYGAME SETUP
pygame.init()
# screen_width = 1200
# screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
level = Level(level_map,screen)
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit
            run = False
    screen.fill('black')
    level.run()
    pygame.display.update()
    clock.tick(60)