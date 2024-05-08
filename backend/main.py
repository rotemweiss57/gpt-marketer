import os
import time
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from langgraph.graph import Graph

# Import agent classes
from .agents import SearchAgent, WriterAgent, CritiqueAgent, DesignerAgent


class MasterAgent:
    def __init__(self):
        self.output_dir = f"frontend/static/outputs/run_{int(time.time())}"
        os.makedirs(self.output_dir, exist_ok=True)

    def run(self, data: dict):
        print(data)
        # Extract the queries from the input data
        target = data.get("leads")
        product_description = data.get("product_description")
        company_name = data.get("user_company")
        email_address = data.get("user_email")
        first_name = data.get("user_first_name")
        last_name = data.get("user_last_name")
        logo = data.get("logo", None)
        # print(logo)

        # Create a list dict for each target
        emails = []
        for id, lead in target.items():
            email = {

                # target data
                "name": lead.get("name"),
                "email": lead.get("email"),
                "title": lead.get("title"),
                "domain": lead.get("email").split("@")[1],
                "logo": logo,

                # user data
                "product_description": product_description,
                "user_company": company_name,
                "user_email": email_address,
                "user_first_name": first_name,
                "user_last_name": last_name
            }
            emails.append(email)

        # Initialize agents
        search_agent = SearchAgent()
        writer_agent = WriterAgent()
        critique_agent = CritiqueAgent()
        designer_agent = DesignerAgent(self.output_dir)

        # Define a Langchain graph
        workflow = Graph()

        # Add nodes for each agent
        workflow.add_node("search", search_agent.run)
        workflow.add_node("write", writer_agent.run)
        workflow.add_node("critique", critique_agent.run)
        workflow.add_node("design", designer_agent.run)

        # Set up edges
        workflow.add_edge('search', 'write')
        workflow.add_edge('write', 'critique')
        workflow.add_conditional_edges(start_key='critique',
                                       condition=lambda x: "accept" if x['critique'] is None else "revise",
                                       conditional_edge_mapping={"accept": "design", "revise": "write"})

        # set up start and end nodes
        workflow.set_entry_point("search")
        workflow.set_finish_point("design")

        # compile the graph
        chain = workflow.compile()

        # Execute the graph for each email using a thread pool
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda x: chain.invoke(x), emails))

        # turn results into a dictionary
        results = {i: results[i] for i in range(len(results))}

        file_name = "emails.csv"
        path = os.path.join(self.output_dir, file_name)

        # Convert results to a pandas DataFrame
        results_pd = pd.DataFrame(results).T

        # Save the DataFrame to CSV at the constructed path
        results_pd.to_csv(path)

        # Return the file path
        return path
