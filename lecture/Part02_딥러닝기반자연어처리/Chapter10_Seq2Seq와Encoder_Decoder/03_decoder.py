####################################################
# 10.3 Decoder: 이전 출력과 문맥으로 다음 토큰 생성
####################################################
transitions = {
    "<BOS>": "I",
    "I": "am",
    "am": "a",
    "a": "student",
    "student": "<EOS>",
}
token = "<BOS>"
generated = []

print("=== Greedy Decoder ===")
while token != "<EOS>":
    token = transitions[token]
    if token != "<EOS>":
        generated.append(token)
    print("현재 토큰:", token)
print("생성 문장:", " ".join(generated))
