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

main_menu_user = {}
#   "\n*** Welcome to Business Inc. LLC's Competency Tracker App ***\n\n1. Student and Teacher Menu": {
#     '\n--- Student and Teacher Menu ---\n\n1. View Active People': view_active_people_and_update,
#     '2. Register a Person': create_person,
#     '3. Reactivate a Person': reactivate_person_option
# }

main_menu_manager = {}

  # "\n*** Welcome to Business Inc. LLC's Competency Tracker App ***\n\n1. Student and Teacher Menu": {
  #   '\n--- Student and Teacher Menu ---\n\n1. View Active People': view_active_people_and_update,
  #   '2. Register a Person': create_person,
  #   '3. Reactivate a Person': reactivate_person_option
  # },
  # '2. Course Menu': {
  #   '\n--- Course Menu ---\n\n1. View Active Courses': view_active_courses_and_deactivate,
  #   '2. Register a Course': create_course,
  #   '3. Reactivate a Course': reactivate_course_option
  # },
  # '3. Cohort Menu': {
  #   '\n--- Cohort Menu ---\n\n1. View Active Cohorts': view_active_cohorts,
  #   '2. Register a Cohort': create_cohort,
  #   '3. Reactivate a Cohort': reactivate_cohort_option
  # },
  # '4. Student Cohort Registration Menu': {
  #   '\n--- Student Cohort Registration Menu ---\n\n1. View Active Cohort Registrations': view_cohort_registrations,
  #   '2. Register Student to Cohort': register_student_option,
  #   '3. Reactivate Cohort Registration': reactivate_cohort_registration_option
  # }

def display_menu(menu):
  for key, value in menu.items():
    print(key)
  
def run_menu(menu):
  quit_pending = False
  while True:
    is_main_menu = False
    menu_options = list(menu.keys())
    if menu_options[0][2] == '*':
      is_main_menu = True
    choices = []
    for i in range(len(menu_options)):
      choices.append(str(i + 1))
    actions = list(menu.values())
    display_menu(menu)
    choice = input("\nPlease choose an option from the menu above, 'q' to quit, or press 'Enter' to return to the previous menu: ")
    if choice.lower() == 'q':
      print('\n - Goodbye! -')
      return True
    elif choice == '' and not is_main_menu:
      return False
    elif choice == '' and is_main_menu:
      pass
    elif choice in choices:
      for i in range(len(choices)):
        if choices[i] == choice:
          if callable(actions[i]):
            actions[i]()
          else:
            quit_pending = run_menu(actions[i])
    else:
      print("\nSorry, I didn't understand your selection. Please enter a valid option.")
    if quit_pending == True:
      break

def login_prompt():
  username = input('enter username: ')
  password = input('enter password: ')
  login_successful = login_manager.attempt_login(cursor, username, password)
  if login_successful:
    if login_manager.is_manager:
      # run_menu(main_menu_manager)
      print('manager menu')
    else:
      # run_menu(main_menu_user)
      print('user menu')
  else:
    print('incorrect login info. Please try again.')

while True:
  login_prompt()