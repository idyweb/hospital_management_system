from flask import Blueprint, current_app
from flask_restx import Api

from sample_project.hospital_management import ns
# from sample_project.person import ns as ns_person
from sample_project.hospital_management import doctor_ns
from sample_project.hospital_management import admin_ns


blueprint = Blueprint('api_1_0', __name__)


api = Api(
    blueprint,
    doc=current_app.config['API_DOCS_URL'],
    catch_all_404s=True
)
api.namespaces.clear()
api.add_namespace(ns)
api.add_namespace(doctor_ns)
api.add_namespace(admin_ns)
