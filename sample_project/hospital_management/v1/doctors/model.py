from sample_project.extensions import db

#create a doctor model
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.String)
    years_of_experience = db.Column(db.Integer)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    