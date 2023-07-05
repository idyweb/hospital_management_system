from flask import request, jsonify
from flask_restx import Resource, fields
from flask import request
from flask_jwt_extended import (create_access_token, get_jwt_identity, jwt_required)
from flask_restx import Resource, fields

from sample_project.extensions import db
from sample_project.hospital_management import ns
from sample_project.hospital_management.v1.patients.service import create_patient, login


#create signup model
signup_model = ns.model(
    "SignUp", {
        "id": fields.Integer(),
        "full_name": fields.String(required=True),
        "gender": fields.String(required=True),
        "date_of_birth": fields.String(),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True)
        
    }
)

# create login model
login_model = ns.model(
    "Login", {
        "username": fields.String(required=True),
        "email": fields.String(),
        "password": fields.String(required=True)
    }
)


class PatientCreate(Resource):
    @ns.expect(signup_model)
    def post(self):
        data = request.json
        full_name = data["full_name"]
        gender = data["gender"]
        date_of_birth = data["date_of_birth"]
        username = data['username']
        email = data['email']
        password = data['password']


        patient = create_patient(full_name, gender, date_of_birth, username, email, password)
        return patient
    

    
class Login(Resource):
    @ns.expect(login_model)
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