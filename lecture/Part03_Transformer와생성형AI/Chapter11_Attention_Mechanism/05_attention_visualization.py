####################################################
# 11장 연결 예제: Attention 행렬을 텍스트 막대로 시각화
####################################################
tokens = ["배송", "정말", "빠름"]
weights = [
    [0.7, 0.2, 0.1],
    [0.2, 0.6, 0.2],
    [0.1, 0.2, 0.7],
]

print("=== Attention Map ===")
print("      ", " ".join(f"{token:4s}" for token in tokens))
for token, row in zip(tokens, weights):
    bars = " ".join(f"{'█' * round(value * 5):4s}" for value in row)
    print(f"{token:4s}  {bars}")
    assert abs(sum(row) - 1.0) < 1e-9
