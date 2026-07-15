import math

tokens = ["배송", "정말", "빨라요"]
scores = [1.0, 0.5, 2.0]

for token, score in zip(tokens, scores):
    print(token, "유사도:", score)
