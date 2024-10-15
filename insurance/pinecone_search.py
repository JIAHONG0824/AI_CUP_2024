import json
from pinecone import Pinecone, ServerlessSpec
from tqdm import tqdm
import time
from openai import OpenAI
client = OpenAI(api_key="sk-7r2vepDTqMd6Rey3R_MZ887D4AD6kyGsk9gmXr8SIvT3BlbkFJcIGq9iuDY1mBgSCmVM_Mf-1mr6Xw2v-MGPUB895LkA")
pc = Pinecone(api_key="ba449aa0-2c00-421b-8e7a-5cccb051bcf7")
Vector_database = pc.Index("insurance")
with open("dataset/preliminary/questions_example.json", "rb") as f:
    questions = json.load(f)["questions"]
questions = [q for q in questions if q["category"] == "insurance"]
pred = {"answers": []}
for q in tqdm(questions):
    embeddings = client.embeddings.create(
        input=q["query"],
        model="text-embedding-3-small",
    )
    # x = pc.inference.embed(
    #     "multilingual-e5-large",
    #     inputs=q["query"],
    #     parameters={"input_type": "query"},
    # )
    result = Vector_database.query(
        namespace="ns1",
        vector=embeddings.data[0].embedding,
        top_k=1,
        include_values=False,
        include_metadata=True,
        # 這裡的filter是用來過濾資料的，這裡的意思是只要id是558或90的資料 最重要的部分
        # if q["source"] is [558,90]
        filter={"source_pdf": {"$in": q["source"]}},
    )
    pred["answers"].append(
        {
            "qid": q["qid"],
            "retrieve": int(result["matches"][0]["metadata"]["source_pdf"]),
        }
    )
    time.sleep(1)
with open("insurance/pred.json", "w", encoding="utf8") as f:
    json.dump(pred, f, ensure_ascii=False, indent=4)
