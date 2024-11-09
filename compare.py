import json
with open('predictions.json','rb') as f:
    predictions = json.load(f)
with open('dataset\preliminary\ground_truths_example.json','rb') as f:
    ground_truths = json.load(f)['ground_truths']
ground_truths=[gt for gt in ground_truths if gt['category']=='insurance']
match=0
for i in range(len(predictions)):
    if int(predictions[i]['retrieve'])==ground_truths[i]['retrieve']:
        match+=1
    else:
        print(predictions[i]['qid'])
print(match/len(predictions))
print(match)