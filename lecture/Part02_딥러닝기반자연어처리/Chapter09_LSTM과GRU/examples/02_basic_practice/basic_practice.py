# Chapter 9 LSTM과 GRU Basic Practice

values = [0.2, 0.9, -0.4, 0.8]
forget_gate = 0.8
input_gate = 0.6

print("=== 입력 확인 ===")
print("문장 값:", values)
print("기억 유지 비율:", forget_gate)

print("\n=== 핵심 처리 ===")
memory = 0.0
memory_history = []
for value in values:
    memory = forget_gate * memory + input_gate * value
    memory_history.append(memory)

print("\n=== 결과 확인 ===")
for step, memory in enumerate(memory_history, 1):
    print(step, "번째 기억:", round(memory, 3))
