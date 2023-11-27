# To test: PYTHONPATH=src python3 -m pytest
# https://www.youtube.com/watch?v=c9oeoN1AnUM
import pytest
import sqlite3
from src.modules import get_datetime_str

# class Crud_db:
#     def __init__(self, database = 'competency_tracker.db'):
#         self.database = database

#     def connect(self):
#         self.connection = sqlite3.connect(self.database)
#         self.cursor = self.connection.cursor()
#         # print('connect seccesfully')

#     def execute(self, query):
#         self.query = query
#         self.cursor.execute(self.query)

#     def close(self): 
#         self.connection.commit()
#         self.connection.close()

# connection = sqlite3.connect('competency_tracker.db')
# cursor = connection.cursor()

# @pytest.fixture
# def test_cursor(tmpdir):
#   'Provides an empty database cursor'
#   db.connect()

#   query = """ SELECT * FROM Users """
#   db.execute(query)
#   result = db.cursor.fetchall()

#   print(result)
  
#   assert len(result) == 0

def test_2_plus_2_is_4():
  assert 2 + 2 == 4

def test_get_datetime_str_returns_str():
  datetime_str = get_datetime_str.get_date_time_str()
  assert isinstance(datetime_str, str)

# def test_table_1_is_users():
#   query = "SELECT name FROM sqlite_master WHERE type='table';"
#   cursor.execute(query)
#   tables = cursor.cursor.fetchall()
#   assert tables[0][0] == 'Users'



# @pytest.fixture
# def phonebook(tmpdir):
#   'Provides an empty Phonebook'
#   phonebook = Phonebook(tmpdir)
#   # Alternate type of return statement that lets you run code after the test case (e.g. to clean up unneeded files)
#   yield phonebook
#   phonebook.clear()

# def test_lookup_by_name(phonebook):
#   phonebook.add('Bob', '12345')
#   number = phonebook.lookup('Bob')
#   assert number == '12345'

# def test_contains_all_names(phonebook):
#   phonebook.add('Bob', '12345')
#   assert phonebook.all_names() == {'Bob'}

# def test_missing_name(phonebook):
#   with pytest.raises(KeyError):
#     phonebook.lookup('Bob')

# def test_is_consistent_with_different_entries(phonebook):
#   phonebook.add('Bob', '12345')
#   phonebook.add('Anna', '01234')
#   assert phonebook.is_consistent()

#   def test_inconsistent_with_duplicate_entries(phonebook):
#     phonebook.add('Bob', '12345')
#     phonebook.add('Sue', '12345')
#     assert not phonebook.is_consistent()

# def test_inconsistent_with_duplicate_prefix(phonebook):
#   phonebook.add('Bob', '12345')
#   phonebook.add('Sue', '123')
#   assert not phonebook.is_consistent()

# @pytest.mark.parametrize(
#   'entry1,entry2,is_consistent', [
#     (('Bob', '12345'), ('Anna', '01234'), True),
#     (('Bob', '12345'), ('Sue', '12345'), False),
#     (('Bob', '12345'), ('Anna', '123'), False),
#   ]
# )

# def test_is_consistent(phonebook, entry1, entry2, is_consistent):
#   phonebook.add(*entry1)
#   phonebook.add(*entry2)
#   assert phonebook.is_consistent() == is_consistent