import Robot
import Board

def getPlan(file):
    out = {}
    for line in open(file, 'r').readlines():
        line = line.replace('(', '')
        line = line.replace(')', '')
        l = line.split(' ')
        
    return out

if __name__ == "__main__":
    board = Board()
    robots = [Robot(x, board) for x in [1, 2, 3]]
    
    for r in robots:
        r.connect()
    
    # get grid
    # get robot pos
    # plan
    # Select parts for this robot
    # Identify preconditions for this robots steps
    # while has steps not completed
    #   check precondition of step
    #   start timeout
    #   if timeout replan
    #   if precondition run step
    
    
