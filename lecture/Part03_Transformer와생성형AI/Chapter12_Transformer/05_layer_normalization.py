import math


####################################################
# 12.5 Layer Normalization: 토큰별 평균과 분산 정규화
####################################################
vector = [1.0, 2.0, 5.0]
mean = sum(vector) / len(vector)
variance = sum((value - mean) ** 2 for value in vector) / len(vector)
normalized = [(value - mean) / math.sqrt(variance + 1e-5) for value in vector]

print("입력:", vector)
print("평균/분산:", round(mean, 4), round(variance, 4))
print("정규화:", [round(value, 4) for value in normalized])
print("정규화 평균:", round(sum(normalized) / len(normalized), 6))
