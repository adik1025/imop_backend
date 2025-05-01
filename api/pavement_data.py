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
        @cross_origin(supports_credentials=True)
        def post(self):
            current_user = g.current_user
            data = request.get_json()
            csv_string = data.get('csv', '')

            try:
                lines = csv_string.strip().split('\n')
                saved_rows = []

                # Skip the header row if it's present
                header = lines[0].lower()
                has_header = all(h in header for h in ['building_name', 'lat', 'lng', 'condition'])
                data_lines = lines[1:] if has_header else lines

                for line in data_lines:
                    # Split the CSV line by commas and clean up the whitespace around each value
                    row = [cell.strip() for cell in line.split(',')]

                    if not row or len(row) < 4 or not any(row):
                        continue  # Skip rows that don't have enough data or are empty

                    # Extract relevant columns only if they are present
                    building_name = row[0] if len(row) > 0 else None
                    lat = float(row[1]) if len(row) > 1 and row[1] else None
                    lng = float(row[2]) if len(row) > 2 and row[2] else None
                    condition = row[3] if len(row) > 3 else None

                    # Only process rows with valid columns (i.e., no missing or invalid values)
                    if building_name and lat is not None and lng is not None and condition:
                        try:
                            pavement = Pavement(
                                building_name=building_name,
                                lat=lat,
                                lng=lng,
                                condition=condition
                            )
                            pavement.create()
                            saved_rows.append(pavement.read())
                        except Exception as row_error:
                            # Optionally log the error or continue silently
                            continue

                return jsonify(saved_rows)
            except Exception as e:
                return {'message': f'Error saving pavements: {e}'}, 500


        
        

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