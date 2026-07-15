# Chapter 16 대규모 언어모델 Practice Starter

models = [
    {"name": "small", "memory_gb": 4, "tokens_per_second": 35},
    {"name": "medium", "memory_gb": 10, "tokens_per_second": 18},
    {"name": "large", "memory_gb": 24, "tokens_per_second": 8},
]
available_memory = 12

print("입력을 먼저 확인하세요.")
print("사용 가능 메모리:", available_memory, "GB")
for model in models:
    print(model)

# TODO 1: Basic Practice를 참고해 핵심 처리를 작성하세요.
# TODO 2: 처리 결과를 출력하세요.
# TODO 3: 아래 도전 과제를 하나 수행하세요.
# 메모리 값을 바꾸고 실행 가능한 모델과 속도의 trade-off를 설명하세요.
