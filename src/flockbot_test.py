from run.flockbot import FlockBot

id = 6

if __name__ == "__main__":
    f = FlockBot('10.0.0.3{}'.format(id))
    print 'connecting to ', id
    
    f.connect()
    f.closeClaw()
    f.read_block()
    f.openClaw()
    f.read_block()
    f.close()
