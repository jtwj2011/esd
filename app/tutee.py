import json
import sys
import os
import pika

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/tutee'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Tutee(db.Model):
    __tablename__ = 'tutee'

    tutee_id = db.Column(db.String(64), primary_key = True)
    contact_number = db.Column(db.String(8), nullable = False)
    name = db.Column(db.String(64), nullable = False)
    gender = db.Column(db.String(1), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    address = db.Column(db.String(64), nullable = False)
    password_hash = db.Column(db.String(64), nullable = False)

    def __init__(self, tutee_id, contact_number, name, gender, age, address, password_hash):
        self.tutee_id = tutee_id
        self.contact_number = contact_number
        self.name = name
        self.gender = gender
        self.age = age
        self.address = address
        self.password_hash = password_hash

    def json(self):
        return {"tutee_id": self.tutee_id, "contact_number": self.contact_number, 
                "name": self.name, "gender": self.gender, 
                "age": self.age, "address": self.address, 
                "password_hash": self.password_hash}

@app.route("/tutee")
def get_all():
    return jsonify({"tutees": [tutee.json() for tutee in Tutee.query.all()]})

@app.route("/tutee/<string:tutee_id>")
def find_by_tutee_id(tutee_id):
    tutee = Tutee.query.filter_by(tutee_id=tutee_id).first()
    if tutee:
        return jsonify(tutee.json())
    return jsonify({"message": "Tutee not found"}), 404



@app.route("/tutee/profile/<string:tutee_id>", methods=['POST'])
def create_tutee_profile(tutee_id):
    if (Tutee.query.filter_by(tutee_id=tutee_id).first()):
        return jsonify({"message": "A tutee with username '{}' already exists.".format(username)}), 400

    data = request.get_json()
    tutee = Tutee(tutee_id, **data) # ** means everything else after email

    try:
        db.session.add(tutee)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred registering the tutee."}), 500

    return jsonify(tutee.json()), 201

#attritubutes that can be updated:
# email, contact, name, address, subject_rate
@app.route("/tutee/<string:tutee_id>/<string:contact_number>/<string:password>/<string:fullname>/<string:address>/", methods=['POST'])
def update_tutee_profile(tutee_id, contact_number, name, address):
    if (Tutee.query.filter_by(tutee_id=tutee_id).first()):
        tutee = Tutee.query.filter_by(tutee_id=tutee_id).first()
        # issue: how do we check if the email is unique inside the database
        if tutee.tutee_id != tutee_id:
            try:
                tutee.tutee_id = tutee_id
                if (Tutee.query.filter_by(tutee_id=tutee.tutee_id).first()==False):
                    db.session.commit()
                else:
                    return jsonify({"message": "Tutee id already exists."}), 500
            except:
                return jsonify({"message": "An error occurred when updating the tutee id."}), 500

        if tutee.contact_number != contact_number:
            try:
                tutee.contact_number = contact_number
                db.session.commit()
            except:
                return jsonify({"message": "An error occurred when updating the contact number."}), 500
        
        if tutee.password != password:
            try:
                tutee.password = password
                db.session.commit()
            except:
                return jsonify({"message": "An error occurred when updating the password."}), 500

        if tutee.name != name:
            try:
                tutee.name = name
                db.session.commit()
            except:
                return jsonify({"message": "An error occurred when updating the name."}), 500

        if tutee.address != address:
            try:
                tutee.address = address
                db.session.commit()
            except:
                return jsonify({"message": "An error occurred when updating the address."}), 500

        return jsonify(tutee.json()), 201

    else:
        return jsonify({"message": "User does not exist in the system."}), 400

viewbookingsURL = "http://localhost:5002/booking/tutee/<tuteeid>"
def view_bookings(tutee_id):
    tutee_id = json.loads(json.dumps(tutee_id, default=str))
    bookings = requests.post(viewbookingsURL, json = tutee_id)
    #display bookings
    print(bookings)

viewsepcificbookingURL = "http://localhost:5002/booking/<booking_id>"
def view_particular_booking(booking_id):
    booking_id = json.loads(json.dumps(booking_id, default=str))
    booking = requests.post(viewspecificbookingURL, json = booking_id)
    #display bookings
    print(booking)

filterbookingbystatusURL = "http://localhost:5002/booking/status/<status>/tutee/<tutee_id>"
def filter_by_booking_status(status):
    status = json.loads(json.dumps(status, default=str))
    bookings = requests.post(filterbookingbystatusURL, json = status)
    #display bookings
    print(booking)

if __name__ == '__main__':
    app.run(port = 5000, debug = True)