from flask import request
from flask_restful import Resource
from pymongo import MongoClient
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 


class BDE_ForgotPWD(Resource):
    def __init__(self,client,db,otp_collection,bde_collection):
        super().__init__()
        self.client = client
        self.db_name = db
        self.bde_collection = bde_collection
        self.collection_name = otp_collection
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]
        self.bde_collection = self.db[self.bde_collection]

    def send_email(self, email, otp,name):
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to Codegnan Placements!</title>
        </head>
        <body>
            <p>Dear BDE { name },</p>
                <p>We have sent you a One-Time-Password(OTP) to verify your request. Please use below code</p>
                <p>Your OTP is:- <b style="font-size:25px">{ otp }</b> </p> 
                <p><b>Note:</b></p>
                <p>This OTP will expire in 10 minutes from the time of request.</p>
                <p>At CodegnanDestination,we are committed in helping you to achieve your goals and aspirations.</p>
                <p>Our team is here to support you in every step.</p>
                <p>Feel free to revert back for any more queries</p><br><br>
            <p><b>Best Regards,</b></p>
            <p>CodegnanDestination Placements Team</p>
            
        </body>
        </html>
        """
        #Emial detials
        sender_email = "Placements@codegnan.com"
        recipient_email = email
        subject = "OTP for your Forgot Password!"
                
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(html_content, 'html'))
        
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(sender_email, 'tlmc pumi pxhy gwko')#Codegnan@0818# Update with your sender's email and password
        smtp_server.sendmail(sender_email, recipient_email, msg.as_string())
        smtp_server.quit()

    def post(self):
        email = request.json.get('email')
        print("bde-forgotpassword to emailvarify",email)
        data = self.bde_collection.find_one({"email": email})
        print('bde---------------',data['name'])
        if not email:
            return {"error": "Email is required"}, 400
        if self.collection.find_one({"email": email}):
            self.collection.drop()
        
        otp = random.randint(100000, 999999)

        # Save OTP to the database
        otp_data = {"email": email,"otp": otp}
        self.collection.insert_one(otp_data)

        # Send OTP email
        self.send_email(email, otp,data['name'])

        return {"message": "OTP sent successfully","user":"BDE-User"}, 200