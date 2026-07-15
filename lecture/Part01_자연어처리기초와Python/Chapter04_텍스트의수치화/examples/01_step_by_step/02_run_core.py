from collections import Counter

documents = [
    "배송이 빠르고 포장이 좋아요",
    "배송이 늦어서 환불하고 싶어요",
    "상품 품질이 정말 좋아요",
]

for number, document in enumerate(documents, 1):
    print(number, document)

word_counts = []
for document in documents:
    words = document.split()
    word_counts.append(Counter(words))

print('핵심 처리 완료')
