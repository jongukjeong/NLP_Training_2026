####################################################
# 15.4 Pipeline: 입력과 표준화된 출력 연결
####################################################
lexicon = {"좋아요": 0.9, "빨라요": 0.8, "느려요": -0.8}
texts = ["배송이 빨라요", "배송이 느려요"]

print("=== 교육용 감성 Pipeline ===")
for text in texts:
    score = sum(value for word, value in lexicon.items() if word in text)
    result = {"label": "POSITIVE" if score >= 0 else "NEGATIVE", "score": abs(score)}
    print(text, "->", result)
