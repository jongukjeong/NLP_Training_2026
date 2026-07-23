####################################################
# 13.3 NSP: 두 문장의 연결 여부를 분류
####################################################
pairs = [
    ("상품을 주문했습니다.", "다음 날 배송되었습니다.", 1),
    ("상품을 주문했습니다.", "오늘 날씨가 맑습니다.", 0),
]
shared = {"상품", "배송", "주문"}

print("=== 문장 쌍 분류 예 ===")
for first, second, answer in pairs:
    overlap = any(word in first and word in second for word in shared)
    prediction = int(overlap or ("주문" in first and "배송" in second))
    print(first, "/", second)
    print("예측/정답:", prediction, "/", answer)
