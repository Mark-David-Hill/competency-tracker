from modules.get_datetime_str import get_date_time_str
from modules.login_manager import *
from modules.database_manager import *
from modules.menu_manager import *
import sqlite3
connection = sqlite3.connect('src/competency_tracker.db')
cursor = connection.cursor()
login_manager = Login_Manager(connection)

password = login_manager.encrypt_password('fiver_pass')
password_str = str(password)
print(password)
print(password_str)

# date = get_date_time_str()
# print(date)


# results = get_results_by_user_and_competency(cursor, 1, 1, 1)
# print(results)

# view_assessment_results(cursor, 1)

# import random
# import time

# for i in range(100):
#   user_id = random.randint(1, 12)
#   # manager_id = user_id
#   # manager_id = random.randint(1, 2)
#   manager_id = random.randint(7, 9)
#   assessment_id = random.randint(1, 21)
#   score = random.randint(1, 5)
#   date = get_date_time_str()
#   add_assessment_result(connection, user_id, manager_id, assessment_id, score, date)
#   time.sleep(1)