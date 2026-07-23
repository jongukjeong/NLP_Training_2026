####################################################
# 11.3 Luong Attention: Query와 Key의 내적
####################################################
query = [0.5, 1.0]
keys = [[1.0, 0.0], [0.2, 0.9], [-0.5, 0.1]]

scores = [
    sum(q * k for q, k in zip(query, key))
    for key in keys
]

print("=== Dot-product Attention ===")
for index, (key, score) in enumerate(zip(keys, scores), 1):
    print(f"key {index}: {key}, 내적={score:.3f}")
print("가장 큰 점수의 위치:", scores.index(max(scores)) + 1)
