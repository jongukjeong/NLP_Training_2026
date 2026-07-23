import math


####################################################
# 14.4 Text Generation: Temperature에 따른 확률 변화
####################################################
logits = {"안내": 2.0, "사과": 1.4, "무시": 0.2}

for temperature in [0.5, 1.0, 2.0]:
    values = {token: math.exp(logit / temperature) for token, logit in logits.items()}
    total = sum(values.values())
    probabilities = {token: round(value / total, 3) for token, value in values.items()}
    print(f"temperature={temperature}: {probabilities}")
