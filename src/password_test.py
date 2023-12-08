from modules.get_datetime_str import get_date_time_str
from modules.login_manager import *
from modules.database_manager import *
from modules.menu_manager import *
import sqlite3
connection = sqlite3.connect('src/competency_tracker.db')
cursor = connection.cursor()
login_manager = Login_Manager(connection)

# password = login_manager.encrypt_password('fiver_pass')
# print(password)

date = get_date_time_str()
print(date)