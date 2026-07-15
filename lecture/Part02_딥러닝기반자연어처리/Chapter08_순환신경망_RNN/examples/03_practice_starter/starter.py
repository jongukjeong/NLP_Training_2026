# Chapter 8 순환신경망 RNN Practice Starter

tokens = ["배송", "정말", "빨라요"]
token_values = {"배송": 0.2, "정말": 0.5, "빨라요": 0.9}

print("입력을 먼저 확인하세요.")
for position, token in enumerate(tokens, 1):
    print(position, token, token_values[token])

# TODO 1: Basic Practice를 참고해 핵심 처리를 작성하세요.
# TODO 2: 처리 결과를 출력하세요.
# TODO 3: 아래 도전 과제를 하나 수행하세요.
# 토큰 순서를 바꾸고 최종 hidden state가 달라지는지 확인하세요.
