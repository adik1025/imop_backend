from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from flask_cors import CORS
from __init__ import db
from model.coords import Coords
from model.user import User
from api.jwt_authorize import token_required
from flask_cors import cross_origin  # Importing cross_origin

coords_api = Blueprint('coords_api', __name__, url_prefix='/api')
CORS(coords_api, supports_credentials=True)
api = Api(coords_api)

class CoordsAPI:

    class _CRUD(Resource):


        def post(self):
            current_user = g.current_user
            data = request.get_json()

            coords = Coords(
                building_name=data.get('building_name'),
                lat=data.get('lat'),
                lng=data.get('lng'),
                condition=data.get('condition')
            )

            try:
                coords.create()
                return jsonify(coords.read())
            except Exception as e:
                return {'message': f'Error saving coordinates: {e}'}, 500


        def get(self):
            coords_id = request.args.get('id')

            if coords_id:
                coord = Coords.query.get(coords_id)
                if not coord:
                    return {'message': 'Coordinates not found'}, 404
                return jsonify(coord.read())

            all_coords = Coords.query.all()
            return jsonify([x.read() for x in all_coords])

        def put(self):
            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for updating coordinates'}, 400

            coord = Coords.query.get(data['id'])
            if not coord:
                return {'message': 'Coordinates not found'}, 404

            try:
                coord.update(data)
                return jsonify(coord.read())
            except Exception as e:
                return {'message': f'Error updating coordinates: {e}'}, 500

        def delete(self):
            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for deleting coordinates'}, 400

            coord = Coords.query.get(data['id'])
            if not coord:
                return {'message': 'Coordinates not found'}, 404

            try:
                coord.delete()
                return {'message': 'Coordinates deleted successfully'}, 200
            except Exception as e:
                return {'message': f'Error deleting coordinates: {e}'}, 500

    api.add_resource(_CRUD, '/coords')
