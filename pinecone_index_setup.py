import argparse
import time
import json
import os
from sentence_transformers import SentenceTransformer
from pinecone import ServerlessSpec, Pinecone
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
BATCH_SIZE = 50


def upsert(index_name):
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    embeddings_model = SentenceTransformer(
        "intfloat/multilingual-e5-large", device="cuda"
    )
    # Create an index if it does not exist
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=1024,
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            metric="cosine",
        )
        print("Index", f'"{index_name}"', "created")
    else:
        print("Index", f'"{index_name}"', "already exists")
    # Wait for the index to be ready
    while not pc.describe_index(index_name).status["ready"]:
        print("Index not ready yet, waiting...")
        time.sleep(3)
    index = pc.Index(index_name)
    with open(f"./documents/{index_name}.json", "rb") as f:
        datas = json.load(f)
    id = 1
    for i in tqdm(range(0, len(datas), BATCH_SIZE)):
        # query to embeddings
        embeddings = embeddings_model.encode(
            [d["text"] for d in datas[i : i + BATCH_SIZE]],
            normalize_embeddings=True,
            prompt="passage:",
        )
        # vectors to upsert
        vectors = []
        for d, e in zip(datas[i : i + BATCH_SIZE], embeddings):
            vectors.append(
                {
                    "id": str(id),
                    "values": e,
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
    upsert(args.index_name)
