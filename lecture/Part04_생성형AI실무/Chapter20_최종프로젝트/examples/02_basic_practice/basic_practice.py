# Chapter 20 최종 프로젝트 Basic Practice

knowledge = {
    "배송": "배송 조회는 주문 내역에서 확인할 수 있습니다.",
    "환불": "환불은 상품 수령 후 7일 이내 신청할 수 있습니다.",
    "계정": "비밀번호는 계정 설정에서 변경할 수 있습니다.",
}
questions = ["배송은 어디서 조회하나요?", "환불 기간은 며칠인가요?"]

print("=== 입력 확인 ===")
print("지식 문서 수:", len(knowledge))
for question in questions:
    print("테스트 질문:", question)

print("\n=== 핵심 처리 ===")
results = []
for question in questions:
    answer = "근거를 찾지 못했습니다."
    source = "없음"
    for keyword, document in knowledge.items():
        if keyword in question:
            answer = document
            source = keyword
            break
    results.append((question, answer, source))

print("\n=== 결과 확인 ===")
for question, answer, source in results:
    print("질문:", question)
    print("답변:", answer)
    print("근거:", source)
    print()
