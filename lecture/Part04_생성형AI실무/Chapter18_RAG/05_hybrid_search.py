####################################################
# 18.5 Hybrid Search: 서로 다른 순위를 RRF로 결합
####################################################
sparse_ranking = ["d1", "d3", "d2"]
dense_ranking = ["d2", "d1", "d4"]
k = 60
scores = {}

for ranking in [sparse_ranking, dense_ranking]:
    for rank, document_id in enumerate(ranking, 1):
        scores[document_id] = scores.get(document_id, 0) + 1 / (k + rank)

print("=== Reciprocal Rank Fusion ===")
for document_id, score in sorted(scores.items(), key=lambda item: item[1], reverse=True):
    print(document_id, f"{score:.5f}")
