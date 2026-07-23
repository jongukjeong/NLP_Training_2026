####################################################
# 9.2 Forget Gate: 이전 기억을 얼마나 남길까?
####################################################
previous_cell = [0.8, -0.4, 0.2]

print("=== Forget Gate 비교 ===")
for gate in [0.1, 0.5, 0.9]:
    retained = [gate * value for value in previous_cell]
    print(f"gate={gate:.1f} -> 유지된 기억={retained}")

print("gate가 0에 가까우면 지우고, 1에 가까우면 유지합니다.")
