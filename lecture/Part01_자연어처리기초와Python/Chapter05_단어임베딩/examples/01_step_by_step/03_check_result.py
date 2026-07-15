import math

vectors = {
    "배송": [0.9, 0.1],
    "택배": [0.8, 0.2],
    "환불": [0.1, 0.9],
    "반품": [0.2, 0.8],
}

for word, vector in vectors.items():
    print(word, vector)

def cosine(a, b):
    dot = a[0] * b[0] + a[1] * b[1]
    length_a = math.sqrt(a[0] ** 2 + a[1] ** 2)
    length_b = math.sqrt(b[0] ** 2 + b[1] ** 2)
    return dot / (length_a * length_b)

target = "배송"
for word in vectors:
    if word != target:
        score = cosine(vectors[target], vectors[word])
        print(target, "↔", word, round(score, 3))
