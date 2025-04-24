import logging
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.event import Event
from flask_cors import CORS
from __init__ import db
from model.pavement_data import Pavement
from model.user import User
from api.jwt_authorize import token_required
from flask_cors import cross_origin  # Importing cross_origin
# Define the blueprint
event_api = Blueprint('event_api', __name__, url_prefix='/api')
CORS(event_api, supports_credentials=True)


api = Api(event_api)  # Create an instance of the Api class


class EventAPI:
    class _CRUD(Resource):


        @cross_origin(supports_credentials=True)        
        def post(self):
            """
            Create a new event.
            """
            data = request.get_json()  # Change JSON to Python dictionary


            if not data:
                return {'message': 'No input data provided'}, 400
            if 'title' not in data:
                return {'message': 'Event title is required'}, 400
            if 'description' not in data:
                return {'message': 'Event description is required'}, 400
            if 'date' not in data:
                return {'message': 'Event date is required'}, 400


            # Create a new event object
            event = Event(title=data['title'], description=data['description'], date=data['date'])
            event.create()


            return jsonify(event.to_dict()), 201
        @cross_origin(supports_credentials=True)
        def get(self):  # Display and retrieve all events
            """
            Retrieve all Events.
            """
            events = Event.query.all()  # Retrieve all events
            if not events:
                return {'message': 'No events found'}, 404  
            return jsonify([event.to_dict() for event in events])  # Return a list of events as JSON
        @cross_origin(supports_credentials=True)        
        def put(self):
            """
            Update an event.
            """
            data = request.get_json()  # Change JSON to Python dictionary


            if not data or 'id' not in data:
                return {'message': 'Event ID is required'}, 400


            event = Event.query.get(data['id'])  # Retrieve event by ID
            if event is None:
                return {'message': 'Event not found'}, 404


            updated_event = event.update(data)
            if updated_event:
                return jsonify(updated_event.to_dict())
            else:
                return {'message': 'An error occurred while updating the event. Please try again.'}, 500
        @cross_origin(supports_credentials=True)
        def delete(self):
            """
            Delete an event.
            """
            data = request.get_json()
            if not data or 'id' not in data:
                return {'message': 'Event ID is required'}, 400
           
            event = Event.query.get(data['id'])
            if event is None:
                return {'message': 'Event not found'}, 404
            event.delete()
            return jsonify({"message": "Event deleted"}), 200


    class _BULK_CRUD(Resource):  # Handle multiple requests at once
        @cross_origin(supports_credentials=True)
        def post(self):
            """
            Handle bulk event creation by sending POST requests to the single event endpoint.
            """
            events = request.get_json()


            if not isinstance(events, list):  # Ensure that the input events is a list.
                return {'message': 'Expected a list of event data'}, 400


            results = {'errors': [], 'success_count': 0, 'error_count': 0}


            for event_data in events:
                try:
                    event = Event(**event_data)
                    event.create()
                    results['success_count'] += 1
                except Exception as e:
                    results['errors'].append({'data': event_data, 'error': str(e)})
                    results['error_count'] += 1


            return jsonify(results), 200
        @cross_origin(supports_credentials=True)
        def get(self):
            """
            Retrieve all events.
            """
            events = Event.query.all()
            if not events:
                return {'message': 'No events found'}, 404  
            return jsonify([event.to_dict() for event in events])


    """
    Map the _CRUD and _BULK_CRUD classes to the API endpoints for /event and /events.
    """
    api.add_resource(_CRUD, '/event')
    api.add_resource(_BULK_CRUD, '/events')