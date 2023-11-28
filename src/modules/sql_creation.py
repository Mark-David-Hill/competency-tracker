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

def get_users(cursor, is_active, limit = 0, order_by = None):
  user_fields = ['user_id', 'first_name', 'last_name', 'phone', 'email', 'password', 'active', 'date_created', 'hire_date', 'user_type']
  where_users = Where_dict('active', is_active, 'equals')
  users_select_dict = Select_dict(user_fields, 'Users', where_users, order_by, limit)
  sql_select = sql_parser.dict_to_sql(users_select_dict)
  print(sql_select)
  rows = cursor.execute(sql_select,).fetchall()
  return rows

