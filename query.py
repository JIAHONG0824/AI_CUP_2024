import json
from pinecone import Pinecone, ServerlessSpec
from tqdm import tqdm
import time
pc = Pinecone(api_key="ba449aa0-2c00-421b-8e7a-5cccb051bcf7")
Vector_database = pc.Index("faq")
with open("dataset/preliminary/questions_example.json", "rb") as f:
    questions = json.load(f)["questions"]
questions = [q for q in questions if q["category"] == "faq"]
pred = {"answers": []}
for q in tqdm(questions):
    x = pc.inference.embed(
        "multilingual-e5-large",
        inputs=q["query"],
        parameters={"input_type": "query"},
    )
    result = Vector_database.query(
        namespace="ns1",
        vector=x[0]["values"],
        top_k=1,
        include_values=False,
        include_metadata=True,
        # 這裡的filter是用來過濾資料的，這裡的意思是只要id是558或90的資料 最重要的部分
        # filter={"id": {"$in": [558, 90]}},
    )
    pred["answers"].append(
        {
            "qid": q["qid"],
            "retrieve": int(result["matches"][0]["metadata"]["id"]),
        }
    )
    time.sleep(1)
with open("pred.json", "w", encoding="utf8") as f:
    json.dump(pred, f, ensure_ascii=False, indent=4)
