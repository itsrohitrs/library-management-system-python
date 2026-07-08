import unittest
from utils import is_valid_email, is_valid_phone, not_empty, get_integer

class TestUtils(unittest.TestCase):

    def test_email_valid(self):
        self.assertTrue(is_valid_email('user@example.com'))
        self.assertTrue(is_valid_email('first.last@sub.domain.co'))
        self.assertFalse(is_valid_email('invalid-email'))
        self.assertFalse(is_valid_email('user@.com'))

    def test_phone_valid(self):
        self.assertTrue(is_valid_phone('+1 234-567-8900'))
        self.assertTrue(is_valid_phone('1234567890'))
        self.assertFalse(is_valid_phone('abc-1234'))

if __name__ == '__main__':
    unittest.main()
