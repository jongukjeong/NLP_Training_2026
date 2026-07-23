####################################################
# 10.2 Encoder: 입력 시퀀스를 문맥 상태로 요약
####################################################
token_values = {"나는": 0.2, "학생": 0.7, "입니다": 0.4}
source = ["나는", "학생", "입니다"]
state = 0.0

print("=== Encoder 상태 ===")
for token in source:
    state = 0.5 * state + token_values[token]
    print(f"{token:4s} -> state={state:.3f}")

context_vector = state
print("최종 context vector:", round(context_vector, 3))
