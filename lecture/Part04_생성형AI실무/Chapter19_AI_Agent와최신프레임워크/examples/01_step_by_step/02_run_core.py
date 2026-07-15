questions = [
    "주문 상태를 알려줘",
    "환불 규정을 알려줘",
    "내 비밀번호를 대신 바꿔줘",
]

for question in questions:
    print("질문:", question)

decisions = []
for question in questions:
    if "주문" in question:
        tool = "order_lookup"
    elif "규정" in question:
        tool = "faq_search"
    else:
        tool = "safe_stop"
    decisions.append((question, tool))

print('핵심 처리 완료')
