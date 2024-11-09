import argparse
import time
import json
import os
from pinecone import ServerlessSpec, Pinecone
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

load_dotenv()


def upsert(index_name):
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=1536,
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            metric="cosine",
        )
        print("Index", f'"{index_name}"', "created")
        time.sleep(3)
    else:
        print("Index", f'"{index_name}"', "already exists")
        exit()
    # Wait for the index to be ready
    while not pc.describe_index(index_name).status["ready"]:
        print("Index not ready yet, waiting...")
        time.sleep(3)

    index = pc.Index(index_name)
    BATCH_SIZE = 50
    try:
        with open(f"./documents/{index_name}.json", "rb") as f:
            datas = json.load(f)
    except FileNotFoundError:
        print(f'File "./documents/{index_name}.json" not found')
        exit()
    id = 1
    for i in tqdm(range(0, len(datas), BATCH_SIZE)):
        response = client.embeddings.create(
            input=[d["text"] for d in datas[i : i + BATCH_SIZE]],
            model="text-embedding-3-small",
        )
        vectors = []
        for d, e in zip(datas[i : i + BATCH_SIZE], response.data):
            vectors.append(
                {
                    "id": str(id),
                    "values": e.embedding,
                    "metadata": d["metadata"],
                }
            )
            id += 1
        index.upsert(vectors)
        time.sleep(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pinecone index設置")
    parser.add_argument("--index_name", type=str, help="faq or finance or insurance")
    args = parser.parse_args()
    if args.index_name in ["faq", "finance", "insurance"]:
        upsert(args.index_name)
    else:
        print('Please input "faq" or "finance" or "insurance"')
        exit()
