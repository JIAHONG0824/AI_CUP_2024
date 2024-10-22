import json
import os
from tqdm import tqdm

with open("./reference/faq/pid_map_content.json", "rb") as f:
    datas = json.load(f)
documents = []
for source, qa_lists in tqdm(datas.items()):
    for qa in qa_lists:
        documents.append(
            {
                "text": qa["question"],
                "metadata": {
                    "question": qa["question"],
                    "answer": qa["answers"],
                    "source": source,
                },
            }
        )
if not os.path.exists("documents"):
    os.makedirs("documents")
with open("./documents/faq.json", "w", encoding="utf8") as f:
    json.dump(documents, f, ensure_ascii=False, indent=4)
