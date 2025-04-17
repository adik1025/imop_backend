import logging
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from __init__ import app, db




class Event(db.Model):  # Define the columns of the table
    """
    Event Model
   
    Represents an event with a title, description, and date.
    """
    __tablename__ = 'Schedules'


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)


    def __init__(self, title, description, date):
        self.title = title
        self.description = description
        if isinstance(date, str):  # Parse date string to date object
            self.date = datetime.strptime(date, '%Y-%m-%d').date()
        else:
            self.date = date


    def __repr__(self):
        return f"<Event(id={self.id}, title={self.title}, description={self.description}, date={self.date})>"


    def to_dict(self):
        """
        Convert the Event object into a dictionary format.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date.strftime('%Y-%m-%d')
        }
       
    def create(self):
        """
        Creates a new event in the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not create event '{self.title}' due to {str(e)}.")
            return None
        return self


    def update(self, data):
        """
        Updates the event with new data.
        """
        for key, value in data.items():
            if hasattr(self, key):
                # Convert date string to date object if necessary
                if key == 'date' and isinstance(value, str):
                    value = datetime.strptime(value, '%Y-%m-%d').date()
                setattr(self, key, value)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not update event '{self.title}' due to {str(e)}.")
            return None
        return self


    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            logging.warning(f"Could not delete event '{self.title}' due to IntegrityError.")
            return None


def initEvents():
    """
    Initializes the Events table with test data.
    """
    with app.app_context():
        db.create_all()
        events = [
            Event(title='UTLY', description='SS-000002-PV1', date='2025-05-20'),
            Event(title='S2024', description='SS-000003-PV1', date='2025-06-15'),
            Event(title='AC1704', description='SS-000006-PV1', date='2025-07-10'),
        ]
        for event in events:
            try:
                event.create()
                print(f"Record created: {repr(event)}")
            except IntegrityError as e:
                db.session.rollback()
                print(f"Records exist or duplicate error: {event.title}, {str(e)}")