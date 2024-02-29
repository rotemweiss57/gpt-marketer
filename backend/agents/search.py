from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI
import json5 as json


class SearchAgent:
    def __init__(self):
        pass

    def search_information(self, query: str):
        # Define the search query structure in a simple JSON format for demonstration
        search_query_template = f"""
        {{
            "query": "{query}",
            "date": "{datetime.now().strftime('%Y-%m-%d')}",
            "summary": "Summary of the search results for the given query."
        }}
        """
        return json.loads(search_query_template)

    def perform_search(self, query: str):
        # Simulate performing a search and structuring the results
        search_results = self.search_information(query)

        prompt = [{
            "role": "system",
            "content": "You are a research assistant. Your purpose is to gather and summarize information on"
                       " a specific topic."
        }, {
            "role": "user",
            "content": f"Search Query: {query}\n"
                       f"Your task is to summarize the key findings from the search results based"
                       f" on the following query:\n"
                       f"{json.dumps(search_results, indent=2)}\n"
        }]

        lc_messages = convert_openai_messages(prompt)
        optional_params = {"response_format": {"type": "json_object"}}

        response = ChatOpenAI(model='gpt-4-0125-preview', max_retries=1, model_kwargs=optional_params).invoke(
            lc_messages).content
        return json.loads(response)

    def refine_search(self, search_results: dict, feedback: str):
        # Simulate refining search results based on feedback
        refined_search_template = f"""
        {{
            "query": "{search_results['query']}",
            "date": "{datetime.now().strftime('%Y-%m-%d')}",
            "summary": "Refined summary of the search results based on feedback: {feedback}"
        }}
        """
        return json.loads(refined_search_template)

    def run(self, query: str, feedback: str = None):
        search_results = self.search_information(query)
        if feedback is not None:
            search_results.update(self.refine_search(search_results, feedback))
        else:
            search_results.update(self.perform_search(query))
        return search_results
