####################################################
# 16.1 LLM: 파라미터 수와 가중치 메모리 추정
####################################################
parameters_billions = 8

print("=== 8B 모델의 이론상 가중치 메모리 ===")
for bits in [32, 16, 8, 4]:
    memory_gb = parameters_billions * bits / 8
    print(f"{bits:2d}-bit: 약 {memory_gb:.1f} GB")
print("실행에는 KV cache와 runtime buffer가 추가로 필요합니다.")
