import random
import pygame
from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=4)
threshold = -0.095  # threshold for path vs obstacle
scale = 60
border = 5 # border size for tiles

def generate_map(tile_size, screen):
    for x in range(0, screen.get_width(), tile_size):
        for y in range(0, screen.get_height(), tile_size):
            # generate a map using Perlin noise
            val = noise([x/scale, y/scale])#gives value between -1 and 1
            if val > threshold:

                # white tlie for path at (x,y) of size = tile_size
                pygame.draw.rect(screen, (200,212,255), (x, y, tile_size-3, tile_size-3))
            else:
                # black tile for obstacle at (x,y) of size = tile_sizergb(204,231,232)
                pygame.draw.rect(screen, (230,226,255), (x, y, tile_size-border, tile_size-border))

            

    


