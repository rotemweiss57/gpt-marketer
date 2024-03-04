import asyncio

from flask import Flask, jsonify, request
from backend.main import MasterAgent
import pandas as pd

backend_app = Flask(__name__)


@backend_app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "Running"}), 200


@backend_app.route('/generate_emails', methods=['GET']) #tmp
async def generate_emails():
    # data = request.json

    path_to_excel = "/Users/rotemweiss/Desktop/gpt-marketer/backend/leads_list.xlsx"
    target = []
    df = pd.read_excel(path_to_excel)
    for idx, row in df.iterrows():
        target.append({'name': row['name'], 'email': row['email'], 'title': row['title']})

    data = {
        "target": target,
        "product_description": "HubSpot CRM for Marketing is a comprehensive, cloud-based platform designed to assist "
                               "businesses in managing their marketing efforts more efficiently. It enables "
                               "organizations to automate and streamline their marketing campaigns across multiple "
                               "channels, providing tools for email marketing, social media management, SEO, "
                               "content creation, and website analytics. With its user-friendly interface, "
                               "HubSpot CRM for Marketing allows marketers to create personalized customer "
                               "experiences, track the effectiveness of their marketing campaigns in real-time, "
                               "and generate detailed reports to measure ROI. Additionally, it offers features for "
                               "lead generation, nurturing, and scoring, helping businesses attract more prospects "
                               "and convert them into loyal customers. Integrated with HubSpot's sales, service, "
                               "and operations software, it ensures a cohesive and aligned approach across all "
                               "customer touchpoints, enhancing overall customer satisfaction and driving business "
                               "growth.",
        "user_company": "HubsSpot",
        "user_email": "rotem@hubspot.com",
        "user_first_name": "Rotem",
        "user_last_name": "Weiss"
    }

    master_agent = MasterAgent()
    await master_agent.run(data)
    return jsonify({"status": "Success"}), 200
