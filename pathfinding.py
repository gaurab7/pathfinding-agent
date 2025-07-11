import math
from queue import PriorityQueue
from enviroment import Node 

def distance(current, goal):
    # euclidean distance for 8 directional movement(up, down, left, right, and diagonals)
    # straight line distance between two points
    # euclidean distance formula: d = sqrt((x2 - x1)^2 + (y2 - y1)^2)
    # so pretty much the distance formula between two points a(x1, y1) and b(x2, y2)
    return math.sqrt((current.x - goal.x) **2 + (current.y - goal.y) ** 2)



def a_star(start: Node, goal: Node):
    # using a priority queue to store the nodes to be evaluated
    # the priority queue will store the nodes in order of their f value
    open = PriorityQueue() # nodes to be evaluated
    closed = PriorityQueue() # nodes already evaluated
  

    # for start node
    start.g = 0 # cost from start to current node(start for start)
    start.h = distance(start, goal) # heuristic cost from current node to goal-->dist from start to goal
    start.f = start.g + start.h # total cost
    open.put(start.f, start) # nodes to be evaluated initially is just the start node

    # main loop for the A* algorithm
    # runs till there are no nodes to be evaluated
    while len(open)>0:
        neighbors = []
        # get the node with least f value from open set
        # this also removes it from the open set
        (f, current) = open.get() # will return the node with least f value cuz used a priority queue with f value as priority
        closed.put(f, current) # add the current node to the closed set
        # check if the current node is the goal node
        if current.x == goal.x and current.y == goal.y:
            # if the current node is the goal node, reconstruct the path going backwards and return the path
            path=[]
            # by default prev is None, so unless update it, it will be None
            # hence start node will have prev as None
            while current.prev is not None:
                path.append(current) # add each node from goal to start
                current = current.prev
            
            return path[::-1] # return path in reverse order as we added it from goal to start

        for neighbor in current.get_neighbors():
            # if the neighbor is already evaluated, skip it
            if closed.has(neighbor):
                continue
            # the g value accumulates from the start node to the current node
            # g of start = 0, g of neighbor of start = g of start + cost to reach neighbor from start = 0 + 16/22
            # g of current = g , g of neighbor = g of current + cost to reach neighbor from current(16/22)
            # 16 for straight movement, 22 for diagonal movement
            # 16 cuz each tile is 16 pixels in size and straight movement is just moving up, down, left, or right by 16 pixels(only x or y changes)
            # 22 cuz diagonal movement is moving up and right by 16 pixels each(so both x and y change by 16 pixels and we can use the distance formula to calculate the distance)
            # using the distance formula for diagonal movement we get sqrt(16^2 + 16^2) = sqrt(512) = 22.6274
            g = current.g + (22 if (neighbor.x != current.x and neighbor.y != current.y) else 16) # so the condition tracks if the movement is straight or diagonal
            # if neighbor.x != current.x and neighbor.y != current.y: diagonal movement as both x and y have changed(if they hadnt x and y would be same, and if only one of them changed, it would be straight movement)
           
            # only add the neighbor to the open set if it is not already in the open set or if the updated g value is less than the current g value of the neighbor
            if not open.has(neighbor) or g < neighbor.g:
                neighbor.g = g # using the smaller g value 
                neighbor.h = distance(neighbor, goal)
                neighbor.f = neighbor.g + neighbor.h # smaller g value means smaller f value
                neighbor.prev = current # set the previous node for this path to the current node
                open.put(neighbor.f, neighbor)
                # if neighbor was already in the open set, we update better values
                # this duplicates the neighbor in open set, but its not a probelm cuz we have a conditon above that checks if node is in closed set
                # as the new duplicate will have a better g value and will be evaluated first(get returns it first as it has a lower f value)
                # then it gets added to the closed set and  if later old duplicate is evaluated, it will be skipped as it is already in the closed set
            elif g > neighbor.g:
                # this path is worse as the cost will be higher, so we skip it
                continue

    # if we reach here, it means we have evaluated all the nodes and did not find the goal node
    # so we return an empty path

    return []
    # if we found the goal node, we can reconstruct the path from the goal node to      


    




