import os
import time
from concurrent.futures import ThreadPoolExecutor
import asyncio

import pandas as pd
from langgraph.graph import Graph

# Import agent classes
from .agents import SearchAgent, WriterAgent, CritiqueAgent, DesignerAgent


class MasterAgent:
    def __init__(self):
        self.output_dir = f"outputs/run_{int(time.time())}"
        os.makedirs(self.output_dir, exist_ok=True)

    async def run(self, data: dict):

        # Extract the queries from the input data
        target = data.get("target")
        product_description = data.get("product_description")
        company_name = data.get("user_company")
        email_address = data.get("user_email")
        first_name = data.get("user_first_name")
        last_name = data.get("user_last_name")

        # Create a list dict for each target
        emails = []
        for lead in target:
            email = {

                # target data
                "name": lead.get("name"),
                "email": lead.get("email"),
                "title": lead.get("title"),
                "domain": lead.get("email").split("@")[1],

                # user data
                "product_description": product_description,
                "user_company": company_name,
                "user_email": email_address,
                "user_first_name": first_name,
                "user_last_name": last_name
            }
            print(email)
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

        # Execute the graph for each email
        results = await asyncio.gather(*(chain.invoke(email) for email in emails))

        # turn results into a dictionary
        results = {i: results[i] for i in range(len(results))}

        # save the results to a csv file
        results_pd = pd.DataFrame(results)
        results_pd.to_csv(f"{self.output_dir}/emails.csv")