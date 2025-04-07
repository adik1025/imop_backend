from flask import Blueprint, jsonify
from flask_restful import Api, Resource
import json
from model.districts import maintenance

districts_api = Blueprint('blueprint_api', __name__, url_prefix='/api/districts')
api = Api(districts_api)

class DistrictsAPI(Resource):
    def get(self):
        
        return maintenance.getGeoJSON()

api.add_resource(DistrictsAPI, "/get")