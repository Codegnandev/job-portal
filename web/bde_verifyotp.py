from flask import request
from flask_restful import Resource
from pymongo import MongoClient


class BDE_ValidateOTP(Resource):
    def __init__(self, client, db, otp_collection):
        super().__init__()
        self.client = client
        self.db_name = db
        self.collection_name = otp_collection
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def post(self):
        data = request.json
        email = data.get("email")
        otp = data.get("otp")
        print("BDE-otp verifying data----",email,otp)

        user = self.collection.find_one({"email": email})

        if user:
            if user["otp"] == otp:
                return {"message": "Email validation successful", "BDE_email":user["email"]}, 200
            else:
                return {"message": "OTP incorrect"}, 400
        else:
            return {"message": "User not found"}, 404
