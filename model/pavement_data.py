# post.py
import logging
from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError
from __init__ import app, db


class Pavement(db.Model):

    __tablename__ = 'pavement_data'

    id = db.Column(db.Integer, primary_key=True)
    cell  = db.Column(db.String(3), nullable=False)

    def __init__(self, cell):

        self.cell = cell

    def __repr__(self):

        return f"Pavement(id={self.id}, cell={self.cell})"

    def create(self):

        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not save '{self.cell}' due to {str(e)}.")
            return None
        return self
        
    def read(self):

        return {
            "id": self.id,
            "cell": self.cell,
        }
    
    def delete(self):

        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    def update(self, data):

        self.cell = data.get('cell', self.cell)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def restore(data):
        for pavement_item in data:
            _ = pavement_item.pop('id', None)  # Remove 'id' from post_data
            pavement_name = pavement_item.get("cell", None)
            pavement = Pavement.query.filter_by(cell=pavement_name).first()
            if pavement:
                pavement.update(pavement_item)
            else:
                pavement = Pavement(**pavement_item)
                pavement.update(pavement_item)
                pavement.create()

def initPavement():

    with app.app_context():

        db.create_all()

        test_data = [ # This is official 2023 data from https://data.sandiego.gov/datasets/streets-overall-condition-index/
            Pavement(cell='a,b,c,d,,e,f,g,h,,i,j,k,l,,m,n,o,p,,q,r,s,t,,u,v,w,x,,y,z'),
        ]
        
        for entry in test_data:
            try:
                entry.create()
                print(f"Record created: {repr(entry)}")
            except IntegrityError:
                db.session.remove()
                print(f"Record already exists: {entry.cell}")