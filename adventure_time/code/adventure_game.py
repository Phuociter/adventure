from settings import*
from level import Level
from overworld import Overworld
from ui import UI
import pygame, sys

class Game:
    def __init__(self):
        #game attributes
        self.max_level = 0
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0

        #overworld creation
        self.overworld = Overworld(0,self.max_level,screen,self.create_level)
        self.status = 'overworld'

        #user interface
        self.ui = UI(screen)

    def create_level(self,current_level):
        self.level = Level(current_level,screen,self.create_overworld,self.change_coins,self.change_health)
        self.status = 'level'

    def create_overworld(self,current_level,new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
        self.status = 'overworld'     

    def change_coins(self,amount):
        self.coins += amount

    def change_health(self,amout):
        self.cur_health += amout

    def check_game_over(self):
        if self.cur_health <= 0 :
            self.cur_health = 100
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(0,self.max_level,screen,self.create_level)
            self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
            self.coins = 0
            self.cur_health = 100
        else:
            self.level.run()
            self.ui.show_health(self.cur_health,self.max_health )
            self.ui.show_coins(self.coins)
            self.check_game_over()

#PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
FPS = 60
clock = pygame.time.Clock()
game = Game()
run = True
while run:  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit
            run = False
    game.run()
    pygame.display.update()
    clock.tick(FPS)