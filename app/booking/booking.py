from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/booking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Booking(db.Model):
    __tablename__ = 'booking'

    booking_id = db.Column(db.String(13), primary_key=True)
    tutor_id = db.Column(db.String(64), nullable=False)
    tutee_id = db.Column(db.String(64), nullable=False)
    payment = db.Column(db.Float(precision=2), nullable=False)
    subjects = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(64), nullable=False)

    def __init__(self, booking_id, tutor_id, tutee_id, payment, subjects):
        self.booking_id = booking_id
        self.tutor_id = tutor_id
        self.tutee_id = tutee_id
        self.payment = payment
        self.subjects = subjects
        self.status = status

    def json(self):
        return {"booking_id": self.booking_id, "tutor_id": self.tutor_id, "tutee_id": self.tutee_id, "payment": self.payment, "subjects": self.subjects, "status": self.status}


@app.route("/booking")
def get_all():
    return jsonify({"Bookings": [booking.json() for booking in Booking.query.all()]})

@app.route("/booking/<string:tutee_id>")
def get_all_bookings_for_tutee(tutee_id):
    return jsonify({"Bookings": [booking.json() for booking in Booking.query.filter_by(tutee_id=tutee_id)]})

@app.route("/booking/<string:tutor_id>")
def get_all_bookings_for_tutor(tutor_id):
    return jsonify({"Bookings": [booking.json() for booking in Booking.query.filter_by(tutor_id=tutor_id)]})

@app.route("/booking/<string:status>")
def get_all_bookings_based_status(status):
    bookings = Booking.query.filter_by(status=status)
    #if bookings:
    return jsonify({"Bookings": [booking.json() for booking in Booking.query.all()]})
    #return jsonify({"message": "No Bookings available." }), 400
    

@app.route("/booking/<string:booking_id>")
def find_by_booking_id(booking_id):
    booking_id = Booking.query.filter_by(booking_id=booking_id).first()
    if booking_id:
        return jsonify(booking_id.json())
    return jsonify({"message": "Booking ID not found."}), 404


@app.route("/booking/<string:booking_id>", methods=['POST'])
def create_booking(booking_id):
    if (Booking.query.filter_by(booking_id=booking_id).first()):
        return jsonify({"message": "A booking with ID '{}' already exists.".format(booking_id)}), 400

    data = request.get_json()
    booking = Booking(booking_id, **data)

    try:
        db.session.add(booking)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the booking."}), 500

    return jsonify(booking.json()), 201

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    
