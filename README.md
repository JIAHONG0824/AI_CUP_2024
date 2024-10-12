### First run the following command to get pred_retrieve_baseline.json
```
python bm25_retrieve.py --question_path dataset\preliminary\questions_example.json --source_path reference --output_path dataset\preliminary\pred_retrieve_baseline.json
```

### Folder structure
```
├── dataset
│   ├── preliminary
│   │   └── questions_example.json
│   │   └── ground_truths_example.json
│   │   └── pred_retrieve_baseline.json
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

### run the following command to get baseline Precision@1 
```
python evaluate_bm25.py
```
```
Precision@1 for faq:  0.9
Precision@1 for finance:  0.44
Precision@1 for insurance:  0.8
Average Precision@1:  0.7133333333333334
```
