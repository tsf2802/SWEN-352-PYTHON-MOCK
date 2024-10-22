import unittest
from unittest.mock import patch, Mock, MagicMock
from library.library_db_interface import Library_DB
from library.patron import Patron

class TestLibraryDbInterface(unittest.TestCase):
    def setUp(self):
        with open('db.json', 'w') as db_file:
            db_file.write('') 
        self.CuT = Library_DB()
        self.addCleanup(self.CuT.close_db)

    @patch('library.library_db_interface.TinyDB')  # Mock TinyDB to avoid actual file creation
    def test_library_db_init(self, mock_tinydb):
        # Call the constructor
        library_db = Library_DB()
        mock_tinydb.assert_called_with("db.json") # Ensure TinyDB was called with the correct file name
        self.assertEqual(library_db.db, mock_tinydb.return_value)
   
    @patch('library.library_db_interface.Library_DB.retrieve_patron')
    def test_insert_patron_already_exists(self, mock_retrieve_patron):
        existing_patron = Patron("mr", "man", 1, "123")
        mock_retrieve_patron.return_value = existing_patron
        mock_patron = MagicMock(spec=Patron)
        mock_patron.get_memberID.return_value = "123"
        result = self.CuT.insert_patron(mock_patron)
        self.assertIsNone(result)

    @patch('library.library_db_interface.TinyDB')
    @patch('library.library_db_interface.Library_DB.retrieve_patron')
    def test_insert_patron_full(self, mock_retrieve_patron, mock_TinyDB):
        mock_db_instance = MagicMock()
        mock_TinyDB.return_value = mock_db_instance
        mock_db_instance.insert.return_value = 7
        mock_retrieve_patron.return_value = None
        library_db = Library_DB()
        mock_patron = Patron("guy", "guy", 1, "7")
        result = library_db.insert_patron(mock_patron)
        self.assertEqual(result, 7)
        self.assertEqual(mock_db_instance.insert.call_count, 1)

    def test_insert_patron_none(self):
        result = self.CuT.insert_patron(None)
        self.assertEqual(result, None)
    
    @patch.object(Library_DB, 'convert_patron_to_db_format', return_value=None)
    def test_insert_patron_valid(self, mock_convert_patron):
        patron = Patron("fname", "lname", 10, "1")
        mock_convert_patron.return_value = {"fname": "fname", "lname": "fname", "age": 10, "memberID": "1"}
        result = self.CuT.insert_patron(patron)
        mock_convert_patron.assert_called_once_with(patron)
        self.assertIsNotNone(result)
        self.assertEqual(result, 1)

    @patch('library.library_db_interface.TinyDB')
    def test_get_patron_count_with_no_patrons(self, MockTinyDB):
        mock_db_instance = MagicMock()
        MockTinyDB.return_value = mock_db_instance
        mock_db_instance.all.return_value = []
        library_db = Library_DB()
        count = library_db.get_patron_count()
        self.assertEqual(count, 0)
    
    @patch('library.library_db_interface.TinyDB')
    def test_get_patron_count_with_two_patrons(self, MockTinyDB):
        mock_db_instance = MagicMock()
        MockTinyDB.return_value = mock_db_instance
        mock_db_instance.all.return_value = [MagicMock(spec=Patron), MagicMock(spec=Patron)]
        library_db = Library_DB()
        count = library_db.get_patron_count()
        self.assertEqual(count, 2)
    
    @patch('library.library_db_interface.TinyDB')
    def test_get_all_patrons(self, MockTinyDB):
        mock_db_instance = MagicMock()
        MockTinyDB.return_value = mock_db_instance
        mock_db_instance.all.return_value = [MagicMock(spec=Patron), MagicMock(spec=Patron)]
        library_db = Library_DB()
        allpatron = library_db.get_all_patrons()
        self.assertEqual(len(allpatron), 2)
    
    def test_update_patrons_none(self):
        result = self.CuT.update_patron(None)
        self.assertEqual(result, None)
    
    @patch('library.library_db_interface.TinyDB')
    def test_update_patrons_full(self, MockTinyDB):
        mock_db_instance = MagicMock()
        MockTinyDB.return_value = mock_db_instance
        mock_db_instance.update.return_value = []
        library_db = Library_DB()
        library_db.update_patron(Patron("mr", "man", 1, "123"))
        self.assertEqual(mock_db_instance.update.call_count, 1)

    @patch('library.library_db_interface.TinyDB')
    def test_retrieve_patrons_full(self, MockTinyDB):
        mock_db_instance = MagicMock()
        MockTinyDB.return_value = mock_db_instance
        mock_db_instance.search.return_value =[{
            'fname': 'person',
            'lname': 'one',
            'age': 20,
            'memberID': '1'
        }] 
        library_db = Library_DB()
        result = library_db.retrieve_patron(1)
        self.assertIsInstance(result, Patron)
        self.assertEqual(mock_db_instance.search.call_count, 1)

    @patch('library.library_db_interface.TinyDB')
    def test_retrieve_patrons_fail(self, MockTinyDB):
        mock_db_instance = MagicMock()
        MockTinyDB.return_value = mock_db_instance
        mock_db_instance.search.return_value =False
        library_db = Library_DB()
        result = library_db.retrieve_patron(1)
        self.assertEqual(result, None)
    
    

if __name__ == '__main__':
    unittest.main()