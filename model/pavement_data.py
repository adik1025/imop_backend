# post.py
import logging
from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError
from __init__ import app, db

class Pavement(db.Model):
    __tablename__ = 'pavement_data'

    id = db.Column(db.Integer, primary_key=True)
    building_name = db.Column(db.String(128), nullable=True)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    condition = db.Column(db.String(64), nullable=True)

    def __init__(self, building_name=None, lat=None, lng=None, condition=None):
        self.building_name = building_name
        self.lat = lat
        self.lng = lng
        self.condition = condition

    def __repr__(self):
        return f"Pavement(id={self.id}, building_name={self.building_name}, lat={self.lat}, lng={self.lng}, condition={self.condition})"

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not save pavement due to {str(e)}.")
            return None

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
        self.lat = data.get('lat', self.lat)
        self.lng = data.get('lng', self.lng)
        self.condition = data.get('condition', self.condition)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

            raise e

    @staticmethod
    def restore(data):
        for pavement_item in data:
            _ = pavement_item.pop('id', None)  # Remove 'id' if present
            pavement = Pavement(
                building_name=pavement_item.get('building_name'),
                lat=pavement_item.get('lat'),
                lng=pavement_item.get('lng'),
                condition=pavement_item.get('condition')
            )
            pavement.create()

def initPavement():
    with app.app_context():
        db.create_all()

        test_data = [
            Pavement(building_name='Library', lat=32.7157, lng=-117.1611, condition='Good'),
            Pavement(building_name='City Hall', lat=32.7167, lng=-117.1620, condition='Fair'),
            Pavement(building_name='Civic Center', lat=32.7145, lng=-117.1600, condition='Poor')
        ]

        for entry in test_data:
            try:
                entry.create()
                print(f"Record created: {repr(entry)}")
            except IntegrityError:
                db.session.remove()
                print(f"Record already exists: {entry.building_name}")