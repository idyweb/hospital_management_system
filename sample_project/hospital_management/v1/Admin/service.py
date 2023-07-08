import bcrypt
from flask_jwt_extended import (create_access_token, create_refresh_token)

from sample_project.hospital_management.v1.Admin.model import Admin
from sample_project.hospital_management.v1.patients.model import Patient
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
    
    # create an access token for the admin
    
    access_token = create_access_token(identity =admin.email)
    refresh_token = create_refresh_token(identity=admin.email)
    output = {
        
        "doctor_id" : admin.id,
        "email" : admin.email
    }

    # return the access token
    return {"access_token": access_token, "refresh_token" :refresh_token, 
            "user":output, "status": True}, 200
    
    
#query all the patients from database
def list_all_patients(page, per_page):
    try:
        
        patients = Patient.query.paginate(page=page, per_page=per_page)
        patient_list = []
        if patients.items:
            
            for patient in patients.items:
                patient_data = {
                    "patient_id" :patient.id,
                    "full_name": patient.full_name,
                    "gender" : patient.gender,
                    "date_of_birth": patient.date_of_birth,
                    "username" : patient.username,
                    "email": patient.email,
                    
                }
                patient_list.append(patient_data)
            return {"message": "List of all patient", "patients": patient_list}
        else:
            return {"message": "List of all patients", "patients": []}
    except Exception as e:
        print(e)

#admin update patient
def update_patient(patient_id, full_name, gender, date_of_birth, username, email,password):
    current_patient = Patient.query.filter_by(username=current_patient).first()
    if not current_patient:
        return {"message": "Invalid user", "status": False}, 401


    patient = Patient.query.get(patient_id)
    if not patient:
        return {"message": "Patient not found", "status": False}, 404
    
    existing_username = Patient.query.filter(Patient.id != patient_id, Patient.username == username).first()
    if existing_username:
        return {"message": "Username already exists", "status": False}, 400

    existing_email = Patient.query.filter(Patient.id != patient_id, Patient.email == email).first()
    if existing_email:
        return {"message": "Email already exists", "status": False}, 400

    if password:
        hashed_password = bcrypt.hashpw(bytes(password, encoding="utf-8"), bcrypt.gensalt())
        patient.password = hashed_password
        
    patient.username = username
    patient.email = email
    patient.full_name = full_name
    patient.gender = gender
    patient.date_of_birth = date_of_birth
    
    
    db.session.commit()

    output = {
        "patient_id" : patient.id,
        "username": patient.username,
        "email": patient.email,
        "full_name": patient.full_name,
        "gender" : patient.gender,
        "date_of_birth" : patient.date_of_birth
        
    }
    return {"message": "Patient updated successfully", "patient": output, "status": True}, 200


def delete_patient(patient_id, current_patient):
    current_patient = Patient.query.filter_by(username=current_patient).first()
    if not current_patient:
        return {"message": "Invalid patient", "status": False}, 401
    

    patient = Patient.query.get(patient_id)
    if not patient:
        return {"message": "Patient not found", "status": False}, 404

    db.session.delete(patient)
    db.session.commit()

    return {"message": "Patient deleted successfully", "status": True}, 200
