# post.py
import logging
from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError
import csv
import os
from __init__ import app, db



class Coords(db.Model):

    __tablename__ = 'coords'

    id = db.Column(db.Integer, primary_key=True)
    building_name  = db.Column(db.String(3), nullable=False)
    lat  = db.Column(db.String(3), nullable=False)
    lng  = db.Column(db.String(3), nullable=False)
    condition  = db.Column(db.String(3), nullable=False)

    def __init__(self, building_name, lat, lng, condition):
        self.building_name = building_name
        self.lat = lat
        self.lng = lng
        self.condition = condition
        
    def __repr__(self):

        return f"Coords(id={self.id}, building_name={self.building_name}, lat={self.lat}, lng={self.lng}, condition={self.condition})"

    def create(self):

        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not save '{self.building_name}' due to {str(e)}.")
            return None
        return self
        
    def read(self):

        return {
            "id": self.id,
            "building_name": self.building_name,
            "lat": self.lat,
            "lng": self.lng,
            "condition": self.condition
        }
    
    def delete(self):

        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    def update(self, data):

        self.building_name = data.get('building_name', self.building_name)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def restore(data):
        for coords_item in data:
            _ = coords_item.pop('id', None)  # Remove 'id' from post_data
            coords_name = coords_item.get("cell", None)
            coord = Coords.query.filter_by(cell=coords_name).first()
            if coord:
                coord.update(coords_item)
            else:
                coord = Coords(**coords_item)
                coord.update(coords_item)
                coord.create()

def initCoords():
    with app.app_context():
        db.create_all()
        
        file_path = "datasets/facilityConditionIndexRatings/facilities_assessment_datasd.csv"
        file_path = "datasets/graffiti_requests_open.csv"
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    building_name = row['building_name']
                    lat = row['lat']
                    lng = row['lng']
                    condition = row['condition']
                    condition = row['status']


                    if not (building_name and lat and lng):
                        continue
                    
                    coord = Coords(
                        building_name=building_name.strip(),
                        lat=lat.strip(),
                        lng=lng.strip(),
                        condition=condition.strip()
                    )
                    try:
                        coord.create()
                        print(f"Record created: {repr(coord)}")
                    except IntegrityError:
                        db.session.remove()
                        print(f"Record already exists or error creating: {building_name}")
        except FileNotFoundError:
            print(f"CSV file not found at path: {file_path}")