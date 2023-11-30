# To test: PYTHONPATH=src python3 -m pytest
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

def test_add_user_works(connection):
  first_name = str(random.randint(0, 100000))
  last_name = str(random.randint(0, 100000))
  phone = str(random.randint(0, 100000))
  email = str(random.randint(0, 100000))
  password = encrypt_password(str(random.randint(0,100000)))
  active = 1
  date_time_str = get_date_time_str()
  user_type = 1
  cursor = connection.cursor()
  add_user(connection, first_name, last_name, phone, email, password, active, date_time_str, date_time_str, user_type)
  all_users = get_users(cursor)
  test_user = get_users(cursor, len(all_users))
  assert test_user[0][1] == first_name and test_user[0][2] == last_name and test_user[0][3] == phone and test_user[0][4] == email and test_user[0][5] == password and test_user[0][6] == active and test_user[0][7] == date_time_str and test_user[0][8] == date_time_str and test_user[0][9] == user_type

def test_edit_user_first_name(connection):
  cursor = connection.cursor()
  edit_user(connection, 7, 'first_name', 'Test First Name')
  users = get_users(cursor, 7)
  assert users[0][1] == 'Test First Name'

def test_edit_user_last_name(connection):
  cursor = connection.cursor()
  edit_user(connection, 7, 'last_name', 'Test Last Name')
  users = get_users(cursor, 7)
  assert users[0][2] == 'Test Last Name'

def test_edit_user_phone(connection):
  cursor = connection.cursor()
  edit_user(connection, 7, 'phone', 'Test Phone')
  users = get_users(cursor, 7)
  assert users[0][3] == 'Test Phone'

def test_edit_user_email(connection):
  cursor = connection.cursor()
  edit_user(connection, 7, 'email', 'Test Email')
  users = get_users(cursor, 7)
  assert users[0][4] == 'Test Email'

def test_edit_user_password(connection):
  cursor = connection.cursor()
  edit_user(connection, 7, 'password', 'Test Password')
  users = get_users(cursor, 7)
  assert users[0][5] == 'Test Password'

def test_edit_user_active(connection):
  cursor = connection.cursor()
  is_active = random.randint(0, 1)
  edit_user(connection, 7, 'active', is_active)
  users = get_users(cursor, 7)
  assert users[0][6] == is_active

def test_edit_user_date_created(connection):
  cursor = connection.cursor()
  date_time_str = get_date_time_str()
  edit_user(connection, 7, 'date_created', date_time_str)
  users = get_users(cursor, 7)
  assert users[0][7] == date_time_str

def test_edit_user_hire_date(connection):
  cursor = connection.cursor()
  date_time_str = get_date_time_str()
  edit_user(connection, 7, 'hire_date', date_time_str)
  users = get_users(cursor, 7)
  assert users[0][8] == date_time_str

def test_edit_user_type(connection):
  cursor = connection.cursor()
  user_type = random.randint(0, 1)
  edit_user(connection, 7, 'user_type', user_type)
  users = get_users(cursor, 7)
  assert users[0][9] == user_type

def test_get_assessment_results_works(cursor):
  results = get_assessment_results(cursor)
  result_id, user_id, manager_id, assessment_id, user_first_name, user_last_name, manager_first_name, manager_last_name, assessment_name, score, date_taken = results[0]
  assert result_id == 1 and user_id == 1 and manager_id == 2 and assessment_id == 3 and user_first_name == 'Mark' and user_last_name == 'Hill'and manager_first_name == 'Krystal' and manager_last_name == 'Hill' and assessment_name == 'Database Proficiency Interview' and score == 4 and date_taken == '2023/11/30 14:46:49'

def test_get_assessment_results_specific_id(cursor):
  results = get_assessment_results(cursor, 3)
  result_id, user_id, manager_id, assessment_id, user_first_name, user_last_name, manager_first_name, manager_last_name, assessment_name, score, date_taken = results
  assert result_id == 3 and user_id == 3 and manager_id == 3 and assessment_id == 6 and user_first_name == 'Daxter' and user_last_name == 'Hill' and manager_first_name == 'Daxter' and manager_last_name == 'Hill' and assessment_name == 'QA Final Project' and score == 3 and date_taken == '2023/11/30 15:28:38'

def test_edit_results_user_id(connection):
  cursor = connection.cursor()
  user_id = random.randint(1, 7)
  edit_assessment_results(connection, 4, 'user_id', user_id)
  results = get_assessment_results(cursor, 4)
  assert results[1] == user_id

def test_edit_results_manager_id(connection):
  cursor = connection.cursor()
  manager_id = random.randint(1, 7)
  edit_assessment_results(connection, 4, 'manager_id', manager_id)
  results = get_assessment_results(cursor, 4)
  assert results[2] == manager_id

def test_edit_results_assessment_id(connection):
  cursor = connection.cursor()
  assessment_id = random.randint(1, 7)
  edit_assessment_results(connection, 4, 'assessment_id', assessment_id)
  results = get_assessment_results(cursor, 4)
  assert results[3] == assessment_id

def test_edit_results_score(connection):
  cursor = connection.cursor()
  score = random.randint(1, 5)
  edit_assessment_results(connection, 4, 'score', score)
  results = get_assessment_results(cursor, 4)
  assert results[9] == score

def test_edit_results_date_taken(connection):
  cursor = connection.cursor()
  date_time_str = get_date_time_str()
  edit_assessment_results(connection, 4, 'date_taken', date_time_str)
  results = get_assessment_results(cursor, 4)
  assert results[10] == date_time_str

# def test_delete_results(connection):
#   cursor = connection.cursor()
#   original_results = get_assessment_results(cursor)
#   last_results_id = original_results[-1][0]
#   new_results_id = last_results_id + 1
#   user_id = random.randint(1, 7)
#   manager_id = random.randint(1, 7)
#   assessment_id = random.randint(1, 7)
#   score = random.randint(1, 5)
#   date_time_str = get_date_time_str()
#   add_assessment_result(connection, user_id, manager_id, assessment_id, score, date_time_str)
#   all_results = get_assessment_results(cursor)
#   results_length = len(all_results)
#   delete_assessment_result(connection, new_results_id)
#   new_results = get_assessment_results(cursor)
#   assert len(new_results) == (results_length - 1)

def test_add_assessment_results_works(connection):
  cursor = connection.cursor()
  original_results = get_assessment_results(cursor)
  last_results_id = original_results[-1][0]
  new_results_id = last_results_id + 1
  user_id = random.randint(1, 7)
  manager_id = random.randint(1, 7)
  assessment_id = random.randint(1, 7)
  score = random.randint(1, 5)
  date_time_str = get_date_time_str()
  add_assessment_result(connection, user_id, manager_id, assessment_id, score, date_time_str)
  all_results = get_assessment_results(cursor)
  test_results = get_assessment_results(cursor, new_results_id)
  assert test_results[1] == user_id and test_results[2] == manager_id and test_results[3] == assessment_id and test_results[9] == score and test_results[10] == date_time_str