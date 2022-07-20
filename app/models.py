import hashlib
from flask_admin.contrib.sqla import ModelView
from app import db, admin
from app.auth import isLoggedIn, checkAdmin

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    userEmail = db.Column(db.String(50), unique=True)
    userPassword = db.Column(db.String(80))

    def __init__(self, username, userEmail, userPassword):
        self.username = username
        self.userEmail = userEmail
        self.userPassword = self.hashPassword(userPassword)

    def hashPassword(self, userPassword):
        hash = hashlib.sha256(userPassword.encode("utf-8")).hexdigest() 
        return hash

class Patient(db.Model):
    pID = db.Column(db.Integer, primary_key=True)
    pName = db.Column(db.String(50), nullable=False)
    pDoB = db.Column(db.Date, nullable=False)
    pAddress = db.Column(db.String, nullable=False)
    pPostcode = db.Column(db.String(15), nullable=False)
    pCity = db.Column(db.String(50), nullable=False)
    pTelephone = db.Column(db.String(20), nullable=False)

    pScans = db.relationship('Scan', backref='patient')

class Doctor(db.Model):
    dID = db.Column(db.Integer, primary_key=True)
    dName = db.Column(db.String(50), nullable=False)
    dTele = db.Column(db.String(20), nullable=False)
    dEmail = db.Column(db.String, nullable=False)

    dScans = db.relationship('Scan', backref='doctor')

class Scan(db.Model):
    sID = db.Column(db.Integer, primary_key=True)
    sDateTime = db.Column(db.Date, nullable=False)
    sModality = db.Column(db.String, nullable=False)
    sImage = db.Column(db.String(100), nullable=False)

    patientID = db.Column(db.Integer, db.ForeignKey('patient.pID'))
    doctorID = db.Column(db.Integer, db.ForeignKey('doctor.dID'))

class TestScan(db.Model):
    tID = db.Column(db.Integer, primary_key=True)
    tImage = db.Column(db.String(100), nullable=False)
    tMask = db.Column(db.String(100), nullable=False)

class MyModelView(ModelView):
    def is_accessible(self):
        if checkAdmin():
            return True
        return False

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Patient, db.session))
admin.add_view(MyModelView(Doctor, db.session))
admin.add_view(MyModelView(Scan, db.session))
admin.add_view(MyModelView(TestScan, db.session))