import random
from perlin_noise import PerlinNoise



def generate_map(tile_width, tile_height, screen, tile):
    for y in range(0, screen.get_height(), tile_height):
         for x in range(0, screen.get_width(), tile_width):
             screen.blit(tile, (x, y))

#path gen
noise = PerlinNoise(octaves=4)
