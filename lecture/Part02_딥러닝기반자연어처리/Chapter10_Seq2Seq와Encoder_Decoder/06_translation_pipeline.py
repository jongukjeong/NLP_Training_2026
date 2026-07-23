####################################################
# 10장 연결 예제: Encoder-Decoder 번역 흐름
####################################################
dictionary = {"나는": "I", "학생": "student", "입니다": "am"}
source = "나는 학생 입니다".split()

encoded = [{"token": token, "position": i} for i, token in enumerate(source)]
translated = [dictionary.get(item["token"], "<UNK>") for item in encoded]
ordered = [translated[0], translated[2], "a", translated[1]]

print("=== 번역 파이프라인 ===")
print("입력:", source)
print("Encoder:", encoded)
print("Decoder:", ordered)
print("출력:", " ".join(ordered))
