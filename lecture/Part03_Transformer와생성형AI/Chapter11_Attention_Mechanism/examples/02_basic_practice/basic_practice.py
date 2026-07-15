# Chapter 11 Attention Basic Practice

import math

tokens = ["배송", "정말", "빨라요"]
scores = [1.0, 0.5, 2.0]

print("=== 입력 확인 ===")
for token, score in zip(tokens, scores):
    print(token, "유사도:", score)

print("\n=== 핵심 처리 ===")
exp_scores = [math.exp(score) for score in scores]
total = sum(exp_scores)
weights = [value / total for value in exp_scores]

print("\n=== 결과 확인 ===")
for token, weight in zip(tokens, weights):
    print(token, "Attention:", round(weight, 3))
print("가중치 합:", round(sum(weights), 3))
