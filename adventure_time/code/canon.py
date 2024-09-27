import pygame
from tiles import AnimateTile

class Canon(AnimateTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, "graphics_2/7-Objects/16-Enemy-Cannon/2-Attack")
        self.rect.y += size - self.image.get_size()[1]
        # self.speed =   # Đặt vị trí ban đầu của pháo
        self.last_fire_time = 1
        self.fire_rate = 0.364 # Tốc độ bắn: 1 viên đạn mỗi giây

    def fire(self, all_sprites, size):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fire_time >= 1000/self.fire_rate:
            if self.animation_completed():
            # Thời gian hiện tại
            # Tạo một viên đạn mới nếu đã đủ thời gian
                cannonball = CanonBall(size, self.rect.x, self.rect.centery)
                all_sprites.add(cannonball)
                self.last_fire_time = current_time  # Cập nhật thời gian cuối cùng bắn

    def animation_completed(self):
        # Kiểm tra xem animation của canon đã hoàn thành chưa
        return self.frame_index >= len(self.frames)-3

class CanonBall(AnimateTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, "graphics_2/7-Objects/16-Enemy-Cannon/3-Cannon Ball")
        self.rect.y += size - self.image.get_size()[1]
        self.speed = 2

    def move(self):
        self.rect.x -= self.speed

    def update(self, shift, current_time):
        self.rect.x += shift
        self.animate()
        self.move()  # Di chuyển viên đạn
        
class Explode(AnimateTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, "graphics_2/7-Objects/1-BOMB/3-Explotion")
        self.rect.y += size - self.image.get_size()[1]
        
        # Thời gian bắt đầu hiệu ứng nổ
        def update(self, shift):
        # Kiểm tra nếu đã đủ thời gian để hiệu ứng nổ biến mất
            self.rect.x += shift
            self.animate()
            # Di chuyển hiệu ứng nổ
