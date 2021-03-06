import unittest
from unittest.mock import Mock, call
from library import library_db_interface
from tinydb import Query


class TestLibbraryDBInterface(unittest.TestCase):

    def setUp(self):
        self.db_interface = library_db_interface.Library_DB()

    def tearDown(self):
        self.db_interface.close_db()

    def test_insert_patron_not_in_db(self):
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=None)
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        self.db_interface.db.insert = Mock(return_value=10)
        self.assertEqual(self.db_interface.insert_patron(patron_mock), 10)

    def test_db_is_not_none(self):
        self.assertNotEqual(self.db_interface.db, None)

    def test_insert_patron_data_none(self):
        patron_mock = Mock()
        self.db_interface.convert_patron_to_db_format = Mock(return_value=None)
        self.assertRaises(ValueError, self.db_interface.insert_patron, patron_mock)

    def test_insert_patron_in_db(self):
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=None)
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        self.db_interface.db.insert = Mock(return_value=None)
        self.assertEqual(self.db_interface.insert_patron(patron_mock), None)

    def test_patron_count(self):
        data = ("hello", "I", "Ham")
        self.db_interface.db.all = Mock(return_value=data)
        self.assertEqual(self.db_interface.get_patron_count(), 3)

    def test_get_all_patrons(self):
        data = ("hello", "I", "Ham")
        self.db_interface.db.all = Mock(return_value=data)
        self.assertEqual(self.db_interface.get_all_patrons(), data)

    def test_update_patron(self):
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        db_update_mock = Mock()
        self.db_interface.db.update = db_update_mock
        self.db_interface.update_patron(Mock())
        db_update_mock.assert_called()

    def test_update_patron_data_none(self):
        mock_patron = Mock()
        mock_patron.get_memberID = Mock(return_value='2134043722848')

        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        db_update_mock = Mock()
        self.db_interface.db.update = db_update_mock
        self.db_interface.update_patron(mock_patron)
        db_update_mock.assert_called_with(data, '2134043722848' == Query().memberID)

    def test_update_patron_with_none(self):
        self.assertEqual(self.db_interface.update_patron(None), None)

    def test_insert_patron_with_none(self):
        self.assertEqual(self.db_interface.insert_patron(None), None)

    def test_convert_patron_to_db_format(self):
        patron_mock = Mock()

        patron_mock.get_fname = Mock(return_value=1)
        patron_mock.get_lname = Mock(return_value=2)
        patron_mock.get_age = Mock(return_value=3)
        patron_mock.get_memberID = Mock(return_value=4)
        patron_mock.get_borrowed_books = Mock(return_value=5)
        self.assertEqual(self.db_interface.convert_patron_to_db_format(patron_mock),
                         {'fname': 1, 'lname': 2, 'age': 3, 'memberID': 4,
                          'borrowed_books': 5})

    def test_retrieve_patron_of_none(self):
        self.db_interface.db.search = Mock(return_value=None)
        self.assertEqual(self.db_interface.retrieve_patron(4), None)

    def test_retrieve_patron(self):
        patron_mock = Mock()

        patron_mock.get_fname = Mock(return_value=1)
        patron_mock.get_lname = Mock(return_value=2)
        patron_mock.get_age = Mock(return_value=3)
        patron_mock.get_memberID = Mock(return_value=4)
        patron_mock.get_borrowed_books = Mock(return_value=5)

        formatted_patron = self.db_interface.convert_patron_to_db_format(patron_mock)
        self.db_interface.retrieve_patron = Mock(return_value=formatted_patron)


        results = {
            0: {
                'fname': 1,
                'lname': 2,
                'age': 3,
                'memberID': 4,
                'borrowed_books': 5
            }
        }
        self.db_interface.db.search = Mock(return_value=results)

        self.assertEqual(self.db_interface.retrieve_patron(3),
                         {'fname': 1, 'lname': 2, 'age': 3, 'memberID': 4, 'borrowed_books': 5})

    def test_retrieve_patron_not_equal_Ids(self):
        db_search_mock = Mock(return_value=None)
        self.db_interface.db.search = db_search_mock
        self.db_interface.retrieve_patron(7)
        db_search_mock.assert_called_with(Query().memberID == 7)

    def test_is_closed(self):
        self.db_interface.close_db()
        self.assertEqual(self.db_interface.db._opened, False)

    def test_is_named_db_json(self):
        self.assertEqual(self.db_interface.DATABASE_FILE, "db.json")


    def test_insert_patron_not_in_mutant(self):
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=None)
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        self.db_interface.db.insert = Mock(return_value=10)
        self.db_interface.insert_patron(patron_mock)
        assert call(None) not in self.db_interface.db.insert.mock_calls
