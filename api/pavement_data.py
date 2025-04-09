from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from flask_cors import CORS
from __init__ import db
from model.pavement_data import Pavement
from model.user import User
from api.jwt_authorize import token_required
from flask_cors import cross_origin  # Importing cross_origin

pavement_api = Blueprint('pavement_api', __name__, url_prefix='/api')
CORS(pavement_api, supports_credentials=True)
api = Api(pavement_api)

class PavementAPI:

    class _CRUD(Resource):
        
        @token_required()
        @cross_origin(supports_credentials=True)  # Add this decorator to handle CORS for PUT requests
        def post(self):

            current_user = g.current_user
            data = request.get_json()

            # if not data or 'seg_id' not in data or 'pci' not in data or 'pci_desc' not in data:
            #     return {'message': 'Segment ID, PCI, and PCI description are required'}, 400

            pavement = Pavement(
                cell=data.get('csv'),
            )

            try:
                pavement.create()
                return jsonify(pavement.read())
            except Exception as e:
                return {'message': f'Error saving pavement: {e}'}, 500

        @token_required()
        @cross_origin(supports_credentials=True)  # Add this decorator to handle CORS for PUT requests
        def get(self):

            pavement_id = request.args.get('id')

            if pavement_id:

                pavement = Pavement.query.get(pavement_id)
                if not pavement:
                    return {'message': 'Pavement not found'}, 404
                return jsonify(pavement.read())

            all_pavements = Pavement.query.all()
            return jsonify([x.read() for x in all_pavements])


        def put(self):

            # data = request.get_json()

            # if not data or 'id' not in data:
            #     return {'message': 'ID is required for updating a hotel'}, 400

            # hotel = Hotel.query.get(data['id'])
            # if not hotel:
            #     return {'message': 'Hotel not found'}, 404

            # try:
            #     hotel.update(data)
            #     return jsonify(hotel.read())
            # except Exception as e:
            #     return {'message': f'Error updating hotel: {e}'}, 500
            return

        def delete(self):

            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for deleting a pavement'}, 400

            pavement = Pavement.query.get(data['id'])
            if not pavement:
                return {'message': 'Pavement not found'}, 404
            try:
                pavement.delete()
                return {'message': 'Pavement deleted successfully'}, 200
            except Exception as e:
                return {'message': f'Error deleting pavement: {e}'}, 500

    api.add_resource(_CRUD, '/pavement')