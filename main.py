import pygame
import sys
from enviroment import generate_map

# initialize simulation
pygame.init()

#display setup
width =1024
height = 768
tile_size = 32 #size of each tile in pixels
screen = pygame.display.set_mode((width, height))#resolution-->4:3(1024x768)
fps = 60
clock = pygame.time.Clock()
pygame.display.set_caption("Self-Driving Car Simulation")



# main loop-keeps the window open and the simulation running
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


   #fill the screen with black color
    screen.fill((0, 0, 0))
    generate_map(tile_size, screen)
    # update the display
    pygame.display.flip()
    clock.tick(fps) #60 frames per second

# quit pygame
pygame.quit()