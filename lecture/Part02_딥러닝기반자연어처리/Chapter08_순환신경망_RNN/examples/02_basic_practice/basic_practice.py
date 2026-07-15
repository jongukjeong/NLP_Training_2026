# Chapter 8 순환신경망 RNN Basic Practice

tokens = ["배송", "정말", "빨라요"]
token_values = {"배송": 0.2, "정말": 0.5, "빨라요": 0.9}

print("=== 입력 확인 ===")
for position, token in enumerate(tokens, 1):
    print(position, token, token_values[token])

print("\n=== 핵심 처리 ===")
hidden = 0.0
history = []
for token in tokens:
    hidden = 0.5 * hidden + token_values[token]
    history.append((token, hidden))

print("\n=== 결과 확인 ===")
for token, hidden in history:
    print(token, "후 hidden state:", round(hidden, 3))
print("최종 상태:", round(hidden, 3))
