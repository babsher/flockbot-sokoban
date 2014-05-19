from run.flockbot import FlockBot
from run.robot import Robot
from time import sleep
import zerorpc

id = 5

if __name__ == "__main__":
    f = FlockBot('10.0.0.3{}'.format(id))
    f = Robot(5,5)
    print 'connecting to ', id
    
    f.connect()
    f.rotate(15, 180)
    print f.read_block()
    print f.read_block()
    f.close()
