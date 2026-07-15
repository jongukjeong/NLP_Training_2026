source_sentence = "나는 학생 입니다"
dictionary = {"나는": "I", "학생": "student", "입니다": "am"}

source_tokens = source_sentence.split()
print("입력 토큰:", source_tokens)

encoded = source_tokens
decoded = []
for token in encoded:
    decoded.append(dictionary.get(token, "[UNK]"))

print('핵심 처리 완료')
