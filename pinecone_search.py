import argparse
import json
import os
from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder
from pinecone import ServerlessSpec, Pinecone
from dotenv import load_dotenv

# from openai import OpenAI
from tqdm import tqdm

load_dotenv()


def search(index_name):
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    embeddings_model = SentenceTransformer(
        "intfloat/multilingual-e5-large", device="cuda"
    )
    reranker = CrossEncoder(
        "jinaai/jina-reranker-v2-base-multilingual",
        device="cuda",
        trust_remote_code=True,
    )
    # rerank_name = "bge-reranker-v2-m3"
    index = pc.Index(index_name)
    # Load questions with category "faq"
    with open("dataset/preliminary/questions_example.json", "rb") as f:
        questions = json.load(f)["questions"]
    questions = [q for q in questions if q["category"] == index_name]

    predictions = []
    # Search for each question
    for question in tqdm(questions):
        query = question["query"]
        # query to embeddings
        embeddings = embeddings_model.encode(
            query, normalize_embeddings=True, prompt="query:"
        )
        # embeddings search results
        results = index.query(
            vector=embeddings.tolist(),
            top_k=10,
            include_values=False,
            include_metadata=True,
            filter={"source": {"$in": [str(q) for q in question["source"]]}},
        )
        # predictions.append(
        #     {
        #         "qid": question["qid"],
        #         "retrieve": results["matches"][0]["metadata"]["source"],
        #         "category": question["category"],
        #     }
        # )
        original_documents = [
            {"id": str(i), "text": x["metadata"]["text"], "metadata": x["metadata"]}
            for i, x in enumerate(results["matches"])
        ]
        # rerank the search results
        rank = reranker.rank(
            query=query,
            documents=[d["text"] for d in original_documents],
            top_k=5,
            return_documents=True,
        )
        predictions.append(
            {
                "qid": question["qid"],
                "retrieve": original_documents[rank[0]["corpus_id"]]["metadata"][
                    "source"
                ],
                "category": question["category"],
            }
        )
    with open(f"predictions_{index_name}.json", "w", encoding="utf8") as f:
        json.dump(predictions, f, ensure_ascii=False, indent=4)
    print("Predictions saved.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pinecone search")
    parser.add_argument("--index_name", type=str, help="faq or finance or insurance")
    args = parser.parse_args()
    search(args.index_name)
