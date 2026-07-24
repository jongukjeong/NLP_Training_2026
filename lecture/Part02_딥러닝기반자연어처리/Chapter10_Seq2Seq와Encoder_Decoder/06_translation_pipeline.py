####################################################
# 10.6 번역 파이프라인과 간단한 평가
####################################################
dictionary = {"나는": "I", "학생": "student", "입니다": "am"}
source = "나는 학생 입니다".split()
reference = "I am a student".split()

encoded = [{"token": token, "position": i} for i, token in enumerate(source)]
translated = [dictionary.get(item["token"], "<UNK>") for item in encoded]
ordered = [translated[0], translated[2], "a", translated[1]]

print("=== 번역 파이프라인 ===")
print("입력:", source)
print("Encoder:", encoded)
print("Decoder:", ordered)
print("출력:", " ".join(ordered))

exact_match = ordered == reference
length_difference = len(ordered) - len(reference)

print("\n=== 간단한 평가 ===")
print("참고 번역:", " ".join(reference))
print("완전 일치:", exact_match)
print("생성-참고 길이 차이:", length_difference)
print("실제 번역 평가는 BLEU·chrF와 사람 평가도 함께 사용합니다.")
