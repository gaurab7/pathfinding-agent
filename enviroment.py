import random
import pygame
from perlin_noise import PerlinNoise


noise = PerlinNoise(octaves=4)
threshold = -0.18  # threshold for path vs obstacle
scale = 60
map = [] # to store the generated map
neon_green = (57, 255, 20) # color for path
grass = (107,142,37)
obstacles = (125, 125, 125)
muddy = (101, 67, 33)
pen = 50


class Node:
    # cnstructor for the Node class
    def __init__(self, x, y, type=0):
        self.x = x
        self.y = y
        self.g = 0  # cost from start to current node
        self.h = 0  # heuristic cost from current node to goal
        self.f = 0  # total cost (g + h
        # default is null so that when we reach the goal node, we can reconstruct the path by going backwards from the goal node to the start node, start node will have prev as None
        # this way we can stop when we reach the start node
        self.prev = None  # previous node in the path--> as in the node that was used to reach this node
        self.type = type
    
        if self.type == 0:
            self.penalty = 0
        elif self.type == 1:
            self.penalty = 1000
        elif self.type == 2:
            self.penalty = pen #penalty
  
def get_neighbors(current: Node, map):
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
            nx, ny = current.x + dx, current.y + dy  # this is pixel coordinates, wont work for map which is a list whose index would be [0,1,2,3,4] not [o,16,32,48,64]
            x, y = nx//16, ny//16 # to convert to list index
            # at first did this in the init constructuor itself
            # later realized that if this happened in the constructor:
            # it would create a  neighbors for current node and for each neighbor it would create neighbor nodes again recursively
            # creating infinite recursion

            # say at the left edge when trying to find neighbors, u cant move further left but without bound check this function tries to go further left(no where to go)--> out of range error
            if (0 <= x < len(map) and 0 <= y < len(map[x])): # bound check--> without this nodes at edge cause out of range index shit
              if(map[x][y].type ==1):
                 continue
              elif (map[x][y].type ==0) or (map[x][y].type==2):# say leftmost node is node[0][0] without bound check-->map[x][y] tries to search map[-16][0], map[-16][-16],.... which dont exist 
                 # do not create a Node(x,y)--> causes recursive node gen
                 # and always do these sort of things outside the actual class(caused same problem)
                 # did neighbor = Node(x,y)
                 # what happened is: map already has all the Node objects we need, but this created new Node objects continously 
                 # so same node existed in two mem locs(map and wherever this funciton stored it)
                 # so somehow the pathfindig func gets into an infinite loop
                 neighbor = map[x][y]
                 neighbors.append(neighbor)  # add the neighbor to the list of neighbors
         
         return neighbors

def generate_map(tile_size, surface):
    global map
    map = [] # to reset the map each time the func gets called--> so that if we create new map, old one gets deleted
    for x in range(0, surface.get_width(), tile_size):
        row = [] # to store the row of tiles
        for y in range(0, surface.get_height(), tile_size):
            # generate a map using Perlin noise
            val = noise([x/scale, y/scale])#gives value between -1 and 1          
            # map generation based on the threshold so that we can control the number of each type of tiles
            if val > threshold + 0.12:
                row.append(Node(x,y,0))
                # cyan tlie for path at (x,y) of size = tile_size
                pygame.draw.rect(surface, grass, (x, y, tile_size, tile_size))
            elif val > threshold:
                row.append(Node(x,y,2))
                pygame.draw.rect(surface, muddy, (x, y, tile_size, tile_size))
            else:
                row.append(Node(x,y,1))
                # magma tile for obstacle at (x,y) of size = tile_sizergb(204,231,232)
                pygame.draw.rect(surface, obstacles, (x, y, tile_size-5, tile_size-5))
        map.append(row)
    return map
    
def setGoal(surface, tile_size, map, pos,start):
    x, y = pos
    x, y = x//tile_size, y//tile_size
    if(map[x][y].type == 0 or map[x][y]==2)  and (x, y != start.x//tile_size, start.y//tile_size): # goal or start can only be walkable nodes
         pygame.draw.rect(surface, (255, 215, 0), (x * tile_size, y * tile_size, tile_size, tile_size))
         goal = Node(x * tile_size, y * tile_size) # goal point in pixel coordinates
         return goal
    
    else: 
        return None

def setStart(surface, tile_size, map, pos):
    x, y = pos
    x, y = x//tile_size, y//tile_size # to get map indexes 
    if (map[x][y].type == 0 or map[x][y]==2): # goal or start can only be walkable nodes
        pygame.draw.rect(surface, (255, 250, 250), (x * tile_size, y * tile_size, tile_size, tile_size))
        start = Node(x * tile_size, y * tile_size)
        return start
    else:
        return None

def plainMap(surface, tile_size, mode):
    global map
    map = [] # to reset the map each time the func gets called--> so that if we create new map, old one gets deleted
    for x in range(0, surface.get_width(), tile_size):
        row = [] # to store the row of tiles
        for y in range(0, surface.get_height(), tile_size):
            row.append(Node(x,y,0))           
            # cyan tlie for path at (x,y) of size = tile_size
            border = 0 if mode == 1 else 3
            pygame.draw.rect(surface, grass, (x, y, tile_size-border, tile_size-border))
         
        map.append(row)
    return map

def changeTyoe(map, surface, tile_size, pos, mode):
    # pos is a tuple with literal pixel coordinates
    x, y = pos 
    x, y = x//tile_size, y//tile_size # need list indexes for map(list) 0,12,32,64-->0,1,2,3,4..
    if map[x][y].type == 0:
        map[x][y].type = 2
        map[x][y].penalty = pen
        pygame.draw.rect(surface, (0,0,0), (x*tile_size, y*tile_size, tile_size, tile_size)) # clearing the tile first--> otherwise border is cyan and not black
        border = 0 if mode == 1 else 3
        pygame.draw.rect(surface, muddy, (x*tile_size, y*tile_size, tile_size-border, tile_size-border)) 
    elif map[x][y].type ==2:
        map[x][y].type = 1
        pygame.draw.rect(surface, (0,0,0), (x*tile_size, y*tile_size, tile_size, tile_size)) # avoids looking weird when changing colors
        border = 5
        pygame.draw.rect(surface, obstacles, (x*tile_size, y*tile_size, tile_size-border, tile_size-border)) 
    elif map[x][y].type == 1:
        map[x][y].type= 0
        map[x][y].penalty = 0
        pygame.draw.rect(surface, (0,0,0), (x*tile_size, y*tile_size, tile_size, tile_size)) # clearing the tile first--> otherwise border is cyan and not black
        border = 0 if mode == 1 else 3
        pygame.draw.rect(surface, grass, (x*tile_size, y*tile_size, tile_size-border, tile_size-border)) 





    
