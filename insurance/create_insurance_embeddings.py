import json
from pinecone import Pinecone, ServerlessSpec
from tqdm import tqdm
import time
from openai import OpenAI
client = OpenAI(api_key="sk-7r2vepDTqMd6Rey3R_MZ887D4AD6kyGsk9gmXr8SIvT3BlbkFJcIGq9iuDY1mBgSCmVM_Mf-1mr6Xw2v-MGPUB895LkA")
pc = Pinecone(api_key="ba449aa0-2c00-421b-8e7a-5cccb051bcf7")
Vector_database = pc.Index("insurance")
with open("insurance/insurance_documents.json", "rb") as f:
    documents = json.load(f)
BATCH_SIZE = 50
vec_num = 0
for i in tqdm(range(0, len(documents), BATCH_SIZE)):
    embeddings = client.embeddings.create(
        input=[doc["text"] for doc in documents[i : i + BATCH_SIZE]],
        model="text-embedding-3-small",
    )
    # embeddings = pc.inference.embed(
    #     "multilingual-e5-large",
    #     inputs=[doc["text"] for doc in documents[i : i + BATCH_SIZE]],
    #     parameters={"input_type": "passage"},
    # )
    vectors = []
    for d, e in zip(documents[i : i + BATCH_SIZE], embeddings.data):
        vectors.append(
            {"id": f"{vec_num}", "values": e.embedding, "metadata": d["metadata"]}
        )
        vec_num += 1
    Vector_database.upsert(
        vectors=vectors,
        namespace="ns1",
    )
    time.sleep(2)
