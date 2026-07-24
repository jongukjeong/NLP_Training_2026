import math


####################################################
# 9.5 GRU: update gate와 reset gate
####################################################
previous_hidden = 0.7
candidate_hidden = -0.2

print("=== 1. Update Gate: 이전 상태와 후보 상태 섞기 ===")
for update_gate in [0.1, 0.5, 0.9]:
    hidden = (
        update_gate * previous_hidden
        + (1 - update_gate) * candidate_hidden
    )
    print(f"update={update_gate:.1f} -> hidden={hidden:.3f}")

print("\nupdate가 클수록 새 hidden은 이전 hidden=0.7에 가까워집니다.")

print("\n=== 2. Reset Gate: 후보 상태 만들기 ===")
current_input = 0.3
for reset_gate in [0.0, 0.5, 1.0]:
    reset_previous = reset_gate * previous_hidden
    candidate = math.tanh(current_input + reset_previous)
    print(
        f"reset={reset_gate:.1f}, 이전 상태 반영={reset_previous:.3f} "
        f"-> candidate={candidate:.3f}"
    )

print("\nreset이 클수록 후보를 만들 때 이전 hidden을 더 많이 참고합니다.")
print("GRU는 별도의 cell state 없이 hidden state 하나를 갱신합니다.")
