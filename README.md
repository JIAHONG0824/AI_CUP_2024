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
temp
faq改用embeddings方法\
precision 0.96\
match 48/50\
問題數過少 不曉得提升幅度多大\
另外insurance和finance兩種\
performance出奇地差 幾乎找不到\
特別需要改善
