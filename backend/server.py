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
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    company_name = request.form.get('company_name')
    email_address = request.form.get('email_address')
    product_description = request.form.get('product_description')

    # Handling the file part
    file = request.files.get('leads_file')

    if file and allowed_file(file.filename):
        # Here you can process the Excel file
        # For example, loading the file using pandas
        df = pd.read_excel(file)
        leads_dict = {
            i + 1: {
                "name": row["name"],
                "title": row["title"],
                "email": row["email"]
            } for i, row in df.iterrows()
        }


        # Assuming processing and passing data to MasterAgent as needed
        master_agent = MasterAgent()
        data = {
            "leads": leads_dict,
            "product_description": product_description,
            "company_name": company_name,
            "email_address": email_address,
            "first_name": first_name,
            "last_name": last_name,
        }
        master_agent.run(data)

        return jsonify({"status": "Success"}), 200
    elif not file:
        return Response("No file uploaded", status=400)
    else:
        return Response("Unsupported file type or other error", status=400)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'xlsx', 'xls'}


if __name__ == "__main__":
    backend_app.run(debug=True)
