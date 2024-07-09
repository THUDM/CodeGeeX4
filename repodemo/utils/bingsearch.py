import requests
from bs4 import BeautifulSoup as BS4

BING_API_KEY = "<your_bing_api_key>"


def search_with_bing(query: str, search_timeout=30, top_k=6) -> list[dict]:
    """
    Search with bing and return the contexts.
    参考文档: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
    """
    response = requests.get(
        url="https://api.bing.microsoft.com/v7.0/search",
        headers={"Ocp-Apim-Subscription-Key": BING_API_KEY},
        params={
            "q": query,
            "responseFilter": ["webpages"],
            "freshness": "month",
            "mkt": "zh-CN",
        },
        timeout=search_timeout,
    )
    try:
        json_content = response.json()
        # print(json_content)
        contexts = json_content["webPages"]["value"][:top_k]
        # logger.info("Web搜索完成")
        return contexts
    except Exception as e:
        # logger.error(f"搜索失败，错误原因: {e}")
        print(f"搜索失败，错误原因: {e}")
        return []


def fetch_url(url):
    response = requests.get(url)
    # use beautifulsoup4 to parse html
    soup = BS4(response.text, "html.parser")
    plain_text = soup.get_text()
    return plain_text


def bing_search_prompt(input):
    contents = search_with_bing(input, search_timeout=5, top_k=6)
    citations = "\n\n".join(
        [
            f"[[citation:{i + 1}]]\n```markdown\n{item['snippet']}\n```"
            for i, item in enumerate(contents)
        ]
    )
    prompt = f"[引用]\n{citations}\n问：{input}\n"
    return prompt
