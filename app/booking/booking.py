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
    subject = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(64), nullable=False)

    def __init__(self, booking_id, tutor_id, tutee_id, payment, subject, status):
        self.booking_id = booking_id
        self.tutor_id = tutor_id
        self.tutee_id = tutee_id
        self.payment = payment
        self.subject = subject
        self.status = status

    def json(self):
        return {"booking_id": self.booking_id, "tutor_id": self.tutor_id, "tutee_id": self.tutee_id, "payment": self.payment, "subject": self.subject, "status": self.status}


@app.route("/booking")
def get_all():
    return jsonify({"Bookings": [booking.json() for booking in Booking.query.all()]})

@app.route("/booking/tutee/<string:tutee_id>")
def get_all_bookings_for_tutee(tutee_id):
    tuteeid = Booking.query.filter_by(tutee_id=tutee_id).first()
    if tuteeid:
        return jsonify(tuteeid.json())
    return jsonify({"message": "Tutee ID not found"}), 404

@app.route("/booking/tutor/<string:tutor_id>")
def get_all_bookings_for_tutor(tutor_id):
    tutorid = Booking.query.filter_by(tutor_id=tutor_id).first()
    if tutorid:
        return jsonify(tutorid.json())
    return jsonify({"message": "Tutor ID not found"}), 404

@app.route("/booking/status/<string:status>")
def get_all_bookings_based_status(status):
    status = Booking.query.filter_by(status=status)
    if status:
        return jsonify({"Bookings": [status.json() for status in Booking.query.all()]})
    return jsonify({"message": "Status not found"}), 404
    
@app.route("/booking/<string:booking_id>")
def find_by_booking_id(booking_id):
    booking_id = Booking.query.filter_by(booking_id=booking_id).first()
    if booking_id:
        return jsonify(booking_id.json())
    return jsonify({"message": "Booking ID not found."}), 404


@app.route("/booking/create/<string:booking_id>", methods=['POST'])
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

@app.route("/booking/delete/<string:booking_id>", methods=['DELETE'])
def delete_booking(booking_id):
    if not (Booking.query.filter_by(booking_id=booking_id).first()):
        return jsonify({"message": "A booking with ID '{}' does not exist.".format(booking_id)}), 400

    booking = Booking.query.filter_by(booking_id=booking_id).first()

    try:
        db.session.delete(booking)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred deleting the booking."}), 500

    return jsonify({"message": "Your booking has been successfully deleted"}), 201

# @app.route("/booking/filter/location/<string:location>")
# def filter_by_location(location):
@app.route("/booking/accept/<string:booking_id>", methods=['PUT'])
def accept_booking(booking_id):
    if not (Booking.query.filter_by(booking_id=booking_id).first()):
        return jsonify({"message": "A booking with ID '{}' is not found.".format(booking_id)}), 400  

    update = Booking.query.filter_by(booking_id=booking_id).first()

    try:
        update.status = 'Accepted'
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred updating the booking status."}), 500

    return jsonify({"message": "Your booking has been accepted."}), 201

@app.route("/booking/reject/<string:booking_id>", methods=['PUT'])
def reject_booking(booking_id):
    if not (Booking.query.filter_by(booking_id=booking_id).first()):
        return jsonify({"message": "A booking with ID '{}' is not found.".format(booking_id)}), 400  

    update = Booking.query.filter_by(booking_id=booking_id).first()

    try:
        update.status = 'Rejected'
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred updating the booking status."}), 500

    return jsonify({"message": "Your booking has been rejected."}), 201


if __name__ == '__main__':
    app.run(port=5002, debug=True)
    
