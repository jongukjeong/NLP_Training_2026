####################################################
# 13장 연결 예제: Tokenize -> Encoder -> Classifier
####################################################
vocabulary = {"[CLS]": 1, "[SEP]": 2, "배송이": 3, "빨라요": 4}
sentence = "배송이 빨라요"
tokens = ["[CLS]"] + sentence.split() + ["[SEP]"]
input_ids = [vocabulary.get(token, 0) for token in tokens]
cls_representation = sum(input_ids) / len(input_ids)
probability = min(1.0, cls_representation / 4)

print("tokens:", tokens)
print("input_ids:", input_ids)
print("[CLS] 기반 긍정 확률(교육용):", round(probability, 3))
