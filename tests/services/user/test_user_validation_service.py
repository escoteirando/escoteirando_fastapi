import unittest
from src.services.user.user_validation_service import UserValidationService


class TestUserValidationService(unittest.TestCase):
    def test_email(self):
        v = UserValidationService.Instance()
        s, m = v.is_valid_email("guionardo@gmail.com")
        self.assertTrue(s)
        s, m = v.is_valid_email("guionardo_gmail.com")
        self.assertFalse(s)
