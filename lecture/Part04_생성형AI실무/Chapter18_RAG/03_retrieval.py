####################################################
# 18.3 Retrieval: Top-k와 Recall@k
####################################################
ranked_ids = ["d3", "d1", "d4", "d2"]
relevant_ids = {"d1", "d2"}

print("=== Recall@k ===")
for k in [1, 2, 3, 4]:
    found = relevant_ids & set(ranked_ids[:k])
    recall = len(found) / len(relevant_ids)
    print(f"Recall@{k}={recall:.2f}, 찾은 문서={sorted(found)}")
