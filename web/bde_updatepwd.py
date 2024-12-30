from flask import request
from flask_restful import Resource
from pymongo import MongoClient

class BDE_updatePWD(Resource):
    def __init__(self,client,db,bde_collection):
        super().__init__()
        self.client = client 
        self.db = db
        self.bde_collection = bde_collection
        self.db = self.client[self.db]
        self.bde_collection = self.db[self.bde_collection]

    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        print("BDE user_data----",email,password)
        if not email:
            return {"error":"Email not found Try again after sometime"},400
        else:
            user = self.bde_collection.find_one({"email":email})
            if user:
                self.bde_collection.update_one({"email":email},{"$set": {"password":password}})
                return {"message":"Password Updated Successfully..!","user":"BDE-User"}, 200
            else:
                return {"message": "No data Found for this email"},400