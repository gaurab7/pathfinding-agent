import pygame
import sys
from enviroment import generate_map, start_pt, Node
from pathfinding import a_star, draw_path

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
neon_green = (57, 255, 20)


#load the map, start point and goal 
surface = pygame.Surface((width, height)) #create a surface for the map
# made the mistake of calling this inside the main while loop, which caused the map to be generated repeatedly
# was not visible but when printed the map to console, found that it was contionusly generating multiople maps
#so moved it outside the main loop to draw the map only once
map = generate_map(tile_size, surface) #generate the map using Perlin noise
start, goal = start_pt(surface, tile_size, map) #generate the start point on the map surface
path = a_star(start, goal, map, surface, tile_size) # yields all the nodes in the path so tha we can iterate over them one at a time
searching = True



# main loop-keeps the window open and the simulation running
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


   #fill the screen with black color
    screen.fill((20, 20, 20))
    screen.blit(surface, (0, 0)) #draw the map on the screen
   # start_pt(screen, tile_size) #generate the start point on the map

    if searching:
        try:
            node = next(path)
            if isinstance(node, Node):  # path is found
                if (node.x, node.y) not in [(start.x, start.y), (goal.x, goal.y)]:
                    pygame.draw.rect(surface, neon_green, (node.x, node.y, tile_size, tile_size))
                    pygame.display.update()
                    
        except StopIteration:
            searching = False
    # update the display
    pygame.display.flip()
    clock.tick(fps) #60 frames per second

# quit pygame
pygame.quit()