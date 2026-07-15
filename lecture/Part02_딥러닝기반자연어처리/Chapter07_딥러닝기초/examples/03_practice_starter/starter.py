# Chapter 7 딥러닝 기초 Practice Starter

sentences = [
    ("배송이 빠르고 좋아요", 1),
    ("환불이 늦고 불편해요", 0),
    ("상품이 정말 좋아요", 1),
]
weights = {"좋아요": 2, "빠르고": 1, "늦고": -1, "불편해요": -2}

print("입력을 먼저 확인하세요.")
for sentence, label in sentences:
    print("문장:", sentence, "정답:", label)

# TODO 1: Basic Practice를 참고해 핵심 처리를 작성하세요.
# TODO 2: 처리 결과를 출력하세요.
# TODO 3: 아래 도전 과제를 하나 수행하세요.
# 오분류 문장이 생기도록 문장을 추가하고 가중치를 조정하세요.
