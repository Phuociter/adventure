import pygame
from tiles import AnimateTile

class Enemy(AnimateTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, 'graphics/enemy/run')
        self.rect.y += size - self.image.get_size()[1]
        self.speed = 3

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0 :
            self.image  = pygame.transform.flip(self.image,True,False)

    def reverse(self):
        self.speed *= -1

    def update(self,shift):
        self.rect.x += shift# quái di chuyển có tốc độ bằng tốc độ của camera
        self.animate()
        self.move()
        self.reverse_image()
