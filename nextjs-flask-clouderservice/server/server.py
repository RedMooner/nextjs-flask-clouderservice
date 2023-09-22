from flask import Flask, jsonify
from flask_cors import CORS

# app instance
app = Flask(__name__)
CORS(app)

@app.route("/api/home", methods=['GET'])
def home():
    return jsonify(
        {
            'message': 'Hello World from py!'
        })


if (__name__ == '__main__'):
    app.run(debug=True,port=8080)  # run app in debug mode
