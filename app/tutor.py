# handles profile upload and booking request?


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/tutor'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/tutor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
CORS(app)



class Tutor(db.Model):
    __tablename__ = 'tutor'
    tutor_id = db.Column(db.String(24), primary_key=True)
    contact_number = db.Column(db.String(8), nullable=False)
    name = db.Column(db.String(12), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(50), primary_key = True)
    subject_rate = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(1), nullable = False)
    review = db.Column(db.String(50), nullable = False)
    password_hash = db.Column(db.String(64))


    def __init__(self, tutor_id, contact_number, name, location, level, subject, subject_rate, gender, review, password_hash):
        self.tutor_id = tutor_id
        self.contact_number = contact_number
        self.name = name
        self.location = location
        self.level = level
        self.subject = subject
        self.subject_rate = subject_rate
        self.gender = gender
        self.review = review
        self.password_hash = password_hash

    def json(self):
        return {"tutor_id": self.tutor_id, "contact_number": self.contact_number, "name": self.name, "location": self.location, "level": self.level,"subject": self.subject, "subject_rate": self.subject_rate, "gender": self.gender, "review": self.review, "password_hash": self.password_hash}


# class Review(db.Model):
#     email = db.Column(db.String(24), primary_key=True)
#     # didnt set nullable=False to allow zero records
#     review_record = db.Column(db.String(100))

#     def __init__(self, email, review_record):
#         self.email = email
#         self.review_record = review_record

#     def json(self):
#         return {"email": self.email, "review_record": self.review_record}


@app.route("/tutor")
def get_all():
	return jsonify({"Tutor": [tutor.json() for tutor in Tutor.query.all()]})


@app.route("/tutor/<string:tutor_id>")
def find_by_profile_id(tutor_id):
    tutor = Tutor.query.filter_by(tutor_id=tutor_id).first()
    if tutor:
        return jsonify({"Tutor": [tutor.json() for tutor in Tutor.query.filter_by(tutor_id=tutor_id).all()]})
    return jsonify({"message": "Profile not found."}), 404


@app.route("/tutor/<string:tutor_id>", methods=['POST'])
def create_tutor_profile(tutor_id):
    if (Tutor.query.filter_by(tutor_id=tutor_id).first()):
        return jsonify({"message": "A user with tutor_id '{}' already exists.".format(tutor_id)}), 400

    data = request.get_json()
    tutor = tutor(email, **data)

    try:
        db.session.add(tutor)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred when uploading the profile."}), 500

    return jsonify(tutor.json()), 201


@app.route("/tutor/<string:tutor_id>/<string:review>", methods=['POST'])
def create_review(tutor_id,review):
    if (Tutor.query.filter_by(tutor_id=tutor_id).first()):
        tutor = Tutor.query.filter_by(tutor_id=tutor_id).first()
        try:
            tutor.review = review
            db.session.commit()
        except:
            return jsonify({"message": "An error occurred when updating the review."}), 500
        return jsonify(tutor.json()), 201

    else:
        return jsonify({"message": "User does not exist in the system."}), 400


#attritubutes that can be updated:
# email, contact, name, address, subject_rate
@app.route("/tutor/<string:tutor_id>/<string:contact_number>/<string:name>/<string:subject>/<string:subject_rate>/<string:address>/", methods=['PUT'])
def update_tutor_profile(tutor_id, contact_number, name, location, level, subject, subject_rate):
    if (Tutor.query.filter_by(tutor_id=tutor_id).first()):
        tutor = Tutor.query.filter_by(tutor_id=tutor_id).first()
        # issue: how do we check if the email is unique inside the database
        if tutor.tutor_id != tutor_id:
            try:
                tutor.tutor_id = tutor_id
                if (Tutor.query.filter_by(tutor_id=tutor.tutor_id).first()==False):
                    db.session.commit()
                else:
                    return jsonify({"message": "tutor_id already exists."}), 500
            except:
                return jsonify({"message": "An error occurred when updating the tutor_id."}), 500

        if tutor.contact_number != contact_number:
            try:
                tutor.contact_number = contact_number
                db.session.commit()
            except:
                return jsonify({"message": "An error occurred when updating the contact number."}), 500

        if tutor.name != name:
            try:
                tutor.name = name
                db.session.commit()
            except:
                return jsonify({"message": "An error occurred when updating the name."}), 500

        if tutor.address != address:
            try:
                tutor.address = address
                db.session.commit()
            except:
                return jsonify({"message": "An error occurred when updating the address."}), 500

        return jsonify(tutor.json()), 201

    else:
        return jsonify({"message": "User does not exist in the system."}), 400




@app.route("/tutor/gender/<string:gender>")
def filter_by_gender(gender):
    tutor = Tutor.query.filter_by(gender=gender).first()
    if tutor:
        return jsonify({"Tutor": [tutor.json() for tutor in Tutor.query.filter_by(gender=gender).all()]})
    return jsonify({"message": "Profile not found."}), 404



#filter by level, subject, price range
# @app.route("/tutor/<string:level>/<string:subject>/<string:rate>", methods=['POST'])
# def filter_by_level_subject_rate(level, subject, rate):



if __name__ == '__main__':
    app.run(port=5001, debug=True)
