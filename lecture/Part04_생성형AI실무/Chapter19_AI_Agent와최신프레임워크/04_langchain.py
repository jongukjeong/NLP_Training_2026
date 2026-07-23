####################################################
# 19.4 LangChain: 순서가 고정된 Chain
####################################################
documents = ["환불은 3일 이내 처리됩니다.", "배송은 2일 걸립니다."]
question = "환불 기간"

retrieved = [doc for doc in documents if "환불" in doc]
context = "\n".join(retrieved)
answer = context if context else "근거 없음"

print("질문:", question)
print("검색:", retrieved)
print("답변:", answer)
print("검색 -> 조합 -> 답변의 순서를 개발자가 고정한 Chain입니다.")
