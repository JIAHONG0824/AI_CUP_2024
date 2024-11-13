import json
import os
import re
from tqdm import tqdm


def build_finance_json():
    """
    讀取 `finance_markdown` 資料夾內的所有檔案，將每個檔案內容分割後，
    存入 `finance.json` 檔案中。

    每個檔案的內容被 `[sep]` 分割，第一部分為 head，後續部分為 content，
    每段 content 將與 head 合併，形成一份文件記錄。

    finance.json 的格式如下：
    [
        {
            "text": "內容",
            "metadata": {
                "source": "資料來源"
            }
        },
        ...
    ]
    """
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
                {
                    "text": head + "\n" + content,
                    "metadata": {"source": file.split(".")[0]},
                }
            )
    print("number of documents in finance:", len(documents))
    with open("./documents/finance.json", "w", encoding="utf8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=4)


def build_insurance_json():
    """
    讀取 `insurance_markdown` 資料夾內的所有 `.md` 檔案，清除標題與圖片後，
    將內容分割並儲存至 `insurance.json` 中。

    將每個檔案的內容以換行分隔，並附上對應的資料夾名稱作為 metadata source。

    insurance.json 的格式如下：
    [
        {
            "text": "內容",
            "metadata": {
                "text": "內容",
                "source": "資料來源"
            }
        },
        ...
    ]
    """
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
                # 移除標題
                texts = re.sub(r"^#+.*$", "", texts, flags=re.MULTILINE)
                # 移除圖片
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


def build_faq_json():
    """
    讀取 `pid_map_content.json` 檔案，將每個問題與答案儲存至 `faq.json` 檔案中。

    每筆資料包含 question、answer 以及 source 資訊。

    faq.json 的格式如下：
    [
        {
            "text": "問題",
            "metadata": {
                "question": "問題",
                "answer": "答案",
                "source": "資料來源"
            }
        },
        ...
    ]
    """
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


# 主程式
if __name__ == "__main__":
    # 檢查並建立 `documents` 資料夾
    if not os.path.exists("documents"):
        os.makedirs("documents")

    build_finance_json()
    build_insurance_json()
    build_faq_json()
