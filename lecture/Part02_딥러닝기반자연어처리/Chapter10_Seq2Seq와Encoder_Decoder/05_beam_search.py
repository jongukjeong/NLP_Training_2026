import math


####################################################
# 10.5 Beam Search: 누적 확률이 높은 후보 여러 개 유지
####################################################
BEAM_WIDTH = 2
MAX_STEPS = 5
LENGTH_ALPHA = 0.7

# 학습된 Decoder의 Softmax 출력을 흉내 낸 작은 확률표
next_token_probabilities = {
    ("<BOS>",): {"I": 0.8, "Me": 0.2},
    ("<BOS>", "I"): {"am": 0.7, "like": 0.3},
    ("<BOS>", "Me"): {"student": 0.8, "am": 0.2},
    ("<BOS>", "I", "am"): {"a": 0.6, "student": 0.4},
    ("<BOS>", "I", "like"): {"NLP": 0.8, "student": 0.2},
    ("<BOS>", "Me", "student"): {"<EOS>": 1.0},
    ("<BOS>", "I", "am", "a"): {"student": 0.9, "<EOS>": 0.1},
    ("<BOS>", "I", "am", "student"): {"<EOS>": 1.0},
    ("<BOS>", "I", "like", "NLP"): {"<EOS>": 1.0},
    ("<BOS>", "I", "am", "a", "student"): {"<EOS>": 1.0},
}

# 각 beam은 (토큰 tuple, 누적 log probability)로 저장한다.
beams = [(("<BOS>",), 0.0)]

print("=== Beam Search (beam width=2) ===")
for step in range(1, MAX_STEPS + 1):
    expanded = []

    for tokens, log_score in beams:
        if tokens[-1] == "<EOS>":
            expanded.append((tokens, log_score))
            continue

        choices = next_token_probabilities.get(tokens, {"<EOS>": 1.0})
        for next_token, probability in choices.items():
            expanded.append(
                (tokens + (next_token,), log_score + math.log(probability))
            )

    beams = sorted(expanded, key=lambda item: item[1], reverse=True)[:BEAM_WIDTH]

    print(f"\n[{step}단계]")
    for tokens, log_score in beams:
        visible = " ".join(tokens[1:])
        print(f"  {visible:18s} log_score={log_score:.4f}")

    if all(tokens[-1] == "<EOS>" for tokens, _ in beams):
        break

print("\n=== 최종 길이 정규화 점수 ===")
ranked = []
for tokens, log_score in beams:
    output_length = max(1, len(tokens) - 2)  # BOS와 EOS 제외
    normalized = log_score / (output_length ** LENGTH_ALPHA)
    ranked.append((normalized, tokens))

for normalized, tokens in sorted(ranked, reverse=True):
    sentence = " ".join(token for token in tokens[1:] if token != "<EOS>")
    print(f"{sentence:18s} normalized_score={normalized:.4f}")
