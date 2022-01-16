from flask import Flask, jsonify, request


app = Flask(__name__)

@app.route('/')
@app.route('/index2', methods=['GET'])
def index2():
    return 'Disaster Alerting System Server is running'
