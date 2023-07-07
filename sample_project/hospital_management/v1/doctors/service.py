import bcrypt
from flask_jwt_extended import (create_access_token, create_refresh_token)

from sample_project.hospital_management.v1.doctors.model import Doctor
from sample_project.extensions import db

def create_doctor(first_name, last_name, gender, date_of_birth, years_of_experience, email, password):
    existing_doctor = Doctor.query.filter_by(email).first()
    
    if existing_doctor:
        return {"message": "email already exist", "status" :False}, 400
    
    hashed_password = bcrypt.hashpw(bytes(password, encoding="utf-8"), bcrypt.gensalt())
    
    doctor = Doctor(first_name, last_name, gender, date_of_birth, years_of_experience, email, hashed_password)
    db.session.add(doctor)
    db.session.commit()
    
    output = {
        
        "doctor_id" : doctor.id,
        "first_name" : doctor.first_name,
        "last_name": doctor.last_name,
        "gender" : doctor.gender,
        "date_of_birth" : doctor.date_of_birth,
        "years_of_experience" : doctor.years_of_experience,
        "email": doctor.email,
        
    }
    print(output)
    return {"message": f"Nice to have you, Dr. {first_name}{last_name}", "doctor": output, "status": True}, 201