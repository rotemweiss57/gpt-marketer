from multiprocessing import Process
import requests
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import threading
import pandas as pd

from backend.server import backend_app

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.secret_key = 'your_secret_key'


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/product')
def product():
    return render_template('product.html')


@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    company_name = request.form['company_name']
    email_address = request.form['email_address']
    product_description = request.form['product_description']
    leads_file = request.files['leads_file']
    logo = request.form['logo']

    if leads_file:
        # Define the directory path
        temp_dir = 'temp'
        # Check if the directory exists, if not, create it
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Define the full path to save the file
        filepath = os.path.join(temp_dir, leads_file.filename)
        # Save the file
        leads_file.save(filepath)

        # Reading the Excel file
        df = pd.read_excel(filepath, engine='openpyxl')

        # Converting to the desired dictionary format:
        # format is  {'product_description': '0', 'user_company': '0', 'user_email': 'omer.n99@gmail.com',
        # 'user_first_name': '0', 'user_last_name': '0', 'leads': {1: {'name': 'Mark Morrison', 'email':
        # 'mark.morrison@deltacorp.com', 'title': 'Marketing Coordinator'}, 2:.....

        data = {}
        data['product_description'] = product_description
        data['user_company'] = company_name
        data['user_email'] = email_address
        data['user_first_name'] = first_name
        data['user_last_name'] = last_name
        data['logo'] = logo


        # Convert DataFrame to a list of dictionaries
        leads_list = df.to_dict('records')
        session['leads_data'] = leads_list

        # Move data to submit table data route
        user_info = data
        session['user_info'] = user_info

        # Clean up the temporary file
        os.remove(filepath)
    else:
        leads_list = []

    # Redirect to the success page with the email address to display
    return redirect(url_for('preview_leads', leads_list=leads_list))


@app.route('/submit-table-data', methods=['POST'])
def submit_table_data():
    data = request.json  # This is the data sent from the client
    user_info = session.get('user_info')

    data_dict = {}
    data_dict['product_description'] = user_info['product_description']
    data_dict['user_company'] = user_info['user_company']
    data_dict['user_email'] = user_info['user_email']
    data_dict['user_first_name'] = user_info['user_first_name']
    data_dict['user_last_name'] = user_info['user_last_name']
    data_dict['logo'] = user_info['logo']

    leads = {'leads': {i + 1: lead for i, lead in enumerate(data['leads'])}}

    data_dict['leads'] = leads['leads']

    # Send the data_dict to the backend server
    backend_url = 'http://localhost:8000/generate_emails'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(backend_url, json=data_dict, headers=headers)

    if response.status_code == 200:
        results = response.json()
        path = results["path"]
        # Store results in session or pass only necessary data for redirection
        session['path'] = path  # Example, consider security implications
        return render_template('email_confirmation.html')
    else:
        return jsonify({'success': False, 'error': 'Error processing your request'}), 500




@app.route('/preview_leads')
def preview_leads():
    leads_data = session.get('leads_data', [])
    email = request.args.get('email')

    return render_template('preview_leads.html', email=email, leads_list=leads_data)


@app.route('/email_confirmation')
def email_confirmation():
    path = session.get('path')  # Ensure 'path' is correctly set in the session

    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(path)

    # Convert the DataFrame to a list of dictionaries for easier handling in the template
    data = df.to_dict(orient='records')

    # Pass the 'data' list to your template
    return render_template('email_confirmation.html', data=data)


# Define a function to run the frontend app
def run_frontend():
    app.run(debug=True, port=5000, use_reloader=False)


# Define a function to run the backend app
def run_backend():
    backend_app.run(debug=True, port=8000, use_reloader=False)


if __name__ == '__main__':
    # Start the backend server
    backend_process = Process(target=run_backend)
    backend_process.start()

    # Start the frontend server
    frontend_process = Process(target=run_frontend)
    frontend_process.start()

    # Join the processes so that the main process waits for them to complete
    backend_process.join()
    frontend_process.join()
