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
    tutee_contact_number = db.Column(db.String(8), nullable = False)
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


@app.route("/tutee/subject/<string:subject>")
def filter_by_Tutee_subject(subject):
    tutor = Tutor.query.filter_by(subject=subject).first()
    if tutor:
        return jsonify({"Tutor": [tutor.json() for tutor in Tutor.query.filter_by(subject=subject).all()]})
    return jsonify({"message": "Profile not found."}), 404



@app.route("/tutee/level/<string:level>")
def filter_by_Tutee_levels(level):
    tutee= Tutee.query.filter_by(level=level).first()
    if tutee:
        return jsonify({"Tutee": [tutee.json() for tutee in Tutee.query.filter_by(level=level).all()]})
    return jsonify({"message": "Profile not found."}), 404


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

@app.route("/tutee/request/<string:tutor_id>/<string:tutee_id>/<string:subject>")
def create_request(tutor_id, tutor_contact_number, tutee_id, tutee_contact_number, subject):
    """Create a new order according to the order_input"""
    # assume status==200 indicates success
    status = 200
    message = "Success"

    booking_id = 
    # Load the order info from a cart (from a file in this case; can use DB too, or receive from HTTP requests)
    try:
        with open(order_input) as sample_order_file:
            cart_order = json.load(sample_order_file)
    except:
        status = 501
        message = "An error occurred in loading the order cart."
    finally:
        sample_order_file.close()
    if status!=200:
        print("Failed order creation.")
        return {'status': status, 'message': message}

    # Return the newly created order when creation is succssful
    if status==200:
        print("OK order creation.")
        return order

def send_request(request):
    """inform Tutor/Booking Management as needed"""
    # default username / password to the borker are both 'guest'
    hostname = "localhost" # default broker hostname. Web management interface default at http://localhost:15672
    port = 5000 # default messaging port.
    # connect to the broker and set up a communication channel in the connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
        # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
        # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
    channel = connection.channel()

    # set up the exchange if the exchange doesn't exist
    exchangename="tutee_topic"
    channel.exchange_declare(exchange=exchangename, exchange_type='topic')

    # prepare the message body content
    message = json.dumps(order, default=str) # convert a JSON object to a string

   
    channel.basic_publish(exchange=exchangename, routing_key="tutor.request", body=message)
       

##start here
    # if "failure" in payment: # if some error happened in order creation
    #     # inform Error handler
    #     channel.queue_declare(queue='errorhandler', durable=True) # make sure the queue used by the error handler exist and durable
    #     channel.queue_bind(exchange=exchangename, queue='errorhandler', routing_key='*.error') # make sure the queue is bound to the exchange
    #     channel.basic_publish(exchange=exchangename, routing_key="shipping.error", body=message,
    #         properties=pika.BasicProperties(delivery_mode = 2) # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange)
    #     )
    #     print("Order status ({:d}) sent to error handler.".format(order["status"]))
    # inform Shipping and exit
        # prepare the channel and send a message to Shipping
    channel.queue_declare(queue='tutor', durable=True) # make sure the queue used by Shipping exist and durable
    channel.queue_bind(exchange=exchangename, queue='tutor', routing_key='*.request') # make sure the queue is bound to the exchange
    channel.basic_publish(exchange=exchangename, routing_key="tutor.request", body=message,
        properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
        )
    )
    print("Request sent to Tutor.")
    # close the connection to the broker
    connection.close()

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
    request = create_request()
    send_request(request)