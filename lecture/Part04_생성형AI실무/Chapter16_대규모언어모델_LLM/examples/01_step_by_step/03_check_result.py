models = [
    {"name": "small", "memory_gb": 4, "tokens_per_second": 35},
    {"name": "medium", "memory_gb": 10, "tokens_per_second": 18},
    {"name": "large", "memory_gb": 24, "tokens_per_second": 8},
]
available_memory = 12

print("사용 가능 메모리:", available_memory, "GB")
for model in models:
    print(model)

runnable = []
for model in models:
    if model["memory_gb"] <= available_memory:
        runnable.append(model)

for model in runnable:
    seconds = 100 / model["tokens_per_second"]
    print(model["name"], "실행 가능, 100토큰 예상", round(seconds, 1), "초")
