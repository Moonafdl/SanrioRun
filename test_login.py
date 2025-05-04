import unittest
from unittest.mock import patch, mock_open
import pygame
import json
import hashlib
from start import LoginSystem
from login import InputBox

class TestLoginSystem(unittest.TestCase):
    def setUp(self):
        pygame.init()  
        pygame.font.init()  
        self.login = LoginSystem(800, 600)
        self.test_user = "test_user"
        self.test_pass = "test_pass"
        self.hashed_pass = hashlib.sha256(self.test_pass.encode()).hexdigest()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_successful_registration(self, mock_file, mock_exists):
        mock_exists.return_value = False
        result = self.login.register_user(self.test_user, self.test_pass)
        self.assertTrue(result)
        mock_file().write.assert_called_with(json.dumps(
            {self.test_user: self.hashed_pass}, indent=4
        ))

@patch('os.path.exists')
def test_duplicate_registration(self, mock_exists):
    mock_exists.return_value = True
    user_data = json.dumps({self.test_user: self.hashed_pass})
    with patch('builtins.open', mock_open(read_data=user_data)):
        result = self.login.register_user(self.test_user, self.test_pass)
        self.assertFalse(result)

    @patch('os.path.exists')
    def test_successful_login(self, mock_exists):
        mock_exists.return_value = True
        with patch('builtins.open', mock_open(read_data=json.dumps(
            {self.test_user: self.hashed_pass}
        ))):
            result = self.login.authenticate_user(self.test_user, self.test_pass)
            self.assertTrue(result)

    @patch('os.path.exists')
    def test_failed_login(self, mock_exists):
        mock_exists.return_value = True
        with patch('builtins.open', mock_open(read_data=json.dumps(
            {self.test_user: self.hashed_pass}
        ))):
            result = self.login.authenticate_user(self.test_user, "wrong_pass")
            self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()