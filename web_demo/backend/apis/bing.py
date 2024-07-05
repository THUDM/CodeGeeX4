"""
Bing Search
"""
import os

import requests
from backend.apis.api import API

BING_API_KEY = os.getenv('BING_API_KEY')


class BingSearchAPI(API):
    def __init__(self):
        self.url = "https://api.bing.microsoft.com/v7.0/search"

    def search(self, query, freshness=None):
        """
        Search with bing

        References: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
        """
        response = requests.get(
            url=self.url,
            headers={"Ocp-Apim-Subscription-Key": BING_API_KEY},
            params={
                "q": query,
                "mkt": 'zh-CN',
                "freshness": freshness,
            },
            timeout=10,
        )
        try:
            json_content = response.json()
            contexts = json_content['webPages']['value'][:4]
            search_res = [{
                "url": item['url'],
                "title": item['name'],
                "snippet": item['snippet']
            } for item in contexts]
            return search_res
        except Exception as e:
            print(f"Searching failed, caused by {e}")
            return []
