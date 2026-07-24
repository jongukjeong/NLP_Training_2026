import math


####################################################
# 9.1 LSTM: 세 gate와 두 state의 흐름
####################################################


def sigmoid(value):
    """임의의 실수를 0~1 사이의 gate 값으로 바꾼다."""
    return 1 / (1 + math.exp(-value))


inputs = [0.3, -0.2, 0.8]
hidden, cell = 0.0, 0.0

print("=== LSTM 상태 흐름 ===")
for step, value in enumerate(inputs, 1):
    previous_hidden = hidden
    previous_cell = cell

    # 실제 LSTM은 gate마다 별도의 가중치 행렬과 bias를 학습한다.
    # 여기서는 계산 흐름을 보기 위해 고정된 간단한 식을 사용한다.
    forget = sigmoid(value + previous_hidden + 1.0)
    input_gate = sigmoid(value - previous_hidden)
    candidate = math.tanh(value + previous_hidden)
    output_gate = sigmoid(value + previous_hidden)

    kept_memory = forget * previous_cell
    new_memory = input_gate * candidate
    cell = kept_memory + new_memory
    hidden = output_gate * math.tanh(cell)

    print(f"\n[{step}단계] 입력 x={value:+.2f}")
    print(
        f"  gate      : forget={forget:.4f}, "
        f"input={input_gate:.4f}, output={output_gate:.4f}"
    )
    print(
        f"  cell 계산 : {kept_memory:+.4f}(이전 기억) "
        f"{new_memory:+.4f}(새 기억) = {cell:+.4f}"
    )
    print(f"  hidden    : {hidden:+.4f}")

print("\ncell state는 오래 전달할 내부 기억, hidden state는 현재 출력 역할을 합니다.")
