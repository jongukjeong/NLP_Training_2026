import math

vectors = {
    "배송": [0.9, 0.1],
    "택배": [0.8, 0.2],
    "환불": [0.1, 0.9],
    "반품": [0.2, 0.8],
}

for word, vector in vectors.items():
    print(word, vector)
