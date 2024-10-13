import json
with open("pred.json", "rb") as f:
    pred = json.load(f)["answers"]
print(pred[0])
with open("dataset/preliminary/ground_truths_example.json","rb") as f:
    ground_truths = json.load(f)["ground_truths"]
ground_truths= [g for g in ground_truths if g["category"] == "faq"]
print(ground_truths[0])
match=0
for i in range(len(pred)):
    if pred[i]["retrieve"] == ground_truths[i]["retrieve"]:
        match+=1
print(match/len(pred))
print(match)
