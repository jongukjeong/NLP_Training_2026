####################################################
# 12.4 FFN: 각 토큰에 같은 작은 신경망 적용
####################################################
tokens = [[0.2, -0.1], [0.8, 0.4], [-0.3, 0.7]]


def ffn(vector):
    hidden = [max(0.0, 2 * vector[0]), max(0.0, -vector[1] + 0.5)]
    return [hidden[0] + hidden[1], hidden[0] - hidden[1]]


print("=== Position-wise FFN ===")
for index, token in enumerate(tokens, 1):
    print(f"토큰 {index}: {token} -> {ffn(token)}")
