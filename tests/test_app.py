# To test: PYTHONPATH=src python3 -m pytest
# https://www.youtube.com/watch?v=c9oeoN1AnUM
import pytest
import sqlite3
from src.modules.get_datetime_str import *
from src.modules.login_manager import *
from src.modules.database_manager import *
import random

@pytest.fixture
def connection(tmpdir):
  'Provides a connection for the test Database'
  connection = sqlite3.connect("tests/competency_tracker.db")
  yield connection
  connection.close()

@pytest.fixture
def cursor(tmpdir):
  'Provides a cursor for the test Database'
  # connection = sqlite3.connect(":memory:")
  connection = sqlite3.connect("tests/competency_tracker.db")
  cursor = connection.cursor()
  yield connection
  connection.close()

def test_get_datetime_str_returns_str():
  datetime_str = get_date_time_str()
  assert isinstance(datetime_str, str)

def test_encrypt_returns_expected_type():
  hash = encrypt_password('Hello')
  assert isinstance(hash, bytes)

def test_check_password_returns_true_when_same():
  test_string_1 = 'Hello'
  test_string_2 = 'Hello'
  hash = encrypt_password(test_string_1)
  result = check_password(test_string_2, hash)
  assert result is True

def test_check_password_returns_false_when_different():
  test_string_1 = 'Hello'
  test_string_2 = 'Goodbye'
  hash = encrypt_password(test_string_1)
  result = check_password(test_string_2, hash)
  assert result is False

def test_cursor_exists(cursor):
  assert cursor

def test_competency_1_is_computer_anatomy(cursor):
  competency = get_competencies(cursor, 1)
  assert competency[0][0] == 'Computer Anatomy'

def test_there_are_at_least_16_competencies_in_db(cursor):
  competencies = get_competencies(cursor)
  assert len(competencies) >= 16

def test_user_1_is_mark(cursor):
  user = get_users(cursor, 1, 1)
  assert user[0][1] == 'Mark'

def test_there_are_at_least_4_active_users(cursor):
  users = get_users(cursor, True)
  assert len(users) >= 4

def test_there_are_at_least_2_active_users(cursor):
  users = get_users(cursor, 0)
  assert len(users) >= 2

def test_successfully_add_competency(connection):
  rand_str = str(random.randint(0, 100))
  date_time_str = get_date_time_str()
  cursor = connection.cursor()
  add_competency(connection, rand_str, date_time_str)
  all_competencies = get_competencies(cursor)
  test_competency = get_competencies(cursor, len(all_competencies))
  assert test_competency[0][0] == rand_str

def test_edit_competency_works(connection):
  cursor = connection.cursor()
  rand_str = str(random.randint(0, 100))
  edit_competency(connection, rand_str, 5)
  edited_competency = get_competencies(cursor, 5)
  assert edited_competency[0][0] == rand_str


def delete_assessment_result(connection, id):
  pass