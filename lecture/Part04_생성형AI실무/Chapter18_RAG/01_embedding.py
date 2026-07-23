import math


####################################################
# 18.1 Embedding: 코사인 유사도
####################################################
query = [1.0, 0.0]
documents = {"배송 문서": [0.8, 0.6], "환불 문서": [0.1, 0.9]}


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


for name, vector in documents.items():
    print(name, f"유사도={cosine(query, vector):.3f}")
