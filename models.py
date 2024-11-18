from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    patients = db.relationship('Patient', backref='doctor', lazy=True, cascade='all, delete-orphan')


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    dob = db.Column(db.String(80))
    phone = db.Column(db.String(10))
    email = db.Column(db.String(80))
    address = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    logs = db.relationship('PatientLog', backref='patient', lazy=True, cascade='all, delete-orphan')


class PatientLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.String(80), nullable=False)
    notes = db.Column(db.Text)
