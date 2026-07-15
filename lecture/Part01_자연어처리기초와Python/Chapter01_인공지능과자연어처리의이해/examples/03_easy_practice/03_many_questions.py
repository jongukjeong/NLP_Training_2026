questions = [
    "배송이 아직 안 왔어요.",
    "상품을 환불하고 싶어요.",
    "상담원과 통화하고 싶어요.",
]

for question in questions:
    if "환불" in question:
        intent = "환불 문의"
    elif "배송" in question:
        intent = "배송 문의"
    else:
        intent = "기타 문의"

    print(question, "→", intent)
