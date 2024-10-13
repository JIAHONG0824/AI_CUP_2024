import json
from pinecone import Pinecone
from openai import OpenAI
from tqdm import tqdm
import time

# set up OpenAI
client = OpenAI(
    api_key="sk-7r2vepDTqMd6Rey3R_MZ887D4AD6kyGsk9gmXr8SIvT3BlbkFJcIGq9iuDY1mBgSCmVM_Mf-1mr6Xw2v-MGPUB895LkA"
)
# set up Pinecone
pc = Pinecone(api_key="ba449aa0-2c00-421b-8e7a-5cccb051bcf7")
Vector_database = pc.Index("insurance")

# read documents
with open("insurance_documents.json", "rb") as f:
    documents = json.load(f)

BATCH_SIZE = 50
vector_id = 0
for i in tqdm(range(0, len(documents), BATCH_SIZE)):
    # you can use another embedding model here
    response = client.embeddings.create(
        input=[d["text"] for d in documents[i : i + BATCH_SIZE]],
        model="text-embedding-3-small",
    )
    vectors = []
    for d, e in zip(documents[i : i + BATCH_SIZE], response.data):
        vectors.append(
            {
                "id": str(vector_id),
                "values": e.embedding,
                "metadata": {
                    "source_pdf": int(d["metadata"]["source_pdf"]),
                },
            }
        )
        vector_id += 1
    Vector_database.upsert(vectors=vectors, namespace="ns1", show_progress=True)
    time.sleep(2)
