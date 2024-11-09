import json
import os
import re
from tqdm import tqdm

# create documents folder
if not os.path.exists("documents"):
    os.makedirs("documents")

# build finance.json
documents = []
for file in tqdm(os.listdir("finance_markdown")):
    with open(f"finance_markdown/{file}", "r", encoding="utf8") as f:
        texts = f.read()
    texts = texts.split("[sep]")
    head = texts[0]
    contents = texts[1:]
    for content in contents:
        content = content.strip()
        documents.append(
            {"text": head + "\n" + content, "metadata": {"source": file.split(".")[0]}}
        )
print("number of documents in finance:", len(documents))
with open("./documents/finance.json", "w", encoding="utf8") as f:
    json.dump(documents, f, ensure_ascii=False, indent=4)
# build insurance.json
documents = []
for folder in tqdm(os.listdir("insurance_markdown")):
    for file in os.listdir(os.path.join("insurance_markdown", folder)):
        if file.endswith(".md"):
            with open(
                os.path.join("insurance_markdown", folder, file),
                "r",
                encoding="utf-8",
            ) as f:
                texts = f.read()
                f.close()
            # remove headers
            texts = re.sub(r"^#+.*$", "", texts, flags=re.MULTILINE)
            # remove images
            texts = re.sub(r"!\[.*?\]\(.*?\)", "", texts)
            texts = re.sub(r"\n{2,}", "\n\n", texts)
            texts = texts.strip()
            for text in texts.split("\n\n"):
                documents.append(
                    {"text": text, "metadata": {"text": text, "source": folder}}
                )
print("number of documents in insurance:", len(documents))
with open("./documents/insurance.json", "w", encoding="utf8") as f:
    json.dump(documents, f, ensure_ascii=False, indent=4)
# build faq.json
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
print("number of documents in faq:", len(documents))
with open("./documents/faq.json", "w", encoding="utf8") as f:
    json.dump(documents, f, ensure_ascii=False, indent=4)
