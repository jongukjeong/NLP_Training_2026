####################################################
# 15.5 Fine-tuning: Dataset -> Tokenize -> Batch -> Train
####################################################
records = [
    {"text": "배송이 빨라요", "label": 1},
    {"text": "환불이 느려요", "label": 0},
]
vocabulary = {"배송이": 1, "빨라요": 2, "환불이": 3, "느려요": 4}

batch = {
    "input_ids": [[vocabulary[word] for word in row["text"].split()] for row in records],
    "labels": [row["label"] for row in records],
}
print("학습 Batch:", batch)
print("batch size:", len(batch["labels"]))
