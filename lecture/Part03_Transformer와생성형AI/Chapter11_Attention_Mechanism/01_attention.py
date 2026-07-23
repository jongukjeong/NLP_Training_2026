import math


####################################################
# 11.1 Attention: 중요한 입력에 더 큰 가중치 부여
####################################################
tokens = ["그", "제품은", "좋다"]
scores = [0.2, 0.5, 1.4]
exp_scores = [math.exp(score) for score in scores]
weights = [value / sum(exp_scores) for value in exp_scores]

print("=== Attention 가중치 ===")
for token, score, weight in zip(tokens, scores, weights):
    print(f"{token:4s} score={score:.1f}, weight={weight:.3f}")
print("가중치 합:", round(sum(weights), 6))
