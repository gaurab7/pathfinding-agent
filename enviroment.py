import random
import pygame
from perlin_noise import PerlinNoise


class Node:
    # cnstructor for the Node class
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0  # cost from start to current node
        self.h = 0  # heuristic cost from current node to goal
        self.f = 0  # total cost (g + h
        # default is null so that when we reach the goal node, we can reconstruct the path by going backwards from the goal node to the start node, start node will have prev as None
        # this way we can stop when we reach the start node
        self.prev = None  # previous node in the path--> as in the node that was used to reach this node

  
        def get_neighbors(self):
            dir = [
                # so straight up, down, left, and right movements only change x or y by 16 pixels, hence the +16 or -16 depending on the direction(can use a grapg to visualize this)
                # whereas diagonal movements change both x and y by 16 pixels, hence the +16 or -16 in both x and y for each diagonal direction
                (0, 16),   # up
                (0, -16),  # down
                (16, 0),   # right
                (-16, 0),  # left
                (16, 16),   # bottom-right
                (-16, -16), # top-left
                (16, -16),  # top-right
                (-16, 16)   # bottom-left
            ]
            neighbors = []
            for dx, dy in dir:
                nx, ny = self.x + dx, self.y + dy
            
            # at first did this in the init constructuor itself
            # later realized that if this happened in the constructor:
            # it would create a  neighbors for current node and for each neighbor it would create neighbor nodes again recursively
            # creating infinite recursion
            neighbor = Node(nx, ny)  # create a new node for the neighbor
            neighbors.append(neighbor)  # add the neighbor to the list of neighbors
            return neighbors


noise = PerlinNoise(octaves=4)
threshold = -0.095  # threshold for path vs obstacle
scale = 60
border = 6 # border size for tiles
map = [] # to store the generated map
neon_green = (57, 255, 20) # color for path

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
               start = Node(x * tile_size, y * tile_size) # start point in pixel coordinates
               nodes += 1
        else:
            x = random.randint(0, len(map)-1)
            y = random.randint(0, len(map[x])-1)
            # with the previous check also check whether or not the tile is the start tile
            if (map[x][y]==0 and x != start_x // tile_size and y != start_y // tile_size):
                pygame.draw.rect(surface, (255, 215, 0), (x * tile_size, y * tile_size, tile_size, tile_size))
                goal = Node(x * tile_size, y * tile_size) # goal point in pixel coordinates
                found = True
                break
    return start, goal

    


