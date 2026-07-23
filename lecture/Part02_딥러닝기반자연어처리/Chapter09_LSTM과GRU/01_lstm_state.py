import math


####################################################
# 9.1 LSTM: hidden state와 cell state
####################################################
sigmoid = lambda x: 1 / (1 + math.exp(-x))
inputs = [0.3, -0.2, 0.8]
hidden, cell = 0.0, 0.0

print("=== LSTM 상태 흐름 ===")
for step, value in enumerate(inputs, 1):
    forget = sigmoid(value + hidden)
    candidate = math.tanh(value)
    cell = forget * cell + (1 - forget) * candidate
    hidden = math.tanh(cell)
    print(f"{step}단계: cell={cell:.4f}, hidden={hidden:.4f}")

print("cell state는 장기 기억, hidden state는 현재 출력 역할을 합니다.")
