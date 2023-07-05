#import libraries
import bcrypt
from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required)

from sample_project.hospital_management.v1.patients.model import Patient
from sample_project.extensions import db

def create_patient(full_name, gender, date_of_birth, username, email, password):
    existing_patient = Patient.query.filter_by(username=username).first()
    
    if existing_patient:
        return {"message": "Username already exists", "status": False}, 400
    
    existing_email = Patient.query.filter_by(email=email).first()
    if existing_email:
        return {"message": "Email already exists", "status": False}, 400
    
    hashed_password = bcrypt.hashpw(bytes(password, encoding="utf-8"), bcrypt.gensalt())
    patient = Patient(full_name=full_name, gender=gender, date_of_birth=date_of_birth,username=username, email=email, password=hashed_password)
    db.session.add(patient)
    db.session.commit()
    
    output = {
        
        "patient_id" : patient.id,
        "full_name" : patient.full_name,
        "gender" : patient.gender,
        "date_of_birth" : patient.date_of_birth,
        "username": patient.username,
        "email": patient.email,
        
    }
    print(output)
    return {"message": "Patient created successfully", "patient": output, "status": True}, 201


def login(data):
    username = data['username']
    email = data['email']
    password = data['password']
    

    patient =Patient.query.filter_by(username = username).first()
    if not patient:
        return {"message": "Invalid username or password", "status":False}, 401
    
    #check if email matches
    if patient.email != email:
        return {"message" : "invalid email or password", "status" : False}, 401
    
    if not bcrypt.checkpw(bytes(password, encoding="utf-8"), patient.password):
        
        return {"message" : "invalid password", "status" : False}
    
    # create an access token for the patient
    
    access_token = create_access_token(identity =patient.username)
    refresh_token = create_refresh_token(identity=patient.username)
    output = {
        
        "patient_id" : patient.id,
        "username" : patient.username,
        "email" : patient.email
    }

    # return the access token
    return {"access_token": access_token, "refresh_token" :refresh_token, 
            "patient":output, "status": True}, 200