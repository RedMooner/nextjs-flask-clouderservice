from flask import Flask, jsonify
from flask_cors import CORS
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from native.fs_gpg import *
# app instance
app = Flask(__name__)  # create an instance of Flask
CORS(app)  # enable cross-origin resource sharing

engine = create_engine('sqlite:///database.db')  # database


session = scoped_session(sessionmaker(
    autoflush=False, autocommit=False, bind=engine))  # session

Base = declarative_base()  # create a base class
Base.query = session.query_property()  # add query methods to the base class


from models.models import *  # import all models

Base.metadata.create_all(bind=engine)  # create all tables

@app.route("/api/home", methods=['GET'])
def home():
    return jsonify(
        {
            'message': 'Hello World from pyt!'
        })

@app.route("/api/register", methods=['GET'])
def register():
    generate_key("test","test","mail.ru","123")
    return jsonify(
        {
            'message': 'you are succesfully registered !'
        })
@app.route("/api/logout", methods=['POST'])
def logout():
    pass
@app.route("/api/login", methods=['POST'])
def login():
    pass


#cloude service endpoints

@app.route("/api/getfiles", methods=['GET'])
def getfiles():
    decrypt()
    return jsonify("getfiles");

@app.route("/api/uploadFile", methods=['GET'])
def uploadFile():
    encrypt()
    return  jsonify("uploadFile");

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()

if (__name__ == '__main__'):
    app.run(debug=True, port=8080)  # run app in debug mode
