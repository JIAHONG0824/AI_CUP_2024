import json
import os
from llama_index.postprocessor.voyageai_rerank import VoyageAIRerank
from llama_index.embeddings.voyageai import VoyageEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex
from pinecone import Pinecone, ServerlessSpec
from llama_index.core import StorageContext
from llama_index.core import Document
from llama_index.core import Settings
from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
Settings.chunk_size = 30000
Settings.embed_model = VoyageEmbedding(
    model_name="voyage-3",
    voyage_api_key=os.getenv("VOYAGEAI_API_KEY"),
    embed_batch_size=100,
)
voyageai_rerank = VoyageAIRerank(
    top_k=1,
    model="rerank-2",
    truncation=True,
    api_key=os.getenv("VOYAGEAI_API_KEY"),
)

pc = Pinecone()
# finance index
pinecone_index = pc.Index("finance")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
finance_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
# insurance index
pinecone_index = pc.Index("insurance")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
insurance_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
# faq index
pinecone_index = pc.Index("faq")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
faq_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
# read questions
with open("questions_preliminary.json", "rb") as f:
    quitestions = json.load(f)["questions"]
predictions = {"answers": []}
for q in tqdm(quitestions):
    if q["category"] == "finance":
        index = finance_index
    elif q["category"] == "insurance":
        index = insurance_index
    else:
        index = faq_index
    query = q["query"]
    filters = MetadataFilters(
        filters=[
            MetadataFilter(
                key="source",
                operator=FilterOperator.IN,
                value=[str(s) for s in q["source"]],
            ),
        ]
    )
    retriever = index.as_retriever(similarity_top_k=100, filters=filters)
    nodes = retriever.retrieve(query)
    nodes = voyageai_rerank.postprocess_nodes(nodes, query_str=query)
    predictions["answers"].append(
        {
            "qid": q["qid"],
            "retrieve": nodes[0].metadata["source"],
        }
    )
with open("pred_retrieve_example 2.json", "w", encoding="utf8") as f:
    json.dump(predictions, f, ensure_ascii=False, indent=4)
