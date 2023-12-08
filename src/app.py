# To Start:
# python3 -m pipenv shell
# cd <directory>
# python3 app.py

# mark@gmail.com password = 'mark_pass'
# krystal@gmail.com password = 'krystal_pass'
# etc.

from modules.get_datetime_str import get_date_time_str
from modules.login_manager import *
from modules.database_manager import *
from modules.menu_manager import *
import sqlite3
connection = sqlite3.connect('src/competency_tracker.db')
cursor = connection.cursor()
login_manager = Login_Manager(connection)

# user = get_users(cursor, 1, 1)
# for field in user[0]:
#   print(field)

# rows = get_users(cursor, True, 2)
# for row in rows:
#   print(row)

# date_time = get_date_time_str()
# print(date_time)

# password = encrypt_password('test@gmail.com')
# print(password)


# results = get_assessment_results(cursor, 3)
# print(results)
# result_id, user_id, manager_id, assessment_id, user_first_name, user_last_name, manager_first_name, manager_last_name, assessment_name, score, date_taken = results[0]
# print(result_id)

# user_data = login_manager.attempt_login(login_manager.cursor, 'rune@gmail.com', 'rune_pass')
# # print(login_manager.current_user)
# print(user_data)
# id, first_name, last_name, phone, email, password_hash_str, is_active, date_created, hire_date, user_type = user_data
# login_manager.current_user = login_manager.User(id, first_name, last_name, phone, email, password_hash_str, is_active, date_created, hire_date, user_type)
# print(login_manager.current_user.full_name)


def login_prompt():
  username = input('enter username: ')
  password = input('enter password: ')
  login_successful = login_manager.attempt_login(cursor, username, password)
  if login_successful:
    if login_manager.is_manager:
      run_menu(manager_menu, login_manager)
    else:
      run_menu(user_menu, login_manager)
    return True
  else:
    print('incorrect login info. Please try again.')
    return False
  
def placeholder():
  print('placeholder')
  
main_menu = {
  "\n*** Welcome to Business Inc. LLC's Competency Tracker App ***\n\n1. User Login": login_prompt,
  "2. Quit": 'quit'
}

user_menu = {
  "\n--- User Menu ---\n\n1. View/Edit my Profile": placeholder,
  '2. View My Competency Data': placeholder, #Give option to export report to CSV?
  '3. View My Assessment Data': placeholder, #Give option to export report to CSV?
  '4. Logout': 'logout'
}

manager_menu = {}

run_menu(main_menu, login_manager)