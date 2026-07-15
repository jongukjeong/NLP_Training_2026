prompt = "고객에게 배송 지연을"
next_tokens = {"안내합니다": 0.55, "사과합니다": 0.35, "무시합니다": 0.10}

print("Prompt:", prompt)
print("다음 토큰 후보:", next_tokens)

selected = ""
highest = -1.0
for token, probability in next_tokens.items():
    if probability > highest:
        selected = token
        highest = probability

print("선택 토큰:", selected)
print("생성 결과:", prompt, selected)
