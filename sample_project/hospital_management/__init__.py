from flask_restx import Namespace


ns = Namespace("Patient", path="/patient")
from sample_project.hospital_management.v1.patients import views as patient_view

ns.add_resource(patient_view.PatientCreate, "/create")
ns.add_resource(patient_view.Login, "/login")


#doctor route
doctor_ns = Namespace("Doctor", path="/doctor")
from sample_project.hospital_management.v1.doctors import views as doctor_view

doctor_ns.add_resource(doctor_view.DoctorCreate, "/create")
doctor_ns.add_resource(doctor_view.Login, "/login")