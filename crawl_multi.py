import wikipedia
import wikipediaapi
import os
import time
import random
import threading
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# 初始化 Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent='FengLuo(fl38@rice.edu)')

# 创建线程锁，避免 log 文件同时写入冲突
log_lock = threading.Lock()

def clean_keyword(keyword):
    words = keyword.split()
    remove_suffixes = {"CDP", "city", "town", "village", "municipality", "borough"}
    cleaned_words = [word for word in words if word not in remove_suffixes]
    cleaned_keyword = " ".join(cleaned_words)
    return f"{cleaned_keyword}, {words[-1]}"

def log_missing(keyword, log_file):
    """线程安全地写入 log 文件"""
    with log_lock:  # 确保只有一个线程能写入
        with open(log_file, "a", encoding="utf-8") as log_f:
            log_f.write(f"{keyword}\n")

def fetch_wikipedia_data(keyword, output_dir, log_file):
    if random.random() < 0.7:
        time.sleep(random.uniform(0.3, 1.0))

    cleaned_keyword = clean_keyword(keyword)
    page = wiki_wiki.page(cleaned_keyword)

    if not page.exists():
        search_results = wikipedia.search(cleaned_keyword)
        if not search_results:
            log_missing(keyword, log_file)
            return f"❌ No Wikipedia page found for '{keyword}', logged."

        best_match = search_results[0]
        page = wiki_wiki.page(best_match)

    if page.exists():
        file_path = os.path.join(output_dir, f"{page.title.replace(' ', '_')}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"Title: {page.title}\n")
            f.write(f"URL: {page.fullurl}\n\n")
            f.write(f"Summary:\n{page.summary}\n\n")
            f.write(f"Full Content:\n{page.text}\n")
        return f"✅ Saved: {file_path} (Summary Length: {len(page.summary)})"
    else:
        log_missing(keyword, log_file)
        return f"❌ No Wikipedia page found for '{keyword}', logged."

def process_keywords(input_file, output_dir, log_file, max_workers=10):
    os.makedirs(output_dir, exist_ok=True)
    
    with open(input_file, "r", encoding="utf-8") as f:
        keywords = [line.strip() for line in f.readlines()]

    print(f"📌 Processing {len(keywords)} keywords using {max_workers} threads...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_keyword = {executor.submit(fetch_wikipedia_data, keyword, output_dir, log_file): keyword for keyword in keywords}

        for future in tqdm(as_completed(future_to_keyword), total=len(keywords)):
            try:
                result = future.result()
                if result:
                    print(result)
            except Exception as e:
                print(f"⚠️ Error processing {future_to_keyword[future]}: {e}")

if __name__ == "__main__":
    # input_file = "data/unique_cities.txt"
    # output_dir = "data/wiki/city/"
    # log_file = "data/missing_pages.log"

    input_file = "data/unique_attractions.txt"
    output_dir = "data/wiki/attraction/"
    log_file = "data/missing_pages.log"

    process_keywords(input_file, output_dir, log_file, max_workers=3)
