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

# 設定嵌入模型與文件分割大小
Settings.chunk_size = 30000
Settings.embed_model = VoyageEmbedding(
    model_name="voyage-3",
    voyage_api_key=os.getenv("VOYAGEAI_API_KEY"),
    embed_batch_size=100,
)


def indexing(index_name):
    """
    建立指定名稱的索引。

    此函式讀取 JSON 格式的文件檔案，並依據內容創建相應的索引。

    參數:
        index_name (str): 索引名稱，對應 ./documents/{index_name}.json 檔案。

    程式流程:
    - 從指定的 JSON 檔案讀取文件資料。
    - 依據文件內容創建 Document 對象並加入文件列表中。
    - 透過 Pinecone 服務創建向量儲存，並以文件內容創建索引。

    顯示:
    - 列印文件數量與索引建立狀態。
    """
    print("processing", index_name)

    # 讀取指定文件的 JSON 資料
    with open(f"./documents/{index_name}.json", "rb") as f:
        docs = json.load(f)
    print("number of documents in", index_name, ":", len(docs))

    # 創建文件列表
    documents = []
    for doc in docs:
        temp = Document()
        temp.text = doc["text"]
        temp.metadata = doc["metadata"]
        documents.append(temp)

    # 初始化 Pinecone 服務並建立向量儲存
    pc = Pinecone()
    pinecone_index = pc.Index(index_name)
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 根據文件內容建立索引
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    print(index_name, "index created")


if __name__ == "__main__":
    """
    主函式。

    運行時，依序為 'finance'、'insurance' 和 'faq' 建立索引。
    """
    indexing("finance")
    indexing("insurance")
    indexing("faq")
