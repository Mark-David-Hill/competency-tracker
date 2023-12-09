from modules.sql_parser import SQL_parser
sql_parser = SQL_parser()

class Select_dict:
  def __init__(self, fields, table, where, order_by, limit):
    self.fields = fields
    self.table = table
    self.where = where
    self.order_by = order_by
    self.limit = limit

class Where_dict:
  def __init__(self, field, value, operator):
    self.field = field
    self.value = value
    self.operator = operator

# Users SELECT sql creation. for user_type, 0 = standard user, 1 = manager
def get_users(cursor, id = -1, limit = 0, order_by = None):
  try:
    user_fields = ['user_id', 'first_name', 'last_name', 'phone', 'email', 'password', 'active', 'date_created', 'hire_date', 'user_type']
    if id != -1:
      where_users = Where_dict('user_id', id, 'equals')
    else:
      where_users = None
    users_select_dict = Select_dict(user_fields, 'Users', where_users, order_by, limit)
    sql_select = sql_parser.dict_to_sql(users_select_dict)
    rows = cursor.execute(sql_select,).fetchall()
    return rows
  except Exception as e:
    print(f'\n- ERROR: {e}. Could not get Users data.')

def get_users_with_search(cursor, search_str):
  try:
    like_value = '%' + search_str + '%'
    sql_select = '''SELECT user_id, first_name, last_name, phone, email, password, active, date_created, hire_date, user_type
                  FROM Users WHERE first_name LIKE ? or last_name LIKE ?'''
    rows = cursor.execute(sql_select, (like_value, like_value,)).fetchall()
    return rows
  except Exception as e:
    print(f'\n- ERROR: {e}. Could not get Users data.')

def get_user_with_specific_email(cursor, email_str):
  try:
    sql_select = '''SELECT user_id, first_name, last_name, phone, email, password, active, date_created, hire_date, user_type
                  FROM Users WHERE email = ?'''
    row = cursor.execute(sql_select, (email_str,)).fetchone()
    return row
  except Exception as e:
    print(f'\n- ERROR: {e}. Could not find user with "{email_str}" User Name.')

def get_competencies(cursor, id = -1, limit = 0, order_by = None):
  try:
    competency_fields = ['name', 'date_created']
    if id != -1:
      where_competencies = Where_dict('competency_id', id, 'equals')
    else:
      where_competencies = None
    competencies_select_dict = Select_dict(competency_fields, 'Competencies', where_competencies, order_by, limit)
    sql_select = sql_parser.dict_to_sql(competencies_select_dict)
    rows = cursor.execute(sql_select,).fetchall()
    return rows
  except Exception as e:
    print(f'\n- ERROR: {e}. Could not get Competencies data.')

def get_assessments(cursor, id = -1, limit = 0, order_by = None):
  try:
    if id != -1:
      sql_select = '''
        SELECT a.competency_id, a.name, a.date_created, c.name
        FROM Assessments a
        JOIN Competencies c ON a.competency_id = c.competency_id
        WHERE a.assessment_id == ?
        '''
      rows = cursor.execute(sql_select,(id,)).fetchall()
      return rows
    else:
      sql_select = '''
        SELECT a.competency_id, a.name, a.date_created, c.name
        FROM Assessments a
        JOIN Competencies c ON a.competency_id = c.competency_id
        '''
      rows = cursor.execute(sql_select).fetchall()
      return rows
  except Exception as e:
    print(f'\n- ERROR: {e}. Could not get Assessment data.')

def get_assessment_results(cursor, user_id = -1, limit = 0, order_by = None):
  try:
    if user_id != -1:
      sql_select = '''
        SELECT ar.result_id, ar.user_id, ar.manager_id, ar.assessment_id, u.first_name, u.last_name, m.first_name, m.last_name, a.name, ar.score, ar.date_taken 
        FROM Assessment_results ar
        JOIN Users u ON ar.user_id = u.user_id
        JOIN Users m ON ar.manager_id = m.user_id
        JOIN Assessments a ON ar.assessment_id = a.assessment_id
        WHERE ar.user_id == ?
        '''
      rows = cursor.execute(sql_select,(user_id,)).fetchall()
      return rows
    else:
      print('TESTING. INSIDE SQL SELECT CODE')
      sql_select = '''
        SELECT ar.result_id, ar.user_id, ar.manager_id, ar.assessment_id, u.first_name, u.last_name, m.first_name, m.last_name, a.name, ar.score, ar.date_taken 
        FROM Assessment_results ar
        JOIN Users u ON ar.user_id = u.user_id
        JOIN Users m ON ar.manager_id = m.user_id
        JOIN Assessments a ON ar.assessment_id = a.assessment_id
        '''
      rows = cursor.execute(sql_select).fetchall()
      return rows
  except Exception as e:
    print(f'\n- ERROR: {e}. Could not get Assessment Result data.')

def get_assessment_results_by_id(cursor, result_id):
  try:
    sql_select = '''
      SELECT ar.result_id, ar.user_id, ar.manager_id, ar.assessment_id, u.first_name, u.last_name, m.first_name, m.last_name, a.name, ar.score, ar.date_taken 
      FROM Assessment_results ar
      JOIN Users u ON ar.user_id = u.user_id
      JOIN Users m ON ar.manager_id = m.user_id
      JOIN Assessments a ON ar.assessment_id = a.assessment_id
      WHERE ar.result_id == ?
      '''
    rows = cursor.execute(sql_select,(result_id,)).fetchone()
    return rows
  except Exception as e:
    print(f'\n- ERROR: {e}. Could not get Assessment Result data.')

def add_competency(connection, name, date_created):
  insert_sql = 'INSERT INTO COMPETENCIES (name, date_created) VALUES (?, ?)'
  try:
    cursor = connection.cursor()
    cursor.execute(insert_sql, (name, date_created,))
    connection.commit()
    print(f'\nSUCCESS: Competency "{name}" Successfully added!')
  except Exception as e:
    print(f'\n- ERROR: {e}. Competency was not added.')

def add_assessment(connection, competency_id, name, date_created):
  insert_sql = 'INSERT INTO Assessments (competency_id, name, date_created) VALUES (?, ?, ?)'
  try:
    cursor = connection.cursor()
    cursor.execute(insert_sql, (competency_id, name, date_created,))
    connection.commit()
    print(f'\nSUCCESS: Assessment "{name}" Successfully added!')
  except Exception as e:
    print(f'\n- ERROR: {e}. Assessment was not added.')

def add_user(connection, first_name, last_name, phone, email, password, active, date_created, hire_date, user_type):
  insert_sql = 'INSERT INTO Users (first_name, last_name, phone, email, password, active, date_created, hire_date, user_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
  try:
    cursor = connection.cursor()
    cursor.execute(insert_sql, (first_name, last_name, phone, email, password, active, date_created, hire_date, user_type))
    connection.commit()
    print(f'\nSUCCESS: User "{first_name} {last_name}" Successfully added!')
  except Exception as e:
    print(f'\n- ERROR: {e}. User was not added.')

def add_assessment_result(connection, user_id, manager_id, assessment_id, score, date_taken):
  insert_sql = 'INSERT INTO Assessment_Results (user_id, manager_id, assessment_id, score, date_taken) VALUES (?, ?, ?, ?, ?)'
  try:
    cursor = connection.cursor()
    cursor.execute(insert_sql, (user_id, manager_id, assessment_id, score, date_taken))
    connection.commit()
    print(f'\nSUCCESS: Assessment Results Successfully added!')
  except Exception as e:
    print(f'\n- ERROR: {e}. Assessment Results were not added.')

def edit_competency(connection, new_name, id):
  try:
    cursor = connection.cursor()
    sql_update = "UPDATE Competencies SET name=? WHERE competency_id=?"
    update_values = (new_name, id,)
    cursor.execute(sql_update, update_values)
    connection.commit()
    print(f'SUCCESS: {new_name} updated!')
  except Exception as e:
    print(f'\n- ERROR: {e}. Competency data was not updated. -')

def edit_assessment(assessment_id, connection, new_name = '', new_competency_id = -1):
  try:
    cursor = connection.cursor()
    sql_update = ''
    if new_name and new_competency_id != -1:
      sql_update = "UPDATE Assessments SET name=?, competency_id=? WHERE assessment_id=?"
      cursor.execute(sql_update, (new_name, new_competency_id, assessment_id,))
      connection.commit()
    elif new_name and new_competency_id == -1:
      sql_update = "UPDATE Assessments SET name=? WHERE assessment_id=?"
      cursor.execute(sql_update, (new_name, assessment_id,))
      connection.commit()
    elif new_competency_id != -1 and not new_name:
      sql_update = "UPDATE Assessments SET competency_id=? WHERE assessment_id=?"
      cursor.execute(sql_update, (new_competency_id, assessment_id,))
      connection.commit()
    print(f'SUCCESS: Assessment ID# {assessment_id} updated!')
  except Exception as e:
    print(f'\n- ERROR: {e}. Assessment data was not updated. -')

def edit_user(connection, id, field_to_update, new_value):
  try:
    cursor = connection.cursor()
    sql_update = ''
    if field_to_update == 'first_name':
      sql_update = f'UPDATE Users SET first_name=? WHERE user_id=?'
    elif field_to_update == 'last_name':
      sql_update = f'UPDATE Users SET last_name=? WHERE user_id=?'
    elif field_to_update == 'phone':
      sql_update = f'UPDATE Users SET phone=? WHERE user_id=?'
    elif field_to_update == 'email':
      sql_update = f'UPDATE Users SET email=? WHERE user_id=?'
    elif field_to_update == 'password':
      sql_update = f'UPDATE Users SET password=? WHERE user_id=?'
    elif field_to_update == 'active':
      sql_update = f'UPDATE Users SET active=? WHERE user_id=?'
    elif field_to_update == 'date_created':
      sql_update = f'UPDATE Users SET date_created=? WHERE user_id=?'
    elif field_to_update == 'hire_date':
      sql_update = f'UPDATE Users SET hire_date=? WHERE user_id=?'
    elif field_to_update == 'user_type':
      sql_update = f'UPDATE Users SET user_type=? WHERE user_id=?'
    update_values = (new_value, id,)
    cursor.execute(sql_update, update_values)
    connection.commit()
    print(f'SUCCESS: User with ID#{id} updated!')
  except Exception as e:
    print(f'\n- ERROR: {e}. Competency data was not updated. -')

def edit_assessment_results(connection, id, field_to_update, new_value):
  try:
    cursor = connection.cursor()
    sql_update = ''
    if field_to_update == 'user_id':
      sql_update = f'UPDATE Assessment_Results SET user_id=? WHERE result_id=?'
    elif field_to_update == 'manager_id':
      sql_update = f'UPDATE Assessment_Results SET manager_id=? WHERE result_id=?'
    elif field_to_update == 'assessment_id':
      sql_update = f'UPDATE Assessment_Results SET assessment_id=? WHERE result_id=?'
    elif field_to_update == 'score':
      sql_update = f'UPDATE Assessment_Results SET score=? WHERE result_id=?'
    elif field_to_update == 'date_taken':
      sql_update = f'UPDATE Assessment_Results SET date_taken=? WHERE result_id=?'
    update_values = (new_value, id,)
    cursor.execute(sql_update, update_values)
    connection.commit()
    print(f'SUCCESS: Assessment Results updated!')
  except Exception as e:
    print(f'\n- ERROR: {e}. Assessment Results were not updated. -')

def delete_assessment_result(connection, id):
  try:
    sql_delete = "DELETE FROM Assessment_Results WHERE result_id=?"
    cursor = connection.cursor()
    cursor.execute(sql_delete, (id,)).fetchone()
    connection.commit()
    print(f'SUCCESS: Assessment Results with ID# {id} successfully Deleted!')
    return True
  except Exception as e:
    print(f'\n- ERROR: {e}. Assessment Results were not deleted -')


def view_assessment_results(cursor, user_id):
  print('\n--- Assessment Results ---')
  user_data = get_users(cursor, user_id)[0]
  user_name = user_data[1] + ' ' + user_data[2]
  rows = get_assessment_results(cursor, user_id)
  if rows:
    print(f'{"id":<4} {"User":<20} {"Manager":<20} {"Assessment":<50} {"Score":<6} {"Date Taken":<20}' )
    for row in rows:
      row_data = []
      manager_name = ''
      if row[1] == row[2]:
        manager_name = 'None'
      else:
        manager_data = get_users(cursor, row[2], 1)[0]
        manager_name = manager_data[1] + ' ' + manager_data[2]
      for i in range(len(row)):
        if row[i]:
          row_data.append(row[i])
        else:
          row_data.append('None')
      try:
        print(f'{row_data[0]:<4} {user_name:<20} {manager_name:<20} {row_data[8]:<50} {row_data[9]:<6} {row_data[10]:<20}')
      except Exception as e:
        print(f'\n- ERROR: {e}. Could not print row data for Assessment Results -')
    input("\nPress 'Enter' to Continue")
  else:
    print(f'\n- There are currently no Assessment Results for this User -')
    return False
  
def get_results_by_user_and_competency(cursor, user_id, competency_id, limit = -1):
  try:
    sql_select = '''
      SELECT ar.result_id, ar.user_id, ar.manager_id, ar.assessment_id, u.first_name, u.last_name, m.first_name, m.last_name, a.name, ar.score, ar.date_taken 
      FROM Assessment_results ar
      JOIN Users u ON ar.user_id = u.user_id
      JOIN Users m ON ar.manager_id = m.user_id
      JOIN Assessments a ON ar.assessment_id = a.assessment_id
      WHERE ar.user_id = ? AND a.competency_id = ?
      ORDER BY ar.date_taken DESC
      LIMIT ?
      '''
    rows = cursor.execute(sql_select,(user_id, competency_id, limit,)).fetchall()
    return rows
  except Exception as e:
    print(f'\n- ERROR: {e}. Could not get Assessment Result data.')

# get_user, get_competencies
# Here, need to get most recent score for each competency and Average competency score across all assessment results
# competency_name | Most recent Score | Average Score

def get_competency_summary_data(cursor, user_id, competency_id):
  try:
    sql_select = '''
      SELECT c.name, ar.score, AVG(ar.score)
      FROM Assessment_results ar
      JOIN Assessments a ON ar.assessment_id = a.assessment_id
      JOIN Competencies c ON a.competency_id = c.competency_id
      WHERE ar.user_id = ? AND a.competency_id = ?
      ORDER BY ar.date_taken DESC
      '''
    rows = cursor.execute(sql_select,(user_id, competency_id,)).fetchall()
    return rows
  except Exception as e:
    print(f'\n- ERROR: {e}. Could not get Competency Summary Data.')

def get_most_recent_score(cursor, user_id, competency_id):
  try:
    sql_select = '''
      SELECT ar.score
      FROM Assessment_results ar
      JOIN Assessments a ON ar.assessment_id = a.assessment_id
      JOIN Competencies c ON a.competency_id = c.competency_id
      WHERE ar.user_id = ? AND a.competency_id = ?
      ORDER BY ar.date_taken DESC
      '''
    row = cursor.execute(sql_select,(user_id, competency_id,)).fetchone()
    return row
  except Exception as e:
    print(f'\n- ERROR: {e}. Could not get Competency Summary Data.')

def view_user_competency_summary(cursor, user_id):
  user_data = get_users(cursor, user_id)[0]
  user_name = user_data[1] + ' ' + user_data[2]
  print(f'\n--- {user_name} Competency Summary ---')
  rows = []
  recent_scores = []
  all_competencies = get_competencies(cursor)
  for i in range(len(all_competencies)):
    row = get_competency_summary_data(cursor, user_id, i + 1)
    rows.append(row)
    recent_score = get_most_recent_score(cursor, user_id, i + 1)
    recent_scores.append(recent_score[0])
  if rows:
    print(f'{"Competency":<30} {"Score":<7} {"Ave Score":<5}')
    for i in range(len(rows)):
      row = rows[i]
      row_data = []
      for j in range(len(row)):
        if row[j]:
          row_data.append(row[j])
        else:
          row_data.append('None')
      try:
        row = row_data[0]
        most_recent_score = recent_scores[i]
        print(f'{row[0]:<30} {most_recent_score:<7} {row[2]:<5.2f}')
      except Exception as e:
        print(f'\n- ERROR: {e}. Could not print row data for Competency Results -')
    input("\nPress 'Enter' to Continue")
  else:
    print(f'\n- There are currently no Competency Results for this User -')
    return False

def view_user_info(cursor, user_id):
  print('\n--- User Profile ---')
  rows = get_users(cursor, user_id)
  if rows:
    print(f'{"id":<2} {"First Name":<12} {"Last Name":<12} {"Phone":<15} {"Email":<25} {"Active":<7} {"Date Created":<20} {"Hire Date":<20} {"User Type":<8}')
    for row in rows:
      row_data = []
      for i in range(len(row)):
        if row[i]:
          row_data.append(row[i])
        else:
          row_data.append('None')
      is_active_str = 'False'
      if row_data[6] == 1:
        is_active_str = 'True'
      user_type_str = 'User'
      if row_data[9] == 1:
        user_type_str = 'Manager'
      try:
        print(f'{row_data[0]:<2} {row_data[1]:<12} {row_data[2]:<12} {row_data[3]:<15} {row_data[4]:<25} {is_active_str:<7} {row_data[7]:<20} {row_data[8]:<20} {user_type_str:<8}')
      except Exception as e:
        print(f'\n- ERROR: {e}. Could not print row data for person -')
  else:
    print(f'\n- There are currently no Active People -')
    return False
  
def view_all_users_info(cursor):
  print('\n--- User Profile ---')
  rows = get_users(cursor)
  if rows:
    print(f'{"id":<2} {"First Name":<12} {"Last Name":<12} {"Phone":<15} {"Email":<25} {"Active":<7} {"Date Created":<20} {"Hire Date":<20} {"User Type":<8}')
    for row in rows:
      row_data = []
      for i in range(len(row)):
        if row[i]:
          row_data.append(row[i])
        else:
          row_data.append('None')
      is_active_str = 'False'
      if row_data[6] == 1:
        is_active_str = 'True'
      user_type_str = 'User'
      if row_data[9] == 1:
        user_type_str = 'Manager'
      try:
        print(f'{row_data[0]:<2} {row_data[1]:<12} {row_data[2]:<12} {row_data[3]:<15} {row_data[4]:<25} {is_active_str:<7} {row_data[7]:<20} {row_data[8]:<20} {user_type_str:<8}')
      except Exception as e:
        print(f'\n- ERROR: {e}. Could not print row data for person -')
  else:
    print(f'\n- There are currently no Active People -')
    return False
  
def edit_user_info_prompt(connection, cursor, user_id, current_is_manager, login_manager):
  user_data = get_users(cursor, user_id)[0]
  id, first_name, last_name, phone, email, password, is_active, date_created, hire_date, user_type = user_data
  edit_user_choice = input("\nTo update a field, enter the first letter of the field.\nTo change the User's password, type 'PASSWORD'\nTo return to the previous menu, press 'Enter'.\n>>>").lower()
  if edit_user_choice == 'i':
    print("\nThe User's ID cannot be changed.")
  elif edit_user_choice == 'f':
    print(f'\nCurrent First Name: {first_name}')
    new_first_name = input('New First Name: ')
    edit_user(connection, user_id, 'first_name', new_first_name)
  elif edit_user_choice == 'l':
    print(f'\nCurrent Last Name: {last_name}')
    new_last_name = input('New Last Name: ')
    edit_user(connection, user_id, 'last_name', new_last_name)
  elif edit_user_choice == 'p':
    print(f'\nCurrent Phone Number: {phone}')
    new_phone = input('New Phone Number: ')
    edit_user(connection, user_id, 'phone', new_phone)
  elif edit_user_choice == 'e':
    print(f'\nCurrent Phone Email: {email}')
    new_email = input('New Email: ')
    edit_user(connection, user_id, 'email', new_email)
  elif edit_user_choice == 'a':
    if current_is_manager:
      if is_active == 1:
        choice = input(f"User '{first_name} {last_name}' is currently active. Do you want to deactivate this user? If deactivated they will no longer be able to log in. (Y/N): ")
        if choice.lower() == 'y':
          edit_user(connection, user_id, 'active', 0)
      elif is_active == 0:
        choice = input(f"User '{first_name} {last_name}' is currently inactive. Do you want to activate this user? (Y/N): ")
        if choice.lower() == 'y':
          edit_user(connection, user_id, 'active', 1)
    else:
      print('Sorry, only Managers are allowed to activate or deactivate Users.')
  elif edit_user_choice == 'd':
    print(f'\nCurrent Date Created: {date_created}')
    new_date_created = input('New Date Created: ')
    edit_user(connection, user_id, 'date_created', new_date_created)
  elif edit_user_choice == 'h':
    print(f'\nCurrent Hire Date: {hire_date}')
    new_hire_date = input('New Hire Date: ')
    edit_user(connection, user_id, 'hire_date', new_hire_date)
  elif edit_user_choice == 'u':
    if current_is_manager:
      if user_type == 1:
        choice = input(f"User '{first_name} {last_name}' is currently a Manager. Do you want to change them to be a standard User? (Y/N): ")
        if choice.lower() == 'y':
          edit_user(connection, user_id, 'user_type', 0)
      elif user_type == 0:
        choice = input(f"User '{first_name} {last_name}' is currently a standard User. Do you want to change them to be a manager? (Y/N): ")
        if choice.lower() == 'y':
          edit_user(connection, user_id, 'user_type', 1)
    else:
      print("Sorry, only Managers are allowed to change a User's Type.")
  elif edit_user_choice.lower() == 'password':
      password_guess = input("Please input the user's current password: ")
      is_correct_password = login_manager.check_password(password_guess, password)
      if is_correct_password:
        new_password = input('Please Choose a new Password: ')
        new_password_2 = input('Please re-type the new Password: ')
        if new_password == new_password_2:
          new_hash = login_manager.encrypt_password(new_password)
          new_hash_bytes = bytes(new_hash, 'utf-8')
          # user_bytes = password_str.encode('utf-8')
          edit_user(connection, user_id, 'password', new_hash)
        else:
          print('- Sorry, the two passwords entered did not match. Please try again. -')
      else:
        print('- Sorry, that password was incorrect. Please try again. -')
  
  
    