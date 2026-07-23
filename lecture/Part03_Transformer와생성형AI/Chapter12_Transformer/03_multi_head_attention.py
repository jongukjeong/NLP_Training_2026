####################################################
# 12.3 Multi-Head Attention: 표현 차원을 여러 관점으로 분할
####################################################
batch, tokens, model_dimension, heads = 2, 5, 8, 2
assert model_dimension % heads == 0
head_dimension = model_dimension // heads

print("입력 shape:", (batch, tokens, model_dimension))
print("Head 분할 shape:", (batch, heads, tokens, head_dimension))
print("Attention 행렬 shape:", (batch, heads, tokens, tokens))
print("결합 출력 shape:", (batch, tokens, model_dimension))
