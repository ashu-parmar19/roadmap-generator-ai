from serpapi import GoogleSearch
import os

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', "358eb693155e6a3fb721e86f6e4947b48f5f679f572ab6bf5557134a436a834c")

def get_resource_links(skill, num_results=3):
    search = GoogleSearch({
        "q": f"free {skill} learning site:edu OR site :org OR site:com",
        "location": ["United States","india","United Kingdom","Canada","Australia"],
        "hl": "en",
        "gl": "in",
        "api_key": SERPAPI_API_KEY,
        "num": num_results, 
    })

    results = search.get_dict()
    links = []

    for res in results.get('organic_results', []):
        link = res.get('link')
        if link:
            links.append(link)

    return links or [f"https://www.google.com/search?q={skill.replace(' ', '+')}"]  # Return an empty list if no links found

