from flask import request
from flask_restful import Resource
from pymongo import MongoClient
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Request_Callback(Resource):
    def __init__(self, client, db, Req_collection):
        super().__init__()
        self.client = client
        self.db_name = db
        self.collection_name = Req_collection
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def send_email(self, name, email):
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to Codegnan Destination!</title>
            <style>
                /* Global styles */
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #ffffff;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    border-radius: 10px;
                }}
                .content {{
                    text-align: center;
                }}
                h1, p {{
                    margin-bottom: 20px;
                }}
                .button {{
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #FFA500;
                    color: #ffffff;
                    text-decoration: none;
                    border-radius: 5px;
                    transition: background-color 0.3s ease;
                }}
                .button:hover {{
                    background-color: #FFD700;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="content">
                    <h1>Welcome to Codegnan Destination!</h1>
                    <p>Hello, {name},</p>
                    <p>Thank you for submitting your request form. We have successfully received your submission, and our team is currently reviewing your request.</p>
                    <p>We will get back to you within short time, with further updates or if we require additional information.</p>
                    <p>If you have any questions or need further assistance, please do not hesitate to contact us at <b>6301341478</b>,<b>9642988688</b>.</p>
                    <p>We are excited to have you on board and look forward to working together to achieve great success.</p>
                    <a href="https://www.codegnan.com" class="button">Explore Now</a>
                </div>
            </div>
        </body>
        </html>
        """

        sender_email = "placements@codegnan.com"
        recipient_email = email
        subject = "Welcome to Codegnan Placements!"

        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(html_content, 'html'))

        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)  
        smtp_server.starttls()
        smtp_server.login(sender_email, 'tlmc pumi pxhy gwko') 
        smtp_server.sendmail(sender_email, recipient_email, msg.as_string())
        smtp_server.quit()
    
    def post(self):
        name = request.json.get('name')
        email = request.json.get('email')
        phNo = request.json.get('phnumber')
        qualification = request.json.get('qualification')
        state = request.json.get('state')
        city = request.json.get('city')
        timestamp = datetime.now().isoformat()

        if self.db_name not in self.client.list_database_names():
            self.client[self.db_name]

        if self.collection_name not in self.db.list_collection_names():
            self.db.create_collection(self.collection_name)

        Request_data ={
            "name" : name,
            "email" : email,
            "phone_number" : phNo,
            "Qualification" : qualification,
            "state" : state,
            "city" : city,
            "Data_Time" : timestamp
        }
        print('request data:------',Request_data)
        result = self.collection.insert_one(Request_data)
        Request_data['_id'] = str(result.inserted_id)

        self.send_email(name, email)

        return {"message": "New Request Callback Form received successful", "user":Request_data}, 201
