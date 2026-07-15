sentences = [
    ("배송이 빠르고 좋아요", 1),
    ("환불이 늦고 불편해요", 0),
    ("상품이 정말 좋아요", 1),
]
weights = {"좋아요": 2, "빠르고": 1, "늦고": -1, "불편해요": -2}

for sentence, label in sentences:
    print("문장:", sentence, "정답:", label)

results = []
for sentence, label in sentences:
    score = 0
    for word in sentence.split():
        score += weights.get(word, 0)
    prediction = 1 if score > 0 else 0
    results.append((sentence, label, score, prediction))

for sentence, label, score, prediction in results:
    print(sentence, "점수:", score, "예측:", prediction, "정답:", label)
