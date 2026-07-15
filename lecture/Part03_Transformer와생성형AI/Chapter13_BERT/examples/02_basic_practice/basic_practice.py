# Chapter 13 BERT Basic Practice

sentence = "배송이 [MASK] 도착했어요"
vocabulary = {"빨리": 0.7, "늦게": 0.2, "안전하게": 0.1}

print("=== 입력 확인 ===")
tokens = sentence.split()
print("토큰:", tokens)
print("MASK 위치:", tokens.index("[MASK]"))

print("\n=== 핵심 처리 ===")
best_word = ""
best_score = -1.0
for word, score in vocabulary.items():
    if score > best_score:
        best_word = word
        best_score = score

print("\n=== 결과 확인 ===")
completed = sentence.replace("[MASK]", best_word)
print("후보:", vocabulary)
print("선택:", best_word)
print("완성 문장:", completed)
