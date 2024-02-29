from datetime import datetime
from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI
import json5 as json

sample_json = """
{
  "subject": subject of the email,
  "date": today's date,
  "email_content": [
    "introduction paragraph ",
    "main paragraph",
    "conclusion paragraph",
    ]
}
"""

sample_revise_json = """
{
  "subject": subject of the email,
  "email_content": [
    "introduction paragraph ",
    "main paragraph",
    "conclusion paragraph",
    ],
    "message": "message to the critique"
}
"""


class WriterAgent:
    def __init__(self):
        pass

    def writer(self, query: str, target: str, sources: list):

        prompt = [{
            "role": "system", # Should we leave as system or change?
            "content": "You are a marketing email writer. Your sole purpose is to write a well-written personalized "
                       "marketing email about a product using a list of articles.\n "
                        # should tavily results be called articles?
        }, {
            "role": "user",
            "content": f"Product Description: {query}"
                       f"Target Company: {target}"
                       f"{sources}\n"
                       f"Your task is to write a personalized and engaging marketing "
                       f"email for me based on the provided query, sources and product description"
                       f"based on the sources.\n "
                       f"Please return nothing but a JSON in the following format:\n"
                       f"{sample_json}\n "

        }]

        lc_messages = convert_openai_messages(prompt)
        optional_params = {
            "response_format": {"type": "json_object"}
        }

        response = ChatOpenAI(model='gpt-4-0125-preview', max_retries=1, model_kwargs=optional_params).invoke(lc_messages).content
        return json.loads(response)

    def revise(self, article: dict):
        prompt = [{
            "role": "system",
            "content": "You are editing a marketing email. Your sole purpose is to edit a personalized and "
                       "engaging email about a product topic based on given critique\n "
        }, {
            "role": "user",
            "content": f"{str(article)}\n"
                        f"Your task is to edit the email based on the critique given.\n "
                        f"Please return json format of the 'email_content' and a new 'message' field"
                        f"to the critique that explain your changes or why you didn't change anything.\n"
                        f"please return nothing but a JSON in the following format:\n"
                        f"{sample_revise_json}\n "

        }]

        lc_messages = convert_openai_messages(prompt)
        optional_params = {
            "response_format": {"type": "json_object"}
        }

        response = ChatOpenAI(model='gpt-4-0125-preview', max_retries=1, model_kwargs=optional_params).invoke(lc_messages).content
        response = json.loads(response)
        print(f"For article: {article['title']}")
        print(f"Writer Revision Message: {response['message']}\n")
        return response

    def run(self, article: dict):
        critique = article.get("critique")
        if critique is not None:
            article.update(self.revise(article))
        else:
            article.update(self.writer(article["query"], article["sources"]))
        return article