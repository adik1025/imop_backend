# post.py
import logging
from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError
from __init__ import app, db


class Pavement(db.Model):

    __tablename__ = 'pavement_data'

    id = db.Column(db.Integer, primary_key=True)
    seg_id  = db.Column(db.String(3), nullable=False)
    pci = db.Column(db.String(3), nullable=False)
    pci_desc = db.Column(db.String(3), nullable=False)

    def __init__(self, seg_id, pci, pci_desc):

        self.seg_id = seg_id
        self.pci = pci
        self.pci_desc = pci_desc

    def __repr__(self):

        return f"Pavement(id={self.id}, seg_id={self.seg_id}, pci={self.pci}, pci_desc={self.pci_desc})"

    def create(self):

        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not save '{self.seg_id}', '{self.pci}', and '{self.pci_desc}' due to {str(e)}.")
            return None
        return self
        
    def read(self):

        return {
            "id": self.id,
            "seg_id": self.seg_id,
            "pci": self.pci,
            "pci_desc": self.pci_desc
        }
    
    def delete(self):

        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    def update(self, data):

        self.seg_id = data.get('seg_id', self.seg_id)
        self.pci = data.get('pci', self.pci)
        self.pci_desc = data.get('pci_desc', self.pci_desc)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def restore(data):
        for pavement_item in data:
            _ = pavement_item.pop('id', None)  # Remove 'id' from post_data
            pavement_name = pavement_item.get("hotel", None)
            pavement = Pavement.query.filter_by(hotel=pavement_name).first()
            if pavement:
                pavement.update(pavement_item)
            else:
                pavement = Pavement(**pavement_item)
                pavement.update(pavement_item)
                pavement.create()

def initHotel():

    with app.app_context():

        db.create_all()

        test_data = [ # This is official 2023 data from https://data.sandiego.gov/datasets/streets-overall-condition-index/
            Pavement(seg_id='SS-000001-PV1', pci='', pci_desc=''),
            Pavement(seg_id='SS-000002-PV1', pci='56.59', pci_desc='Fair'),
            Pavement(seg_id='SS-000003-PV1', pci='80', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000004-PV1', pci='86.4', pci_desc='Good'),
            Pavement(seg_id='SS-000005-PV1', pci='67.86', pci_desc='Fair'),
            Pavement(seg_id='SS-000006-PV1', pci='95.53', pci_desc='Good'),
            Pavement(seg_id='SS-000007-PV1', pci='87.44', pci_desc='Good'),
            Pavement(seg_id='SS-000008-PV1', pci='67.61', pci_desc='Fair'),
            Pavement(seg_id='SS-000009-PV1', pci='89.71', pci_desc='Good'),
            Pavement(seg_id='SS-000010-PV1', pci='70.12', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000011-PV1', pci='86.65', pci_desc='Good'),
            Pavement(seg_id='SS-000012-PV1', pci='91.41', pci_desc='Good'),
            Pavement(seg_id='SS-000013-PV1', pci='51.16', pci_desc='Poor'),
            Pavement(seg_id='SS-000014-PV1', pci='91.47', pci_desc='Good'),
            Pavement(seg_id='SS-000015-PV1', pci='91.31', pci_desc='Good'),
            Pavement(seg_id='SS-000016-PV1', pci='60.48', pci_desc='Fair'),
            Pavement(seg_id='SS-000018-PV1', pci='57.95', pci_desc='Fair'),
            Pavement(seg_id='SS-000019-PV1', pci='19.88', pci_desc='Serious'),
            Pavement(seg_id='SS-000020-PV1', pci='43.24', pci_desc='Poor'),
            Pavement(seg_id='SS-000021-PV1', pci='50.49', pci_desc='Poor'),
            Pavement(seg_id='SS-000022-PV1', pci='47.7', pci_desc='Poor'),
            Pavement(seg_id='SS-000023-PV1', pci='45.9', pci_desc='Poor'),
            Pavement(seg_id='SS-000024-PV1', pci='92.34', pci_desc='Good'),
            Pavement(seg_id='SS-000025-PV1', pci='88.2', pci_desc='Good'),
            Pavement(seg_id='SS-000026-PV1', pci='12.92', pci_desc='Serious'),
            Pavement(seg_id='SS-000027-PV1', pci='63.64', pci_desc='Fair'),
            Pavement(seg_id='SS-000028-PV1', pci='70.29', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000029-PV1', pci='52.46', pci_desc='Poor'),
            Pavement(seg_id='SS-000030-PV1', pci='70.97', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000031-PV1', pci='85.4', pci_desc='Good'),
            Pavement(seg_id='SS-000032-PV1', pci='29.76', pci_desc='Very Poor'),
            Pavement(seg_id='SS-000033-PV1', pci='74.85', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000034-PV1', pci='69.2', pci_desc='Fair'),
            Pavement(seg_id='SS-000035-PV1', pci='79.71', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000036-PV1', pci='86.54', pci_desc='Good'),
            Pavement(seg_id='SS-000037-PV1', pci='25.73', pci_desc='Very Poor'),
            Pavement(seg_id='SS-000038-PV1', pci='48.64', pci_desc='Poor'),
            Pavement(seg_id='SS-000039-PV1', pci='29.24', pci_desc='Very Poor'),
            Pavement(seg_id='SS-000041-PV1', pci='87.52', pci_desc='Good'),
            Pavement(seg_id='SS-000042-PV1', pci='80.79', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000043-PV1', pci='80.32', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000044-PV1', pci='76.79', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000045-PV1', pci='78.2', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000046-PV1', pci='75.71', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000047-PV1', pci='53.83', pci_desc='Poor'),
            Pavement(seg_id='SS-000048-PV1', pci='90.6', pci_desc='Good'),
            Pavement(seg_id='SS-000049-PV1', pci='88.76', pci_desc='Good'),
            Pavement(seg_id='SS-000050-PV1', pci='73.17', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000051-PV1', pci='67.73', pci_desc='Fair'),
            Pavement(seg_id='SS-000052-PV1', pci='82.81', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000053-PV1', pci='74.86', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000054-PV1', pci='64.07', pci_desc='Fair'),
            Pavement(seg_id='SS-000055-PV1', pci='67.02', pci_desc='Fair'),
            Pavement(seg_id='SS-000056-PV1', pci='89.45', pci_desc='Good'),
            Pavement(seg_id='SS-000057-PV1', pci='82.67', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000058-PV1', pci='79.04', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000059-PV1', pci='70.72', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000060-PV1', pci='98.26', pci_desc='Good'),
            Pavement(seg_id='SS-000061-PV1', pci='98.21', pci_desc='Good'),
            Pavement(seg_id='SS-000062-PV1', pci='54.28', pci_desc='Poor'),
            Pavement(seg_id='SS-000063-PV1', pci='54.81', pci_desc='Poor'),
            Pavement(seg_id='SS-000064-PV1', pci='85.56', pci_desc='Good'),
            Pavement(seg_id='SS-000065-PV1', pci='74.58', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000066-PV1', pci='61.82', pci_desc='Fair'),
            Pavement(seg_id='SS-000067-PV1', pci='55.34', pci_desc='Fair'),
            Pavement(seg_id='SS-000068-PV1', pci='37.51', pci_desc='Very Poor'),
            Pavement(seg_id='SS-000069-PV1', pci='82', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000070-PV1', pci='90.8', pci_desc='Good'),
            Pavement(seg_id='SS-000071-PV1', pci='49.29', pci_desc='Poor'),
            Pavement(seg_id='SS-000072-PV1', pci='62.1', pci_desc='Fair'),
            Pavement(seg_id='SS-000073-PV1', pci='64.31', pci_desc='Fair'),
            Pavement(seg_id='SS-000074-PV1', pci='74.55', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000075-PV1', pci='76.1', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000076-PV1', pci='35.85', pci_desc='Very Poor'),
            Pavement(seg_id='SS-000078-PV1', pci='32.11', pci_desc='Very Poor'),
            Pavement(seg_id='SS-000079-PV1', pci='86.4', pci_desc='Good'),
            Pavement(seg_id='SS-000080-PV1', pci='90.1', pci_desc='Good'),
            Pavement(seg_id='SS-000081-PV1', pci='39.12', pci_desc='Very Poor'),
            Pavement(seg_id='SS-000082-PV1', pci='66.94', pci_desc='Fair'),
            Pavement(seg_id='SS-000083-PV1', pci='64.12', pci_desc='Fair'),
            Pavement(seg_id='SS-000084-PV1', pci='71.77', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000085-PV1', pci='74.54', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000086-PV1', pci='74.39', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000087-PV1', pci='66.75', pci_desc='Fair'),
            Pavement(seg_id='SS-000088-PV1', pci='87.6', pci_desc='Good'),
            Pavement(seg_id='SS-000089-PV1', pci='43.04', pci_desc='Poor'),
            Pavement(seg_id='SS-000090-PV1', pci='83.88', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000091-PV1', pci='98.8', pci_desc='Good'),
            Pavement(seg_id='SS-000092-PV1', pci='94', pci_desc='Good'),
            Pavement(seg_id='SS-000093-PV1', pci='100', pci_desc='Good'),
            Pavement(seg_id='SS-000094-PV1', pci='82.06', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000095-PV1', pci='77.48', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000096-PV1', pci='70.12', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000097-PV1', pci='61.66', pci_desc='Fair'),
            Pavement(seg_id='SS-000098-PV1', pci='62.29', pci_desc='Fair'),
            Pavement(seg_id='SS-000099-PV1', pci='83.62', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000100-PV1', pci='74.32', pci_desc='Satisfactory'),
            Pavement(seg_id='SS-000101-PV1', pci='67.16', pci_desc='Fair'),
            Pavement(seg_id='SS-000102-PV1', pci='57.02', pci_desc='Fair'),
            Pavement(seg_id='SS-000103-PV1', pci='74.66', pci_desc='Satisfactory')
        ]
        
        for entry in test_data:
            try:
                entry.create()
                print(f"Record created: {repr(entry)}")
            except IntegrityError:
                db.session.remove()
                print(f"Record already exists: {entry.seg_id}, {entry.pci}, {entry.pci_desc}")