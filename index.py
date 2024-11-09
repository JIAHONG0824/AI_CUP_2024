import json
import os
from llama_index.embeddings.voyageai import VoyageEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex
from pinecone import Pinecone, ServerlessSpec
from llama_index.core import StorageContext
from llama_index.core import Document
from llama_index.core import Settings
from dotenv import load_dotenv

load_dotenv()
# Settings.embed_model = VoyageEmbedding(model_name="voyage-finance-2",voyage_api_key=os.getenv("VOYAGEAI_API_KEY"))
Settings.chunk_size = 30000
Settings.embed_model = VoyageEmbedding(
    model_name="voyage-3",
    voyage_api_key=os.getenv("VOYAGEAI_API_KEY"),
    embed_batch_size=100,
)

# indexing finance, insurance, faq
def indexing(index_name):
    print("processing", index_name)
    with open(f"./documents/{index_name}.json", "rb") as f:
        docs = json.load(f)
    print("number of documents in", index_name, ":", len(docs))
    documents = []
    for doc in docs:
        temp = Document()
        temp.text = doc["text"]
        temp.metadata = doc["metadata"]
        documents.append(temp)
    pc = Pinecone()
    pinecone_index = pc.Index(index_name)
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    print(index_name, "index created")


if __name__ == "__main__":
    indexing("finance")
    indexing("insurance")
    indexing("faq")
