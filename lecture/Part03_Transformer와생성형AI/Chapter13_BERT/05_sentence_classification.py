####################################################
# 13.5 Sentence Classification: 확률, 임계값, 오류 확인
####################################################
results = [
    ("배송이 빨라요", 0.91, 1),
    ("제품은 좋지만 비싸요", 0.56, 0),
    ("환불이 너무 느려요", 0.12, 0),
]
threshold = 0.6

print("=== 문장 분류 ===")
correct = 0
for text, probability, answer in results:
    prediction = int(probability >= threshold)
    correct += prediction == answer
    print(f"{text}: 확률={probability:.2f}, 예측={prediction}, 정답={answer}")
print("정확도:", correct / len(results))
