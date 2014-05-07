from run.flockbot import FlockBot
from run.robot import Robot
from time import sleep
import zerorpc

id = 0

if __name__ == "__main__":
    f = FlockBot('10.0.0.3{}'.format(id))
    f = Robot(0, 0)
    print 'connecting to ', id
    
    f.connect()
    while True:
        print f.read_block()
    f.close()
