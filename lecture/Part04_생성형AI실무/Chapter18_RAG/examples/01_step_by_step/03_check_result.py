documents = [
    "배송 조회는 주문 내역에서 확인할 수 있습니다.",
    "환불은 상품 수령 후 7일 이내 신청할 수 있습니다.",
    "비밀번호는 계정 설정에서 변경할 수 있습니다.",
]
question = "환불은 며칠 안에 신청하나요?"

print("질문:", question)
for number, document in enumerate(documents, 1):
    print(number, document)

question_words = set(question.replace("?", "").split())
scores = []
for document in documents:
    document_words = set(document.replace(".", "").split())
    scores.append(len(question_words & document_words))
best_index = scores.index(max(scores))

print("검색 점수:", scores)
print("선택 근거:", documents[best_index])
print("답변: 선택된 근거를 확인해 답변합니다.")
