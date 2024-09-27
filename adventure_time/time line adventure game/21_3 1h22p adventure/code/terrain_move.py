import pygame
from tiles import StaticTile

class Terrain_Moving(StaticTile):

    def __init__(self, size, x, y,surface):
        super().__init__(size, x, y,surface)
        self.speed = 3

    def move(self):
        self.rect.x += self.speed
            
    def reverse(self):
        self.speed *= -1

    def update(self,shift):
        self.rect.x += shift
        self.move()
