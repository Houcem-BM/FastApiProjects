from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import Error
import time

# Initialize FastAPI application
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define data models
class User(BaseModel):
    userName: str
    password: str

class Student(BaseModel):
    name: str
    grade: int

# Sample user credentials
users = [
    User(userName="houssem", password="1995@"),
    User(userName="Dadi", password="dadi1995@"),
]

# Database connection function
def get_db_connection():
    for _ in range(5):  # Retry up to 5 times
        try:
            connection = mysql.connector.connect(
                host="mysql-db",
                user="admin",
                password="pswrd",
                database="students_db",
            )
            return connection
        except Error as e:
            print("Error while connecting to MySQL, retrying in 5 seconds:", e)
            time.sleep(5)  # Wait 5 seconds before retrying
    print("Error: Unable to connect to MySQL after multiple retries.")
    return None


# Database setup function
def setup_database():
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS students (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        grade INT NOT NULL
                    );
                ''')
                connection.commit()
        except Error as e:
            print("Error while setting up database:", e)
        finally:
            connection.close()

#setup_database()

# API Endpoints
@app.post("/students/{username}")
async def check_users(user_check: User):
    """Validate user credentials."""
    for user in users:
        if user_check.userName == user.userName and user_check.password == user.password:
            setup_database()
            return {"message": "welcome"}
    return {"message": "access denied"}

@app.get("/students/")
def read_students():
    """Fetch all students from the database."""
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM students")
                rows = cursor.fetchall()
                print("rows", rows)             
                return [{"id": row[0], "name": row[1], "grade": row[2]} for row in rows]
        except Error as e:
            print("Error:", e)
            return {"error": "Failed to fetch students"}
        finally:
            connection.close()

@app.post("/students/")
async def create_student(student: Student):
    """Add a new student to the database."""
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                #cursor.execute("INSERT INTO students (name, grade) VALUES (?, ?)", (student.name, student.grade))
                cursor.execute("INSERT INTO students (name, grade) VALUES (%s, %s)", (student.name, student.grade))
                connection.commit()
                return {"message": "Student added successfully"}
        except Error as e:
            print("Error:", e)
            return {"error": "Failed to create student"}
        finally:
            connection.close()

@app.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
    """Update an existing student's information."""
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE students SET name = %s, grade = %s WHERE id = %s",
                    (student.name, student.grade, student_id),
                )
                connection.commit()
                return {"id": student_id, **student.dict()}
        except Error as e:
            print("Error:", e)
            return {"error": "Failed to update student"}
        finally:
            connection.close()

@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    """Delete a student from the database."""
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
                connection.commit()
                return {"message": "Student deleted"}
        except Error as e:
            print("Error:", e)
            return {"error": "Failed to delete student"}
        finally:
            connection.close()

