####################################################
# 16.4 Gemma 계열: 모델 크기와 하드웨어 예산 비교
####################################################
models = [
    {"name": "small", "memory": 4.5, "quality": 0.76},
    {"name": "medium", "memory": 9.0, "quality": 0.83},
    {"name": "large", "memory": 18.0, "quality": 0.86},
]
available_memory = 12

runnable = [model for model in models if model["memory"] <= available_memory]
best = max(runnable, key=lambda model: model["quality"])
print("실행 가능:", [model["name"] for model in runnable])
print("예산 내 최고 평가 모델:", best)
