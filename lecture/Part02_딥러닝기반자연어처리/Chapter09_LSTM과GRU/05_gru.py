####################################################
# 9.5 GRU: update gate로 이전 상태와 후보 상태 결합
####################################################
previous_hidden = 0.7
candidate_hidden = -0.2

print("=== GRU Update Gate ===")
for update_gate in [0.1, 0.5, 0.9]:
    hidden = (
        update_gate * previous_hidden
        + (1 - update_gate) * candidate_hidden
    )
    print(f"update={update_gate:.1f} -> hidden={hidden:.3f}")

print("GRU는 별도의 cell state 없이 hidden state 하나를 갱신합니다.")
