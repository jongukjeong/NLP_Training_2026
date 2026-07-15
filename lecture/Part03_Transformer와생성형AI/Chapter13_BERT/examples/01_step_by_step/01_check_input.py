sentence = "배송이 [MASK] 도착했어요"
vocabulary = {"빨리": 0.7, "늦게": 0.2, "안전하게": 0.1}

tokens = sentence.split()
print("토큰:", tokens)
print("MASK 위치:", tokens.index("[MASK]"))
