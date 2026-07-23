####################################################
# 14.5 ChatGPT 이해: 역할별 메시지와 대화 문맥
####################################################
messages = [
    {"role": "system", "content": "근거가 없으면 모른다고 답하세요."},
    {"role": "user", "content": "배송 상태를 알려주세요."},
    {"role": "assistant", "content": "주문 번호를 알려주세요."},
    {"role": "user", "content": "A-102입니다."},
]

print("=== 대화 메시지 ===")
for message in messages:
    print(f"[{message['role']}] {message['content']}")
print("메시지 수:", len(messages))
