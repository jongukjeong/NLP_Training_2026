####################################################
# 17장 연결 예제: 정확도와 형식 준수율 분리 평가
####################################################
outputs = [
    {"parsed": True, "prediction": "배송", "answer": "배송"},
    {"parsed": True, "prediction": "기타", "answer": "환불"},
    {"parsed": False, "prediction": None, "answer": "계정"},
]
total = len(outputs)
parsed = sum(row["parsed"] for row in outputs)
correct = sum(
    row["parsed"] and row["prediction"] == row["answer"]
    for row in outputs
)

print("정확도:", f"{correct / total:.1%}")
print("형식 준수율:", f"{parsed / total:.1%}")
