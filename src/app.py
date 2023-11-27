# To Start:
# python3 -m pipenv shell
# cd <directory>
# python3 app.py

from modules.get_datetime_str import get_date_time_str
import sqlite3
connection = sqlite3.connect('competency_tracker.db')
cursor = connection.cursor()

# print(cursor)

# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# tables = cursor.fetchall()
# print(tables[0][0])

print(get_date_time_str())
