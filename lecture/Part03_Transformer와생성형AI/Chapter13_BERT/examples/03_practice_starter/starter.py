# Chapter 13 BERT Practice Starter

sentence = "배송이 [MASK] 도착했어요"
vocabulary = {"빨리": 0.7, "늦게": 0.2, "안전하게": 0.1}

print("입력을 먼저 확인하세요.")
tokens = sentence.split()
print("토큰:", tokens)
print("MASK 위치:", tokens.index("[MASK]"))

# TODO 1: Basic Practice를 참고해 핵심 처리를 작성하세요.
# TODO 2: 처리 결과를 출력하세요.
# TODO 3: 아래 도전 과제를 하나 수행하세요.
# 후보 단어와 점수를 바꿔 MASK 결과를 비교하세요.
