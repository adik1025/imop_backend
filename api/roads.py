# api.py
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource  # used for REST API building
from model.roads import RoadModel  # import your RoadModel class

# Blueprint for Road API
road_api = Blueprint('road_api', __name__, url_prefix='/api')
api = Api(road_api)

class RoadAPI:
    class _Predict(Resource):
        def post(self):
            """
            Endpoint to predict 'pci23_d' class (e.g., 'Satisfactory', 'Good', 'Very Poor', etc.)
            based on road segment features.
            
            Example JSON body:
            {
              "pwidth": 36,
              "pav_length": 400.6361,
              "paveclass": "AC Improved",
              "funclass": "CL 2 LANE SUB-COLLECTOR"
            }
            """
            # Get JSON payload from the request
            road_features = request.get_json()
            
            # Get the singleton instance of the RoadModel
            road_model = RoadModel.get_instance()
            
            # Run the prediction
            response = road_model.predict(road_features)
            
            # Return the prediction probabilities (or single class) as JSON
            return jsonify(response)

    # Add the _Predict resource to the API
    api.add_resource(_Predict, '/roads')
