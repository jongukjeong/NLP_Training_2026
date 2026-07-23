####################################################
# 15장 연결 예제: Model Card 조건으로 모델 선택
####################################################
models = [
    {"name": "ko-small", "task": "sentiment", "language": "ko", "size": 100},
    {"name": "en-small", "task": "sentiment", "language": "en", "size": 90},
    {"name": "ko-large", "task": "sentiment", "language": "ko", "size": 800},
]
memory_limit = 500

selected = [
    model for model in models
    if model["task"] == "sentiment"
    and model["language"] == "ko"
    and model["size"] <= memory_limit
]
print("조건을 만족하는 모델:", selected)
