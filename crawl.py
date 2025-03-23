import wikipedia
import wikipediaapi
import os
import time
import random
from tqdm import tqdm

# 初始化 Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent='FengLuo(fl38@rice.edu)')

def clean_keyword(keyword):
    """
    清理关键词，移除无关的后缀，并转换成更适合 Wikipedia 的格式。
    """
    words = keyword.split()
    # 移除常见的城市类型后缀
    remove_suffixes = {"CDP", "city", "town", "village", "municipality", "borough"}
    cleaned_words = [word for word in words if word not in remove_suffixes]
    cleaned_keyword = " ".join(cleaned_words)
    return f"{cleaned_keyword}, {words[-1]}"  # 确保格式为 "City, State"

def fetch_wikipedia_data(keyword, output_dir, log_file):
    """
    爬取 Wikipedia 页面，使用模糊搜索处理找不到的页面情况。
    """
    time.sleep(random.uniform(1, 3))  # 随机延迟，防止 API 过载

    # 清理关键词，确保格式正确
    cleaned_keyword = clean_keyword(keyword)

    # 先尝试精确查找
    page = wiki_wiki.page(cleaned_keyword)

    # 如果找不到，尝试模糊搜索
    if not page.exists():
        search_results = wikipedia.search(cleaned_keyword)
        if not search_results:
            with open(log_file, "a", encoding="utf-8") as log_f:
                log_f.write(f"{keyword}\n")
            print(f"❌ No Wikipedia page found for '{keyword}', logged in {log_file}.")
            return
        best_match = search_results[0]
        print(f"🔍 Using best match: {best_match}")
        page = wiki_wiki.page(best_match)

    if page.exists():
        file_path = os.path.join(output_dir, f"{page.title.replace(' ', '_')}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"Title: {page.title}\n")
            f.write(f"URL: {page.fullurl}\n\n")
            f.write(f"Summary:\n{page.summary}\n\n")
            f.write(f"Full Content:\n{page.text}\n")
        print(f"✅ Saved: {file_path} (Summary Length: {len(page.summary)})")
    else:
        with open(log_file, "a", encoding="utf-8") as log_f:
            log_f.write(f"{keyword}\n")
        print(f"❌ No Wikipedia page found for '{keyword}', logged in {log_file}.")

def process_keywords(input_file, output_dir, log_file):
    """
    读取城市名称，去重，并查询 Wikipedia。
    """
    os.makedirs(output_dir, exist_ok=True)
    
    with open(input_file, "r", encoding="utf-8") as f:
        keywords = [line.strip() for line in f.readlines()]

    print(f"📌 Processing {len(keywords)} keywords...")

    for keyword in tqdm(keywords):
        print(f"🔍 Fetching: {keyword}")
        fetch_wikipedia_data(keyword, output_dir, log_file)


if __name__ == "__main__":
    input_file = "data/unique_cities.txt"  # 关键词文件
    output_dir = "data/wiki/city/"  # 输出目录
    log_file = "data/missing_pages.log"  # 记录未找到的页面

    process_keywords(input_file, output_dir, log_file)
