import unittest
from unittest.mock import patch, Mock
from library.library import Library

"""
Filename: test_library.py
Description: Unit tests for the Library class.
"""

class TestLibrary(unittest.TestCase):
    def setUp(self):
        # Patch the external dependencies
        patcher_db = patch("library.library.Library_DB")
        patcher_api = patch("library.library.Books_API")

        # Start the patches
        self.mock_db_class = patcher_db.start()
        self.mock_api_class = patcher_api.start()
        self.addCleanup(patcher_db.stop)
        self.addCleanup(patcher_api.stop)

        # Create the mocks
        self.library = Library()
        self.mock_db = self.library.db
        self.mock_api = self.library.api

    def test_is_ebook_true(self):
        # Setup
        book_title = "book"
        self.mock_api.get_ebooks.return_value = [
            {"title": "book", "ebook_count": 1}
        ]
        
        # Expected
        result = self.library.is_ebook(book_title)
        
        # Assert
        self.assertTrue(result)

    def test_is_ebook_false(self):
        # Setup
        book_title = "book"
        self.mock_api.get_ebooks.return_value = []
        
        # Expected
        result = self.library.is_ebook(book_title)
        
        # Assert
        self.assertFalse(result)

    def test_get_ebooks_count(self):
        # Setup
        book_title = "book"
        self.mock_api.get_ebooks.return_value = [
            {"title": "book", "ebook_count": 2},
            {"title": "book", "ebook_count": 4}
        ]
        
        # Expected
        result = self.library.get_ebooks_count(book_title)
        
        # Assert
        self.assertEqual(result, 6)

    def test_is_book_by_author_true(self):
        # Setup
        author = "author"
        book_title = "book"
        self.mock_api.books_by_author.return_value = ["book"]
        
        # Expected
        result = self.library.is_book_by_author(author, book_title)
        
        # Assert
        self.assertTrue(result)

    def test_is_book_by_author_false(self):
        # Setup
        author = "author"
        book_title = "book"
        self.mock_api.books_by_author.return_value = ["another book"]
        
        # Expected
        result = self.library.is_book_by_author(author, book_title)
        
        # Assert
        self.assertFalse(result)

    def test_get_languages_for_book(self):
        # Setup
        book_title = "book"
        self.mock_api.get_book_info.return_value = [
            {"title": "book", "language": ["english", "spanish", "french"]}
        ]
        
        # Expected
        result = self.library.get_languages_for_book(book_title)        
        
        # Assert
        self.assertEqual(len(result), 3)
        
    def test_get_languages_for_book_no_languages(self):
        # Setup
        book_title = "book"
        self.mock_api.get_book_info.return_value = [
            {"title": "book", "language": []}
        ]
        
        # Expected
        result = self.library.get_languages_for_book(book_title)        
        
        # Assert
        self.assertEqual(len(result), 0)

    def test_register_patron(self):
        # Setup
        fname = "fname"
        lname = "lname"
        age = 10
        memberID = 1
        self.mock_db.insert_patron.return_value = memberID
        
        # Expected
        result = self.library.register_patron(fname, lname, age, memberID)
        
        # Assert
        self.assertEqual(result, memberID)
        
    def test_is_patron_registered_true(self):
        # Setup
        patron = Mock()
        patron.get_memberID.return_value = "1"
        self.mock_db.retrieve_patron.return_value = patron
        
        # Expected
        result = self.library.is_patron_registered(patron)
        
        # Assert
        self.assertTrue(result)

    def test_is_patron_registered_false(self):
        # Setup
        patron = Mock()
        self.mock_db.retrieve_patron.return_value = None
        
        # Expected
        result = self.library.is_patron_registered(patron)
        
        # Assert
        self.assertFalse(result)

    def test_borrow_book(self):
        # Setup
        patron = Mock()
        book_title = "book"
        
        # Expected
        self.library.borrow_book(book_title, patron)
        
        # Assert
        patron.add_borrowed_book.assert_called_with(book_title.lower())

    def test_return_borrowed_book(self):
        # Setup
        patron = Mock()
        book_title = "book"
        
        # Expected
        self.library.return_borrowed_book(book_title, patron)
        
        # Assert
        patron.return_borrowed_book.assert_called_with(book_title.lower())

    def test_is_book_borrowed_true(self):
        # Setup
        patron = Mock()
        book_title = "book"
        patron.get_borrowed_books.return_value = ["book", "another book"]
        
        # Expected
        result = self.library.is_book_borrowed(book_title, patron)
        
        # Assert
        self.assertTrue(result)
        
    def test_is_book_borrowed_false(self):
        # Setup
        patron = Mock()
        book_title = "book"
        patron.get_borrowed_books.return_value = ["another book"]
        
        # Expected
        result = self.library.is_book_borrowed(book_title, patron)
        
        # Assert
        self.assertFalse(result)
    
if __name__ == "__main__":
    unittest.main()