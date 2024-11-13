# 專案文件

## 專案結構
```plaintext
專案根目錄
├── Model/
│   └── index.py               # 向量儲存索引
├── Preprocess/
│   ├── build_json.py          # 用於生成 JSON 的腳本
│   └── insurance_pdf_2_md.py     # 將保險 PDF 文件轉換為 Markdown 的腳本
├── .gitignore                 # Git 忽略文件
├── README.md                  # 專案說明文件
├── main.py                    # 執行預測操作的主腳本
├── questions_preliminary.json # 包含 900 題的 JSON 文件
└── requirements.txt           # 依賴項列表
```
## 1. 安裝相依套件
在執行專案前，請先安裝相依套件：
```
pip install -r requirements.txt
```
## 2. PDF 轉換為 Markdown

### 概述
本專案將財務（finance）及保險（insurance）相關的 PDF 檔案轉換為 Markdown 格式，以便後續處理。

### 轉換細節
- **保險 PDF**：透過 [Marker](https://github.com/VikParuchuri/marker) 將保險類 PDF 檔案轉換為 Markdown 格式。
- **財務 PDF**：透過 [LlamaCloud 的 Parse 服務](https://cloud.llamaindex.ai/project/37d122c8-90cf-422c-b8dd-5bcdf26d6cd6/parse) 將財務類 PDF 檔案轉換為 Markdown 格式，並由四名組員每日上傳財務類 PDF 檔案，確保轉換工作的持續進行。

## 3. 前處理步驟

### 保險 Markdown 檔案處理
為了進行進一步分析，我們使用 `Preprocess/build_json.py` 對保險數據進行以下前處理：

- **讀取檔案**：腳本會讀取 `insurance_markdown` 資料夾中的所有 `.md` 檔案。
- **數據清理**：移除 Markdown 內容中的標題與圖片，以確保資料一致性。
- **分段儲存**：將清理後的內容按行分割，並儲存至 `insurance.json`，同時為每行數據附加原始資料夾名稱作為來源 metadata，便於後續查閱和處理。

### 財務 Markdown 檔案處理
對財務類 PDF 檔案的處理需人工協助，以確保內容準確性。我們的處理步驟如下：

1. **手動比對與標記**：對比每個 Markdown 檔案與原始 PDF，並在每處 PDF 換頁位置手動加入 `[sep]` 符號以標記分頁。
2. **資料清理**：由成員自行判斷是否刪除無關或冗餘資訊，僅保留有用的內容。

接下來使用 `Preprocess/build_json.py` 進行以下處理：

- **讀取檔案**：讀取 `finance_markdown` 資料夾內的所有檔案。
- **分段儲存**：每個檔案的內容依照 `[sep]` 分割，將第一部分設為 head，其後每段 content 與 head 合併，形成一筆完整的文件記錄，最終存入 `finance.json` 中。
### faq 檔案處理
faq檔案不需要額外處理步驟。

## 4. 操作說明

### 下載並處理 Markdown 檔案

1. **下載 Markdown 檔案**：從[前處理完成](https://drive.google.com/drive/u/0/folders/1ldEWRbzwjKm6Q3_dyoq8YIJRfygjiNFl)下載轉換後的 Markdown (`.md`) 檔案，並將它們分別存入 `insurance_markdown` 資料夾和 `finance_markdown` 資料夾中，以便後續處理。

2. **執行 `build_json.py`**：下載完成後，執行 `Preprocess/build_json.py` 以建立
finance、insurance、faq對應的json檔案

```
python Preprocess/build_json.py
```
## 5. 執行比賽測試資料

- `main.py` 用於比賽時執行測試資料，並進行預測或其他指定操作。此程式會使用前處理過的資料進行推理或預測。

## 6. 初賽題目

- **questions_preliminary.json**：包含初賽的 900 題題目資料，供比賽測試和驗證模型使用。
