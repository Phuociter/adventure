import pygame

class Moving_Terrain(pygame.sprite.Sprite):
    def __init__(self, width,heght, x, y,surface):
        super().__init__()
        self.image = pygame.Surface((width,heght))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.image = surface
        self.speed = 3
        self.direction = pygame.math.Vector2(0,0)

    def move(self):
        self.rect.x += self.speed 
            
    def reverse(self):
        self.direction.x = -1
        self.speed *= self.direction.x

    def update(self,shift):
        self.rect.x += shift
        self.move()

