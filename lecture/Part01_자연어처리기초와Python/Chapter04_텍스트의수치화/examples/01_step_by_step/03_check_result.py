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

for number, counts in enumerate(word_counts, 1):
    print(number, dict(counts))

query = "배송이 늦어요"
query_words = set(query.split())
for number, document in enumerate(documents, 1):
    score = len(query_words & set(document.split()))
    print(number, "검색 점수:", score)
