####################################################
# 9장 연결 예제: 기억을 이용한 간단한 감성 분류
####################################################
sentences = [
    ("배송이 느리지만 제품은 정말 좋아요", 1),
    ("제품은 좋지만 배송이 너무 느려요", 0),
]
scores = {"느리지만": -1.0, "좋지만": 0.8, "좋아요": 1.0, "느려요": -1.0}
forget_gate = 0.6

print("=== 순서를 반영한 감성 분류 ===")
for sentence, answer in sentences:
    memory = 0.0
    for token in sentence.split():
        memory = forget_gate * memory + scores.get(token, 0.0)
    prediction = int(memory >= 0)
    print(f"{sentence}\n  기억={memory:.3f}, 예측={prediction}, 정답={answer}")
