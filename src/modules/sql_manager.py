class SQL_Manager:
  def __init__(self, cursor):
    self.cursor = cursor

  # Perform Queries
  def get_all_data_from_table(self, table_name, is_active=True):
    try:
      sql_select = ''
      if table_name == 'Users':
        sql_select = "SELECT user_id, first_name, last_name, phone, email, date_created, hire_date, user_type FROM People WHERE active=?"
        rows = self.cursor.execute(sql_select, (is_active,)).fetchall()
      else:
        if table_name == 'Competencies':
          sql_select = 'SELECT competency_id, name, date_created FROM Competencies'
        elif table_name == 'Assessments':
          sql_select = 'SELECT assessment_id, competency_id, name, date_created FROM Assessments'
        rows = self.cursor.execute(sql_select,).fetchall()
      return rows
    except Exception as e:
      print(f'\n- ERROR: {e}. table_name data could not be loaded. -')