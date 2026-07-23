####################################################
# 12.1 Transformer Architecture: 잔차 연결 흐름
####################################################
token_vector = [0.2, -0.1, 0.7]
attention_output = [0.4, 0.3, -0.2]
after_attention = [
    original + update
    for original, update in zip(token_vector, attention_output)
]
ffn_output = [max(0.0, value * 1.5) for value in after_attention]

print("입력:", token_vector)
print("Attention + Residual:", after_attention)
print("FFN:", ffn_output)
