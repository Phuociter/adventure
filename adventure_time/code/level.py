import pygame 
import os.path
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Crate, Coin, Palm
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect
from game_data import levels
from moving_terrain import Moving_Terrain
from canon import Canon,Explode,CanonBall
from random import randint

class Level:
    def __init__(self,current_level,surface,create_overworld,change_coins,change_health):
        #general setup
        self.display_surface = surface#Lưu trữ bề mặt hiển thị của level chơi.
        self.world_shift = 0

        #audio all
        self.coins_sound = pygame.mixer.Sound('audio/effects/coin.wav')
        self.stomp_sound = pygame.mixer.Sound('audio/effects/stomp.wav')

        #Overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        #player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.setup_player(player_layout,change_health)

        #user interface
        self.change_coins = change_coins

        #particles
        #dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        #explosion 
        self.explosion_sprites = pygame.sprite.Group()
        
        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')#lưu trữ 1 nhóm sprite

        #terrain moving
        terrain_file = level_data.get('moving_terrain')

        if terrain_file and os.path.exists(terrain_file):
            moving_terrain_layout = import_csv_layout(level_data['moving_terrain'])
            self.terrain_moving_sprites = pygame.sprite.Group()
            self.setup_terrain_moving(moving_terrain_layout)
        else:
            self.terrain_moving_sprites = pygame.sprite.Group()

        #setup canon 
        self.canon_file = level_data.get('canon')
        #khởi tạo nhóm sprite cho đạn canon
        self.canonball_sprites = pygame.sprite.Group()
        
        if self.canon_file and os.path.exists(self.canon_file):

            canon_layout = import_csv_layout(level_data['canon'])
            self.canon_sprites = self.create_tile_group(canon_layout, 'canon')

            canonball_layout = import_csv_layout(level_data['canonball'])
            self.canonball_sprites = self.create_tile_group(canonball_layout, 'canonball')

            explode = import_csv_layout(level_data['explode'])
            self.explode_sprites = self.create_tile_group(explode, 'explode')

        #grass layout
        grass_layout = import_csv_layout(level_data['grass'])#lấy dữ liệu tọa độ level từ file csv sử dụng hàm import import_csv_layout
        self.grass_sprites = self.create_tile_group(grass_layout,'grass')#lưu trữ 1 nhóm sprite
        #coins
        coins_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites  = self.create_tile_group(coins_layout,'coins')#lưu trữ 1 nhóm sprite

        #crates
        crates_layout = import_csv_layout(level_data['crates'])
        self.crates_sprites = self.create_tile_group(crates_layout,'crates')#lưu trữ 1 nhóm sprite

        # fg palm
        fg_palm_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites  = self.create_tile_group(fg_palm_layout,'fg palms')#lưu trữ 1 nhóm sprite

        # bg palm
        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites  = self.create_tile_group(bg_palm_layout,'bg palms')#lưu trữ 1 nhóm sprite

        #enemy
        enemies_layout = import_csv_layout(level_data['enemies'])
        self.enemies_sprites  = self.create_tile_group(enemies_layout,'enemies')#lưu trữ 1 nhóm sprite

        #constraints
        constraints_layout = import_csv_layout(level_data['constraints'])
        self.constraints_sprites  = self.create_tile_group(constraints_layout,'constraints')#lưu trữ 1 nhóm sprite

        #decoration
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 40,level_width)
        self.clouds = Clouds(300,level_width,35)

        self.show_Message = False
        self.message_start_time = pygame.time.get_ticks()
        self.message_duration = 0

    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()#lớp giúp tổ chức và quản lí sprite
        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)

                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                        
                    if type == 'coins':
                        if val == '0': sprite = Coin(tile_size,x,y,'graphics/coins/gold',2)
                        if val == '1': sprite = Coin(tile_size,x,y,'graphics/coins/silver',1)

                    if type == 'crates':
                        sprite = Crate(tile_size,x,y)

                    if type == 'fg palms':
                        if val == '0': sprite = Palm(tile_size,x,y,'graphics/terrain/palm_small',38)						
                        if val == '1': sprite = Palm(tile_size,x,y,'graphics/terrain/palm_large',64)

                    if type == 'bg palms':
                        sprite = Palm(tile_size,x,y,'graphics/terrain/palm_bg',64)

                    if type == 'enemies':
                        sprite = Enemy(tile_size,x,y)

                    if type == 'canon':
                        canon = Canon(tile_size,x,y)
                        sprite = canon
                        canon.fire(self.canonball_sprites,5)

                    if type == 'explode':
                        sprite = Explode(tile_size,x,y)

                    if type == 'canonball':
                        sprite = CanonBall(tile_size, x, y)  # Gán giá trị cho sprite

                    if type == 'constraints':
                        sprite = Tile(tile_size,x,y)
                    
                    sprite_group.add(sprite)
        return sprite_group
    
    def setup_terrain_moving(self,layout):
        sprite_width = 3 * tile_size
        sprite_height = tile_size

        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != '-1' :
                    x = col_index * tile_size
                    y = row_index * tile_size

                    terrain_moving_tile = pygame.image.load('graphics/terrain/terrain_moving.png').convert_alpha()
                    sprite = Moving_Terrain(sprite_width,sprite_height,x,y,terrain_moving_tile)
                    self.terrain_moving_sprites.add(sprite)
    
    def setup_player(self,layout,change_health):
        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x,y),self.display_surface,self.create_jump_particles,change_health)
                    self.player.add(sprite)
                if val == '1':
                    hat_surface = pygame.image.load('graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size,x,y,hat_surface)
                    self.goal.add(sprite)

    def terrain_moving_collision_reverse(self):
        for moving_terrain in self.terrain_moving_sprites:
            colliding_constraints = pygame.sprite.spritecollide(moving_terrain, self.constraints_sprites, False)
            if colliding_constraints:
                    moving_terrain.reverse()

    def enemy_collision_reverse(self):
        for enemy in self.enemies_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraints_sprites,False):
                enemy.reverse()

    def create_jump_particles(self,pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10,5)
        else:
            pos += pygame.math.Vector2(10,-5)
        jump_particle_sprite = ParticleEffect(pos,'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * 3
        collidable_sprites = (self.terrain_sprites.sprites() + self.crates_sprites.sprites() 
                            + self.fg_palm_sprites.sprites() + self.terrain_moving_sprites.sprites())
        
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0: 
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = (self.terrain_sprites.sprites() + self.crates_sprites.sprites() 
        + self.fg_palm_sprites.sprites() + self.terrain_moving_sprites.sprites())
        
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                self.player_on_moving_terrain()
                
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
    
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        
    def player_on_moving_terrain(self):
        player = self.player.sprite
        sprites = self.terrain_moving_sprites.sprites()

        for sprite in sprites :
            if player.collision_rect.colliderect(sprite.rect):
                player.collision_rect.topleft += pygame.math.Vector2(sprite.direction * sprite.speed * -1)
        
    def check_canonball_collissions(self):
        for cannonball in self.canonball_sprites.sprites():
        # Xử lý va chạm với constraints_bomb_sprite
            if pygame.sprite.spritecollide(cannonball, self.constraints_sprites, False):
                cannonball.kill()

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        if player_x  < screen_width / 1 and direction_x  < 0:
            self.world_shift = 3
            player.speed = 0
        elif player_x > screen_width - (screen_width / 1) and direction_x > 0:
            self.world_shift = -3
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 3

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
            self.dust_sprite.add(fall_dust_particle)

    def check_death(self):
            if self.player.sprite.rect.top > screen_height:
                self.create_overworld(self.current_level,0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite,self.goal,False) and len(self.coins_sprites)==0:
            self.create_overworld(self.current_level,self.new_max_level)
            self.show_message = False
        elif pygame.sprite.spritecollide(self.player.sprite,self.goal,False) and len(self.coins_sprites):
            self.show_Message = True
            self.message_start_time = pygame.time.get_ticks()
            self.message_duration = 5000

    def show_message(self, message, position):
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.topright = position
        self.display_surface.blit(text, text_rect)

    def check_coins_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite,self.coins_sprites,True)
        if collided_coins:
            self.coins_sound.play()
            for coin in collided_coins:
                self.change_coins(coin.value)

    def check_enemies_collisions(self):
        enemies_collisions = (pygame.sprite.spritecollide(self.player.sprite,self.enemies_sprites,False) 
                            + pygame.sprite.spritecollide(self.player.sprite,self.canonball_sprites,False))
        if enemies_collisions:
            for enemy in enemies_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.stomp_sound.play()
                    self.player.sprite.direction.y = -13
                    explosion_sprite = ParticleEffect(enemy.rect.center,'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def run(self):
        #run the entire game / level

        #sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface,self.world_shift)

        #bg_palm
        self.bg_palm_sprites.update(self.world_shift)    
        self.bg_palm_sprites.draw(self.display_surface)

        #terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        #terrain moving
        self.terrain_moving_sprites.update(self.world_shift)
        self.terrain_moving_collision_reverse()
        self.terrain_moving_sprites.draw(self.display_surface)

        #enemy
        self.enemies_sprites.update(self.world_shift)
        self.constraints_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemies_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)

        #crate
        self.crates_sprites.update(self.world_shift)
        self.crates_sprites.draw(self.display_surface)

        #grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        #coins
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        #fg_palm
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        #dust paticles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        #canon
        if self.canon_file:
            self.canon_sprites.update(self.world_shift)
            self.canon_sprites.draw(self.display_surface)

            self.canonball_sprites.update(self.world_shift, current_time=pygame.time.get_ticks())
            self.canonball_sprites.draw(self.display_surface)

            for canon in self.canon_sprites.sprites():
                canon.fire(self.canonball_sprites, 5)
            self.check_canonball_collissions()
            
        #player sprtie
        self.player.update()
        self.horizontal_movement_collision()

        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()

        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.check_death()
        self.check_win()

        self.check_coins_collisions()
        self.check_enemies_collisions()

        if self.show_Message:
            if pygame.time.get_ticks() - self.message_start_time < self.message_duration:
                message = "You must pick up all the coins!"
                message_position = (self.player.sprite.rect.right + 330, self.player.sprite.rect.top-20)
                self.show_message(message, message_position)

        #water
        self.water.draw(self.display_surface,self.world_shift)