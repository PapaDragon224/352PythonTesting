import unittest
from unittest.mock import Mock
from library import library
import json
from library.patron import Patron
import os

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.lib = library.Library()
        # self.books_data = [{'title': 'Learning Python', 'ebook_count': 3}, {'title': 'Learning Python (Learning)', 'ebook_count': 1}, {'title': 'Learning Python', 'ebook_count': 1}, {'title': 'Learn to Program Using Python', 'ebook_count': 1}, {'title': 'Aprendendo Python', 'ebook_count': 1}, {'title': 'Python Basics', 'ebook_count': 1}]
        with open(os.getcwd() + '/tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())

    def tearDown(self):
        self.lib.db.close_db()

    def test_is_ebook_true(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.lib.is_ebook('learning python'))

    def test_is_ebook_false(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertFalse(self.lib.is_ebook('not an ebook'))

    def test_get_ebooks_count(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertEqual(self.lib.get_ebooks_count("learning python"), 8)

    def test_is_book_by_author_true(self):
        self.lib.api.books_by_author = Mock(return_value=['Learning Python'])
        self.assertTrue(self.lib.is_book_by_author('Smith', 'Learning Python'))
        self.lib.api.books_by_author.assert_called_once_with('Smith')

    def test_is_book_by_author_false(self):
        self.lib.api.books_by_author = Mock(return_value=['Not Learning Python'])
        self.assertFalse(self.lib.is_book_by_author('Johnson', 'Learning Python'))
        self.lib.api.books_by_author.assert_called_once_with('Johnson')

    def test_get_languages_for_book(self):
        self.lib.api.get_book_info = Mock(return_value=[{'title': 'Learning Python', 'language': ['eng']}])
        self.assertEqual({'eng'}, self.lib.get_languages_for_book('learning python'))
        self.lib.api.get_book_info.assert_called_once_with('learning python')

    def test_register_patron(self):
        def assert_patron_correct(patron):
            self.assertIsNotNone(patron)
            self.assertEqual(patron.fname, 'first')
            self.assertEqual(patron.lname, 'last')
            self.assertEqual(patron.age, 18)
            self.assertEqual(patron.memberID, 1)
            return unittest.mock.DEFAULT
        self.lib.db.insert_patron = Mock(return_value=1)
        self.lib.db.insert_patron.side_effect = assert_patron_correct
        self.assertEqual(self.lib.register_patron('first', 'last', 18, 1), 1)
        self.lib.db.insert_patron.assert_called_once()

    def test_is_patron_registered_true(self):
        self.lib.db.retrieve_patron = Mock(return_value=Patron('first', 'last', 18, 1))
        patron = Patron('first', 'last', 18, 1)
        self.assertTrue(self.lib.is_patron_registered(patron))
        self.lib.db.retrieve_patron.assert_called_once_with(1)

    def test_is_patron_registered_false(self):
        self.lib.db.retrieve_patron = Mock(return_value=None)
        patron = Patron('first', 'last', 18, 1)
        self.assertFalse(self.lib.is_patron_registered(patron))
        self.lib.db.retrieve_patron.assert_called_once_with(1)

    def test_borrow_book(self):
        name = "Learning Python"
        patron = Patron('first', 'last', 18, 1)
        patron.add_borrowed_book = Mock()
        self.lib.db.update_patron = Mock()
        self.lib.borrow_book(name, patron)
        patron.add_borrowed_book.assert_called_once_with(name.lower())
        self.lib.db.update_patron.assert_called_once_with(patron)

    def test_return_borrowed_book(self):
        name = "Learning Python"
        patron = Patron('first', 'last', 18, 1)
        patron.return_borrowed_book = Mock()
        self.lib.db.update_patron = Mock()
        self.lib.return_borrowed_book(name, patron)
        patron.return_borrowed_book.assert_called_once_with(name.lower())
        self.lib.db.update_patron.assert_called_once_with(patron)

    def test_is_book_borrowed_true(self):
        name = "Learning Python"
        patron = Patron('first', 'last', 18, 1)
        patron.get_borrowed_books = Mock(return_value=[name.lower()])
        self.assertTrue(self.lib.is_book_borrowed(name, patron))
        patron.get_borrowed_books.assert_called_once()

    def test_is_book_borrowed_false(self):
        name = "Learning Python"
        patron = Patron('first', 'last', 18, 1)
        patron.get_borrowed_books = Mock(return_value=['a different book'])
        self.assertFalse(self.lib.is_book_borrowed(name, patron))
        patron.get_borrowed_books.assert_called_once()
