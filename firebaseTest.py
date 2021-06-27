import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
###############################################################
import flask
from flask import jsonify # <- `jsonify` instead of `json`
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import request, render_template, url_for, redirect, send_from_directory, flash
from flask import Response, make_response
################################################################
from werkzeug.utils import secure_filename
from sqlalchemy import update, func
from sqlalchemy.ext.declarative import DeclarativeMeta
import flask, decimal, datetime, json, pprint, sys, importlib, os, errno
from sqlalchemy.inspection import inspect
import zipfile
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.serving import run_simple
import docker
from docker import client
import dockerpty
client = docker.from_env()
client = docker.APIClient(base_url='unix://var/run/docker.sock')
from io import BytesIO
from docker import APIClient
from os import path
from pathlib import Path
from time import time
import shutil
from time import sleep
from time import *             #meaning from time import EVERYTHING
#### NEW IMPORTS ####
from time import sleep
from flask import copy_current_request_context
import threading
import datetime
#####################
from werkzeug.exceptions import HTTPException
from flask import abort
from werkzeug.exceptions import Unauthorized
#####################

#######################################
#### Use a service account & Initialise the FIREBASE ######
cred = credentials.Certificate('/home/chiefai/firebaseTest/vitalsigns-d97ae-firebase-adminsdk-tlhpz-2916b2a50e.json')
default_app = firebase_admin.initialize_app(cred)
dbfirestore = firestore.client()

######### UPLOAD FOLDER OPTIONS ###################
UPLOAD_FOLDER = "/home/chiefai/production/data"
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'pdf', 'png', 'jpg', 'jpeg', 'tif', 'tiff', 'gif', 'h5', 'pkl', 'py', 'joblib', 'zip', '7z'])
###################################################


#### Initialise the Flask app
#app = flask.Flask(__name__, template_folder='templates')
app = Flask(__name__)
#app.config['SECRET_KEY'] = 'supersecretkeygoeshere'

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response
app.after_request(add_cors_headers)


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        """JSON encoder function for SQLAlchemy special classes."""
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


class AlchemyEncoder(json.JSONEncoder):
 def default(self, obj):
     if isinstance(obj.__class__, DeclarativeMeta):
     # an SQLAlchemy class
        fields = {}
        for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
            data = obj.__getattribute__(field)
            try:
                json.dumps(data) # this will fail on non-encodable values, like other classes
                fields[field] = data
            except TypeError:
                fields[field] = None
       # a json-encodable dict
        return fields
     return json.JSONEncoder.default(self, obj)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://chiefai:123456@localhost:5433/chiefai2'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
engine = create_engine("postgresql://chiefai:123456@localhost:5433/chiefai2")
Session = sessionmaker(bind=engine)
session=Session()
db = SQLAlchemy(app)
app.json_encoder = DecimalEncoder
############################################################

############################################################
class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

class Bloodoxygen(db.Model, Serializer):
    bloodoxygen_id = db.Column(db.Integer, primary_key=True)
    bloodoxygen_percentage = db.Column(db.Integer)
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))

    def __init__(self, bloodoxygen_id, bloodoxygen_percentage, date, time):
        self.bloodoxygen_id = bloodoxygen_id
        self.bloodoxygen_percentage = bloodoxygen_percentage
        self.date = date
        self.time = time

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class Bloodpressure(db.Model, Serializer):
    bloodoxygen_id = db.Column(db.Integer, primary_key=True)
    systolic_value = db.Column(db.Integer)
    diastolic_value = db.Column(db.Integer)
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))

    def __init__(self, bloodpressure_id, systolic_value, diastolic_value, date, time):
        self.bloodoxygen_id = bloodpressure_id
        self.systolic_value = systolic_value
        self.diastolic_value = diastolic_value
        self.date = date
        self.time = time

    def serialize(self):
        d = Serializer.serialize(self)
        return d

class Heartrate(db.Model, Serializer):
    heartrate_id = db.Column(db.Integer, primary_key=True)
    heartrate_value = db.Column(db.Integer)
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))

    def __init__(self, heartrate_id, heartrate_value, date, time):
        self.heartrate_id = heartrate_id
        self.heartrate_value = heartrate_value
        self.date = date
        self.time = time

    def serialize(self):
        d = Serializer.serialize(self)
        return d

class Users(db.Model, Serializer):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    age = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    height = db.Column(db.String(50))
    weight = db.Column(db.String(50))

    def __init__(self, user_id, username, age, gender, height, weight):
        self.user_id = user_id
        self.username = username
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight

    def serialize(self):
        d = Serializer.serialize(self)
        return d


###########################################################################################################################################################
###########################################################################################################################################################

################## Using Stream() Function - Blood Oxygen ###################
@app.route('/firebasetestBloodOxygenStreamMethod', methods=['GET', 'POST'])
def firebasetestBloodOxygenStreamMethod():
 if request.method == 'GET':
    users_ref1 = db.collection(u'BloodOxygen/Values/1njOjma35hhGUlQ5JAYT1gufiwE3') #### This line of code is working! ####
    docs = users_ref1.stream()
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
    return jsonify(f'{doc.id} => {doc.to_dict()}')
#############################################################################

#################### Using Get() Function - Blood Oxygen ####################
@app.route('/firebasetestBloodOxygenGetMethod', methods=['GET', 'POST'])
def firebasetestBloodOxygenGetMethod():
 if request.method == 'GET':
    doc_ref1 = db.collection(u'BloodOxygen').document(u'Values/0kYnCgZV8MQnaxqzNnveBjbQO6u1/gSeUWcG57xjDRBKTx824') #### This line of code is working! ####
    #doc_ref1 = db.collection(u'BloodOxygen').document(u'Values').collection(u'0kYnCgZV8MQnaxqzNnveBjbQO6u1').document(u'gSeUWcG57xjDRBKTx824')
    doc = doc_ref1.get()
    if doc.exists:
        print(f'Document data for Blood Oxygen: {doc.to_dict()}')
    else:
        print(u'No such document!')
    return jsonify(f'Document data for Blood Oxygen: {doc.to_dict()}')

#############################################################################


################## Using Stream() Function - Blood Pressure ###################
@app.route('/firebasetestBloodPressureStreamMethod', methods=['GET', 'POST'])
def firebasetestBloodPressureStreamMethod():
 if request.method == 'GET':
    users_ref2 = db.collection(u'BloodPressure/Values/1njOjma35hhGUlQ5JAYT1gufiwE3') #### This line of code is working! ####
    docs = users_ref2.stream()
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
    return jsonify(f'{doc.id} => {doc.to_dict()}')
#############################################################################

#################### Using Get() Function - Blood Pressure ####################
@app.route('/firebasetestBloodPressureGetMethod', methods=['GET', 'POST'])
def firebasetestBloodPressureGetMethod():
 if request.method == 'GET':
    doc_ref2 = db.collection(u'BloodPressure').document(u'Values/1njOjma35hhGUlQ5JAYT1gufiwE3/0kCq6XdO6JTTs7ZjQbdZ') #### This line of code is working! ####
    doc = doc_ref2.get()
    if doc.exists:
        print(f'Document data for Blood Pressure: {doc.to_dict()}')
    else:
        print(u'No such document!')
    return jsonify(f'Document data for Blood Pressure: {doc.to_dict()}')

#############################################################################


################## Using Stream() Function - Heart Rate ###################
@app.route('/firebasetestHeartRateStreamMethod', methods=['GET', 'POST'])
def firebasetestHeartRateStreamMethod():
 if request.method == 'GET':
    users_ref3 = db.collection(u'HeartRate/Values/1njOjma35hhGUlQ5JAYT1gufiwE3') #### This line of code is working! ####
    docs = users_ref3.stream()
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
    return jsonify(f'{doc.id} => {doc.to_dict()}')
#############################################################################

#################### Using Get() Function - Heart Rate ####################
@app.route('/firebasetestHeartRateGetMethod', methods=['GET', 'POST'])
def firebasetestHeartRateGetMethod():
 if request.method == 'GET':
    doc_ref3 = db.collection(u'HeartRate').document(u'Values/1njOjma35hhGUlQ5JAYT1gufiwE3/5o2NtKcoJY70xC8uVlKD') #### This line of code is working! ####
    doc = doc_ref3.get()
    if doc.exists:
        print(f'Document data for Heart Rate: {doc.to_dict()}')
    else:
        print(u'No such document!')
    return jsonify(f'Document data for Heart Rate: {doc.to_dict()}')

############################################################################


################## Using Stream() Function - User ###################
@app.route('/firebasetestUserStreamMethod', methods=['GET', 'POST'])
def firebasetestUserStreamMethod():
 if request.method == 'GET':
    users_ref4 = db.collection(u'User/Values/YW2JNYalaJhBelWpvUQayjRDJHy2') #### This line of code is working! ####
    docs = users_ref4.stream()
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
    return jsonify(f'{doc.id} => {doc.to_dict()}')
#############################################################################

#################### Using Get() Function - User ####################
@app.route('/firebasetestUserGetMethod', methods=['GET', 'POST'])
def firebasetestUserGetMethod():
 if request.method == 'GET':
    doc_ref4 = db.collection(u'User').document(u'Values/IwELeKkVaZYlF7BuytQQPq6jx503/ca9BBv55SHX0Qp7eOkab') #### This line of code is working! ####
    doc = doc_ref4.get()
    if doc.exists:
        print(f'Document data for User: {doc.to_dict()}')
    else:
        print(u'No such document!')
    return jsonify(f'Document data for User: {doc.to_dict()}')

############################################################################

###################################################################################################################################################

#################### Using Get() Function - Blood Oxygen ####################
@app.route('/firebasetestBlodOxygenQuery', methods=['GET', 'POST'])
def firebasetestBlodOxygenQuery():
 if request.method == 'POST':
    #doc_ref1 = dbfirestore.collection(u'BloodOxygen').document(u'Values/0kYnCgZV8MQnaxqzNnveBjbQO6u1/gSeUWcG57xjDRBKTx824') #### This line of code is working! ####
    doc_ref1 = dbfirestore.collection(u'BloodOxygen').document(u'Values').collection(u'0kYnCgZV8MQnaxqzNnveBjbQO6u1').document(u'gSeUWcG57xjDRBKTx824')
    #query_ref = dbfirestore.collection(u'BloodOxygen').where(u'BloodOxygen', u'==', u'Values')
    doc = doc_ref1.get()
    #doc = query_ref.get()
    #bloodoxygenid = Bloodoxygen.query.order_by(Bloodoxygen.bloodoxygen_id.desc()).first().bloodoxygen_id + 1
    #bloodoxygenid = Bloodoxygen.query.order_by(Bloodoxygen.bloodoxygen_id.desc()).first().bloodoxygen_id + 1
    bloodoxygenid = dbfirestore.collection_group(u'User').where(u'name', u'==', u'Zyra').get()
    id = (bloodoxygenid)
    date = doc.to_dict()['date']
    time = doc.to_dict()['time']
    bloodoxygenpercentage = doc.to_dict()['value']
    #result = Bloodoxygen(bloodoxygenid, bloodoxygenpercentage, date, time)
    #db.session.add(result)
    #db.session.commit()
    #print ("Record ADDED Successfully!")
    #BloodOxygen = Bloodoxygen.query.all()
    #return jsonify(BloodOxygen = Bloodoxygen.serialize_list(BloodOxygen))
    #return jsonify(f'Document data for Blood Oxygen: {doc.to_dict()}')
    return jsonify(id, bloodoxygenpercentage, date, time)
    #print (bloodoxygenid, bloodoxygenpercentage, date, time)
    #return jsonify(result)
#############################################################################
'''
##### WRITE DATA for Covid Risk #####
@app.route('/firebaseWriteDataCovidRisk', methods=['GET', 'POST'])
def firebaseWriteDataCovidRisk():
 if request.method == 'POST':
    data = {u'name': u'Covid Risk', u'value': u'70'}
    ####  Add a new doc in collection #####
    dbfirestore.collection(u'Covid Risk').document(u'Records').set(data)
    return 'Record ADDED Successfully!'
############################################################################

##### WRITE DATA for Immunity Index #####
@app.route('/firebaseWriteDataImmunityIndex', methods=['GET', 'POST'])
def firebaseWriteDataImmunityIndex():
 if request.method == 'POST':
    data = {u'name': u'Immunity Index', u'value': u'20'}
    ####  Add a new doc in collection #####
    dbfirestore.collection(u'Immunity Index').document(u'Records').set(data)
    return 'Record ADDED Successfully!'
############################################################################

##### WRITE DATA for Inflammation Index #####
@app.route('/firebaseWriteDataInflammationIndex', methods=['GET', 'POST'])
def firebaseWriteDataInflammationIndex():
 if request.method == 'POST':
    data = {u'name': u'Inflammation Index', u'value': u'50'}
    ####  Add a new doc in collection #####
    dbfirestore.collection(u'Inflammation Index').document(u'Records').set(data)
    return 'Record ADDED Successfully!'
############################################################################
'''

print ('Got till here!')

############################################################################
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(host='0.0.0.0')

