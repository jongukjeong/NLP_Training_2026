knowledge = {
    "배송": "배송 조회는 주문 내역에서 확인할 수 있습니다.",
    "환불": "환불은 상품 수령 후 7일 이내 신청할 수 있습니다.",
    "계정": "비밀번호는 계정 설정에서 변경할 수 있습니다.",
}
questions = ["배송은 어디서 조회하나요?", "환불 기간은 며칠인가요?"]

print("지식 문서 수:", len(knowledge))
for question in questions:
    print("테스트 질문:", question)
