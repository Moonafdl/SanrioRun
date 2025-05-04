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
        pygame.display.set_mode((1, 1))  # Initialize a minimal pygame window
        self.player = Cinna(100, 300)
        self.world = DummyWorld()

    def tearDown(self):
        pygame.quit()

    def test_move_right(self):
        old_x = self.player.rect.x
        self.player.move(False, True, self.world)
        # Ensure that the player moved to the right
        self.assertGreater(self.player.rect.x, old_x)

    def test_move_left(self):
        old_x = self.player.rect.x
        self.player.move(True, False, self.world)
        # Ensure that the player moved to the left
        self.assertLess(self.player.rect.x, old_x)

    def test_jump_once(self):
        # Ensure that jumping properly affects vel_y
        self.player.in_air = False
        self.player.jumps = 0
        self.player.jump = True
        self.player.move(False, False, self.world)
        # After jumping, vel_y should be negative
        self.assertLess(self.player.vel_y, 0)
        # The player should have one jump now
        self.assertEqual(self.player.jumps, 1)

    def test_double_jump_limit(self):
        self.player.jumps = MAX_JUMPS
        self.player.jump = True
        initial_vel = self.player.vel_y
        self.player.move(False, False, self.world)
        # After attempting a second jump, the player should not go upwards
        self.assertGreater(self.player.vel_y, 0)  # Player should start falling or stay grounded
        self.assertEqual(self.player.jumps, MAX_JUMPS)  # No more jumps allowed

    def test_gravity_applies(self):
        # Make sure the player is not in the air and test gravity application
        self.player.vel_y = 0
        self.player.move(False, False, self.world)
        # Gravity should apply, and the velocity should be greater than 0 (falling down)
        self.assertGreater(self.player.vel_y, 0)

    def test_collision_with_obstacle(self):
        # Add a mock obstacle at position (150, 300) with size (50, 50)
        self.world.obstacles = [(None, pygame.Rect(150, 300, 50, 50))]
        
        old_x = self.player.rect.x
        self.player.move(False, True, self.world)  # Try moving right
        
        # The player should not move past the obstacle, so X position should not change
        self.assertEqual(self.player.rect.x, old_x)

if __name__ == '__main__':
    unittest.main()
