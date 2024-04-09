from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel

app = FastAPI()



# Connect to MongoDB
client = MongoClient("mongodb+srv://sam:WeR713@library.4ggu5na.mongodb.net/?retryWrites=true&w=majority&appName=library")
db = client.library_db
students_collection = db["students"]

class Student(BaseModel):
    name: str
    age: int
    gender: str

@app.post("/students/", response_model=dict, status_code=201)
def create_student(student: Student):
    inserted_student = students_collection.insert_one(student.dict())
    return {"id": str(inserted_student.inserted_id), **student.dict()}

@app.get("/students/{student_id}", response_model=Student)
def read_student(student_id: str):
    student = students_collection.find_one({"_id": ObjectId(student_id)})
    if student:
        # Convert MongoDB document to Pydantic model instance
        return Student(**student)
    else:
        raise HTTPException(status_code=404, detail="Student not found")


@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: str, student: Student):
    updated_student = students_collection.update_one({"_id": ObjectId(student_id)}, {"$set": student.dict()})
    if updated_student.modified_count:
        return student
    else:
        raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: str):
    deleted_student = students_collection.delete_one({"_id": ObjectId(student_id)})
    if deleted_student.deleted_count:
        return
    else:
        raise HTTPException(status_code=404, detail="Student not found")

# HTML response with Swagger UI link
html_with_docs_link = """
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI with Swagger UI</title>
    </head>
    <body>
        <h1>Welcome to Library Management System</h1>
        <p>Access Swagger UI <a href="/docs">here</a>.</p>
    </body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return html_with_docs_link