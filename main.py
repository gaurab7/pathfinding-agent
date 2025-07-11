import pygame
import sys
from enviroment import generate_map, start_pt

# initialize simulation
pygame.init()

#display setup
width =1024
height = 768
tile_size = 16 #size of each tile in pixels
screen = pygame.display.set_mode((width, height))#resolution-->4:3(1024x768)
fps = 60
clock = pygame.time.Clock()
pygame.display.set_caption("Pathfinding Simulation") #title of the window


#load the map, start point and goal 
surface = pygame.Surface((width, height)) #create a surface for the map
# made the mistake of calling this inside the main while loop, which caused the map to be generated repeatedly
# was not visible but when printed the map to console, found that it was contionusly generating multiople maps
#so moved it outside the main loop to draw the map only once
generate_map(tile_size, surface) #generate the map using Perlin noise
start, goal = start_pt(surface, tile_size) #generate the start point on the map surface

# main loop-keeps the window open and the simulation running
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


   #fill the screen with black color
    screen.fill((0, 0, 0))
    screen.blit(surface, (0, 0)) #draw the map on the screen
   # start_pt(screen, tile_size) #generate the start point on the map
    # update the display
    pygame.display.flip()
    clock.tick(fps) #60 frames per second

# quit pygame
pygame.quit()