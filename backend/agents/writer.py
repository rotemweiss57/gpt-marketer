from datetime import datetime
from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI
import json5 as json

sample_json = """
{
    "subject": subject of the email,
    "email_content": "email content",
"""

sample_revise_json = """
{
    "subject": subject of the email,
    "email_content": "email content",
    "message": "message to the critique",
    "number_of_revisions": "number of revisions made to the email"
}
"""


class WriterAgent:
    def __init__(self):
        pass

    def writer(self, email: dict):

        prompt = [{
            "role": "system",
            "content": "You are a marketing email writer. Your sole purpose is to write a well-written personalized"
                       "marketing email about my product based on provided context and sources."
                       "Write less than 150 words, and add new line tagging so the text would be styled for HTML\n"
        }, {
            "role": "user",
            "content": f"{str(email)}\n"

                       f"Your task is to write a personalized and engaging email about a product topic based on the "
                       f"given context and news sources.\n"
                       f"This is the recipient: {email['name']}, the sender: {email['user_first_name']} {email['user_last_name']}"
                       f"please return nothing but a JSON in the following format without any images:\n"
                       f"{sample_json}\n"

        }]

        lc_messages = convert_openai_messages(prompt)
        optional_params = {
            "response_format": {"type": "json_object"}
        }

        response = ChatOpenAI(model='gpt-4-0125-preview', max_retries=1, model_kwargs=optional_params).invoke(
            lc_messages).content
        return json.loads(response)

    def revise(self, email: dict):
        prompt = [{
            "role": "system",
            "content": "You are editing a marketing email. Your sole purpose is to edit a personalized and "
                       "engaging email about a product topic based on given critique\n"
                       "Write less than 150 words, and add new line tagging so the text would be styled for HTML\n"
        }, {
            "role": "user",
            "content": f"subject: {email['subject']}\n"
                        f"email_content: {email['email_content']}\n"
                        f"message: {email.get('message')}\n"
                       f"number_of_revisions: {email.get('number_of_revisions', 0)}\n"
                       f"Your task is to edit the email based on the critique given and explain the changes made in "
                       f"the message field.\n"
                       f"if you cannot change the email based on the critique, please return the same email and "
                       f"explain why in the message field\n"
                       f"Also, please increment number_of_revisions by 1\n"
                       f"Please return nothing but a JSON in the following format:\n"
                       f"{sample_revise_json}\n "

        }]

        lc_messages = convert_openai_messages(prompt)
        optional_params = {
            "response_format": {"type": "json_object"}
        }

        response = ChatOpenAI(model='gpt-4-0125-preview', max_retries=1, model_kwargs=optional_params).invoke(
            lc_messages).content
        response = json.loads(response)
        print(f"For article: {email['title']}")
        print(f"Writer Revision Message: {response['message']}\n")
        return response

    def run(self, email: dict):
        critique = email.get("critique")
        if critique is not None:
            email.update(self.revise(email))
        else:
            email.update(self.writer(email))
            print(email)
        return email
