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
    competency_fields = ['name', 'date_created', 'competency_id']
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
        SELECT a.competency_id, a.name, a.date_created, c.name, a.assessment_id
        FROM Assessments a
        JOIN Competencies c ON a.competency_id = c.competency_id
        WHERE a.assessment_id == ?
        '''
      rows = cursor.execute(sql_select,(id,)).fetchall()
      return rows
    else:
      sql_select = '''
        SELECT a.competency_id, a.name, a.date_created, c.name, a.assessment_id
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
    rows = cursor.execute(sql_select,(result_id,)).fetchall()
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

def view_assessment_results(cursor, user_id = None, results_id = None, show_continue_prompt = True):
  print('\n--- Assessment Results ---')
  rows = None
  if user_id:
    rows = get_assessment_results(cursor, user_id)
  elif results_id:
    rows = get_assessment_results_by_id(cursor, results_id)
  else:
    rows = get_assessment_results(cursor)

  if rows:
    print(f'{"id":<4} {"User":<20} {"Manager":<20} {"Assessment":<50} {"Score":<6} {"Date Taken":<20}' )
    for row in rows:
      first_name = row[4]
      last_name = row[5]
      user_name = first_name + ' ' + last_name
      manager_name = 'None'
      if row[1] != row[2]:
        manager_first_name = row[6]
        manager_last_name = row[7]
        manager_name = manager_first_name + ' ' + manager_last_name
      
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
    if show_continue_prompt:
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

def get_most_recent_assessment(cursor, user_id, competency_id):
  try:
    sql_select = '''
      SELECT a.name
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

def get_most_recent_assessment_date_taken(cursor, user_id, competency_id):
  try:
    sql_select = '''
      SELECT ar.date_taken
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
  email = user_data[4]
  print(f'\n--- {user_name} Competency Summary ---')
  rows = []
  recent_scores = []
  all_competencies = get_competencies(cursor)
  for i in range(len(all_competencies)):
    row = get_competency_summary_data(cursor, user_id, i + 1)
    if row[0][0]:
      rows.append(row)
    else:
      competency_name = all_competencies[i][0]
      new_row = [[]]
      new_row[0].append(competency_name)
      new_row[0].append(0)
      new_row[0].append(0)
      rows.append(new_row)
    recent_score = get_most_recent_score(cursor, user_id, i + 1)
    if recent_score:
      recent_scores.append(recent_score[0])
    else:
      recent_scores.append(0)
  if rows:
    print(f'{"User Name":<20} {"Email":<25} {"Competency":<30} {"Score":<7} {"Ave Score":<5}')
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
        print(f'{user_name:<20} {email:<25} {row[0]:<30} {most_recent_score:<7} {row[2]:<5.2f}')
      except Exception as e:
        print(f'\n- ERROR: {e}. Could not print row data for Competency Results -')
    input("\nPress 'Enter' to Continue")
  else:
    print(f'\n- There are currently no Competency Results for this User -')
    return False

def view_user_info(cursor, user_id):
  try:
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
          print(f'\n- ERROR: {e}. Could not print row data for that User -')
    else:
      print(f'\n- Could not retrieve data for User with that ID -')
      return False
  except Exception as e:
    print(f'\n- ERROR: {e}. Could not get info for that User -')
  
def view_all_users_info(cursor, search_str = None):
  print('\n--- User Profile ---')
  rows = None
  if not search_str:
    rows = get_users(cursor)
  else:
    rows = get_users_with_search(cursor, search_str)
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
        print(f'\n- ERROR: {e}. Could not print row data for that User -')
  else:
    print(f'\n- There are currently no Users -')
    return False
  
def view_all_assessments(cursor):
  print('\n--- Assessments ---')
  rows = get_assessments(cursor)
  if rows:
    print(f'{"id":<2} {"Name":<50} {"Competency":<30} {"Date Created":<20}')
    for row in rows:
      row_data = []
      for i in range(len(row)):
        if row[i]:
          row_data.append(row[i])
        else:
          row_data.append('None')
      try:
        print(f'{row_data[4]:<2} {row_data[1]:<50} {row_data[3]:<30} {row_data[2]:<20}')
      except Exception as e:
        print(f'\n- ERROR: {e}. Could not print row data for that Assessment -')
  else:
    print(f'\n- There are currently no Assessments -')
    return False
  
def view_all_competencies(cursor):
  print('\n--- Competencies ---')
  rows = get_competencies(cursor)
  if rows:
    print(f'{"id":<3} {"Name":<30} {"Date Created":<20}')
    for row in rows:
      row_data = []
      for i in range(len(row)):
        if row[i]:
          row_data.append(row[i])
        else:
          row_data.append('None')
      try:
        print(f'{row_data[2]:<3} {row_data[0]:<30} {row_data[1]}')
      except Exception as e:
        print(f'\n- ERROR: {e}. Could not print row data for that Competency -')
  else:
    print(f'\n- There are currently no Competencies -')
    return False
  
def view_competency(cursor, competency_id):
  # print('\n--- Competencies ---')
  rows = get_competencies(cursor, competency_id)
  if rows:
    print(f'{"id":<3} {"Name":<30} {"Date Created":<20}')
    for row in rows:
      row_data = []
      for i in range(len(row)):
        if row[i]:
          row_data.append(row[i])
        else:
          row_data.append('None')
      try:
        print(f'{row_data[2]:<3} {row_data[0]:<30} {row_data[1]}')
      except Exception as e:
        print(f'\n- ERROR: {e}. Could not print row data for that Competency -')
  else:
    print(f'\n- There are currently no Competencies -')
    return False
  
def view_assessment(cursor, assessment_id):
  # print('\n--- Assessments ---')
  rows = get_assessments(cursor, assessment_id)
  if rows:
    print(f'{"id":<2} {"Name":<50} {"Competency":<30} {"Date Created":<20}')
    for row in rows:
      row_data = []
      for i in range(len(row)):
        if row[i]:
          row_data.append(row[i])
        else:
          row_data.append('None')
      # competency_name = ''
      # row_data.append(competency_name)
      try:
        print(f'{row_data[4]:<2} {row_data[1]:<50} {row_data[3]:<30} {row_data[2]:<20}')
      except Exception as e:
        print(f'\n- ERROR: {e}. Could not print row data for that Assessment -')
  else:
    print(f'\n- There are currently no Assessments -')
    return False
  
def get_user_id_prompt():
  id = input('\nPlease enter the id of the User you would like view/edit the info for: ')
  return id
  
def edit_user_info_prompt(connection, cursor, user_id, current_is_manager, login_manager, is_view_all_mode = False):
  try:
    user_data = get_users(cursor, user_id)[0]
    id, first_name, last_name, phone, email, password, is_active, date_created, hire_date, user_type = user_data
    edit_user_choice = ''
    if is_view_all_mode:
      edit_user_choice = input("\nTo update a field, enter the first letter of the field.\nTo change the User's password, type 'PASSWORD'\nTo view this User's Competency Summary, type 'SUMMARY'\nTo view all Assessment Results for this User, type 'VIEW'\nTo record a new Assessment Result for this User, type 'RECORD'\nTo return to the previous menu, press 'Enter'.\n>>>").lower()
    else:
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
    elif is_view_all_mode and edit_user_choice.lower() == 'summary':
      view_user_info(cursor, user_id)
      view_user_competency_summary(cursor, user_id)
    elif is_view_all_mode and edit_user_choice.lower() == 'view':
      view_assessment_results(cursor, user_id)
    elif is_view_all_mode and edit_user_choice.lower() == 'record':
      view_all_users_info(cursor)
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
  except Exception as e:
    print(f'\n- ERROR: {e}. Could not fulfill the request -')


def get_competency_id_prompt():
  id = input('\nPlease enter the id of the Competency you would like to edit: ')
  return id

def get_assessment_id_prompt():
  id = input('\nPlease enter the id of the Assessment you would like to edit: ')
  return id

def get_results_id_prompt():
  id = input('\nPlease enter the id of the Assessment Results you would like to edit: ')
  return id


def edit_competency_prompt(connection, cursor, competency_id, login_manager):
  is_manager = login_manager.is_manager
  if is_manager:
    try:
      competency_data = get_competencies(cursor, competency_id)[0]
      competency_name, date_created, id = competency_data
      edit_competency_choice = input("\nTo change the name of this competency, type 'NAME'\nTo view a summary of all Users levels for this Competency, type 'SUMMARY'\nTo return to the previous menu, press 'Enter'.\n>>>").lower()

      if edit_competency_choice.lower() == 'name':
        print(f'\nCurrent Competency Name: {competency_name}')
        new_competency_name = input('New Competency Name: ')
        edit_competency(connection, new_competency_name, competency_id)
      elif edit_competency_choice.lower() == 'summary':
        view_competency_results_summary(cursor, competency_id)
      elif edit_competency_choice.lower() == '':
        pass
      else:
        print('- Sorry, that was not a valid choice. Please try again -')

    except Exception as e:
      print(f'\n- ERROR: {e}. Could not fulfill the request -')
  else:
    print('- Sorry, you do not have access to editing Competencies')

def edit_assessment_prompt(connection, cursor, assessment_id, login_manager):
  is_manager = login_manager.is_manager
  if is_manager:
    try:
      assessment_data = get_assessments(cursor, assessment_id)[0]
      # competency_name, date_created, id = assessment_data
      assessment_name = assessment_data[1]
      competency_id = assessment_data[0]

      edit_competency_choice = input("\nTo change the name of this Assessment, type 'NAME'\nTo change the Competency associated with this Assessment, type 'COMP'\nTo return to the previous menu, press 'Enter'.\n>>>").lower()

      if edit_competency_choice.lower() == 'name':
        print(f'\nCurrent Assessment Name: {assessment_name}')
        new_assessment_name = input('New Assessment Name: ')
        edit_assessment(assessment_id, connection, new_assessment_name)
      elif edit_competency_choice.lower() == 'comp':
        view_all_competencies(cursor)
        print(f'\nCurrent Competency ID: {competency_id}')
        new_competency_id = input('New Competency ID: ')
        edit_assessment(assessment_id, connection, None, new_competency_id)
      elif edit_competency_choice.lower() == '':
        pass
      else:
        print('- Sorry, that was not a valid choice. Please try again -')

    except Exception as e:
      print(f'\n- ERROR: {e}. Could not fulfill the request -')
  else:
    print('- Sorry, you do not have access to editing Competencies')

def edit_assessment_result_prompt(connection, cursor, result_id, login_manager):
  is_manager = login_manager.is_manager
  if is_manager:
    try:
      result_data = get_assessment_results_by_id(cursor, result_id)[0]
      user_id = result_data[1]
      manager_id = result_data[2]
      assessment_id = result_data[3]
      score = result_data[9]
      date_taken = result_data[10]

      edit_competency_choice = input("\nTo change the User ID for these Assessment Results, type 'USER'\nTo change the Manager ID, type 'MANAGER'\nTo change the Assessment ID, type 'ASSESSMENT'\nTo change the Score, type 'SCORE'\nTo change the Date Taken, type 'DATE'\nTo return to the previous menu, press 'Enter'.\n>>>").lower()

      if edit_competency_choice.lower() == 'user':
        view_all_users_info(cursor)
        print(f'\nCurrent User ID: {user_id}')
        new_user_id = input('New User ID: ')
        if new_user_id:
          edit_assessment_results(connection, result_id, 'user_id', new_user_id)
      elif edit_competency_choice.lower() == 'manager':
        view_all_users_info(cursor)
        print(f'\nCurrent Manager ID: {manager_id}')
        new_manager_id = input('New Manager ID: ')
        if new_manager_id:
          edit_assessment_results(connection, result_id, 'manager_id', new_manager_id)
      elif edit_competency_choice.lower() == 'assessment':
        view_all_assessments(cursor)
        print(f'\nCurrent Assessment ID: {assessment_id}')
        new_assessment_id = input('New Assessment ID: ')
        if new_assessment_id:
          edit_assessment_results(connection, result_id, 'assessment_id', new_assessment_id)
      elif edit_competency_choice.lower() == 'score':
        print(f'\nCurrent Score: {score}')
        new_score = input('New Score: ')
        if new_score:
          edit_assessment_results(connection, result_id, 'score', new_score)
      elif edit_competency_choice.lower() == 'date':
        print(f'\nCurrent Date Taken: {date_taken}')
        new_date = input('New Date Taken (format: YYYY/MM/DD hh:mm:ss): ')
        if new_date:
          edit_assessment_results(connection, result_id, 'date_taken', new_date)
      elif edit_competency_choice.lower() == '':
        pass
      else:
        print('- Sorry, that was not a valid choice. Please try again -')

    except Exception as e:
      print(f'\n- ERROR: {e}. Could not fulfill the request -')
  else:
    print('- Sorry, you do not have access to editing Competencies')

def view_competency_results_summary(cursor, competency_id):
  # view_competency(cursor, competency_id)
  competency_data = get_competencies(cursor, competency_id)[0]
  competency_name = competency_data[0]
  # Comp ID, Comp Name, Average Competency Score For All Users, User ID, User Name, Competency Score, Assessment, Date Taken
  all_users = get_users(cursor)
  print(f'\n--- {competency_name} Competency Summary ---')
  average_score = 0
  active_user_count = 0
  sum_of_scores = 0


  if all_users:
    for user in all_users:
      user_id = user[0]
      is_active = False
      if user[6]:
        is_active = True
      if is_active:
        active_user_count += 1
        recent_score = get_most_recent_score(cursor, user_id, competency_id)
        if recent_score:
          sum_of_scores += recent_score[0]

  if sum_of_scores > 0 and active_user_count > 0:
    average_score = sum_of_scores / active_user_count


  if all_users:
    print(f'{"ID":<3} {"Competency":<30} {"Avg Score":<10} {"User ID":<8} {"User Name":<20} {"User Score":<12} {"Assessment":<50} {"Date Taken":<20}')
    for user in all_users:
      user_id = user[0]
      user_name = user[1] + ' ' + user[2]
      user_score = 0
      user_score_data = get_most_recent_score(cursor, user_id, competency_id)
      if user_score_data:
        user_score = user_score_data[0]
      assessment_name = ''
      assessment_name_data = get_most_recent_assessment(cursor, user_id, competency_id)
      if assessment_name_data:
        assessment_name = assessment_name_data[0]
      date_taken = ''
      date_taken_data = get_most_recent_assessment_date_taken(cursor, user_id, competency_id)
      if date_taken_data:
        date_taken = date_taken_data[0]
      print(f'{competency_id:<3} {competency_name:<30} {average_score:<10.2f} {user_id:<8} {user_name:<20} {user_score:<12} {assessment_name:<50} {date_taken:<20}')
    input("\nPress 'Enter' to Continue")
  else:
    print(f'\n- There are currently no Users to provide data for the report -')
    return False