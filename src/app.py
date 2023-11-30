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

results = get_assessment_results(cursor)
print(results[0])
result_id, user_id, manager_id, assessment_id, user_first_name, user_last_name, manager_first_name, manager_last_name, assessment_name, score, date_taken = results[0]
print(result_id)