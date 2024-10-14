import json

with open("reference/faq/pid_map_content.json", "rb") as f:
    pid_map_content = json.load(f)
total = 0
for i in range(len(pid_map_content)):
    total += len(pid_map_content[str(i)])
print(total)
documents = []
for i in range(len(pid_map_content)):
    for qa in pid_map_content[str(i)]:
        documents.append(
            {"text": qa["question"], "metadata": {"answers": qa["answers"], "id": i}}
        )
print(len(documents))
with open("faq/faq_documents.json", "w", encoding="utf8") as f:
    json.dump(documents, f, ensure_ascii=False, indent=4)
