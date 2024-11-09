import argparse
import json


def Precision(index_name):
    with open("dataset/preliminary/ground_truths_example.json", "rb") as f:
        ground_truths = json.load(f)["ground_truths"]
    with open(f"predictions_{index_name}.json", "rb") as f:
        predictions = json.load(f)
    ground_truths = [gt for gt in ground_truths if gt["category"] == index_name]
    match = 0
    for i in range(len(predictions)):
        if int(predictions[i]["retrieve"]) == ground_truths[i]["retrieve"]:
            match += 1
    print(f"{index_name} Precision: {match/len(predictions)}")
    print(f"{index_name} hit: {match}/{len(ground_truths)}")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--index_name", type=str, help="faq or finance or insurance")
    args = argparser.parse_args()
    try:
        Precision(args.index_name)
    except Exception as e:
        print(e)
        print("index_name should be one of faq, finance, insurance")
