# To Start:
# python3 -m pipenv shell
# cd <directory>
# python3 app.py

# mark@gmail.com password = 'mark_pass'
# krystal@gmail.com password = 'krystal_pass'
# etc.

from modules.get_datetime_str import get_date_time_str
from modules.password_util import *
from modules.sql_creation import get_users
import sqlite3
connection = sqlite3.connect('src/competency_tracker.db')
cursor = connection.cursor()

rows = get_users(cursor, True, 2)
for row in rows:
  print(row)