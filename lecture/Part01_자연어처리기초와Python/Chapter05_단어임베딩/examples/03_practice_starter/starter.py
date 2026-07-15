# Chapter 5 단어 임베딩 Practice Starter

import math

vectors = {
    "배송": [0.9, 0.1],
    "택배": [0.8, 0.2],
    "환불": [0.1, 0.9],
    "반품": [0.2, 0.8],
}

print("입력을 먼저 확인하세요.")
for word, vector in vectors.items():
    print(word, vector)

# TODO 1: Basic Practice를 참고해 핵심 처리를 작성하세요.
# TODO 2: 처리 결과를 출력하세요.
# TODO 3: 아래 도전 과제를 하나 수행하세요.
# 새 단어와 2차원 벡터를 추가하고 가장 비슷한 단어를 찾으세요.
