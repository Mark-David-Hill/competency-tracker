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

def test_cursor_exists(cursor):
  assert cursor

def test_competency_1_is_computer_anatomy(cursor):
  competency = get_competencies(cursor, 1)
  assert competency[0][0] == 'Computer Anatomy'

def test_there_are_at_least_16_competencies_in_db(cursor):
  competencies = get_competencies(cursor)
  assert len(competencies) >= 16

def test_user_1_is_mark(cursor):
  user = get_users(cursor, 1)
  id, first_name, last_name, phone, email, password, active, date_created, hire_date, user_type = user[0]
  assert id == 1 and first_name == 'Mark' and last_name == 'Hill' and phone == '801-292-7777' and email == 'mark@gmail.com' and password == '$2b$12$JmRFOv1XnLK72syCscNqau9o0P2Xkb5LU4mPVWJ16LFr.gtyditki' and active == 1 and date_created == '2023/11/28 15:05:57' and hire_date == '2023/11/28 15:07:34' and user_type == 1

def test_check_password_works_for_mark(cursor):
  user = get_users(cursor, 1)
  original_password = 'mark_pass'
  hash = user[0][5]
  result = check_password(original_password, hash)
  assert result is True

def test_returns_false_with_incorrect_mark_password(cursor):
  user = get_users(cursor, 1)
  original_password = 'mark_wrong_password'
  hash = user[0][5]
  result = check_password(original_password, hash)
  assert result is False

# def test_there_are_at_least_4_active_users(cursor):
#   users = get_users(cursor)
#   assert len(users) >= 4

# def test_there_are_at_least_2_active_users(cursor):
#   users = get_users(cursor)
#   assert len(users) >= 2

def test_successfully_add_competency(connection):
  rand_str = str(random.randint(0, 100000))
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

def test_at_least_9_assessments(cursor):
  assessments = get_assessments(cursor)
  assert len(assessments) >= 9

def test_assessment_id_1_is_data_types_quiz(cursor):
  assessment = get_assessments(cursor, 1)
  assert assessment[0][1] == 'Data Types Quiz'

def test_edit_assessment_name_works(connection):
  cursor = connection.cursor()
  rand_str = str(random.randint(0, 100))
  edit_assessment(5, connection, rand_str)
  edited_assessment = get_assessments(cursor, 5)
  assert edited_assessment[0][1] == rand_str

def test_edit_assessment_competency_id_works(connection):
  cursor = connection.cursor()
  rand_int = str(random.randint(1, 10))
  edit_assessment(6, connection, None, rand_int)
  edited_assessment = get_assessments(cursor, 6)
  assert str(edited_assessment[0][0]) == rand_int

def test_edit_assessment_name_and_competency_id_works(connection):
  cursor = connection.cursor()
  rand_str = str(random.randint(0, 100))
  rand_int = str(random.randint(1, 10))
  edit_assessment(7, connection, rand_str, rand_int)
  edited_assessment = get_assessments(cursor, 7)
  assert edited_assessment[0][1] == rand_str and str(edited_assessment[0][0] == rand_int)

def test_successfully_add_assessment(connection):
  rand_str = str(random.randint(0, 100000))
  rand_int = random.randint(1, 10)
  date_time_str = get_date_time_str()
  cursor = connection.cursor()
  add_assessment(connection, rand_int, rand_str, date_time_str)
  all_assessments = get_assessments(cursor)
  test_assessment = get_assessments(cursor, len(all_assessments))
  assert test_assessment[0][0] == rand_int and test_assessment[0][1] == rand_str

def test_user_search_works_last_name(cursor):
  users = get_users_with_search(cursor, 'Hill')
  assert users[0][1] == 'Mark' and users[1][1] == 'Krystal' and users[2][1] == 'Daxter' and users[3][1] == 'Rune'

def test_user_search_works_first_name(cursor):
  users = get_users_with_search(cursor, 'nacti')
  assert users[0][1] == 'Inactiboy' and users[1][1] == 'Inactigirl'