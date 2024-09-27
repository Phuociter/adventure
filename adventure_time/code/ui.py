import pygame

class UI:
    def __init__(self,surface):
        #setup
        self.display_surface = surface
        
        #health
        self.health_bar  = pygame.image.load('graphics/ui/health_bar.png').convert_alpha()
        self.health_bar_topleft = (64,39)
        self.bar_max_width = 152
        self.bar_max_height = 4

        #coins
        self.coins = pygame.image.load('graphics/ui/coin.png').convert_alpha()
        self.coin_rect = self.coins.get_rect(topleft = (30,71))
        self.font = pygame.font.Font('graphics/ui/ARCADEPI.ttf',30)

    def show_health(self,current,full):
        self.display_surface.blit(self.health_bar,(30,10))
        current_health_ratio = current/full
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect(self.health_bar_topleft,(current_bar_width,self.bar_max_height))
        pygame.draw.rect(self.display_surface,'#dc4949',health_bar_rect)

    def show_coins(self,amount):
        self.display_surface.blit(self.coins,self.coin_rect)
        coin_amount_surf = self.font.render(str(amount),False,'#33323d')
        coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 5,self.coin_rect.centery + 1))
        self.display_surface.blit(coin_amount_surf,coin_amount_rect)
