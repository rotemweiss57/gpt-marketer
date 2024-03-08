from multiprocessing import Process

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import threading
import pandas as pd

from backend.server import backend_app

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.secret_key = 'your_secret_key'

email_list = {'1': {'lead_name': "Mark Morrison",
                    'lead_email': "mark.morrison@nvidia.com",
                    'lead_subject': "Elevate Nvidia's Marketing Strategy with HubSpot CRM",
                    'lead_body': "Dear Mark Morrison, As the Marketing Coordinator at Nvidia, "
                                 "you're at the forefront of the fast-evolving tech industry, "
                                 "where staying updated with the latest marketing innovations is crucial. "
                                 "HubSpot CRM for Marketing is designed to propel your marketing efforts forward, "
                                 "aligning perfectly with Nvidia's dynamic environment.We've been following Nvidia's "
                                 "leadership in AI and your outstanding contributions to the field. It's clear that "
                                 "your commitment to innovation is what sets Nvidia apart. HubSpot CRM for Marketing "
                                 "is built to enhance your pioneering work, facilitating seamless marketing campaigns "
                                 "across multiple channels. Our platform offers powerful tools for email marketing, social media,"
                                 " SEO, content creation, and website analytics, empowering you to create personalized customer journeys."
                                 " With features focused on lead generation, nurturing, and scoring, our aim is to help you attract "
                                 "and convert prospects into dedicated customers, supporting Nvidia's growth goals. Integrating "
                                 "with HubSpot's comprehensive suite offers a unified approach to all customer interactions, "
                                 "enhancing satisfaction and fostering growth. In light of Nvidia's recent advancements and the "
                                 "competitive landscape, leveraging our state-of-the-art solution could be a strategic move. "
                                 "I would love the opportunity to discuss how HubSpot CRM for Marketing can elevate Nvidia's "
                                 "marketing efforts and support your continued market leadership. Please contact me at "
                                 "rotem@hubspot.com to schedule a conversation. Looking forward to potentially collaborating "
                                 "and driving Nvidia's marketing to new heights. Best regards, Rotem Weiss HubSpot"},
              '2': {'lead_name': "Mark Morrison",
                    'lead_email': "mark.morrison@nvidia.com",
                    'lead_subject': "Elevate Nvidia's Marketing Strategy with HubSpot CRM",
                    'lead_body': "Dear Mark Morrison, As the Marketing Coordinator at Nvidia, "
                                 "you're at the forefront of the fast-evolving tech industry, "
                                 "where staying updated with the latest marketing innovations is crucial. "
                                 "HubSpot CRM for Marketing is designed to propel your marketing efforts forward, "
                                 "aligning perfectly with Nvidia's dynamic environment.We've been following Nvidia's "
                                 "leadership in AI and your outstanding contributions to the field. It's clear that "
                                 "your commitment to innovation is what sets Nvidia apart. HubSpot CRM for Marketing "
                                 "is built to enhance your pioneering work, facilitating seamless marketing campaigns "
                                 "across multiple channels. Our platform offers powerful tools for email marketing, social media,"
                                 " SEO, content creation, and website analytics, empowering you to create personalized customer journeys."
                                 " With features focused on lead generation, nurturing, and scoring, our aim is to help you attract "
                                 "and convert prospects into dedicated customers, supporting Nvidia's growth goals. Integrating "
                                 "with HubSpot's comprehensive suite offers a unified approach to all customer interactions, "
                                 "enhancing satisfaction and fostering growth. In light of Nvidia's recent advancements and the "
                                 "competitive landscape, leveraging our state-of-the-art solution could be a strategic move. "
                                 "I would love the opportunity to discuss how HubSpot CRM for Marketing can elevate Nvidia's "
                                 "marketing efforts and support your continued market leadership. Please contact me at "
                                 "rotem@hubspot.com to schedule a conversation. Looking forward to potentially collaborating "
                                 "and driving Nvidia's marketing to new heights. Best regards, Rotem Weiss HubSpot"},
              '3': {'lead_name': "Mark Morrison",
                    'lead_email': "mark.morrison@nvidia.com",
                    'lead_subject': "Elevate Nvidia's Marketing Strategy with HubSpot CRM",
                    'lead_body': "Dear Mark Morrison, As the Marketing Coordinator at Nvidia, "
                                 "you're at the forefront of the fast-evolving tech industry, "
                                 "where staying updated with the latest marketing innovations is crucial. "
                                 "HubSpot CRM for Marketing is designed to propel your marketing efforts forward, "
                                 "aligning perfectly with Nvidia's dynamic environment.We've been following Nvidia's "
                                 "leadership in AI and your outstanding contributions to the field. It's clear that "
                                 "your commitment to innovation is what sets Nvidia apart. HubSpot CRM for Marketing "
                                 "is built to enhance your pioneering work, facilitating seamless marketing campaigns "
                                 "across multiple channels. Our platform offers powerful tools for email marketing, social media,"
                                 " SEO, content creation, and website analytics, empowering you to create personalized customer journeys."
                                 " With features focused on lead generation, nurturing, and scoring, our aim is to help you attract "
                                 "and convert prospects into dedicated customers, supporting Nvidia's growth goals. Integrating "
                                 "with HubSpot's comprehensive suite offers a unified approach to all customer interactions, "
                                 "enhancing satisfaction and fostering growth. In light of Nvidia's recent advancements and the "
                                 "competitive landscape, leveraging our state-of-the-art solution could be a strategic move. "
                                 "I would love the opportunity to discuss how HubSpot CRM for Marketing can elevate Nvidia's "
                                 "marketing efforts and support your continued market leadership. Please contact me at "
                                 "rotem@hubspot.com to schedule a conversation. Looking forward to potentially collaborating "
                                 "and driving Nvidia's marketing to new heights. Best regards, Rotem Weiss HubSpot"},
              '4': {'lead_name': "Mark Morrison",
                    'lead_email': "mark.morrison@nvidia.com",
                    'lead_subject': "Elevate Nvidia's Marketing Strategy with HubSpot CRM",
                    'lead_body': "Dear Mark Morrison, As the Marketing Coordinator at Nvidia, "
                                 "you're at the forefront of the fast-evolving tech industry, "
                                 "where staying updated with the latest marketing innovations is crucial. "
                                 "HubSpot CRM for Marketing is designed to propel your marketing efforts forward, "
                                 "aligning perfectly with Nvidia's dynamic environment.We've been following Nvidia's "
                                 "leadership in AI and your outstanding contributions to the field. It's clear that "
                                 "your commitment to innovation is what sets Nvidia apart. HubSpot CRM for Marketing "
                                 "is built to enhance your pioneering work, facilitating seamless marketing campaigns "
                                 "across multiple channels. Our platform offers powerful tools for email marketing, social media,"
                                 " SEO, content creation, and website analytics, empowering you to create personalized customer journeys."
                                 " With features focused on lead generation, nurturing, and scoring, our aim is to help you attract "
                                 "and convert prospects into dedicated customers, supporting Nvidia's growth goals. Integrating "
                                 "with HubSpot's comprehensive suite offers a unified approach to all customer interactions, "
                                 "enhancing satisfaction and fostering growth. In light of Nvidia's recent advancements and the "
                                 "competitive landscape, leveraging our state-of-the-art solution could be a strategic move. "
                                 "I would love the opportunity to discuss how HubSpot CRM for Marketing can elevate Nvidia's "
                                 "marketing efforts and support your continued market leadership. Please contact me at "
                                 "rotem@hubspot.com to schedule a conversation. Looking forward to potentially collaborating "
                                 "and driving Nvidia's marketing to new heights. Best regards, Rotem Weiss HubSpot"},
              }

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

        # Converting to the desired dictionary format:
        # format is  {'product_description': '0', 'user_company': '0', 'user_email': 'omer.n99@gmail.com',
        # 'user_first_name': '0', 'user_last_name': '0', 'leads': {1: {'name': 'Mark Morrison', 'email':
        # 'mark.morrison@deltacorp.com', 'title': 'Marketing Coordinator'}, 2:.....
        data_dict = {}
        main_dict = {}
        main_dict['product_description'] = product_description
        main_dict['user_company'] = company_name
        main_dict['user_email'] = email_address
        main_dict['user_first_name'] = first_name
        main_dict['user_last_name'] = last_name
        main_dict['leads'] = data_dict

        for idx, row in df.iterrows():
            data_dict[idx + 1] = {'name': row['name'], 'email': row['email'], 'title': row['title']}

        # Do something with data_dict
        print("dictionary of leads:", main_dict)

        ### 2. Data to be displayed in success.html

        # Convert DataFrame to a list of dictionaries
        leads_list = df.to_dict('records')

        session['leads_data'] = leads_list

        # Clean up the temporary file
        os.remove(filepath)
    else:
        leads_list = []
    # Redirect to the success page with the email address to display
    return redirect(url_for('success', index=False, leads_list=leads_list))


@app.route('/success')
def success():
    leads_data = session.get('leads_data', [])
    email = request.args.get('email')
    return render_template('success.html', email=email, index=False, leads_list=leads_data)

@app.route('/email_confirmation')
def email_confirmation():
    return render_template('email_confirmation.html', emails=email_list)


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