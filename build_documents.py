import argparse
import json
import os
import re
from tqdm import tqdm

documents = []


def main():
    global documents
    with open("./reference/faq/pid_map_content.json", "rb") as f:
        datas = json.load(f)
    for source, qa_lists in tqdm(datas.items()):
        for qa in qa_lists:
            documents.append(
                {
                    "text": qa["question"],
                    "metadata": {
                        "text": qa["question"],
                        "answer": qa["answers"],
                        "source": source,
                    },
                }
            )
    save_documents("faq")
    documents = []
    process_markdown("finance")
    documents = []
    process_markdown("insurance")


# Save documents to json file
def save_documents(type):
    with open(f"./documents/{type}.json", "w", encoding="utf8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=4)


# Process markdown files and save documents to json file
def process_markdown(type):
    for folder in tqdm(os.listdir(f"./{type}_markdown")):
        for file in os.listdir(os.path.join(f"./{type}_markdown", folder)):
            if file.endswith(".md"):
                with open(
                    os.path.join(f"./{type}_markdown", folder, file),
                    "r",
                    encoding="utf-8",
                ) as f:
                    texts = f.read()
                    f.close()
                texts = re.sub(r"^#{1,6}.*\n?", "", texts, flags=re.MULTILINE)
                texts = re.sub(r"!\[.*?\]\(.*?\)", "", texts)
                texts = re.sub(r"\n{3,}", "\n\n", texts)
                texts = texts.replace(" ", "")
                texts = texts.strip()
                for text in texts.split("\n\n"):
                    if len(text) < 10:
                        continue
                    documents.append(
                        {"text": text, "metadata": {"text": text, "source": folder}}
                    )
    save_documents(type)


if __name__ == "__main__":
    if not os.path.exists("./documents"):
        os.mkdir("./documents")
    main()
