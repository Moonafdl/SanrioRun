import unittest
import pygame
from start import Cinna, GRAVITY, TILE_SIZE, MAX_JUMPS

# Dummy world with no obstacles
class DummyWorld:
    def __init__(self):
        self.obstacles = []

class TestPlayerMovement(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1)) 
        self.player = Cinna(100, 300)
        self.world = DummyWorld()

    def tearDown(self):
        pygame.quit()

    def test_move_right(self):
        old_x = self.player.rect.x
        self.player.move(False, True, self.world)
        self.assertGreater(self.player.rect.x, old_x)

    def test_move_left(self):
        old_x = self.player.rect.x
        self.player.move(True, False, self.world)
        self.assertLess(self.player.rect.x, old_x)

    def test_jump_once(self):
        self.player.in_air = False
        self.player.jumps = 0
        self.player.jump = True
        self.player.move(False, False, self.world)
        self.assertEqual(self.player.jumps, 1)
        self.assertLess(self.player.vel_y, 0)

    def test_double_jump_limit(self):
        self.player.jumps = MAX_JUMPS
        self.player.jump = True
        initial_vel = self.player.vel_y
        self.player.move(False, False, self.world)
        self.assertGreater(self.player.vel_y, 0)  
        self.assertEqual(self.player.jumps, MAX_JUMPS) 


    def test_gravity_applies(self):
        self.player.vel_y = 0
        self.player.move(False, False, self.world)
        self.assertGreater(self.player.vel_y, 0) 

if __name__ == '__main__':
    unittest.main()
