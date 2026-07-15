tokens = ["배송", "정말", "빨라요"]
token_values = {"배송": 0.2, "정말": 0.5, "빨라요": 0.9}

for position, token in enumerate(tokens, 1):
    print(position, token, token_values[token])
