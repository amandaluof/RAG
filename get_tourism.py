import requests
from bs4 import BeautifulSoup
import os
import time

# 设置Wikipedia的基础URL
BASE_URL = "https://en.wikipedia.org"
START_URL = BASE_URL + "/wiki/Tourist_attractions_in_the_United_States"
HEADERS = {"User-Agent": "FengLuo(fl38@rice.edu)"}
# HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

# 存储数据的目录
OUTPUT_DIR = "data/wiki/tourist_attractions"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 爬取页面并解析HTML
def get_soup(url):
    time.sleep(1)  # 避免请求过快被封
    print(url)
    response = requests.get(url, headers=HEADERS)
    print(response)
    return BeautifulSoup(response.text, "html.parser")

# 解析页面，提取链接
def get_links(url, keyword_filter=None):
    soup = get_soup(url)
    links = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        title = link.get_text(strip=True)
        if href.startswith("/wiki/") and not ":" in href:  # 过滤掉非百科页面
            full_url = BASE_URL + href
            if keyword_filter is None or keyword_filter in href:
                links.append((title, full_url))
    return links

# 递归爬取所有景点
def scrape_tourist_attractions():
    # 1️⃣ 获取各州的旅游景点页面
    state_links = get_links(START_URL, "Tourist_attractions_in_")

    import pdb;pdb.set_trace()
    # 2️⃣ 逐个访问每个州的页面，提取具体景点
    for state_name, state_url in state_links:
        print(f"Scraping: {state_name} - {state_url}")

        # 获取该州的所有景点链接
        attraction_links = get_links(state_url)

        
        # 存储到文件
        file_path = os.path.join(OUTPUT_DIR, f"{state_name.replace(' ', '_')}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            for attraction_name, attraction_url in attraction_links:
                f.write(f"{attraction_name}\t{attraction_url}\n")
        
        print(f"Saved: {file_path}")

if __name__ == "__main__":
    scrape_tourist_attractions()
