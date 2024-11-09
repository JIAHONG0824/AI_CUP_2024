import argparse
import json
import os
import re
from tqdm import tqdm


def faq():
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


def insurance():
    documents = []
    for folder in os.listdir("insurance_markdown"):
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
    if not os.path.exists("documents"):
        os.makedirs("documents")
    with open("./documents/insurance.json", "w", encoding="utf8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=4)

def finance():
    documents=[]
    for folder in os.listdir('finance_markdown'):
        for file in os.listdir(os.path.join('finance_markdown',folder)):
            if file.endswith('.md'):
                with open(os.path.join('finance_markdown',folder,file),'r',encoding='utf-8') as f:
                    texts=f.read()
                    f.close()
                # remove headers
                texts = re.sub(r"^#+.*$", "", texts, flags=re.MULTILINE)
                # remove images
                texts = re.sub(r"!\[.*?\]\(.*?\)", "", texts)
                texts = re.sub(r"\n{2,}", "\n\n", texts)
                texts=texts.replace(' ','')
                texts=texts.strip()
                for text in texts.split('\n\n'):
                    if len(text)==0:
                        continue
                    documents.append(
                        {
                            'text':text,
                            'metadata':{
                                'text':text,
                                'source':folder
                            }
                        }
                    )
    if not os.path.exists('documents'):
        os.makedirs('documents')
    with open('./documents/finance.json','w',encoding='utf8') as f:
        json.dump(documents,f,ensure_ascii=False,indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pinecone index setup")
    parser.add_argument("--type", type=str, help="faq or finance or insurance")
    args = parser.parse_args()
    if args.type == "faq":
        faq()
    elif args.type == "insurance":
        insurance()
    elif args.type == "finance":
        finance()
    else:
        print('Please provide a valid type: "faq" or "finance" or "insurance"')
        exit()
