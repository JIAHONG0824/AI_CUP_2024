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
#embeddings
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
- Averaged Precision@1: 0.7133333333333334
```
