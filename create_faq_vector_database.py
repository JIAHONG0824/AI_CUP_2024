import json
from tqdm import tqdm
from pinecone import Pinecone, ServerlessSpec

# Pinecone setup
pc = Pinecone(api_key="2a66b057-f78a-4bd3-9fb1-9d4d92a5edcb")
index_name = "faq"
index = pc.Index(index_name)

datas = []
documents = []
with open("reference/faq/pid_map_content.json", "rb") as f:
    documents = json.load(f)
for qid, qa in documents.items():
    for i in range(len(qa)):
        datas.append(
            {
                "question": qa[i]["question"],
                "metadata": {
                    "question": qa[i]["question"],
                    "answer": qa[i]["answers"],
                    "source_id": qid,
                },
            }
        )
BATCH_SIZE = 50
vec_id = 0
for i in tqdm(range(0, len(datas), BATCH_SIZE)):
    embeddings = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[d["question"] for d in datas[i : i + BATCH_SIZE]],
        parameters={"input_type": "passage"},
    )
    vectors = []
    for d, e in zip(datas[i : i + BATCH_SIZE], embeddings):
        vectors.append(
            {"id": f"{vec_id}", "values": e["values"], "metadata": d["metadata"]}
        )
        vec_id += 1
    index.upsert(
        vectors=vectors,
        namespace="ns1",
    )
