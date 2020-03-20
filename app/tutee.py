from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/tuition' # root for username, pw empty. if got pw -> root:pw@
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # initialise connection to db
CORS(app)

class Tutee(db.Model):
    __tablename__ = 'tutee'

    email = db.Column(db.String(64), primary_key = True)
    password = db.Column(db.String(64), nullable = False)
    fullname = db.Column(db.String(64), nullable = False)
    gender = db.Column(db.String(1), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    address = db.Column(db.String(64), nullable = False)
    contact_number = db.Column(db.String(8), nullable = False)

    def __init__(self, email, password, fullname, gender, age, address, contact_number):
        self.email = email
        self.password = password
        self.fullname = fullname
        self.gender = gender
        self.age = age
        self.address = address
        self.contact_number = contact_number

    def json(self):
        return {"email": self.email, "password": self.password, 
                "fullname": self.fullname, "gender": self.gender, 
                "age": self.age, "address": self.address, 
                "contact_number": self.contact_number}

@app.route("/tutee")
def get_all():
    return jsonify({"tutees": [tutee.json() for tutee in Tutee.query.all()]})

@app.route("/tutee/<string:email>")
def find_by_email(email):
    tutee = Tutee.query.filter_by(email=email).first()
    if tutee:
        return jsonify(tutee.json())
    return jsonify({"message": "Tutee not found"}), 404

@app.route("/tutee/<string:email>", methods=['POST'])
def register(isbn13):
    if (Tutee.query.filter_by(email=email).first()):
        return jsonify({"message": "A tutee with username '{}' already exists.".format(username)}), 400

    data = request.get_json()
    tutee = Tutee(email, **data) # ** means everything else after email

    try:
        db.session.add(tutee)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred registering the tutee."}), 500

    return jsonify(tutee.json()), 201

# basically prevents another file from doing app.run even if they import tutee.py
# because then __name__ is tutee.py
# but __main__ is the name of that file
if __name__ == '__main__':
    app.run(port = 5000, debug = True) # specify port in case u want to run more services