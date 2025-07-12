import pygame
import sys
from enviroment import generate_map, plainMap, changeTyoe, setGoal, setStart, Node
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
goalSet = False
startSet = []
paths = [] # yields all the nodes in the path so tha we can iterate over them one at a time
searching = True
mode = 1

# reset and new map functions
def reset(surface, tile_size, map, mode):
    global startSet, goalSet, paths, searching
    
    startSet = []
    goalSet = False
    paths = []
    searching = True
    
    # Redraw the existing map from the stored Node types
    for row in map:
        for node in row:
            pygame.draw.rect(surface, (0, 0, 0), (node.x, node.y, tile_size, tile_size))  # clear tile
            color = (0, 100, 100) if node.type == 0 else (255, 69, 0)
            if mode==0:
              border = 3 if node.type == 0 else 5
            else:
              border = 0 if node.type == 0 else 5
            pygame.draw.rect(surface, color, (node.x, node.y, tile_size - border, tile_size - border))
    
    pygame.display.flip()

def newMap(tile_size):
    global startSet, goalSet, paths, searching, map, surface
    startSet = []
    goalSet = False
    paths = []
    searching = True
    map =[]
    # Clear and redraw the map surface so it’s fresh
    surface.fill((0,0,0))
    map = generate_map(tile_size, surface)
    screen.blit(surface, (0,0))
    pygame.display.flip()
    return map

def dismode(surface, tile_size, map, mode):
    for row in map:
        for node in row:
            pygame.draw.rect(surface, (0, 0, 0), (node.x, node.y, tile_size, tile_size))  # clear tile
            color = (0, 100, 100) if node.type == 0 else (255, 69, 0)
            if mode==0:
              border = 3 if node.type == 0 else 5 
            else:
              border = 0 if node.type == 0 else 5
            pygame.draw.rect(surface, color, (node.x, node.y, tile_size - border, tile_size - border))


# main loop-keeps the window open and the simulation running
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                pos = pygame.mouse.get_pos()
                if not goalSet:
                    goal = setGoal(surface, tile_size, map, pos)
                    if goal != None:
                        goalSet = True
                else:
                    start = setStart(surface, tile_size, map, pos, goal)
                    if start != None:
                        startSet.append(start)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paths = []
                for start in startSet:
                    path = a_star(start, goal, map, surface, tile_size)
                    paths.append(path)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                mode = 1 # reset changes mode back to default
                reset(surface, tile_size, map, mode)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                mode = 1 # new map shold also be in default mode at first
                surface.fill((0,0,0))
                map = generate_map(tile_size, surface)
                screen.blit(surface, (0,0))
                pygame.display.flip()

                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                # changing the display mode
                mode = 0 if mode == 1 else 1 # surprised this works
                dismode(surface, tile_size, map, mode)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                mode = 1 # plain map too in default mode at first
                surface.fill((0,0,0))
                map = plainMap(surface, tile_size, mode)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3: # right click
                pos = pygame.mouse.get_pos()
                changeTyoe(map, surface, tile_size, pos, mode)







   #fill the screen with black color
    screen.fill((0, 0, 0))
    screen.blit(surface, (0, 0)) #draw the map on the screen
   # start_pt(screen, tile_size) #generate the start point on the map

    for path in paths:
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