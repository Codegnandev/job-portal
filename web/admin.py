from flask import Request,request,jsonify
from flask_restful import Resource,abort
from pymongo import MongoClient

class AdminLogin(Resource):
    def __init__(self, client, db, admin_collection):
        super().__init__()
        self.client = client
        self.db_name = db
        self.collection_name = admin_collection
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def post(self):
        email = request.json.get("username")
        password = request.json.get("password")
        print('*'*50,email,password)
       
        if self.db_name not in self.client.list_database_names():
            self.client[self.db_name]

        
        if self.collection_name not in self.db.list_collection_names():
            self.db.create_collection(self.collection_name)

        # data = {"email": email,"password": password}
        # self.collection.insert_one(data)

        user = self.collection.find_one({"email": email})
        if user:
            # Email exists, check password
            if user["password"] == password:
                return {"message": "Login successful","userType":"admin"}, 200
            else:
                return {"message": "Username & Password incorrect"}, 400
        else:
            return {"message": "User not found"}, 404
