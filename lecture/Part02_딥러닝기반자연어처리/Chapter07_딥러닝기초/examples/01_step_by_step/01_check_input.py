sentences = [
    ("배송이 빠르고 좋아요", 1),
    ("환불이 늦고 불편해요", 0),
    ("상품이 정말 좋아요", 1),
]
weights = {"좋아요": 2, "빠르고": 1, "늦고": -1, "불편해요": -2}

for sentence, label in sentences:
    print("문장:", sentence, "정답:", label)
