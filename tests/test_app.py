# To test: PYTHONPATH=src python3 -m pytest
# https://www.youtube.com/watch?v=c9oeoN1AnUM
import pytest
import sqlite3
from src.modules import get_datetime_str
from src.modules.password_util import *

@pytest.fixture
def cursor(tmpdir):
  'Provides a test Database'
  tables_to_create = [
  """
  CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    date_created TEXT NOT NULL,
    hire_date TEXT NOT NULL,
    user_type INTEGER NOT NULL
  )
  """,
  """
  CREATE TABLE IF NOT EXISTS Competencies (
    competency_id INTEGER NOT NULL UNIQUE,
    name TEXT NOT NULL UNIQUE,
    date_created TEXT NOT NULL,
    PRIMARY KEY(competency_id AUTOINCREMENT) 
  )
  """,
  """
  CREATE TABLE IF NOT EXISTS Assessments (
    assessment_id INTEGER NOT NULL UNIQUE,
    competency_id INTEGER NOT NULL,
    name TEXT NOT NULL UNIQUE,
    date_created TEXT NOT NULL,
    PRIMARY KEY(assessment_id AUTOINCREMENT),
    FOREIGN KEY (competency_id) REFERENCES Competencies (competency_id)
  )
  """,
  """
  CREATE TABLE Assessment_Results (
    result_id INTEGER NOT NULL UNIQUE,
    user_id INTEGER NOT NULL,
    manager_id INTEGER,
    assessment_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    date_taken TEXT NOT NULL,
    PRIMARY KEY("result_id" AUTOINCREMENT),
    FOREIGN KEY(manager_id)
    REFERENCES Users(user_id), 
    FOREIGN KEY(assessment_id) REFERENCES Assessments(assessment_id),
    FOREIGN KEY("user_id") REFERENCES "Users"("user_id") 
  )
  """
  ]
  connection = sqlite3.connect(":memory:")
  cursor = connection.cursor()

  for table in tables_to_create:
    cursor.execute(table).fetchall()
    connection.commit()
  # phonebook = Phonebook(tmpdir)
  # Alternate type of return statement that lets you run code after the test case (e.g. to clean up unneeded files)
  yield connection
  connection.close()

def test_2_plus_2_is_4():
  assert 2 + 2 == 4

def test_get_datetime_str_returns_str():
  datetime_str = get_datetime_str.get_date_time_str()
  assert isinstance(datetime_str, str)

def test_encrypt_returns_expected_type():
  hash = encrypt('Hello')
  assert isinstance(hash, bytes)

def test_check_password_returns_true_when_same():
  test_string_1 = 'Hello'
  test_string_2 = 'Hello'
  hash = encrypt(test_string_1)
  result = check_password(test_string_2, hash)
  assert result is True

def test_check_password_returns_false_when_different():
  test_string_1 = 'Hello'
  test_string_2 = 'Goodbye'
  hash = encrypt(test_string_1)
  result = check_password(test_string_2, hash)
  assert result is False

def test_cursor_exists(cursor):
  assert cursor







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