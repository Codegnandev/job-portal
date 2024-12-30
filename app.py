from flask import Flask
from flask_cors import CORS
import os
os.chdir(os.path.abspath(os.curdir))
from web.get_student_details import GetStudentDetails
from web.select_all import UpdateJobApplicants
from web.refreshboard import GoogleSheetReader
from flask_restful import Api
from web.bdelogin import BdeLogin
from web.get_job_details import GetJobDetails
from web.resumedownload import DownloadResumes
from web.bdesignup import BdeSignup
from web.companylogin import CompanyLogin
from web.companysignup import CompanySignup
from web.jobsapplied import GetAppliedJobsList
from web.applyforjobs import JobApplication
from web.studentsapplied import GetAppliedStudentList
from web.list_openings import ListOpenings
from web.studentsignup import StudentSignup
from web.studentlogin import StudentLogin
from web.jobpostings import JobPosting  # Import JobPosting from jobpostings module
from web.update_resume import UpdateResume
from web.student_OTP import StudentVerification
from web.validateOTP import ValidateOTP
import json
import urllib.parse
from pymongo import MongoClient 
from web.admin import AdminLogin
from web.all_student import GetAllStudents
from web.all_resumes import AllResumes
from web.edit_job import EditJob
from web.forgotpwd import ForgotPwd
from web.updatepwd import Updatepassword
from web.bde_forgotpwd import BDE_ForgotPWD
from web.bde_verifyotp import BDE_ValidateOTP
from web.bde_updatepwd import  BDE_updatePWD
from web.Request_otp import Quick_Request
from web.Request_call_form import Request_Callback


with open('local_config.json', 'r') as config_file:
    config_data = json.load(config_file)

MONGO_CONFIG = config_data['MONGO_CONFIG']

class MyFlask(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uri = MONGO_CONFIG['url']
        
        parsed_uri = urllib.parse.urlparse(uri)
        escaped_username = urllib.parse.quote_plus(parsed_uri.username)
        escaped_password = urllib.parse.quote_plus(parsed_uri.password)

        # Reconstruct URI with escaped username and password
        escaped_uri = uri.replace(parsed_uri.username, escaped_username).replace(parsed_uri.password, escaped_password)

        self.client = MongoClient(escaped_uri)
        self.db = self.client[MONGO_CONFIG['db_name']]
        self.collection = self.db[MONGO_CONFIG['collection_name']]

        self.bde_login_collection = MONGO_CONFIG["BDE_LOGIN"]["collection_name"]
        self.student_login_collection = MONGO_CONFIG["STUDENT_LOGIN"]["collection_name"]
        self.job_details_collection = MONGO_CONFIG["JOBS"]["collection_name"]
        self.company_login_collection = MONGO_CONFIG["COMPANY"]["collection_name"]
        self.otp_collection = MONGO_CONFIG["OTP_COLLECTION"]["collection_name"]
        self.admin_collection = MONGO_CONFIG["Admin_COLLECTION"]["collection_name"]
        self.request_call = MONGO_CONFIG["Web_Requests"]["collection_name"]
        
        self.DASHBOARDSHEET = config_data["DASHBOARD_GSHEET"]["url"]
        self.DASHBOARD_COLLECTION = config_data["DASHBOARD_GSHEET"]["collection"]
        self.SHEET_NAME = config_data["DASHBOARD_GSHEET"]["sheetname"]


    def add_api(self):
        api = Api(self, catch_all_404s=True)
        api.add_resource(
            StudentSignup,
            "/api/v1/signup",
            resource_class_kwargs={
                'client' : self.client,
                'db' : "codegnan_prod",
                'collection' : self.student_login_collection
                }
        )
        api.add_resource(
            StudentLogin,
            "/api/v1/studentlogin",
            resource_class_kwargs={
                'client' : self.client,
                'db' : "codegnan_prod",
                'collection' : self.student_login_collection
                }
        )
        api.add_resource(
            BdeSignup,
            "/api/v1/bdesignup",
            resource_class_kwargs = {
                'client' : self.client,
                'db' : "codegnan_prod",
                'collection' : self.bde_login_collection
            }
        )
        api.add_resource(
            BdeLogin,
            "/api/v1/bdelogin",
            resource_class_kwargs = {
                'client' : self.client,
                'db_name' : "codegnan_prod",
                'collection' : self.bde_login_collection
            }
        )
        api.add_resource(
            CompanyLogin,
            "/api/v1/companylogin",
            resource_class_kwargs = {
                'client' : self.client,
                'db' : "codegnan_prod",
                'collection' : self.company_login_collection
            }
        )
        api.add_resource(
            CompanySignup,
            "/api/v1/companysignup",
            resource_class_kwargs = {
                'client' : self.client,
                'db' : "codegnan_prod",
                'collection' : self.company_login_collection
            }
        )
        api.add_resource(
            JobPosting,
            "/api/v1/postjobs",
            resource_class_kwargs={
                'client' : self.client,
                'db' : "codegnan_prod",
                'collection': self.job_details_collection,
                'student_collection': self.student_login_collection
            }
        )
        api.add_resource(
            ListOpenings,
            "/api/v1/listopenings",
            resource_class_kwargs={
                'client' : self.client,
                'db' : "codegnan_prod",
                'collection': self.job_details_collection
            }
        )
        api.add_resource(
            JobApplication,
            "/api/v1/applyforjob",
            resource_class_kwargs = {
                'client' : self.client,
                'db' : "codegnan_prod",
                'job_collection': self.job_details_collection,
                'student_collection': self.student_login_collection
            }
        )
        api.add_resource(
            GetAppliedStudentList,
            "/api/v1/getappliedstudentslist",
            resource_class_kwargs = {
                'client' : self.client,
                'db' : "codegnan_prod",
                'job_collection': self.job_details_collection,
                'student_collection': self.student_login_collection
            }
        )
        api.add_resource(
            GetAppliedJobsList,
            "/api/v1/getappliedjobslist",
            resource_class_kwargs = {
                'client' : self.client,
                'db' : "codegnan_prod",
                'job_collection': self.job_details_collection,
                'student_collection': self.student_login_collection
            }
        )
        api.add_resource(
            DownloadResumes,
            "/api/v1/downloadresume",
            resource_class_kwargs = {
                'client' : self.client,
                'db': "codegnan_prod",
                "student_collection": self.student_login_collection
            }
        )

        api.add_resource(
            UpdateJobApplicants,
            "/api/v1/updatejobapplicants",
            resource_class_kwargs={
                'client' : self.client,
                'db' : "codegnan_prod",
                'job_collection': self.job_details_collection,
                'student_collection': self.student_login_collection,
                'bde_collection':self.bde_login_collection
            }
        )
        
        api.add_resource(
            GoogleSheetReader,
            "/api/v1/refreshdashboard",
            resource_class_kwargs = {
            }
        )

        api.add_resource(
            GetStudentDetails,
            "/api/v1/getstudentdetails",
            resource_class_kwargs={
                'client' : self.client,
                'db' : "codegnan_prod",
                'student_collection': self.student_login_collection
            }
        )

        api.add_resource(
            GetJobDetails,
            "/api/v1/getjobdetails",
            resource_class_kwargs={
                'client' : self.client,
                'db' : "codegnan_prod",
                'job_collection': self.job_details_collection
            }
        )
        api.add_resource(
            UpdateResume,
            "/api/v1/updateresume",
            resource_class_kwargs = {
                'client' : self.client, 
                'db': "codegnan_prod",
                "student_collection": self.student_login_collection
            }
        )
        api.add_resource(
            StudentVerification,
            "/api/v1/studentotp",
            resource_class_kwargs={
                'client' : self.client,
                'db' : "codegnan_prod",
                'otp_collection': self.otp_collection
            }
        )
        api.add_resource(
            ValidateOTP,
            "/api/v1/verifyotp",
            resource_class_kwargs={
                'client' : self.client,
                'db' : "codegnan_prod",
                'otp_collection': self.otp_collection
            }
        )
        api.add_resource(
            AdminLogin,
            "/api/v1/admin",
            resource_class_kwargs={
                'client' : self.client,
                'db' : "codegnan_prod",
                'admin_collection':self.admin_collection
            }
        )
        api.add_resource(
            GetAllStudents,
            "/api/v1/allstudents",
            resource_class_kwargs={
                'client' : self.client,
                'db' : "codegnan_prod",
                'student_collection': self.student_login_collection
            }
        )
        api.add_resource(
            AllResumes,
            "/api/v1/allresumes",
            resource_class_kwargs={
                'client' : self.client,
                'db' : "codegnan_prod",
                'student_collection': self.student_login_collection
            }
        )
        api.add_resource(
            EditJob,
            "/api/v1/editjob",
            resource_class_kwargs = {
                'client' : self.client, 
                'db': "codegnan_prod",
                "job_collection": self.job_details_collection
            }
        )
        api.add_resource(
            ForgotPwd,
            "/api/v1/forgotpassword",
            resource_class_kwargs={
                'client' : self.client,
                'db' : "codegnan_prod",
                'otp_collection': self.otp_collection,
                'std_collection':self.student_login_collection
            }
        )
        api.add_resource(
            Updatepassword,
            "/api/v1/updatepassword",
            resource_class_kwargs = {
                'client' : self.client, 
                'db': "codegnan_prod",
                "student_collection": self.student_login_collection
            }
        )
        api.add_resource(
            BDE_ForgotPWD,
            "/api/v1/bdeforgotpwd",
            resource_class_kwargs={
                'client' : self.client,
                'db' : "codegnan_prod",
                'otp_collection': self.otp_collection,
                'bde_collection':self.bde_login_collection
            }
        )
        api.add_resource(
            BDE_ValidateOTP,
            "/api/v1/verifybdeotp",
            resource_class_kwargs={
                'client' : self.client,
                'db' : "codegnan_prod",
                'otp_collection': self.otp_collection
            }
        )
        api.add_resource(
            BDE_updatePWD,
            "/api/v1/bdeupdatepwd",
            resource_class_kwargs={
            'client':self.client,
            'db':"codegnan_prod",
            'bde_collection':self.bde_login_collection
            }
        )
        api.add_resource(
            Quick_Request,
            "/api/v1/callrequest",
            resource_class_kwargs={
                'client' : self.client,
                'db' : "codegnan_prod",
                'Req_collection': self.otp_collection
            }
        )
        api.add_resource(
            Request_Callback,
            "/api/v1/requestform",
            resource_class_kwargs={
                'client':self.client,
                'db':'codegnan_prod',
                "Req_collection":self.request_call
            }       
        )
app = MyFlask(__name__)
app.add_api()
CORS(app,support_credentials=True)
if __name__ == '__main__':
    app.run()
