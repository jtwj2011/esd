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
    tutor_contact_number = db.Column(db.String(8), nullable=False)
    name = db.Column(db.String(12), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(50), primary_key = True)
    subject_rate = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(1), nullable = False)
    review = db.Column(db.String(50), nullable = False)
    password_hash = db.Column(db.String(64))


    def __init__(self, tutor_id, contact_number, name, level, subject, subject_rate, gender, review, password_hash):
        self.tutor_id = tutor_id
        self.contact_number = contact_number
        self.name = name
        self.level = level
        self.subject = subject
        self.subject_rate = subject_rate
        self.gender = gender
        self.review = review
        self.password_hash = password_hash

    def json(self):
        return {"tutor_id": self.tutor_id, "contact_number": self.contact_number, "name": self.name, "level": self.level,"subject": self.subject, "subject_rate": self.subject_rate, "gender": self.gender, "review": self.review, "password_hash": self.password_hash}


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


@app.route("/tutor/profile/<string:tutor_id>")
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
    tutor = tutor(tutor_id, **data)

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
@app.route("/tutor/<string:tutor_id>/<string:contact_number>/<string:name>/<string:level>/<string:subject>/<string:subject_rate>", methods=['PUT'])
def update_tutor_profile(tutor_id, contact_number, name, level, subject, subject_rate):      #how to change password?   
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

        if tutor.level != level:
            try:
                tutor.level = level
                db.session.commit()
            except:
                return jsonify({"message": "An error occurred when updating the level."}), 500

        if tutor.subject != subject:
            try:
                tutor.subject = subject
                db.session.commit()
            except:
                return jsonify({"message": "An error occurred when updating the subject."}), 500

        if tutor.subject_rate != subject_rate:
            try:
                tutor.subject_rate = subject_rate
                db.session.commit()
            except:
                return jsonify({"message": "An error occurred when updating the subject rate."}), 500


        return jsonify(tutor.json()), 201

    else:
        return jsonify({"message": "User does not exist in the system."}), 400




@app.route("/tutor/gender/<string:gender>")
def filter_by_gender(gender):
    tutor = Tutor.query.filter_by(gender=gender).first()
    if tutor:
        return jsonify({"Tutor": [tutor.json() for tutor in Tutor.query.filter_by(gender=gender).all()]})
    return jsonify({"message": "Profile not found."}), 404



@app.route("/tutor/subject/<string:subject>")
def filter_by_Tutor_subject(subject):
    tutor = Tutor.query.filter_by(subject=subject).first()
    if tutor:
        return jsonify({"Tutor": [tutor.json() for tutor in Tutor.query.filter_by(subject=subject).all()]})
    return jsonify({"message": "Profile not found."}), 404



@app.route("/tutor/level/<string:level>")
def filter_by_Tutor_levels(level):
    tutor = Tutor.query.filter_by(level=level).first()
    if tutor:
        return jsonify({"Tutor": [tutor.json() for tutor in Tutor.query.filter_by(level=level).all()]})
    return jsonify({"message": "Profile not found."}), 404


def receiveRequest():
    # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue="tutor", durable=True) # 'durable' makes the queue survive broker restarts so that the messages in it survive broker restarts too
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='*.request') # bind the queue to the exchange via the key
        # any routing_key with two words and ending with '.order' will be matched

    # set up a consumer and start to wait for coming messages
    channel.basic_qos(prefetch_count=1) # The "Quality of Service" setting makes the broker distribute only one message to a consumer if the consumer is available (i.e., having finished processing and acknowledged all previous messages that it receives)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True) # 'auto_ack=True' acknowledges the reception of a message to the broker automatically, so that the broker can assume the message is received and processed and remove it from the queue
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("Received an order by " + file)
    result = processRequest(json.loads(body))
    # print processing result; not really needed
    json.dump(result, sys.stdout, default=str) # convert the JSON object to a string and print out on screen
    print() # print a new line feed to the previous json dump
    print() # print another new line as a separator

def processRequest(request):
    print("Processing a request:")
    print(request)
    # Can do anything here. E.g., publish a message to the error handler when processing fails.
    resultstatus = bool(random.getrandbits(1)) # simulate success/failure with a random True or False
    result = {'status': resultstatus, 'message': 'Simulated random s result.', 'order': order}
    resultmessage = json.dumps(result, default=str) # convert the JSON object to a string
    if not resultstatus: # inform the error handler when shipping fails
        print("Failed shipping.")
        # send the message to the eror handler
        channel.queue_declare(queue='errorhandler', durable=True) # make sure the queue used by the error handler exist and durable
        channel.queue_bind(exchange=exchangename, queue='errorhandler', routing_key='*.error') # make sure the queue is bound to the exchange
        channel.basic_publish(exchange=exchangename, routing_key="shipping.error", body=resultmessage,
            properties=pika.BasicProperties(delivery_mode = 2) # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange)
        )
    else:
        print("OK shipping.")
    return result


#filter by level, subject, price range
# @app.route("/tutor/<string:level>/<string:subject>/<string:rate>", methods=['POST'])
# def filter_by_level_subject_rate(level, subject, rate):



if __name__ == '__main__':
    app.run(port=5001, debug=True)
