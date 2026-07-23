import math


####################################################
# 11.4 Self-Attention: 같은 문장의 모든 토큰 관계 계산
####################################################
vectors = [[1.0, 0.0], [0.8, 0.2], [0.0, 1.0]]
scale = math.sqrt(len(vectors[0]))
matrix = [
    [sum(a * b for a, b in zip(query, key)) / scale for key in vectors]
    for query in vectors
]

print("=== Self-Attention score matrix ===")
for row in matrix:
    print([round(value, 3) for value in row])
print("shape:", (len(matrix), len(matrix[0])))
