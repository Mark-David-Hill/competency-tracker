class SQL_parser:
  def __init__(self):
    pass

  def get_operator_str(self, str):
    operator = ''
    if str == 'lessthan':
      operator = '<'
    elif str == 'greaterthan':
      operator = '>'
    elif str == 'equals':
      operator = '='
    elif str == 'lessthanorequals':
      operator = '<='
    elif str == 'greaterthanorequals':
      operator = '>='
    elif str == 'LIKE':
      operator = 'LIKE'
    return operator

  def dict_to_sql(self, sql_dict):
    sql_str = 'SELECT '
    field_list = sql_dict.fields
    for i in range(len(field_list)):
      if i < (len(field_list) - 1):
        sql_str += (field_list[i] + ', ')
      else:
        sql_str += (field_list[i] + ' ')

    sql_str += 'FROM '
    from_value = sql_dict.table
    sql_str += from_value + ' '

    try:
      if sql_dict.where.AND:
        sql_str += 'WHERE '
        for i in range(len(sql_dict.where.AND)):
          if i > 0 and i < len(sql_dict.where.AND):
            sql_str += 'AND '
          where_clause = sql_dict.where.AND[i]
          sql_str += str(where_clause['field']) + ' '
          operator = str(where_clause['operator'])
          operator = self.get_operator_str(operator)
          sql_str += operator + ' '
          if type(where_clause['value']) is str:
            sql_str += ("'" + str(where_clause['value']) + "' ")
          else:
            sql_str += (f"{where_clause['value']:.2f}" + " ")
    except:
      pass
    try:
      if sql_dict.where:
        sql_str += 'WHERE '
        where_clause = sql_dict.where
        sql_str += str(where_clause.field) + ' '
        operator = str(where_clause.operator)
        operator = self.get_operator_str(operator)
        sql_str += operator + ' '
        if type(where_clause.value) is str:
          sql_str += ("'" + str(where_clause.value) + "' ")
        else:
          sql_str += (f"{where_clause.value:.2f}" + " ")
    except:
      pass
      
    if sql_dict.order_by:
      sql_str += 'ORDER BY '
      sql_str += sql_dict.order_by['field'] + ' '
      if sql_dict.order_by['order']:
        sql_str += sql_dict.order_by['order']

    if sql_dict.limit:
      sql_str += 'LIMIT '
      sql_str += str(sql_dict.limit)

    return sql_str

  def get_where_str_list(self, str_list):
    operators = ['<=', '>=', '=', '<', '>', 'LIKE']
    clause_operator = ''
    for operator in operators:
      for str in str_list:
        if operator in str:
          clause_operator = operator
          break
      if clause_operator != '':
        break
    where_str_list = []
    if len(str_list) > 1:
      where_str_list = str_list
    else:
      where_str_list = str_list[0].split(operator)
      where_str_list.insert(1, operator)
    where_str_list
    for i in range(len(where_str_list)):
      str = where_str_list[i]
      if (str[0] == "'" and str[-1] == "'") or (str[0] == '"' and str[-1] == '"'):
        where_str_list[i] = str[1:-1]
    return where_str_list

  def get_clause_data(self, query_list, clause, target_and_index = 0):
    and_index = -1
    select_data = []
    current_clause = ''
    for word in query_list:
      if word.lower() == 'select' or word.lower() == 'from' or word.lower() == 'where' or word.lower() == 'and' or word.lower() == 'order' or word.lower() == 'limit':
        if word.lower == 'and':
          and_index += 1
          if and_index == target_and_index:
            current_clause = word
          elif and_index > target_and_index:
            return select_data
        else:
          if word.lower() == 'and':
            and_index += 1
          current_clause = word
      elif current_clause.lower() == clause:
        new_word = word
        if word[-1] == ',':
          new_word = word[:-1]
        elif (word[0] == "'" and word[-1] == "'") or (word[0] == '"' and word[-1] == '"'):
          new_word = word[1:-1]
        if current_clause.lower() == 'and' and and_index == target_and_index:
          select_data.append(new_word)
        elif current_clause.lower() == 'and' and and_index > target_and_index:
          return select_data
        elif current_clause.lower() != 'and':
          select_data.append(new_word)
    return select_data

  def parse_sql(self, query):
    try:
      lower_query_str = query.lower()
      query_list = query.split()
      lower_query_list = lower_query_str.split()
      and_count = lower_query_str.count(' and ')
      if lower_query_list[0] == 'select' and 'from' in lower_query_list:
        sql_dict = {
          'fields': [],
          'table': '',
          'where': {},
          'order_by': {},
          'limit': 0
        }

        select_data_fields = self.get_clause_data(query_list, 'select')
        for field in select_data_fields:
          sql_dict.fields.append(field)

        from_data_fields = self.get_clause_data(query_list, 'from')
        sql_dict.table = from_data_fields[0]

        if 'limit' in lower_query_str:
          limit_data_fields = self.get_clause_data(query_list, 'limit')
          sql_dict.limit = limit_data_fields[0]

        if 'where' in lower_query_list and and_count > 0:
          sql_dict.where = {'AND':[]}
          raw_where_data = self.get_clause_data(query_list, 'where')
          where_data = self.get_where_str_list(raw_where_data)
          sql_dict.where.AND.append({})
          sql_dict.where.AND[0]['field'] = where_data[0]
          sql_dict.where.AND[0]['value'] = where_data[2]
          sql_dict.where.AND[0]['operator'] = where_data[1]

          for i in range(and_count):
            sql_dict.where.AND.append({})
            raw_and_data = self.get_clause_data(query_list, 'and', i)
            and_data = self.get_where_str_list(raw_and_data)
            dict_index = i + 1
            sql_dict.where.AND[dict_index]['field'] = and_data[0]
            sql_dict.where.AND[dict_index]['value'] = and_data[2]
            sql_dict.where.AND[dict_index]['operator'] = and_data[1]
        elif 'where' in lower_query_str and and_count == 0:
          raw_where_data = self.get_clause_data(query_list, 'where')
          where_data = self.get_where_str_list(raw_where_data)
          sql_dict.where.field = where_data[0]
          sql_dict.where.value = where_data[2]
          sql_dict.where.opetor = where_data[1]
        
        if 'order by' in lower_query_str:
          order_by_data = self.get_clause_data(query_list, 'order')
          if order_by_data[0].lower() == 'by':
            sql_dict.order_by['field'] = order_by_data[1]
            if len(order_by_data) <= 2:
              sql_dict.order_by['order'] = 'ASC'
            else:
              sql_dict.order_by['order'] = order_by_data[2]

        return sql_dict
      else:
        print('Incorrect format. Could not parse the query.')
      
    except Exception as e:
      print(f'Error {e}. Could not convert query to dictionary')