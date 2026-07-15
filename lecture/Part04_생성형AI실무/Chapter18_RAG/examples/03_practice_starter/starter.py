# Chapter 18 RAG Practice Starter

documents = [
    "배송 조회는 주문 내역에서 확인할 수 있습니다.",
    "환불은 상품 수령 후 7일 이내 신청할 수 있습니다.",
    "비밀번호는 계정 설정에서 변경할 수 있습니다.",
]
question = "환불은 며칠 안에 신청하나요?"

print("입력을 먼저 확인하세요.")
print("질문:", question)
for number, document in enumerate(documents, 1):
    print(number, document)

# TODO 1: Basic Practice를 참고해 핵심 처리를 작성하세요.
# TODO 2: 처리 결과를 출력하세요.
# TODO 3: 아래 도전 과제를 하나 수행하세요.
# 질문과 문서를 추가하고 검색 결과가 틀리는 사례를 하나 찾으세요.
