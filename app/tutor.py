# handles profile upload and booking request?


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/tutor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
CORS(app)



class profile(db.Model):
    __tablename__ = 'profile'

    email = db.Column(db.String(24), primary_key=True)
    contact_number = db.Column(db.String(8), nullable=False)
    name = db.Column(db.String(12), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    subject_rate = db.relationship('subject_rate', backref='profile', lazy=True)

    def __init__(self, pid, contact_number, name, email, subject_rate):
        self.email = email
        self.contact_number = contact_number
        self.name = name
        self.subject_rate = subject_rate

    def json(self):
        return {"email": self.email, "contact number": self.contact_number, "name": self.name, "address": self.address, "subjects and rates": self.subject_rate}



class subject_rate(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(10), nullable=False)
    rate = db.Column(db.Integer)



@app.route("/tutor")
def get_all():
	return jsonify({"profile": [profile.json() for profile in profile.query.all()]})


@app.route("/tutor/<string:email>")
def find_by_profile_id(email):
    profile = profile.query.filter_by(email=email).first()
    if profile:
        return jsonify(profile.json())
    return jsonify({"message": "Profile not found."}), 404


@app.route("/tutor/<string:email>", methods=['POST'])
def create_profile():
    if (profile.query.filter_by(email=email).first()):
        return jsonify({"message": "A user with email '{}' already exists.".format(email)}), 400

    data = request.get_json()
    profile = profile(email, **data)

    try:
        db.session.add(profile)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred when uploading the profile."}), 500

    return jsonify(profile.json()), 201



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
