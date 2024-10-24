### Folder structure
```
├── dataset
│   ├── preliminary
│   │   └── questions_example.json
│   │   └── ground_truths_example.json
└── reference
    ├── faq
    │   └── pid_map_content.json
    ├── insurance
    │   ├── 1.pdf
    │   ├── 2.pdf
    │   └── ...
    └── finance
        ├── 0.pdf
        ├── 1.pdf
        └── ...
```
### First run the following command to get pred_retrieve.json
```
python bm25_retrieve.py --question_path dataset\preliminary\questions_example.json --source_path reference --output_path pred_retrieve.json
```
### run the following command to get baseline Precision@1 
```
python evaluate_bm25.py
```
# BM25
```
Performance Metrics:

1. FAQ Domain:
   - Precision@1: 0.9
   - Matched: 45 out of 50

2. Finance Domain:
   - Precision@1: 0.44
   - Matched: 22 out of 50

3. Insurance Domain:
   - Precision@1: 0.8
   - Matched: 40 out of 50

Overall Average:
- Averaged Precision@1: 0.7133333333333334
```
### embeddings
```
Performance Metrics:

1. FAQ Domain:
   - Precision@1: 0.96
   - Matched: 48 out of 50

2. Finance Domain:
   - Precision@1: 0.54
   - Matched: 27 out of 50

3. Insurance Domain:
   - Precision@1: 0.88
   - Matched: 44 out of 50

Overall Average:
- Averaged Precision@1: 0.7933333
```
### embeddings:multilingual-e5-large
### reranker:jina-reranker-v2-base-multilingual
```
Performance Metrics:

1. FAQ Domain:
   - Precision@1: 0.94
   - Matched: 47 out of 50

2. Finance Domain:
   - Precision@1: 0.42
   - Matched: 21 out of 50

3. Insurance Domain:
   - Precision@1: 0.98
   - Matched: 49 out of 50

Overall Average:
- Averaged Precision@1: 0.78
```
加了reranker之後 目前只需要改善finance的performance
目前想到利用LLM對table做summary summary拿來轉成embeddings
其餘還有什麼方法?
