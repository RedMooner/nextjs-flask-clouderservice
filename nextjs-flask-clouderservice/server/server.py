from models.models import *  # import all models
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from native.fs_gpg import *
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from Config import Config
# app instance
app = Flask(__name__)  # create an instance of Flask

app.config.from_object(Config)

CORS(app)  # enable cross-origin resource sharing

engine = create_engine('sqlite:///database.db')  # database


session = scoped_session(sessionmaker(
    autoflush=False, autocommit=False, bind=engine))  # session

Base = declarative_base()  # create a base class
Base.query = session.query_property()  # add query methods to the base class


jwt = JWTManager(app)
# Base.metadata.drop_all(bind=engine) # create all tables
Base.metadata.create_all(bind=engine)  # create all tables


@jwt_required()
@app.route("/api/home", methods=['GET'])
def home():
    return jsonify(
        {
            'message': 'Hello World from pyt!'
        })


@app.route("/api/register", methods=['POST'])
def register():
    Name = request.json['Name']
    Surname = request.json['Surname']
    Email = request.json['Email']
    Password = request.json['Password']
    user = User(Name, Email, Password)
    session.add(user)
    session.commit()
    token = user.get_token()
    generate_key(Name, Surname, "clouder.com", Password)
    print("key generated")
    print(token)
    return jsonify(
        {
            'token': token
        })


@app.route("/api/logout", methods=['POST'])
def logout():
    pass


@app.route("/api/login", methods=['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
        user = User.authenticate(username, password)
        token = user.get_token()
        print(token)
        return jsonify(
            {
                'status': token
            })
    except:
        return jsonify(
            {
                'status': "Invalid Credentials"
            })

# cloude service endpoints


@app.route("/api/getfiles", methods=['GET'])
def getfiles():
    decrypt()
    return jsonify("getfiles")


@app.route("/api/uploadFile", methods=['GET'])
def uploadFile():
    encrypt()
    return jsonify("uploadFile")


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if (__name__ == '__main__'):
    app.run(debug=True, port=8080)  # run app in debug mode
