documents = [
    "배송 조회는 주문 내역에서 확인할 수 있습니다.",
    "환불은 상품 수령 후 7일 이내 신청할 수 있습니다.",
    "비밀번호는 계정 설정에서 변경할 수 있습니다.",
]
question = "환불은 며칠 안에 신청하나요?"

print("질문:", question)
for number, document in enumerate(documents, 1):
    print(number, document)
