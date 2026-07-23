####################################################
# 12장 연결 예제: Encoder Block shape와 잔차 연결 검사
####################################################
tokens = [[0.2, 0.7], [-0.1, 0.4], [0.8, 0.3]]
attention = [[0.1, -0.2], [0.2, 0.1], [-0.3, 0.4]]
residual = [
    [a + b for a, b in zip(token, update)]
    for token, update in zip(tokens, attention)
]
output = [[max(0.0, value) for value in token] for token in residual]

print("입력 shape:", (len(tokens), len(tokens[0])))
print("잔차 연결:", residual)
print("Encoder 출력:", output)
assert len(output) == len(tokens) and len(output[0]) == len(tokens[0])
