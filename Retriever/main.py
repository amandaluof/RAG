import os
import re
import pandas as pd
from tqdm import tqdm

from sentence_transformers import SentenceTransformer
from datasets import load_dataset

from extract_search import DenseRetrievalExactSearch

def buld_csv(folders):
    # 用于存储数据的列表
    data = []

    # 处理文件
    for folder in tqdm(folders):
        for filename in tqdm(os.listdir(folder)):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read()

                # 获取 _id
                _id = filename  # 直接使用文件名作为唯一 ID

                # 处理 title
                if folder in ["attraction_split", "city_split"]:
                    title = re.sub(r'_\d+\.txt$', '', filename)  # 去掉 _数字
                else:
                    title = filename.replace(".txt", "")  # 直接去掉扩展名

                # 存储数据
                data.append({"_id": _id, "title": title, "text": text})

    # 转换为 DataFrame
    df = pd.DataFrame(data)
    df.to_csv("dataset.csv", index=False, encoding="utf-8")

    return df

# text_embedding_model = SentenceTransformer("NovaSearch/stella_en_400M_v5", trust_remote_code=True) # It can be worked in CPU.
text_embedding_model = SentenceTransformer("dunzhang/stella_en_400M_v5", trust_remote_code=True) # It can be worked in CPU.

retriver_params = {"batch_size":128, "corpus_size":5000}
dense_retriever = DenseRetrievalExactSearch(
        text_embedding_model,
        **retriver_params,
        )

# corpus creating
folders = ["../data/wiki/attraction_split", "../data/wiki/city_split", "../data/wiki/attraction", "../data/wiki/city"]
# folders = ["../data/wiki/attraction"]
buld_csv(folders)

dataset = load_dataset("csv", data_files="dataset.csv")
dataset["train"] = dataset["train"].add_column("id", range(len(dataset["train"])))
corpus = dataset["train"]

search_params = {"top_k":10, "score_function":"cos_sim", "return_sorted":True}

queries = {0: "new york", 1: "chicago"}

res = dense_retriever.search(
    corpus,
    queries,
    **search_params
)

for query_id, retrieved_docs in res.items():
    print(f"\nQuery {query_id}: {queries[query_id]}")  # 输出查询内容
    print("Top-K retrieved documents:")
    sorted_docs = sorted(retrieved_docs.items(), key=lambda x: x[1], reverse=True)
    
    for doc_id, score in sorted_docs.items():
        doc = corpus[doc_id]  # 获取文档内容
        print(f"  - ID: {doc_id}, Title: {doc['title']}, Score: {score:.4f}")