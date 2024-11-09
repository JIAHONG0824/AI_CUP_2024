import argparse
import voyageai
import time
import json
import os
from pinecone import ServerlessSpec, Pinecone
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

load_dotenv()


def search(index_name):
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    vo = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
    rerank_name = "bge-reranker-v2-m3"
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
        response = client.embeddings.create(
            input=query,
            model="text-embedding-3-small",
        )
        # embeddings search results
        results = index.query(
            vector=response.data[0].embedding,
            top_k=10,
            include_values=False,
            include_metadata=True,
            filter={"source": {"$in": [str(q) for q in question["source"]]}},
        )
        original_documents = [
            {"id": str(i), "text": x["metadata"]["text"], "metadata": x["metadata"]}
            for i, x in enumerate(results["matches"])
        ]
        docs=[d['text'] for d in original_documents]
        reranking=vo.rerank(query,docs,model="rerank-2",top_k=1)
        check=reranking.results[0].index
        predictions.append(
            {
                "qid": question["qid"],
                "retrieve": original_documents[check]["metadata"]["source"],
                "category": question["category"],
            }
        )
        # temp = [
        #     {"id": str(i), "text": x["metadata"]["text"]}
        #     for i, x in enumerate(results["matches"])
        # ]
        # rerank documents
        # rerank_results = pc.inference.rerank(
        #     model=rerank_name,
        #     query=query,
        #     documents=temp,
        #     top_n=1,
        #     return_documents=False,
        # )
        # top_1 = rerank_results.data[0].index
        # rerank_documents = []
        # rerank_documents.append(original_documents[top_1])
    #     predictions.append(
    #         {
    #             "qid": question["qid"],
    #             "retrieve": rerank_documents[0]["metadata"]["source"],
    #             "category": question["category"],
    #         }
    #     )
    with open("predictions.json", "w", encoding="utf8") as f:
        json.dump(predictions, f, ensure_ascii=False, indent=4)
    print("Predictions saved.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pinecone search")
    parser.add_argument("--index_name", type=str, help="faq or finance or insurance")
    args = parser.parse_args()
    search(args.index_name)
