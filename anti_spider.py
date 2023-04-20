from fake_useragent import UserAgent
import requests
"""
反爬虫
"""
def run(url):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    print("伪装headers:", headers)
    response = requests.get(url, headers=headers)
    return response