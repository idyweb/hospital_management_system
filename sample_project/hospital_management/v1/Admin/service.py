import bcrypt
from flask_jwt_extended import (create_access_token, create_refresh_token)

from sample_project.hospital_management.v1.Admin.model import Admin
from sample_project.extensions import db

def create_admin(username, email, password):
    existing_admin = Admin.query.filter_by(email=email).first()
    
    if existing_admin:
        return {"message": "email already exist", "status" :False}, 400
    
    hashed_password = bcrypt.hashpw(bytes(password, encoding="utf-8"), bcrypt.gensalt())
    
    admin = Admin(username=username, email=email, password=hashed_password)
    db.session.add(admin)
    db.session.commit()
    
    output = {
        
        "admin_id" : admin.id,
        "username" : admin.username,
        "email": admin.email
        
    }
    print(output)
    return {"message": f"Nice to have you, {username}", "admin": output, "status": True}, 201


def login(data):
    email = data['email']
    password = data['password']
    

    admin =Admin.query.filter_by(email = email).first()
    if not admin:
        return {"message": "Invalid username or password", "status":False}, 401
    
    
    if not bcrypt.checkpw(bytes(password, encoding="utf-8"), admin.password):
        
        return {"message" : "invalid password", "status" : False}
    
    # create an access token for the user
    
    access_token = create_access_token(identity =admin.email)
    refresh_token = create_refresh_token(identity=admin.email)
    output = {
        
        "doctor_id" : admin.id,
        "email" : admin.email
    }

    # return the access token
    return {"access_token": access_token, "refresh_token" :refresh_token, 
            "user":output, "status": True}, 200