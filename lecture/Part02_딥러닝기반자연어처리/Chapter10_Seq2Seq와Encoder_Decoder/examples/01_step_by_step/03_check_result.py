source_sentence = "나는 학생 입니다"
dictionary = {"나는": "I", "학생": "student", "입니다": "am"}

source_tokens = source_sentence.split()
print("입력 토큰:", source_tokens)

encoded = source_tokens
decoded = []
for token in encoded:
    decoded.append(dictionary.get(token, "[UNK]"))

print("Encoder 결과:", encoded)
print("Decoder 결과:", decoded)
print("출력 문장:", " ".join(decoded))
