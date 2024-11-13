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

# 載入環境變數
load_dotenv()

# 設定嵌入模型與文件分割大小
Settings.chunk_size = 30000
Settings.embed_model = VoyageEmbedding(
    model_name="voyage-3",
    voyage_api_key=os.getenv("VOYAGEAI_API_KEY"),
    embed_batch_size=100,
)

# 初始化 VoyageAI Rerank 後處理器
voyageai_rerank = VoyageAIRerank(
    top_k=1,
    model="rerank-2",
    truncation=True,
    api_key=os.getenv("VOYAGEAI_API_KEY"),
)

# 初始化 Pinecone 服務與索引
pc = Pinecone()

# 建立財務索引
pinecone_index = pc.Index("finance")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
finance_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

# 建立保險索引
pinecone_index = pc.Index("insurance")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
insurance_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

# 建立 FAQ 索引
pinecone_index = pc.Index("faq")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
faq_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

# 讀取問題
with open("questions_preliminary.json", "rb") as f:
    questions = json.load(f)["questions"]

# 初始化預測結果字典
predictions = {"answers": []}

# 遍歷問題並進行索引查詢與重新排序
for q in tqdm(questions):
    """
    根據問題分類選擇適當的索引，並執行檢索與重新排序。

    流程:
    - 根據問題的分類 ('finance', 'insurance', 'faq') 選擇相應的索引。
    - 使用 MetadataFilters 依據問題來源篩選文件。
    - 檢索結果節點後，使用 VoyageAIRerank 進行重新排序。
    - 將結果追加至 predictions 字典中，包含問題 ID 與最相似的文件來源。

    參數:
        q (dict): 包含問題內容、分類、來源的字典。
    """
    # 根據問題分類選擇索引
    if q["category"] == "finance":
        index = finance_index
    elif q["category"] == "insurance":
        index = insurance_index
    else:
        index = faq_index

    # 設定查詢與篩選條件
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

    # 執行檢索與後處理排序
    retriever = index.as_retriever(similarity_top_k=10, filters=filters)
    nodes = retriever.retrieve(query)
    nodes = voyageai_rerank.postprocess_nodes(nodes, query_str=query)

    # 儲存最相關的來源文件於預測結果
    predictions["answers"].append(
        {
            "qid": q["qid"],
            "retrieve": nodes[0].metadata["source"],
        }
    )

# 將結果寫入 JSON 檔案
with open("pred_retrieve_example_2.json", "w", encoding="utf8") as f:
    json.dump(predictions, f, ensure_ascii=False, indent=4)
