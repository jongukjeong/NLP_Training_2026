import math


####################################################
# 10.5 Beam Search: 누적 확률이 높은 후보 여러 개 유지
####################################################
candidates = [
    (["I", "am", "a", "student"], [0.8, 0.9, 0.7, 0.9]),
    (["I", "am", "student"], [0.8, 0.9, 0.6]),
    (["Me", "student"], [0.2, 0.7]),
]

ranked = []
for tokens, probabilities in candidates:
    log_score = sum(math.log(p) for p in probabilities)
    normalized = log_score / len(tokens)
    ranked.append((normalized, tokens))

print("=== 길이 정규화 Beam 후보 ===")
for score, tokens in sorted(ranked, reverse=True):
    print(f"{' '.join(tokens):16s} score={score:.4f}")
