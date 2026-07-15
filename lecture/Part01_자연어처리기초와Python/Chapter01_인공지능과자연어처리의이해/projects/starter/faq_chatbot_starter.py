print("간단한 FAQ 챗봇을 시작합니다.")

question = input("질문: ")

# 1. 환불 문의를 판별하는 조건을 작성하세요.
if "환불" in question:
    intent = "환불 문의"
    answer = "환불 접수 방법을 안내해 드릴게요."

# 2. 배송 문의를 판별하는 elif 조건을 작성하세요.
elif "배송" in question:
    intent = "배송 문의"
    answer = "배송 조회 방법을 안내해 드릴게요."

# 3. 어느 키워드도 없는 경우를 처리하세요.
else:
    intent = "기타 문의"
    answer = "상담원에게 문의를 전달할게요."

print("분류:", intent)
print("답변:", answer)

# 기본 기능이 실행되면 결제 또는 계정 문의를 하나 추가하세요.
