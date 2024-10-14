import json

with open("reference/faq/pid_map_content.json", "rb") as f:
    datas = json.load(f)
documents = []
for i in range(len(datas)):
    for qa in datas[str(i)]:
        documents.append(
            {
                "text": qa["question"],
                "metadata": {
                    "question": qa["question"],
                    "answers": qa["answers"],
                    "id": i,
                },
            }
        )
with open("faq/faq_documents.json", "w", encoding="utf8") as f:
    json.dump(documents, f, ensure_ascii=False, indent=4)
