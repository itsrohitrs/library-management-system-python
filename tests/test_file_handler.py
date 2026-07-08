import unittest
import os
from file_handler import load_data, save_data

class TestFileHandler(unittest.TestCase):

    def setUp(self):
        self.test_file = 'test_tmp.json'
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load(self):
        data = [{'a': 1}, {'b': 2}]
        save_data(self.test_file, data)
        loaded = load_data(self.test_file)
        self.assertEqual(loaded, data)

    def test_load_missing(self):
        if os.path.exists('missing.json'):
            os.remove('missing.json')
        self.assertEqual(load_data('missing.json'), [])

if __name__ == '__main__':
    unittest.main()
