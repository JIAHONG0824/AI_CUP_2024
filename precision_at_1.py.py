import json
pred=[]
precision=[]
with open("dataset/preliminary/pred_retrieve.json", "r") as f:
    pred = json.load(f)["answers"]
with open("dataset/preliminary/ground_truths_example.json","r") as f:
    ground_truth=json.load(f)["ground_truths"]

for i in range(len(pred)):
    if pred[i]["retrieve"]==ground_truth[i]["retrieve"]:
        precision.append(1)
    else:
        precision.append(0)
result=sum(precision)/len(precision)
print("Average Precision@1: ",result)