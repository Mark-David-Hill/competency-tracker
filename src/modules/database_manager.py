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
  user_fields = ['user_id', 'first_name', 'last_name', 'phone', 'email', 'password', 'active', 'date_created', 'hire_date', 'user_type']
  if id != -1:
    where_users = Where_dict('user_id', id, 'equals')
  else:
    where_users = None
  users_select_dict = Select_dict(user_fields, 'Users', where_users, order_by, limit)
  sql_select = sql_parser.dict_to_sql(users_select_dict)
  rows = cursor.execute(sql_select,).fetchall()
  return rows

def get_users_with_search(cursor, search_str):
  like_value = '%' + search_str + '%'
  sql_select = '''SELECT user_id, first_name, last_name, phone, email, password, active, date_created, hire_date, user_type
                FROM Users WHERE first_name LIKE ? or last_name LIKE ?'''
  rows = cursor.execute(sql_select, (like_value, like_value,)).fetchall()
  return rows

def get_competencies(cursor, id = -1, limit = 0, order_by = None):
  competency_fields = ['name', 'date_created']
  if id != -1:
    where_competencies = Where_dict('competency_id', id, 'equals')
  else:
    where_competencies = None
  competencies_select_dict = Select_dict(competency_fields, 'Competencies', where_competencies, order_by, limit)
  sql_select = sql_parser.dict_to_sql(competencies_select_dict)
  rows = cursor.execute(sql_select,).fetchall()
  return rows

def get_assessments(cursor, id = -1, limit = 0, order_by = None):
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
    
def get_assessment_results(cursor, limit = 0, order_by = None):
  pass

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

def add_user(connection, field_values):
  first_name, last_name, phone, email, password, active, date_created, hire_date, user_type = field_values
  insert_sql = 'INSERT INTO Users (first_name, last_name, phone, email, password, active, date_created, hire_date, user_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
  try:
    cursor = connection.cursor()
    cursor.execute(insert_sql, (first_name, last_name, phone, email, password, active, date_created, hire_date, user_type))
    connection.commit()
    print(f'\nSUCCESS: User "{field_values[0]} {field_values[1]}" Successfully added!')
  except Exception as e:
    print(f'\n- ERROR: {e}. User was not added.')

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


def delete_assessment_result(connection, id):
  pass