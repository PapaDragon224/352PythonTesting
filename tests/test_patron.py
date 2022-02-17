import unittest

from library.patron import Patron, InvalidNameException


class test_patron(unittest.TestCase):


    def setUp(self):
        self.patron = Patron("Jonathan","Pofcher",20,7453)

    def test_patron_exception(self):
        with self.assertRaises(InvalidNameException):
            badPatron = Patron("5", "Jonathan", 20, 7453)

    def test_get_borrowed_books(self):
        books = self.patron.get_borrowed_books()
        self.assertEqual([],books)

    def test_get_fname(self):
        fname = self.patron.get_fname()
        self.assertEqual("Jonathan",fname)

    def test_get_lname(self):
        lname = self.patron.get_lname()
        self.assertEqual("Pofcher", lname)

    def test_get_age(self):
        age = self.patron.get_age()
        self.assertEqual(20,age)

    def test_get_memberID(self):
        memberID = self.patron.get_memberID()
        self.assertEqual(7453,memberID)

    def test_add_borrowed_books(self):
        self.patron.add_borrowed_book("test")
        books = self.patron.get_borrowed_books()
        self.assertEqual(["test"],books)

    def test_add_borrowed_books_uppercase(self):
        self.patron.add_borrowed_book("TEST")
        books = self.patron.get_borrowed_books()
        self.assertEqual(["test"], books)

    def test_add_borrowed_books_dupe(self):
        self.patron.add_borrowed_book("test")
        self.patron.add_borrowed_book("test")
        books = self.patron.get_borrowed_books()
        self.assertEqual(["test"],books)

    def test_return_borrowed_books(self):
        self.patron.add_borrowed_book("test")
        self.patron.return_borrowed_book("test")
        books = self.patron.get_borrowed_books()
        self.assertEqual([],books)

    def test_equals(self):
        patron2 = Patron("Jonathan", "Pofcher", 20, 7453)
        equals = self.patron.__eq__(patron2)
        self.assertEqual(True,equals)

    def test_not_equals(self):
        patron2 = Patron("Jonathan", "Pofcher", 19, 7453)
        equals = self.patron.__ne__(patron2)
        self.assertEqual(True,equals)
