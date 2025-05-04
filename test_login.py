import unittest
import os
import pygame
import json
from start import LoginSystem

class TestLoginSystem(unittest.TestCase):

    def test_dummy(self):
        self.assertEqual(1, 1) 

    def setUp(self):
        pygame.init()  
        self.test_file = 'test_user_data.json'
        self.login = LoginSystem(800, 600)
        self.login.file = self.test_file


    def tearDown(self):
        pygame.quit()  
        if os.path.exists(self.test_file):
            os.remove(self.test_file)


    def test_register_and_auth_success(self):
        u, p = 'testuser', 'secret123'
        result = self.login.register(u, p)
        self.assertTrue(result)
        self.assertTrue(self.login.auth(u, p))

    def test_register_duplicate(self):
        self.login.register('sameuser', 'abc')
        result = self.login.register('sameuser', 'xyz')
        self.assertFalse(result)

    def test_auth_failure(self):
        self.login.register('user1', 'pass1')
        self.assertFalse(self.login.auth('user1', 'wrongpass'))
        self.assertFalse(self.login.auth('notexist', 'pass1'))

if __name__ == '__main__':
    unittest.main()
