import voyageai
import os
from dotenv import load_dotenv
load_dotenv()
vo = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
# This will automatically use the environment variable VOYAGE_API_KEY.
# Alternatively, you can use vo = voyageai.Client(api_key="<your secret key>")

query = "When is Apple's conference call scheduled?"
documents = [
    "The Mediterranean diet emphasizes fish, olive oil, and vegetables, believed to reduce chronic diseases.",
    "Photosynthesis in plants converts light energy into glucose and produces essential oxygen.",
    "20th-century innovations, from radios to smartphones, centered on electronic advancements.",
    "Rivers provide water, irrigation, and habitat for aquatic species, vital for ecosystems.",
    "Apple’s conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET.",
    "Shakespeare's works, like 'Hamlet' and 'A Midsummer Night's Dream,' endure in literature."
]

reranking = vo.rerank(query, documents, model="rerank-2", top_k=3)
for r in reranking.results:
    print(f"Document: {r.document}")
    print(f"Relevance Score: {r.relevance_score}")