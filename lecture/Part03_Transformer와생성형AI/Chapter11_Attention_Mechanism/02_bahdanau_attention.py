import math


####################################################
# 11.2 Bahdanau Attention: 결합 후 비선형 점수 계산
####################################################
query = 0.7
keys = [0.1, 0.8, -0.3]
scores = [math.tanh(query + key) for key in keys]

print("=== Additive Attention ===")
for index, (key, score) in enumerate(zip(keys, scores), 1):
    print(f"key {index}: 값={key:.1f}, 점수={score:.4f}")
print("Query와 Key를 더한 뒤 학습 가능한 비선형 변환을 사용합니다.")
