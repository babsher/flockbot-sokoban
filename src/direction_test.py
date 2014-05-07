from run.robot import Robot
import unittest

class  Direction_TestCase(unittest.TestCase):

    def test_direction_(self):
        r = Robot(0,0)
        r.pos = ((1,1), 'w')
        self.assertEqual( 90, r.getDegrees('n'), 'w->n')
        self.assertEqual(-90, r.getDegrees('s'), 'w->s')
        self.assertEqual(180, r.getDegrees('e'), 'w->s')
        self.assertEqual(  0, r.getDegrees('w'), 'w->w')
        
        r.pos = ((1,1), 'n')
        self.assertEqual(  0, r.getDegrees('n'), 'n->n')
        self.assertEqual(180, r.getDegrees('s'), 'n->s')
        self.assertEqual( 90, r.getDegrees('e'), 'n->e')
        self.assertEqual(-90, r.getDegrees('w'), 'n->w')
        
        r.pos = ((1,1), 's')
        self.assertEqual(180, r.getDegrees('n'), 's->n')
        self.assertEqual(  0, r.getDegrees('s'),   's->s')
        self.assertEqual(-90, r.getDegrees('e'), 's->e')
        self.assertEqual( 90, r.getDegrees('w'),  's->w')
        
        r.pos = ((1,1), 'e')
        self.assertEqual(-90, r.getDegrees('n'), 'e->n')
        self.assertEqual( 90, r.getDegrees('s'), 'e->s')
        self.assertEqual(  0, r.getDegrees('e'), 'e->e')
        self.assertEqual(180, r.getDegrees('w'), 'e->w')

if __name__ == '__main__':
    unittest.main()

