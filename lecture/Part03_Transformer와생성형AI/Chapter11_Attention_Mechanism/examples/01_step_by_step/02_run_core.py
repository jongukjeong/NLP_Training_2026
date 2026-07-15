import math

tokens = ["배송", "정말", "빨라요"]
scores = [1.0, 0.5, 2.0]

for token, score in zip(tokens, scores):
    print(token, "유사도:", score)

exp_scores = [math.exp(score) for score in scores]
total = sum(exp_scores)
weights = [value / total for value in exp_scores]

print('핵심 처리 완료')
