from flask import Flask,send_file,request
from flask_restful import Resource
from pymongo import MongoClient
from gridfs import GridFS


class UpdateResume(Resource):
    #connecting to database for data
    def __init__(self,client,db,student_collection) -> None:
        super().__init__()
        self.client = client
        self.db_name = db
        self.student_update_resume = student_collection
        self.db = self.client[self.db_name]
        self.student_collection = self.db[self.student_update_resume]
        self.fs = GridFS(self.db)
    #post method to getting data
    def post(self):
        student_id = request.form["student_id"]
        resume_file = request.files.get('resume')
        pdf_content = resume_file.read()


        if not student_id:
            return {"error": "Missing required parameter: student_id"}, 400
        else:
            student_doc = self.student_collection.find_one({"id":student_id})

            if student_doc:
                # Find the file document in fs.files collection by filename (student ID)
                file_doc = self.db.fs.files.find_one({"filename": student_id})
                print(file_doc)
                if file_doc:
                    file_id = file_doc["_id"]
                    #deleting exsisted file
                    self.fs.delete(file_id)
                    #updating new file here
                    resume_id = self.fs.put(pdf_content, filename=student_id)
                    student_doc['resume_id'] = str(resume_id)
                    #print("resume updated",resume_id)
                    return {"message": "Resume Updated successful", "userType":"student","student_id":student_id}, 200
                else:
                        # Log or handle if a file is not found
                        print(f"File Not found with filename '{file_doc}'")
                        return {"message": "File Not found with student_id","student_id":student_id}, 404
            else:
                    # Log or handle if a student document is not found
                    print(f"No student found with ID '{student_id}'")
                    return {"message": "No student found","student_id":student_id}, 404
                    
        #return {"message": "Resume successful updated", "student": student_doc}, 201