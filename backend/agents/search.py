from tavily import TavilyClient
import os

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


class SearchAgent:
    def __init__(self):
        # Initialization can be expanded if needed
        pass

    def search_tavily(self, email: dict):
        search_query = f"latest news about {email['domain']}"
        image_query = f"{email['domain']} logo"
        # Perform a search with Tavily, specifying the topic and other parameters
        results = tavily_client.search(query=search_query, topic="news", max_results=5, include_images=False)
        sources = results.get("results", [])
        email['sources'] = sources

        # Attempt to retrieve the first image from the results, defaulting to a placeholder if none are found
        results = tavily_client.search(query=image_query, topic="news", max_results=5, include_images=True)
        # image = results.get("images", [
        #     "https://images.unsplash.com/photo-1542281286-9e0a16bb7366?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8bmV3c3BhcGVyJTIwbmV3c3BhcGVyJTIwYXJ0aWNsZXxlbnwwfHwwfHw%3D&ixlib=rb-1.2.1&w=1000&q=80"])[
        #     0]

        try:
            image = results["images"][0]
        except:
            image = None

        email['image'] = image

        return email

    def run(self, email: dict):
        # Perform the search
        email = self.search_tavily(email)
        return email
