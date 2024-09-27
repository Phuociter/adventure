import pygame
from tiles import StaticTile

class Terrain_Moving_Tile(pygame.sprite.Sprite):

    def __init__(self, width,heght, x, y,surface):
        super().__init__()
        # super().__init__((width,heght), x, y,surface)
        self.image = pygame.Surface((width,heght))# Tạo một bề mặt (Surface) với kích thước (size, size)
        self.rect = self.image.get_rect(topleft=(x,y))
class Terrain_Moving(Terrain_Moving_Tile):
    
    def __init__(self, width,heght, x, y,surface):
        super().__init__(width,heght, x, y,surface)
        self.image = surface
        self.speed = 1

    def move(self):
        self.rect.x += self.speed 
            
    def reverse(self):
        self.speed *= -1

    def update(self,shift):
        self.rect.x += shift
        self.move()
