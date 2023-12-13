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
import csv
connection = sqlite3.connect('src/competency_tracker.db')
cursor = connection.cursor()
login_manager = Login_Manager(connection)

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
    return False

def view_assessment_results_for_current_user():
  user_id = login_manager.user.id
  view_assessment_results(cursor, user_id)

def view_current_user_info():
  user_id = login_manager.user.id
  is_manager = login_manager.is_manager
  view_user_info(cursor, user_id)
  edit_user_info_prompt(connection, cursor, user_id, is_manager, login_manager)

def view_all_users():
  view_all_users_info(cursor)
  user_id = get_user_id_prompt()
  if user_id:
    view_user_info(cursor, user_id)
    is_manager = login_manager.is_manager
    edit_user_info_prompt(connection, cursor, user_id, is_manager, login_manager, True)

def view_all_competencies_option():
  view_all_competencies(cursor)
  competency_id = get_competency_id_prompt()
  current_competency = get_competencies(cursor, competency_id)
  if current_competency:
    view_competency(cursor, competency_id)
    edit_competency_prompt(connection, cursor, competency_id, login_manager)

def view_all_assessments_option():
  view_all_assessments(cursor)
  assessment_id = get_assessment_id_prompt()
  current_assessment = get_assessments(cursor, assessment_id)
  if current_assessment:
    view_assessment(cursor, assessment_id)
    edit_assessment_prompt(connection, cursor, assessment_id, login_manager)

def view_all_assessment_results_option():
  view_assessment_results(cursor, None, None, False)
  results_id = get_results_id_prompt()
  current_results = get_assessment_results_by_id(cursor, results_id)
  if current_results:
    view_assessment_results(cursor, None, results_id, False)
    edit_assessment_result_prompt(connection, cursor, results_id, login_manager)

def view_current_user_competency_summary():
  user_id = login_manager.user.id
  view_user_competency_summary(cursor, user_id)

def get_users_with_search_prompt():
  search_str = input('Please enter your search for either the first or last name of the User you are looking for: ')
  view_all_users_info(cursor, search_str)
  user_id = get_user_id_prompt()
  if user_id:
    view_user_info(cursor, user_id)
    is_manager = login_manager.is_manager
    edit_user_info_prompt(connection, cursor, user_id, is_manager, login_manager, True)

def add_user_prompt():
  print('\nPlease fill out the form below:')
  first_name = input('First Name: ')
  last_name = input('Last Name: ')
  phone = input('Phone: ')
  email = input('Email: ')
  password = input('Password: ')
  hash = login_manager.encrypt_password(password)
  date_created = get_date_time_str()
  hire_date = input('Hire Date: (format: YYYY/MM/DD hh:mm:ss): ')
  active_str = input('Is Active? (0 for inactive, 1 for active): ')
  if active_str == '0' or active_str == '1':
    active = int(active_str)
    user_type_str = input('Type of User? (0 for standard User, 1 for Manager): ')
    if user_type_str == '0' or user_type_str == '1':
      user_type = int(user_type_str)  
      add_user(connection, first_name, last_name, phone, email, hash, active, date_created, hire_date, user_type)
    else:
      print('- Incorrect input. Please try again. -')
  else:
    print('- Incorrect input. Please try again. -')

def add_competency_prompt():
  competency_name = input('\nPlease enter a name for the new competency: ')
  if competency_name:
    date = get_date_time_str()
    add_competency(connection, competency_name, date)
  else:
    print('- Sorry, you did not input a valid name. Please try again. -')

def add_assessment_prompt():
  date = get_date_time_str()
  view_all_competencies(cursor)
  competency_id = input('\nPlease enter the ID# of the competency you would like to create this assessment for: ')
  assessment_name = input('\nPlease enter a name for the new assessment: ')
  if competency_id and assessment_name:
    add_assessment(connection, competency_id, assessment_name, date)
  else:
    print('- Sorry, you did not input a valid name. Please try again. -')

def add_assessment_results_prompt():
  view_all_users_info(cursor)
  user_id = input('\nPlease enter the ID# of the User you would like to create an Assessment Result for: ')
  manager_id = input("\nPlease type the number of the ID for the Manager who oversaw this assessment. Or press 'Enter' if there was no overseeing Manager: ")
  if manager_id == '':
    manager_id = user_id
  view_all_assessments(cursor)
  assessment_id = input("\nPlease type the number of the Assessment you would like to record results for: ")
  score = input('Please enter the score of the assessment as a number between 1 and 5: ')
  score_int = int(score)
  if score_int >= 1 and score_int <= 5:
    date_taken = input('\nPlease enter the date the date the Assessment was taken (format: YYYY/MM/DD hh:mm:ss): ')
    add_assessment_result(connection, user_id, manager_id, assessment_id, score, date_taken)
  else:
    print('- Sorry, the score needs to be an integer between 1 and 5. Please try again.')

def delete_assessment_results_prompt():
  view_assessment_results(cursor, None, None, False)
  result_id = input("\nPlease type the ID# of the Assessment Results you would like to delete, or press 'Enter' to return to the previous menu.\n>>>")
  view_assessment_results(cursor, None, result_id, False)
  confirmation = input('\nAre you sure you want to delete these Assessment Results? (Y/N): ').lower()
  if confirmation == 'y':
    delete_assessment_result(connection, result_id)

def export_user_competency_summary_prompt():
  view_all_users_info(cursor)
  user_id = get_user_id_prompt(True)
  try:
    user_data = get_users(cursor, user_id)
    user_name = user_data[0][1].lower() + '_' + user_data[0][2].lower()
    data_list = get_user_competency_summary_data(cursor, user_id)
    filename = f'src/exports/{user_name}_competency_summary.csv'
    with open(filename, 'w') as outfile:
      fields = ['user_name', 'email', 'competency', 'score', 'avg_score']
      writer = csv.writer(outfile)

      writer.writerow(fields)
      writer.writerows(data_list)
      print(f'\nSUCCESS: "{filename}" created!')
  except Exception as e:
    print(f'\n- ERROR: {e}. Could not Export CSV file')


def export_competency_results_summary_prompt():
  view_all_competencies(cursor)
  competency_id = get_competency_id_prompt(True)
  try:
    competency_data = get_competencies(cursor, competency_id)
    competency_name_list = competency_data[0][0].lower().split()
    competency_name = '_'.join(competency_name_list)
    data_list = get_competency_results_summary_data(cursor, competency_id)
    filename = f'src/exports/{competency_name}_competency_results_summary.csv'
    with open(filename, 'w') as outfile:
      fields = ['id', 'competency', 'avg_score', 'user_id', 'user_name', 'user_score', 'assessment', 'date_taken']
      writer = csv.writer(outfile)

      writer.writerow(fields)
      writer.writerows(data_list)
      print(f'\nSUCCESS: "{filename}" created!')
  except Exception as e:
    print(f'\n- ERROR: {e}. Could not Export CSV file')

def import_csv_files_prompt():
  filename = ''
  raw_filename = input('Please enter the name of the file from the imports folder you would like to import data from: ')
  if len(raw_filename) > 4:
    if raw_filename[-4] == '.' and raw_filename[-3] == 'c' and raw_filename[-2] == 's' and raw_filename[-1] == 'v':
      filename = raw_filename
    else:
      filename = raw_filename + '.csv'
  else:
    filename = raw_filename + '.csv'
  filepath = f'src/imports/{filename}'
  rows = []
  try:
    with open(filepath, 'r') as csv_file:
      csv_reader = csv.reader(csv_file)
      fields = next(csv_reader)
      data_list = []
      # for row in csv_reader:
      #   data_list.append(row)
      for row in csv_reader:
        user_id = row[0]
        assessment_id = row[1]
        manager_id = user_id
        score = row[2]
        date_taken = row[3]
        add_assessment_result(connection, user_id, manager_id, assessment_id, score, date_taken)
  except Exception as e:
    print(f'\n- ERROR: {e}. Could not Import CSV file')
  
main_menu = {
  "\n*** Welcome to Business Inc. LLC's Competency Tracker App ***\n\n1. User Login": login_prompt,
  "2. Quit": 'quit'
}

user_menu = {
  "\n--- User Menu ---\n\n1. View/Edit my Profile": view_current_user_info,
  '2. View User Competency Summary': view_current_user_competency_summary,
  '3. View Assessment Results': view_assessment_results_for_current_user,
  '4. Logout': 'logout'
}

manager_menu = {
  "\n--- Manager Menu ---\n\n1. Personal Profile Menu": {
    '\n+++ Profile Menu+++\n\n1. View/Edit my Profile': view_current_user_info,
    '2. View User Competency Summary': view_current_user_competency_summary,
    '3. View Assessment Results': view_assessment_results_for_current_user,
  },
  '2. Users Menu': {
    '\n+++ Users Menu +++\n\n1. View/Edit Users': view_all_users,
    '2. Search for Users': get_users_with_search_prompt,
    '3. Add new User': add_user_prompt,
  },
  '3. Competencies Menu': {
    '\n+++ Competencies Menu +++\n\n1. View/Edit Competencies': view_all_competencies_option,
    '2. Add new Competency': add_competency_prompt,
  },
  '4. Assessments Menu': {
    '\n+++ Assessments Menu +++\n\n1. View/Edit Assessments': view_all_assessments_option,
    '2. Add new Assessment': add_assessment_prompt
  },
  '5. Assessment Results Menu': {
    '\n+++ Assessment Results Menu +++\n\n1. View/Edit Assessment Results': view_all_assessment_results_option,
    '2. Add new Assessment Result': add_assessment_results_prompt,
    '3. Delete Assessment Result': delete_assessment_results_prompt,
  },
  '6. Import/Export Menu': {
    '\n+++ Import/Export Menu +++\n\n1. Import CSV Files': import_csv_files_prompt,
    '2. Export CSV File': {
      '\n1. Export User Competency Summary': export_user_competency_summary_prompt,
      '2. Export Competency Results Summary': export_competency_results_summary_prompt
    }
  },
  '7. Logout': 'logout'
}

run_menu(main_menu, login_manager)

# import_csv_files_prompt()

# export_competency_results_summary_prompt()



# get_user_competency_summary_data(cursor, 2)
# export_user_competency_summary_prompt()