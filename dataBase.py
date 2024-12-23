import sqlite3 

conn = sqlite3.connect("dataBase.db")

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    grade INTEGER
)
''')   

cursor.execute('''
    INSERT INTO students (name,age,grade) values(?,?,?)
               ''', ("houssem",29,6))

conn.commit()