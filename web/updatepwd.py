from flask import request
from flask_restful import Resource
from pymongo import MongoClient


class Updatepassword(Resource):
    def __init__(self,client,db,student_collection):
        super().__init__()
        self.client = client
        self.db_name = db
        self.student_update_resume = student_collection
        self.db = self.client[self.db_name]
        self.student_collection = self.db[self.student_update_resume]
    
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        print("user data----",email,password)
        if not email:
            return {"error": "Email not found Try again after sometime"}, 400
        else:
            data = self.student_collection.find_one({"email": email})
            if data:
                self.student_collection.update_one({"email":email},{"$set": {"password":password}})
                return {"message":"Password Updated Successfully..!","user":"Student"}, 200
            else:
                return {"message":"No data found for this email"},400