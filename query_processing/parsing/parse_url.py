import httpx
import json
import re




def find_id(url):
    match = re.search(r"/questions/(\d+)", url)
    id = match.group(1) if match else None
    return id


def get_answer_id(q_id):
    api_url = f"https://api.stackexchange.com/2.3/questions/{q_id}"
    params = {
    "site": "stackoverflow",
    
}
    response = httpx.get(url=api_url, params=params).json()
    answer_id = response["items"][0].get("accepted_answer_id")
    return answer_id


def get_answer(a_id):
    api_url = f"https://api.stackexchange.com/2.3/answers/{a_id}"
    params = {
    "site": "stackoverflow",
    "filter": "withbody"
}
    response = httpx.get(api_url, params=params).json()
    return response['items'][0]['body']