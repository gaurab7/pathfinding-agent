import pygame
from enviroment import Node

color = (255, 0, 0)

class Seeker:
    def __init__(self, x, y, goal):
        self.speed = 6
        self.pos = pygame.math.Vector2(x, y)
        self.goal = pygame.math.Vector2(goal.x, goal.y)
        self.dir = pygame.math.Vector2(0, 0)
        self.col = color

    def move_toward(self, target):
        target_pos = pygame.math.Vector2(target.x, target.y)
        direction = target_pos - self.pos
        if direction.length() > self.speed:
            self.dir = direction.normalize()
            self.pos += self.dir * self.speed
            return False  # not yet reached
        else:
            self.pos = target_pos
            return True  # reached the target

   
       
        


def genSeeker(start, surface, tile_size, goal):
    pygame.draw.circle(surface, color, (start.x + tile_size //2, start.y + tile_size//2), 5)
    seeker = Seeker(start.x * tile_size, start.y * tile_size, goal)
    return seeker



def moveSeeker(path, surface, tile_size, seeker):
    while seeker.pos != seeker.goal:
        try:
            target = next(path)
            if isinstance(target, Node):
                target = pygame.math.Vector2(target.x, target.y)
                seeker.dir = target - seeker.pos
                while seeker.pos != target:
                    seeker.pos += seeker.speed * seeker.dir
                    pygame.draw.circle(surface, color, (seeker.pos.x + tile_size //2, seeker.pos.y + tile_size//2), 5)

        except StopIteration:
            return 
            
    

