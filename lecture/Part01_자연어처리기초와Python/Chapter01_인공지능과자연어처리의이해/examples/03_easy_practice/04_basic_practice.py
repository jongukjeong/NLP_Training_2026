questions = [
    "배송이 아직 안 왔어요.",
    "상품을 환불하고 싶어요.",
    "상담원과 통화하고 싶어요.",
]

for question in questions:
    if "환불" in question:
        intent = "환불 문의"
        answer = "환불 접수 방법을 안내해 드릴게요."
    elif "배송" in question:
        intent = "배송 문의"
        answer = "배송 조회 방법을 안내해 드릴게요."
    else:
        intent = "기타 문의"
        answer = "상담원에게 문의를 전달할게요."

    print("질문:", question)
    print("분류:", intent)
    print("답변:", answer)
    print()
