####################################################
# 13.4 Fine-tuning: 사전학습 표현에 작은 분류 헤드 적용
####################################################
representations = [[0.8, 0.2], [0.1, 0.9]]
weights = [1.2, -1.0]
bias = 0.0

print("=== 분류 Head ===")
for vector in representations:
    logit = sum(v * w for v, w in zip(vector, weights)) + bias
    prediction = int(logit >= 0)
    print(f"표현={vector}, logit={logit:.3f}, 분류={prediction}")
print("실제 Fine-tuning은 Encoder와 분류 Head의 가중치를 함께 조정합니다.")
