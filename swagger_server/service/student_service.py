import os
import tempfile
from functools import reduce

# from tinydb import TinyDB, Query

# db_dir_path = tempfile.gettempdir()
# db_file_path = os.path.join(db_dir_path, "students.json")
# student_db = TinyDB(db_file_path)

# def add(student=None):
#     queries = []
#     query = Query()
#     queries.append(query.first_name == student.first_name)
#     queries.append(query.last_name == student.last_name)
#     query = reduce(lambda a, b: a & b, queries)
#     res = student_db.search(query)
#     if res:
#         return 'already exists', 409

#     doc_id = student_db.insert(student.to_dict())
#     student.student_id = doc_id
#     return student.student_id

# def get_by_id(student_id=None, subject=None):
#     student = student_db.get(doc_id=int(student_id))
#     if not student:
#         return 'not found', 404
#     student['student_id'] = student_id
#     print(student)
#     return student

# def delete(student_id=None):
#     student = student_db.get(doc_id=int(student_id))
#     if not student:
#         return 'not found', 404
#     student_db.remove(doc_ids=[int(student_id)])
#     return student_id

from pymongo import MongoClient

mongo_uri = os.getenv('MONGO_URI')

if not mongo_uri:
    client = MongoClient()
else:
    client = MongoClient(mongo_uri)
    
db = client['students']

def add(student=None):
    if db.students.find_one({"first_name": student.first_name, "last_name": student.last_name}):
        return 'already exists', 409
    
    result = db.students.insert_one(student.to_dict())
    student_id = result.inserted_id
    return "Student added successfully"

def get_by_id(student_id=None, subject=None):
    student = db.students.find_one({"student_id": student_id})
    del student["_id"]
    if not student:
        return 'not found', 404
    return student

def delete(student_id=None):
    result = db.students.delete_one({"student_id": student_id})
    if result.deleted_count == 0:
        return 'not found', 404
    return "Student deleted successfully"