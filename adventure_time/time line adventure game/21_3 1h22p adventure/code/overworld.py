import pygame#XEM LẠI HẾT FILE NÀY
from game_data import levels
from support import import_folder
from decoration import Sky

class Node(pygame.sprite.Sprite):
    def __init__(self,pos,status,icon_speed,path):
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        if status == "available":
            self.status = 'available'
        else:
            self.status = 'locked'

        self.rect =self.image.get_rect(center = pos)
        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed / 2),self.rect.centery - (icon_speed / 2),icon_speed,icon_speed)

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self):
        if self.status == 'available':
            self.animate()
        else:
            tint_surf = self.image.copy()
            tint_surf.fill('black',None,pygame.BLEND_RGB_MULT)
            self.image.blit(tint_surf,(0,0))

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image =pygame.image.load('graphics/overworld/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
    
    def update(self):
        self.rect.center = self.pos

class Overworld:

    def __init__(self,start_level,max_level,surface,create_level):
        #setup
        self.display_surface = surface
        self.current_levels = start_level
        self.max_level = max_level
        self.create_level = create_level

        #movement logic
        self.moving = False
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 8

        #sprites
        self.setup_nodes()
        self.setup_icon()
        self.sky = Sky(8)

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'],'available',self.speed,node_data['node_graphics'])
            else:
                node_sprite = Node(node_data['node_pos'],'locked',self.speed,node_data['node_graphics'])
            self.nodes.add(node_sprite)

    def draw_paths(self):
        if self.max_level > 0:
            points = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.max_level]
            pygame.draw.lines(self.display_surface, '#a04f45', False, points, 6)

    def setup_icon(self):#xem lại hàm này
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_levels].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.moving:
            if keys[pygame.K_RIGHT] and self.current_levels < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_levels += 1#xem lại hàm này
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_levels > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_levels -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_levels)

    def update_icon_pos(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_levels]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving  = False
                self.move_direction = pygame.math.Vector2(0,0)#xem lại hàm này

    def get_movement_data(self,target):#xem lại hàm này
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_levels].rect.center)

        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_levels + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_levels - 1].rect.center)

        return(end - start).normalize()

    def run(self):
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.nodes.update()
        
        self.sky.draw(self.display_surface)
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)