import sqlite3

'Provides a test Database'
tables_to_create = [
"""
CREATE TABLE IF NOT EXISTS Users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  phone TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  active INTEGER NOT NULL DEFAULT 1,
  date_created TEXT NOT NULL,
  hire_date TEXT NOT NULL,
  user_type INTEGER NOT NULL
)
""",
"""
CREATE TABLE IF NOT EXISTS Competencies (
  competency_id INTEGER NOT NULL UNIQUE,
  name TEXT NOT NULL UNIQUE,
  date_created TEXT NOT NULL,
  PRIMARY KEY(competency_id AUTOINCREMENT) 
)
""",
"""
CREATE TABLE IF NOT EXISTS Assessments (
  assessment_id INTEGER NOT NULL UNIQUE,
  competency_id INTEGER NOT NULL,
  name TEXT NOT NULL UNIQUE,
  date_created TEXT NOT NULL,
  PRIMARY KEY(assessment_id AUTOINCREMENT),
  FOREIGN KEY (competency_id) REFERENCES Competencies (competency_id)
)
""",
"""
CREATE TABLE Assessment_Results (
  result_id INTEGER NOT NULL UNIQUE,
  user_id INTEGER NOT NULL,
  manager_id INTEGER,
  assessment_id INTEGER NOT NULL,
  score INTEGER NOT NULL,
  date_taken TEXT NOT NULL,
  PRIMARY KEY("result_id" AUTOINCREMENT),
  FOREIGN KEY(manager_id)
  REFERENCES Users(user_id), 
  FOREIGN KEY(assessment_id) REFERENCES Assessments(assessment_id),
  FOREIGN KEY("user_id") REFERENCES "Users"("user_id") 
)
"""
]
connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

for table in tables_to_create:
  cursor.execute(table).fetchall()
  connection.commit()

print(cursor)