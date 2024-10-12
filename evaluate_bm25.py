import json
import os
with open("dataset/preliminary/pred_retrieve_baseline.json", "r") as f:
    predictions = json.load(f)["answers"]
with open("dataset/preliminary/ground_truths_example.json", "r") as f:
    ground_truths = json.load(f)["ground_truths"]
finance = []
insurance = []
faq = []
for i in range(len(ground_truths)):
    if ground_truths[i]["category"] == "finance":
        finance.append(
            {
                "qid": ground_truths[i]["qid"],
                "retrieve": predictions[i]["retrieve"],
                "ground_truths": ground_truths[i]["retrieve"],
                "category": ground_truths[i]["category"],
            }
        )
    elif ground_truths[i]["category"] == "insurance":
        insurance.append(
            {
                "qid": ground_truths[i]["qid"],
                "retrieve": predictions[i]["retrieve"],
                "ground_truths": ground_truths[i]["retrieve"],
                "category": ground_truths[i]["category"],
            }
        )
    elif ground_truths[i]["category"] == "faq":
        faq.append(
            {
                "qid": ground_truths[i]["qid"],
                "retrieve": predictions[i]["retrieve"],
                "ground_truths": ground_truths[i]["retrieve"],
                "category": ground_truths[i]["category"],
            }
        )
if not os.path.exists("baseline"):
    os.makedirs("baseline")
with open("baseline/finance.json", "w") as f:
    json.dump(finance, f, ensure_ascii=False, indent=4)
with open("baseline/insurance.json", "w") as f:
    json.dump(insurance, f, ensure_ascii=False, indent=4)
with open("baseline/faq.json", "w") as f:
    json.dump(faq, f, ensure_ascii=False, indent=4)
faq_match = 0
finance_match = 0
insurance_match = 0
for pred in faq:
    if pred["retrieve"] == pred["ground_truths"]:
        faq_match += 1
for pred in finance:
    if pred["retrieve"] == pred["ground_truths"]:
        finance_match += 1
for pred in insurance:
    if pred["retrieve"] == pred["ground_truths"]:
        insurance_match += 1
print("faq match: ", faq_match)
print("Precision@1 for faq: ", faq_match / len(faq))
print("finance match: ", finance_match)
print("Precision@1 for finance: ", finance_match / len(finance))
print("insurance match: ", insurance_match)
print("Precision@1 for insurance: ", insurance_match / len(insurance))
print(
    "Average Precision@1: ",
    (faq_match + finance_match + insurance_match) / len(ground_truths),
)