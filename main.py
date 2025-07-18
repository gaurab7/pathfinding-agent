import pygame
import sys
from enviroment import generate_map, plainMap, changeTyoe, setGoal, setStart, Node
from pathfinding import a_star, dijkstra

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
grass = (107,142,37)
obstacles = (125, 125, 125)
muddy = (101, 67, 33)


#load the map, start point and goal 
surface = pygame.Surface((width, height)) #create a surface for the map
# made the mistake of calling this inside the main while loop, which caused the map to be generated repeatedly
# was not visible but when printed the map to console, found that it was contionusly generating multiople maps
#so moved it outside the main loop to draw the map only once
mapType='prcdl'
map = generate_map(tile_size, surface) #generate the map using Perlin noise
startSet = False
goalSet =  False
searching = True
move = False
prev = None
changeMade = False
mode = 1
method = None # 0 for astar 1 for dijkstra
# reset and new map functions

# reset doesnt undo changes made to the map, it just deletes the previous simulation
def reset(surface, tile_size, map, mode):
    global startSet, goalSet, searching, prev, method

    prev = None
    
    startSet = False
    goalSet = False
    searching = True
    method = None
    
    # Redraw the existing map from the stored Node types
    for row in map:
        for node in row:
            pygame.draw.rect(surface, (0, 0, 0), (node.x, node.y, tile_size, tile_size))  # clear tile
            if node.type == 0: color = grass
            elif node.type == 2: color = muddy
            else: color = obstacles
            if mode==0:
              border = 3 if node.type == 0 or node.type == 2 else 5
            else:
              border = 0 if node.type == 0 or node.type == 2 else 5
            pygame.draw.rect(surface, color, (node.x, node.y, tile_size - border, tile_size - border))
    
    pygame.display.flip()


def dismode(surface, tile_size, map, mode):
    for row in map:
        for node in row:
            pygame.draw.rect(surface, (0, 0, 0), (node.x, node.y, tile_size, tile_size))  # clear tile
            if node.type == 0: color = grass
            elif node.type == 2: color = muddy
            else: color = obstacles
            if mode==0:
              border = 3 if node.type == 0 else 5 
            else:
              border = 0 if node.type == 0 else 5
            pygame.draw.rect(surface, color, (node.x, node.y, tile_size - border, tile_size - border))

def drawPath():
    global searching, path, move
    try:
        node = next(path)
        if isinstance(node, Node) and (node.x, node.y) not in [(start.x, start.y), (goal.x, goal.y)]:
         pygame.draw.rect(surface, neon_green, (node.x, node.y, tile_size, tile_size))
    except StopIteration:
            searching = True
            move = True
            
# for reseting tile colors only
def softR(surface, tile_size, map, mode):
    
    # Redraw the existing map from the stored Node types
    for row in map:
        for node in row:
            pygame.draw.rect(surface, (0, 0, 0), (node.x, node.y, tile_size, tile_size))  # clear tile
            if node.type == 0: color = grass
            elif node.type == 2: color = muddy
            else: color = obstacles
            if mode==0:
              border = 3 if node.type == 0 or node.type == 2 else 5
            else:
              border = 0 if node.type == 0 or node.type == 2 else 5
            pygame.draw.rect(surface, color, (node.x, node.y, tile_size - border, tile_size - border))
    
    pygame.display.flip()



# main loop-keeps the window open and the simulation running
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #set goal then start positions-->Mouse left click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                pos = pygame.mouse.get_pos()
                if not startSet:
                    start = setStart(surface, tile_size, map, pos)
                    if start != None:
                        startSet = True
                elif not goalSet  and prev == None:
                    goal = setGoal(surface, tile_size, map, pos, start)
                    prev = goal
                    if goal != None:
                        goalSet = True
                elif goalSet and prev != None:
                    softR(surface,tile_size,map,mode)
                    pygame.draw.rect(surface, (250,250,250), (start.x, start.y, tile_size,tile_size))
                    color = grass if prev.type==0 else muddy
                    pygame.draw.rect(surface, color, (prev.x, prev.y, tile_size, tile_size))
                    goal = setGoal(surface, tile_size, map, pos, start)
                    prev = goal
                    if method == 0:
                      path = a_star(start, goal, map, surface, tile_size)
                    else:
                        path = dijkstra(surface, tile_size, map, start, goal)
                    searching=False
                    
                    

        
        # start a star simulation-->SPACE
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                path = a_star(start, goal, map, surface, tile_size)
                searching=False
                method = 0

         # start a star simulation-->D
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                path = dijkstra( surface, tile_size, map, start, goal)
                searching=False
                method = 1

 
                

             
        
        # reset simulation --> r
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                mode = 1 # reset changes mode back to default
                reset(surface, tile_size, map, mode)

        # switch diplay mode-->m        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                # changing the display mode
                mode = 0 if mode == 1 else 1 # surprised this works
                dismode(surface, tile_size, map, mode)

        # switch map mode--> shift+m
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                map = []
                if mapType == 'prcdl':
                 mode = 1 # plain map too in default mode at first
                 surface.fill((0,0,0))
                 map = plainMap(surface, tile_size, mode)
                 mapType = 'plain'
                elif mapType == 'plain':
                    mode = 1
                    mapType = 'prcdl'
                    surface.fill((0,0,0))
                    map = generate_map(tile_size, surface)
                    
        # changing tile type-->right mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3: # right click
                pos = pygame.mouse.get_pos()
                changeTyoe(map, surface, tile_size, pos, mode)
                softR(surface, tile_size,map, mode)
                pygame.draw.rect(surface, (250,250,250), (start.x, start.y, tile_size,tile_size))
                pygame.draw.rect(surface, (255,215,0), (goal.x, goal.y, tile_size,tile_size))
                if searching == False:
                     if method == 0:
                       path = a_star(start, goal, map, surface, tile_size)
                     else:
                       path = dijkstra(surface, tile_size, map, start, goal)


   #fill the screen with black color
    screen.fill((0, 0, 0))
    screen.blit(surface, (0, 0)) #draw the map on the screen
    
   # start_pt(screen, tile_size) #generate the start point on the map
    if not searching:
         drawPath()

    
          
    
    # update the display
    pygame.display.flip()
    clock.tick(fps) #60 frames per second

# quit pygame
pygame.quit()