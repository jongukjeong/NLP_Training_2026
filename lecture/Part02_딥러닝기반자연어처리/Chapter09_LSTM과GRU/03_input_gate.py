####################################################
# 9.3 Input Gate: 새 정보를 얼마나 기록할까?
####################################################
previous_cell = 0.6
candidate = -0.5

print("=== Input Gate 비교 ===")
for input_gate in [0.0, 0.3, 1.0]:
    new_information = input_gate * candidate
    updated_cell = previous_cell + new_information
    print(
        f"gate={input_gate:.1f}, 새 정보={new_information:.2f}, "
        f"갱신 기억={updated_cell:.2f}"
    )
