import json

with open("dataset/preliminary/pred_retrieve_baseline.json", "rb") as f:
    predictions = json.load(f)["answers"]
with open("dataset/preliminary/ground_truths_example.json", "rb") as f:
    ground_truths = json.load(f)["ground_truths"]
match = 0
for i in range(len(predictions)):
    if predictions[i]["retrieve"] == ground_truths[i]["retrieve"]:
        match += 1
print("Precision@1: ", match / len(predictions))
