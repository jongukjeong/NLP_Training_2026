prompts = [
    "배송 지연 안내문을 써줘",
    "고객에게 정중한 말투로 배송 지연 안내문을 3문장으로 써줘",
]
required_words = ["고객", "정중", "3문장"]

for number, prompt in enumerate(prompts, 1):
    print(number, prompt)

scores = []
for prompt in prompts:
    score = 0
    for word in required_words:
        if word in prompt:
            score += 1
    scores.append(score)

print('핵심 처리 완료')
