import pygame
import sys
from enviroment import generate_map

# initialize simulation
pygame.init()

#display setup
width =1024
height = 768
screen = pygame.display.set_mode((width, height))#resolution-->4:3(1024x768)
pygame.display.set_caption("Self-Driving Car Simulation")

#loading assets
car = pygame.image.load("Mark III_Woods.png")
grass = pygame.image.load("grass.png")
tile_width = grass.get_width()
tile_height = grass.get_height()
# main loop-keeps the window open and the simulation running
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


   #fill the screen with grass
    generate_map(tile_width, tile_height, screen, grass)

    # update the display
    pygame.display.flip()

# quit pygame
pygame.quit()