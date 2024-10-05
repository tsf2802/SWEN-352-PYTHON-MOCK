import unittest
from unittest.mock import Mock, patch
from library.ext_api_interface import Books_API
import requests

class TestExtApiInterface(unittest.TestCase):
    def setUp(self):
        self.CuT = Books_API()

    # return 200 with proper data
    @patch("library.ext_api_interface.requests.get")
    def test_make_requests_ok(self, mock_get):
        response_data = {
            "numFound": 0,
            "start": 0,
            "numFoundExact": True,
            "docs": [],
            "num_found": 0,
            "q": "",
            "offset": None
        }
        mock_get()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = response_data


        url = "http://openlibrary.org/search.json"

        result = self.CuT.make_request(url)
        self.assertIsNotNone(result)
        self.assertEqual(result, response_data)

    # return 404 and raise connection error
    @patch("library.ext_api_interface.requests.get")
    def test_make_requests_connection(self, mock_get):
        mock_get()
        mock_get.side_effect = requests.ConnectionError()

        url = "http://openlibrary.org/search.json"

        result = self.CuT.make_request(url)
        self.assertIsNone(result)


    # return 500 to alert about internal server error
    @patch("library.ext_api_interface.requests.get")
    def test_make_requests_internal_server_error(self, mock_get):
        mock_get()
        mock_get.return_value.status_code = 500

        url = "http://openlibrary.org/search.json"

        result = self.CuT.make_request(url)
        self.assertIsNone(result)

    
    # return value of query returns two books
    # book details besides author has been abstracted away for test purposes
    @patch("library.ext_api_interface.Books_API.make_request")
    def test_is_book_available_true(self, mock_ext_api):
        slug = "the+lord+of+the+rings"
        mock_ext_api.return_value = {
            "docs": [
                {"author_name": "J.R.R. Tolkien"},
                {"author_name": "J.R.R. Tolkien"}
            ]
        }
        mock_ext_api()

        result = self.CuT.is_book_available(slug)
        self.assertTrue(result)
    
    # return value of query returns zero books
    @patch("library.ext_api_interface.Books_API.make_request")
    def test_is_book_available_false(self, mock_ext_api):
        slug = "the+lord+of+the+rings"
        mock_ext_api.return_value = {
            "docs": []
        }
        mock_ext_api()

        result = self.CuT.is_book_available(slug)
        self.assertFalse(result)
    
    # return a list of books of length 2
    # details have been abstracted away for test purposes
    @patch("library.ext_api_interface.Books_API.make_request")
    def test_get_books_by_author(self, mock_ext_api):   
        mock_ext_api.return_value = {
            "docs": [
                {
                    "author_name": "J.R.R. Tolkien",
                    "title_suggest": "The Lord of the Rings"   
                },
                {
                    "author_name": "J.R.R. Tolkien",
                    "title_suggest": "The Hobbit"
                }
            ]
        }
        mock_ext_api()

        author = "J.R.R. Tolkien"
        expected_result =["The Lord of the Rings", "The Hobbit"]

        result = self.CuT.books_by_author(author)
        self.assertEqual(result, expected_result)

    # return None from the api call
    # details have been abstracted away for test purposes
    @patch("library.ext_api_interface.Books_API.make_request")
    def test_get_books_by_author_empty(self, mock_ext_api):   
        mock_ext_api.return_value = None
        mock_ext_api()

        author = "J.R.R. Tolkien"

        result = self.CuT.books_by_author(author)
        self.assertEqual([], result)
        
    # return 1 book in the query
    @patch("library.ext_api_interface.Books_API.make_request")
    def test_get_book_info(self, mock_ext_api):
        expected_result = {
            "title": "The Lord of the Rings",
            "publish_year": [2019,2020,2021,2022,2023],
            "publisher": ["publisher1", "publisher2", "publisher3", "publisher4", "publisher5"],
            "language": ["eng", "rus", "swe"]
        }
        mock_ext_api.return_value = {
            "docs": [
                expected_result
            ]
        }
        mock_ext_api()

        book = "The Lord of the Rings"
        result = self.CuT.get_book_info(book)

        self.assertEqual(result, [expected_result])

    # return multiple books in the query
    @patch("library.ext_api_interface.Books_API.make_request")
    def test_get_book_info_multiple(self, mock_ext_api):
        expected_result = {
            "title": "The Lord of the Rings",
            "publish_year": [2019,2020,2021,2022,2023],
            "publisher": ["publisher1", "publisher2", "publisher3", "publisher4", "publisher5"],
            "language": ["eng", "rus", "swe"]
        }
        expected_result1 = {
            "title": "The Lord of the Rings Trilogy",
            "publish_year": [2013, 2014, 2015],
            "publisher": ["publisherA", "publisherB", "publisherC"],
            "language": ["eng", "rus", "swe"]
        }
        mock_ext_api.return_value = {
            "docs": [
                expected_result,
                expected_result1
            ]
        }
        mock_ext_api()

        book = "The Lord of the Rings"
        result = self.CuT.get_book_info(book)

        self.assertEqual(result, [expected_result, expected_result1])
    
    # return no data from external api
    @patch("library.ext_api_interface.Books_API.make_request")
    def test_get_book_info_none(self, mock_ext_api):
        mock_ext_api.return_value = None
        mock_ext_api()
        book = "The Lord of the Rings"
        result = self.CuT.get_book_info(book)

        self.assertEqual([], result)
    

    # return a properly formatted response with one item
    @patch("library.ext_api_interface.Books_API.make_request")
    def test_get_ebooks(self, mock_ext_api):
        api_return_value = {
            "docs": [
                {
                    "title": "The Lord of the Rings",
                    "publish_year": [2019,2020,2021,2022,2023],
                    "publisher": ["publisher1", "publisher2", "publisher3", "publisher4", "publisher5"],
                    "language": ["eng", "rus", "swe"],
                    "ebook_count_i": 24
                }
            ]
        }
        expected_result = {
            "title": "The Lord of the Rings",
            "ebook_count": 24
        }
        mock_ext_api.return_value = api_return_value
        mock_ext_api()
        book = "The Lord of the Rings"
        result = self.CuT.get_ebooks(book)
        self.assertEqual([expected_result], result)

    # return a properly formatted response with multiple items
    @patch("library.ext_api_interface.Books_API.make_request")
    def test_get_ebooks_multiple(self, mock_ext_api):
        api_return_value = {
            "docs": [
                {
                    "title": "The Lord of the Rings",
                    "publish_year": [2019,2020,2021,2022,2023],
                    "publisher": ["publisher1", "publisher2", "publisher3", "publisher4", "publisher5"],
                    "language": ["eng", "rus", "swe"],
                    "ebook_count_i": 24
                },
                {
                    "title": "The Lord of the Rings Trilogy",
                    "publish_year": [2013, 2014, 2015],
                    "publisher": ["publisherA", "publisherB", "publisherC"],
                    "language": ["eng", "rus", "swe"],
                    "ebook_count_i": 40
                }
            ]
        }
        expected_result = [
            {
                "title": "The Lord of the Rings",
                "ebook_count": 24
            },
            {
                "title": "The Lord of the Rings Trilogy",
                "ebook_count": 40
            }
        ]
        mock_ext_api.return_value = api_return_value
        mock_ext_api()
        book = "The Lord of the Rings"
        result = self.CuT.get_ebooks(book)
        self.assertEqual(expected_result, result)


    # return a properly formatted response with no items
    @patch("library.ext_api_interface.Books_API.make_request")
    def test_get_ebooks_multiple(self, mock_ext_api):
        api_return_value = None
        expected_result = []
        mock_ext_api.return_value = api_return_value
        mock_ext_api()
        book = "The Lord of the Rings"
        result = self.CuT.get_ebooks(book)
        self.assertEqual(expected_result, result)
    
    # return a properly formatted response with no items
    @patch("library.ext_api_interface.Books_API.make_request")
    def test_get_ebooks_no_ebooks(self, mock_ext_api):
        api_return_value = {
            "docs":[
                {
                    "title": "The Lord of the Rings",
                    "ebook_count_i" : 0
                }
            ]
        }
        expected_result = []
        mock_ext_api.return_value = api_return_value
        mock_ext_api()
        book = "The Lord of the Rings"
        result = self.CuT.get_ebooks(book)
        self.assertEqual(expected_result, result)





    









    
    

    






