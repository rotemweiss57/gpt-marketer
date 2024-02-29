from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import pandas as pd

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html', index=True)

@app.route('/product')
def product():
    return render_template('product.html', index=False)


@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    company_name = request.form['company_name']
    email_address = request.form['email_address']
    product_description = request.form['product_description']
    leads_file = request.files['leads_file']

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

        ### 1. Data ready to be sent to the backend

        # Converting to the desired dictionary format
        data_dict = {}
        for idx, row in df.iterrows():
            data_dict[idx + 1] = {'name': row['name'], 'email': row['email'], 'title': row['title']}

        # Do something with data_dict
        print("dictionary of leads:", data_dict)

        ### 2. Data to be displayed in success.html

        # Convert DataFrame to a list of dictionaries
        leads_list = df.to_dict('records')

        session['leads_data'] = leads_list

        # Clean up the temporary file
        os.remove(filepath)
    else:
        leads_list = []
    print(leads_list)
    # Redirect to the success page with the email address to display
    return redirect(url_for('success', index=False, leads_list=leads_list))

@app.route('/success')
def success():
    leads_data = session.get('leads_data', [])
    email = request.args.get('email')
    return render_template('success.html', email=email, index=False, leads_list=leads_data)

if __name__ == '__main__':
    app.run(debug=True)
