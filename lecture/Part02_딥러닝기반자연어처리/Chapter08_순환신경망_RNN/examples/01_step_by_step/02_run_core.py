tokens = ["배송", "정말", "빨라요"]
token_values = {"배송": 0.2, "정말": 0.5, "빨라요": 0.9}

for position, token in enumerate(tokens, 1):
    print(position, token, token_values[token])

hidden = 0.0
history = []
for token in tokens:
    hidden = 0.5 * hidden + token_values[token]
    history.append((token, hidden))

print('핵심 처리 완료')
