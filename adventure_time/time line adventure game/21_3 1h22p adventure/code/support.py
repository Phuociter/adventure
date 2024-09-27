from settings import tile_size
from csv import reader
from os import walk
import pygame
#hàm lấy dữ liệu từ file csv : in ra bộ khung cho địa hình map  
def import_folder(path):
    surface_list =[]
    for _,__,image_files in walk(path):#folder name,sub folder, image files
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level =  reader(map,delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)
    cut_tiles = []

    for col in range(tile_num_y):
        for row in range(tile_num_x):
            x = row * tile_size
            y = col * tile_size
            new_surface = pygame.Surface((tile_size,tile_size),flags = pygame.SRCALPHA)
            new_surface.blit(surface,(0,0),pygame.Rect(x,y,tile_size,tile_size))#đặt đồ họa ở góc trên cùng bên trái để cắt
            cut_tiles.append(new_surface)
    return cut_tiles
