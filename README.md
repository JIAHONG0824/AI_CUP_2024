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
python evaluate.py
```
### Baseline Precision@1: 0.7133333333333334
