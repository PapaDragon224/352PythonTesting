import unittest
from unittest.mock import Mock, patch

import requests

from library.ext_api_interface import Books_API


class test_Books_api(unittest.TestCase):


    def setUp(self):
        self.booksAPI = Books_API()

    @patch('requests.get')
    def test_make_request_ok(self,mock):
        mock.return_value.status_code = 200
        response = self.booksAPI.make_request("")
        self.assertNotEqual(response,None)

    @patch('requests.get')
    def test_make_request_bad(self,mock):
        mock.return_value.status_code = 404
        response = self.booksAPI.make_request("")
        self.assertEqual(response,None)

    @patch('requests.get')
    def test_make_request_error(self,mock):
        mock.side_effect = requests.exceptions.ConnectionError()
        response = self.booksAPI.make_request("")
        self.assertEqual(response,None)

    @patch('requests.get')
    def test_is_book_available_true(self,mock):
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {"docs":["test"]}
        response = self.booksAPI.is_book_available("")
        self.assertEqual(response,True)

    @patch('requests.get')
    def test_is_book_available_false(self,mock):
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {}
        response = self.booksAPI.is_book_available("")
        self.assertEqual(response,False)

    @patch('requests.get')
    def test_books_by_author_full(self,mock):
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {"docs":[{"title_suggest":"test"}]}
        response = self.booksAPI.books_by_author("")
        self.assertEqual(response,["test"])


    @patch('requests.get')
    def test_books_by_author_none(self,mock):
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {"docs":[]}
        response = self.booksAPI.books_by_author("")
        self.assertEqual(response,[])

    @patch('requests.get')
    def test_books_by_author_error(self,mock):
        mock.return_value.status_code = 404
        response = self.booksAPI.books_by_author("")
        self.assertEqual(response,[])

    @patch('requests.get')
    def test_get_book_info_full(self,mock):
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {"docs":[{"title":"test","publisher":"penguin","publish_year":"2001","language":"english"}]}
        response = self.booksAPI.get_book_info("")
        self.assertEqual(response,[{"title":"test","publisher":"penguin","publish_year":"2001","language":"english"}])

    @patch('requests.get')
    def test_get_book_info_error(self,mock):
        mock.return_value.status_code = 404
        mock.return_value.json.return_value = {"docs":[{"title":"test","publisher":"penguin","publish_year":"2001","language":"english"}]}
        response = self.booksAPI.get_book_info("")
        self.assertEqual(response,[])

    @patch('requests.get')
    def test_get_ebooks_full(self,mock):
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {"docs":[{"title":"test","ebook_count_i":1}]}
        response = self.booksAPI.get_ebooks("")
        self.assertEqual(response,[{"title":"test","ebook_count":1}])

    @patch('requests.get')
    def test_get_ebooks_error(self,mock):
        mock.return_value.status_code = 404
        mock.return_value.json.return_value = {"docs":[{"title":"test","ebook_count_i":1}]}
        response = self.booksAPI.get_ebooks("")
        self.assertEqual(response,[])

    @patch('requests.get')
    def test_make_request_url(self, mock):
        mock.return_value.status_code = 200
        self.booksAPI.make_request("")
        url = mock.call_args.args
        self.assertNotEqual(url, 'http://openlibrary.org/search.json')

    @patch('requests.get')
    def test_is_book_available_url(self,mock):
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {"docs":"test"}
        self.booksAPI.is_book_available("")
        url = mock.call_args.args
        self.assertEqual(url[0],'http://openlibrary.org/search.json?q=')

    @patch('requests.get')
    def test_author_url(self,mock):
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {"docs":[{"title_suggest":"test"}]}
        self.booksAPI.books_by_author("")
        url = mock.call_args.args
        self.assertEqual(url[0],'http://openlibrary.org/search.json?author=')

    @patch('requests.get')
    def test_info_url(self, mock):
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {"docs": [{"title": "test", "publisher": "penguin", "publish_year": "2001", "language": "english"}]}
        self.booksAPI.get_book_info("")
        url = mock.call_args.args
        self.assertEqual(url[0], 'http://openlibrary.org/search.json?q=')

    @patch('requests.get')
    def test_ebook_url(self, mock):
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {"docs":[{"title":"test","ebook_count_i":2}]}
        self.booksAPI.get_ebooks("")
        url = mock.call_args.args
        self.assertEqual(url[0], 'http://openlibrary.org/search.json?q=')







if __name__ == '__main__':
    unittest.main()