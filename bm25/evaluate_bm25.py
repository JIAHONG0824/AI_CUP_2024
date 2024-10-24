import json

with open("dataset/preliminary/ground_truths_example.json", "rb") as f:
    ground_truths = json.load(f)["ground_truths"]
with open("bm25/pred_retrieve.json", "rb") as f:
    answers = json.load(f)["answers"]
insurance_match = 0
finance_match = 0
faq_match = 0
for i in range(len(answers)):
    if answers[i]["retrieve"] == ground_truths[i]["retrieve"]:
        if ground_truths[i]["category"] == "insurance":
            insurance_match += 1
        elif ground_truths[i]["category"] == "finance":
            finance_match += 1
        else:
            faq_match += 1
print(
    f"""
Performance Metrics:

1. FAQ Domain:
   - Precision@1: {faq_match/50}
   - Matched: {faq_match} out of 50

2. Finance Domain:
   - Precision@1: {finance_match/50}
   - Matched: {finance_match} out of 50

3. Insurance Domain:
   - Precision@1: {insurance_match/50}
   - Matched: {insurance_match} out of 50

Overall Average:
- Averaged Precision@1: {(faq_match+finance_match+insurance_match)/150}
"""
)
