from flask import request
from flask_restx import Resource, fields
from flask import request
from flask_restx import Resource, fields


from sample_project.hospital_management import doctor_ns
from sample_project.hospital_management.v1.doctors.service import create_doctor, login

#create a signup form
#create signup model

signup_model = doctor_ns.model(
    "SignUp", {
        "id": fields.Integer(),
        "first_name": fields.String(required=True),
        "last_name" : fields.String(required=True),
        "gender": fields.String(required=True),
        "date_of_birth": fields.String(),
        "years_of_experience": fields.Integer(),
        "email": fields.String(required=True),
        "password": fields.String(required=True)
        
    }
)
#create a login form
# create login model
login_model = doctor_ns.model(
    "Login", {
        "email": fields.String(),
        "password": fields.String(required=True)
    }
)


class DoctorCreate(Resource):
    @doctor_ns.expect(signup_model)
    def post(self):
        data = request.json
        first_name = data["first_name"]
        last_name = data["last_name"]
        gender = data["gender"]
        date_of_birth = data["date_of_birth"]
        years_of_experience = data["years_of_experience"]
        email = data['email']
        password = data['password']


        doctor = create_doctor(first_name, last_name, gender, date_of_birth, years_of_experience, email, password)
        return doctor
    

    
class Login(Resource):
    @doctor_ns.expect(login_model)
    def post(self):
        """
        Log in an existing user
        """
        try:
            data = request.get_json()
            result = login(data)
            return result
        
        except Exception as e:
            return {"message": e}, 500