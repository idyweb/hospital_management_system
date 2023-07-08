from flask_restx import Namespace

#admin route
admin_ns = Namespace("Admin", path="/admin")
from sample_project.hospital_management.v1.admin import views as admin_view

admin_ns.add_resource(admin_view.AdminCreate, "/create")
admin_ns.add_resource(admin_view.Login, "/login")



#patient route
ns = Namespace("Patient", path="/patient")
from sample_project.hospital_management.v1.patients import views as patient_view

ns.add_resource(patient_view.PatientCreate, "/create")
ns.add_resource(patient_view.Login, "/login")


#doctor route
doctor_ns = Namespace("Doctor", path="/doctor")
from sample_project.hospital_management.v1.doctors import views as doctor_view

doctor_ns.add_resource(doctor_view.DoctorCreate, "/create")
doctor_ns.add_resource(doctor_view.Login, "/login")


