# Chapter 11 Attention Practice Starter

import math

tokens = ["배송", "정말", "빨라요"]
scores = [1.0, 0.5, 2.0]

print("입력을 먼저 확인하세요.")
for token, score in zip(tokens, scores):
    print(token, "유사도:", score)

# TODO 1: Basic Practice를 참고해 핵심 처리를 작성하세요.
# TODO 2: 처리 결과를 출력하세요.
# TODO 3: 아래 도전 과제를 하나 수행하세요.
# scores 중 하나를 크게 바꾸고 Attention이 어디에 집중하는지 확인하세요.
