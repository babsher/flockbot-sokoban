from run.flockbot import FlockBot
from time import sleep

id = 6

if __name__ == "__main__":
    f = FlockBot('10.0.0.3{}'.format(id))
    print 'connecting to ', id
    
    f.connect()
    f.stop()
    sleep(5)
    f.read_block()
    f.moveDistance(15, 20)
    f.read_block()
    f.read_block()
    f.close()
