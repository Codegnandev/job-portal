from flask import Flask,jsonify
from flask_restful import Resource,abort
from pymongo import MongoClient
import logging

class GetAllStudents(Resource):
    def __init__(self,db,client,student_collection):
        super().__init__()
        self.client = client
        self.db = self.client[db]
        self.student_collection = self.db[student_collection]
        self.logger = logging.getLogger(__name__)
    def get(self):
        try:
            student_document = list(self.student_collection.find())
            for data in student_document:
                data['_id'] = str(data['_id'])   

            return jsonify((student_document))

        except Exception as e:
            self.logger.error(f"Database query failed: {e}")
            abort(500, message="Internal server error.")

        return jsonify({"error": "Unknown error occurred."}), 500