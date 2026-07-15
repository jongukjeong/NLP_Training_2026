sentence = "배송이 [MASK] 도착했어요"
vocabulary = {"빨리": 0.7, "늦게": 0.2, "안전하게": 0.1}

tokens = sentence.split()
print("토큰:", tokens)
print("MASK 위치:", tokens.index("[MASK]"))

best_word = ""
best_score = -1.0
for word, score in vocabulary.items():
    if score > best_score:
        best_word = word
        best_score = score

print('핵심 처리 완료')
