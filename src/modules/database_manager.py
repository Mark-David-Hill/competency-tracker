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

def get_assessment_results(cursor, id = -1, limit = 0, order_by = None):
  try:
    if id != -1:
      sql_select = '''
        SELECT ar.result_id, ar.user_id, ar.manager_id, ar.assessment_id, u.first_name, u.last_name, m.first_name, m.last_name, a.name, ar.score, ar.date_taken 
        FROM Assessment_results ar
        JOIN Users u ON ar.user_id = u.user_id
        JOIN Users m ON ar.manager_id = m.user_id
        JOIN Assessments a ON ar.assessment_id = a.assessment_id
        WHERE ar.result_id == ?
        '''
      rows = cursor.execute(sql_select,(id,)).fetchone()
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