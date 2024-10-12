import json
import time
from pinecone import Pinecone
from openai import OpenAI
from tqdm import tqdm

# set up OpenAI
client = OpenAI(
    api_key="sk-7r2vepDTqMd6Rey3R_MZ887D4AD6kyGsk9gmXr8SIvT3BlbkFJcIGq9iuDY1mBgSCmVM_Mf-1mr6Xw2v-MGPUB895LkA"
)
# set up Pinecone
pc = Pinecone(api_key="ba449aa0-2c00-421b-8e7a-5cccb051bcf7")
Vector_database = pc.Index("faq")
with open("dataset/preliminary/questions_example.json", "rb") as f:
    questions = json.load(f)["questions"]
questions = [q for q in questions if q["category"] == "faq"]
predictions = {"answers": []}
for q in tqdm(questions):
    response = client.embeddings.create(
        input=q["query"],
        model="text-embedding-3-small",
        dimensions=512,
    )
    result = Vector_database.query(
        namespace="ns1",
        vector=response.data[0].embedding,
        top_k=1,
        include_values=False,
        include_metadata=True,
    )
    predictions["answers"].append(
        {
            "qid": q["qid"],
            "retrieve": result["matches"][0]["metadata"]["source_id"],
            "category": q["category"],
        }
    )
    time.sleep(1)
with open("faq_pred_retrieve_embedding.json", "w", encoding="utf-8") as f:
    json.dump(predictions, f, ensure_ascii=False, indent=4)
