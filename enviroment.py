import random
import pygame
from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=4)
threshold = -0.095  # threshold for path vs obstacle
scale = 60
border = 6 # border size for tiles
map = [] # to store the generated map

def generate_map(tile_size, surface):
    count = 0
    print(count)
    for x in range(0, surface.get_width(), tile_size):
        row = [] # to store the row of tiles
        for y in range(0, surface.get_height(), tile_size):
            # generate a map using Perlin noise
            val = noise([x/scale, y/scale])#gives value between -1 and 1
            row.append(0 if val > threshold else 1) # 0 for path, 1 for obstacl           
            # map generation based on the threshold so that we can control the number of each type of tiles
            if val > threshold:

                # cyan tlie for path at (x,y) of size = tile_size
                pygame.draw.rect(surface, (0, 100, 100), (x, y, tile_size-3, tile_size-3))
            else:
                # magma tile for obstacle at (x,y) of size = tile_sizergb(204,231,232)
                pygame.draw.rect(surface, (255, 69, 0), (x, y, tile_size-border, tile_size-border))
        map.append(row)
  

def start_pt(surface, tile_size): 
    #generate random start point
    found = False
    nodes = 0
    start_x = 0
    start_y = 0 
    while not found:
        if nodes == 0:
           #random x coordinate on the map
           x = random.randint(0, len(map)-1)
           #random y coordinate on the row x(map[x])
           y = random.randint(0, len(map[x])-1)
           #check if the tile at (x,y ) is a path(0) or not(1)
           if (map[x][y]==0):
               # x and y are the coodinates of the map array not literal coordinates of the pixels on screen
               # multiply by tile_size(32) to get the pixel coordinates 
               # 0*32=0, 1*32=32, 2*32=64, etc
               #gives (0,0), (32,0), (64,0), etc which are the pixel coordinates of the tile
               pygame.draw.rect(surface, (0, 0, 0), (x * tile_size, y * tile_size, tile_size, tile_size))
               start_x, start_y = x * tile_size, y * tile_size
               nodes += 1
        else:
            x = random.randint(0, len(map)-1)
            y = random.randint(0, len(map[x])-1)
            # with the previous check also check whether or not the tile is the start tile
            if (map[x][y]==0 and x != start_x // tile_size and y != start_y // tile_size):
                pygame.draw.rect(surface, (255, 255, 255), (x * tile_size, y * tile_size, tile_size, tile_size))
                found = True
                break
        
    

    


