from flask import request
from flask_restx import Resource, fields
from flask import request
from flask_restx import Resource, fields


from sample_project.hospital_management import admin_ns
from sample_project.hospital_management.v1.Admin.service import create_admin, login

#create a signup form
#create signup model

signup_model = admin_ns.model(
    "SignUp", {
        "id": fields.Integer(),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True)
        
    }
)
#create a login form
# create login model
login_model = admin_ns.model(
    "Login", {
        "email": fields.String(),
        "password": fields.String(required=True)
    }
)


class AdminCreate(Resource):
    @admin_ns.expect(signup_model)
    def post(self):
        data = request.json
        username = data["username"]
        email = data['email']
        password = data['password']


        admin = create_admin(username, email, password)
        return admin
    

    
class Login(Resource):
    @admin_ns.expect(login_model)
    def post(self):
        """
        Log in an existing admin
        """
        try:
            data = request.get_json()
            result = login(data)
            return result
        
        except Exception as e:
            return {"message": e}, 500