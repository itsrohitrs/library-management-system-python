import unittest
import os
import json
from unittest.mock import patch

import auth
import borrow

class TestAuthBorrow(unittest.TestCase):

    def setUp(self):
        # Use test files to avoid touching real data
        self.users_file = 'test_users.json'
        self.books_file = 'test_books.json'
        self.members_file = 'test_members.json'
        self.borrow_file = 'test_borrow_records.json'

        auth.USERS_FILE = self.users_file
        borrow.BOOKS_FILE = self.books_file
        borrow.MEMBERS_FILE = self.members_file
        borrow.BORROW_FILE = self.borrow_file

        # Clean files
        for f in [self.users_file, self.books_file, self.members_file, self.borrow_file]:
            if os.path.exists(f):
                os.remove(f)

    def tearDown(self):
        for f in [self.users_file, self.books_file, self.members_file, self.borrow_file]:
            if os.path.exists(f):
                os.remove(f)

    def write_json(self, filename, data):
        with open(filename, 'w') as fh:
            json.dump(data, fh, indent=4)

    def read_json(self, filename):
        with open(filename, 'r') as fh:
            return json.load(fh)

    def test_login_success_and_failure(self):
        # Prepare a user
        pw = 'secret123'
        hashed = auth.hash_password(pw)
        users = [{'username': 'tester', 'password': hashed, 'role': 'Admin'}]
        self.write_json(self.users_file, users)

        # Successful login
        with patch('builtins.input', side_effect=['tester', pw]):
            user = auth.login()
            self.assertIsNotNone(user)
            self.assertEqual(user.get('username'), 'tester')

        # Failed login
        with patch('builtins.input', side_effect=['tester', 'wrongpw']):
            user = auth.login()
            self.assertIsNone(user)

    def test_issue_and_return_book(self):
        # Prepare member, book, empty borrow records
        members = [{'member_id': 'M1', 'name': 'A', 'email': 'a@b.com', 'phone': '123'}]
        books = [{'book_id': 'B1', 'title': 'T', 'author': 'A', 'genre': 'G', 'quantity': 1, 'availability': 'Available'}]
        borrow_records = []

        self.write_json(self.members_file, members)
        self.write_json(self.books_file, books)
        self.write_json(self.borrow_file, borrow_records)

        # Issue book
        with patch('builtins.input', side_effect=['M1', 'B1']):
            borrow.issue_book()

        books_after = self.read_json(self.books_file)
        borrows_after = self.read_json(self.borrow_file)

        self.assertEqual(books_after[0]['quantity'], 0)
        self.assertEqual(books_after[0]['availability'], 'Not Available')
        self.assertEqual(len(borrows_after), 1)
        self.assertEqual(borrows_after[0]['status'], 'Borrowed')

        # Return book
        with patch('builtins.input', side_effect=['M1', 'B1']):
            borrow.return_book()

        books_end = self.read_json(self.books_file)
        borrows_end = self.read_json(self.borrow_file)

        self.assertEqual(books_end[0]['quantity'], 1)
        self.assertEqual(borrows_end[0]['status'], 'Returned')

    def test_borrow_limit_enforced(self):
        # set borrow limit to 2 for this test
        borrow.BORROW_LIMIT = 2

        members = [{'member_id': 'M2', 'name': 'B', 'email': 'b@b.com', 'phone': '456'}]
        books = [{'book_id': 'B2', 'title': 'T2', 'author': 'A2', 'genre': 'G2', 'quantity': 5, 'availability': 'Available'}]

        # two borrowed records already
        borrow_records = [
            {'member_id': 'M2', 'book_id': 'X1', 'borrow_date': '2026-01-01', 'due_date': '2026-01-08', 'status': 'Borrowed'},
            {'member_id': 'M2', 'book_id': 'X2', 'borrow_date': '2026-01-01', 'due_date': '2026-01-08', 'status': 'Borrowed'}
        ]

        self.write_json(self.members_file, members)
        self.write_json(self.books_file, books)
        self.write_json(self.borrow_file, borrow_records)

        # Attempt to issue another book should be blocked
        with patch('builtins.input', side_effect=['M2', 'B2']):
            borrow.issue_book()

        books_after = self.read_json(self.books_file)
        borrows_after = self.read_json(self.borrow_file)

        # No change expected
        self.assertEqual(books_after[0]['quantity'], 5)
        self.assertEqual(len(borrows_after), 2)


if __name__ == '__main__':
    unittest.main()
