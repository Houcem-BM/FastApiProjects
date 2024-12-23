from fastapi import FastAPI
from pydantic import BaseModel
import json
import sqlite3

# إنشاء تطبيق FastAPI
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # يسمح بالوصول من أي مصدر. قم بتقييد هذا في الإنتاج
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
# تعريف نموذج البيانات باستخدام Pydantic
class User(BaseModel):
    userName: str
    password : str

class Student(BaseModel):
  name: str
  grade: int

users = [
   User(userName = "houssem", password="1995@"),
   User(userName= "Dadi", password= "dadi1995@"),
]

@app.post("/students/{username}")
async def checkUsers(userCheck : User):
   for i in users:
      if userCheck.userName == i.userName and  userCheck.password == i.password :
            return {"message": "welcome"}
   return {"message": "access denied"}


def setup_database():
  try:
    conn = sqlite3.connect('students.db') # إنشاء اتصال بقاعدة البيانات
    cursor = conn.cursor() # إنشاء مؤشر
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade INTEGER
        )
    ''')
    conn.commit() # حفظ التغييرات
  except sqlite3.Error as e:  # التعامل مع الأخطاء المحتملة
    print(e)  # طباعة الخطأ
    return {"error": "Failed to fetch students"}  # إرجاع رسالة خطأ في حالة فشل جلب البيانات

setup_database()



@app.get("/students/")
def read_students():
  try:
    conn = sqlite3.connect('students.db')  # إنشاء اتصال بقاعدة البيانات
    cursor = conn.cursor()  # إنشاء مؤشر (cursor) للتفاعل مع قاعدة البيانات
    cursor.execute("SELECT * FROM students")  # تنفيذ استعلام SQL لجلب جميع الصفوف من جدول students
    rows = cursor.fetchall()  # جلب جميع النتائج من قاعدة البيانات
    conn.close()  # إغلاق الاتصال بقاعدة البيانات
    return rows  # إرجاع البيانات التي تم جلبها من قاعدة البيانات
  except sqlite3.Error as e:  # التعامل مع الأخطاء المحتملة
    print(e)  # طباعة الخطأ
    return {"error": "Failed to fetch students"}  # إرجاع رسالة خطأ في حالة فشل جلب البيانات
 

@app.post("/students/")
async def create_student(student: Student):
  try:
      conn = sqlite3.connect('students.db')
      cursor = conn.cursor()
      cursor.execute("INSERT INTO students (name, grade) VALUES (?, ?)", (student.name, student.grade))
      conn.commit()
      conn.close()
      return {"message": "Student added successfully"}
  except sqlite3.Error as e:
      print(e)
      return {"error": "Failed to create student"}


@app.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
  try:
    conn = sqlite3.connect('students.db')  # إنشاء اتصال بقاعدة البيانات
    cursor = conn.cursor()  # إنشاء مؤشر
    cursor.execute("UPDATE students SET name = ?, grade = ? WHERE id = ?",
                  (student.name, student.grade, student_id))  #SQL لتحديث بيانات طالب
    conn.commit()  # حفظ التغييرات في قاعدة البيانات
    conn.close()  # إغلاق الاتصال
    return {"id": student_id, **student.dict()}  # إرجاع بيانات الطالب المحدثة
  except sqlite3.Error as e:  # في حالة حدوث خطأ
    print(e)  # طباعة الخطأ
    return {"error": "Failed to update student"}  # إرجاع رسالة خطأ

@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
  try:
    conn = sqlite3.connect('students.db')  # إنشاء اتصال بقاعدة البيانات
    cursor = conn.cursor()  # إنشاء مؤشر
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))  # تنفيذ استعلام SQL لحذف طالب
    conn.commit()  # حفظ التغييرات في قاعدة البيانات
    conn.close()  # إغلاق الاتصال
    return {"message": "Student deleted"}  # إرجاع رسالة تأكيد الحذف
  except sqlite3.Error as e:  # في حالة حدوث خطأ
    print(e)  # طباعة الخطأ
    return {"error": "Failed to delete student"}  # إرجاع رسالة خطأ