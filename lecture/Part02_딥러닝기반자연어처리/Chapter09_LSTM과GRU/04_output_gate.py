import math


####################################################
# 9.4 Output Gate: 기억 중 무엇을 밖으로 보낼까?
####################################################
cell_state = 1.2
activated_cell = math.tanh(cell_state)

print("=== Output Gate 비교 ===")
for output_gate in [0.1, 0.5, 0.9]:
    hidden_state = output_gate * activated_cell
    print(f"gate={output_gate:.1f} -> hidden={hidden_state:.4f}")

print("cell state는 그대로 있어도 output gate에 따라 출력은 달라집니다.")
