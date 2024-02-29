from tavily import TavilyClient
import os

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


class SearchAgent:
    def __init__(self):
        # Initialization can be expanded if needed
        pass

    def search_tavily(self, query: str, topic: str = "marketing"):
        """
        Search for marketing-related content using Tavily based on the query.

        Args:
            query (str): The search query, potentially related to the product or target market.
            topic (str): The topic to search for, defaulting to "marketing" to align with the agent's use case.

        Returns:
            tuple: A tuple containing a list of sources and an image URL.
        """
        # Perform a search with Tavily, specifying the topic and other parameters
        results = tavily_client.search(query=query, topic=topic, max_results=10, include_images=True)
        sources = results.get("results", [])

        # Attempt to retrieve the first image from the results, defaulting to a placeholder if none are found
        image = results.get("images", [
            "https://images.unsplash.com/photo-1542281286-9e0a16bb7366?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8bmV3c3BhcGVyJTIwbmV3c3BhcGVyJTIwYXJ0aWNsZXxlbnwwfHwwfHw%3D&ixlib=rb-1.2.1&w=1000&q=80"])[
            0]

        return sources, image

    def run(self, query_info: dict):
        """
        Executes the search process based on a query and updates the provided dict with results.

        Args:
            query_info (dict): A dictionary containing the query and possibly other information.

        Returns:
            dict: The updated dictionary including search results and an image.
        """
        # Extract query and potentially other relevant info (like topic) from the input dict
        query = query_info.get("query")
        topic = query_info.get("topic", "marketing")  # Default to "marketing" if no topic is specified

        # Perform the search
        sources, image = self.search_tavily(query=query, topic=topic)

        # Update the input dict with search results and the selected image
        query_info.update({
            "sources": sources,
            "image": image
        })

        return query_info
