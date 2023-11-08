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
from flask import send_file,flash, request, redirect, url_for

from werkzeug.utils import secure_filename
# app instance
app = Flask(__name__)  # create an instance of Flask

app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = 'uploads'  # make it accessible
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
    # Get the data from the request
    Name = request.json['Name']
    Surname = request.json['Surname']
    Email = request.json['Email']
    Password = request.json['Password']
    # Create a new user
    user = User(Name, Email, Password)
    # Add the user to the session
    session.add(user)
    # Commit the changes to the session
    session.commit()
    # Generate a token for the user
    token = user.get_token()
    # Generate a key for the user
    generate_key(Name, Surname, "clouder.com", Password)
    print("key generated")
    print(token)
    # Return the token
    return jsonify(
        {
            'token': token
        })


@app.route("/api/logout", methods=['POST'])
def logout():
    # This route is used to logout the user
    pass


@app.route("/api/login", methods=['POST'])
def login():
    try:
        # Get the username and password from the request
        username = request.json['username']
        password = request.json['password']
        # Authenticate the user
        user = User.authenticate(username, password)
        # Generate a token for the user
        token = user.get_token()
        print(token)
        # Return the token
        return jsonify(
            {
                'status': token
            })
    # If the credentials are invalid
    except:
        # Return an error message
        return jsonify(
            {
                'status': "Invalid Credentials"
            })
# cloude service endpoints


@app.route('/api/download/<string:filename>', methods=['GET'])
# Decorator to check if a JWT token is provided
@jwt_required()
def downloadFile(filename):
    # Get the user ID from the JWT token
    user_id = get_jwt_identity()
    # Get the user object from the database
    user = User.query.filter(User.id == user_id).one()
    # Create the path to the file
    folder_path = os.path.join("uploads", "users", user.email, filename)
    # Print the path to the file
    print(folder_path)
    # Return the file as an attachment
    return send_file(folder_path, as_attachment=True)

@app.route("/api/getfiles/<string:path>", methods=['GET'])
@jwt_required()
def getfiles(path):
    '''
    GET: /api/getfiles/<path>

    Returns a list of files and folders in the given path.
    '''
    user_id = get_jwt_identity()
    user = User.query.filter(User.id == user_id).one()
    if (path == 'root'):
        return jsonify(get_files_and_folders('', mail=user.email))
    return jsonify(get_files_and_folders(path, mail=user.email))


@app.route("/api/upload", methods=['POST'])
@jwt_required()
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file:
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		resp = jsonify({'message' : 'File successfully uploaded'})
		resp.status_code = 201
		return resp


@app.route("/api/profile", methods=['GET'])
@jwt_required()
def profile():
    # Get the user id from the jwt token
    user_id = get_jwt_identity()
    # Query the user from the database
    user = User.query.filter(User.id == user_id).one()
    # Create a serialized user object
    serialized_user = [
        {
            'id': user.id,
            'email': user.email,
        }
    ]
    # Print the serialized user object
    print(str(serialized_user))
    # Return the serialized user object as a json
    return jsonify(serialized_user)


@app.teardown_appcontext
def shutdown_session(exception=None):
    # Remove the session when the app context is shutdown
    session.remove()


if (__name__ == '__main__'):
    app.run(debug=True, port=8080)  # run app in debug mode