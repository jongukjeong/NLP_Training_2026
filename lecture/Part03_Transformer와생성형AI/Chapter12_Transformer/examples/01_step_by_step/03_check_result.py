token_vector = [0.2, 0.7, -0.1]
attention_output = [0.4, -0.2, 0.3]

print("입력 벡터:", token_vector)
print("Attention 출력:", attention_output)

residual = []
for original, attention in zip(token_vector, attention_output):
    residual.append(original + attention)

activated = [max(0, value) for value in residual]

print("잔차 연결 후:", residual)
print("활성화 후:", activated)
print("shape:", len(activated))
