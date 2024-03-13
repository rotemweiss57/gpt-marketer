import asyncio
import os

from flask import Flask, jsonify, request, Response
from backend.main import MasterAgent
from flask_cors import CORS
import pandas as pd

backend_app = Flask(__name__)

CORS(backend_app)



@backend_app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "Running"}), 200


@backend_app.route('/generate_emails', methods=['POST'])
def generate_emails():
    data = request.json
    master_agent = MasterAgent()
    path = master_agent.run(data)

    return jsonify({"path": path}), 200


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'xlsx', 'xls'}


if __name__ == "__main__":
    backend_app.run(debug=True)
