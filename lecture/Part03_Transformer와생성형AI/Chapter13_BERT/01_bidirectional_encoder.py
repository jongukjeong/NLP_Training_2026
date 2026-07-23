####################################################
# 13.1 Bidirectional Encoder: 양쪽 문맥 사용
####################################################
sentence = ["배송이", "정말", "빨라요"]
position = 1
left_context = sentence[:position]
right_context = sentence[position + 1:]

print("대상 토큰:", sentence[position])
print("왼쪽 문맥:", left_context)
print("오른쪽 문맥:", right_context)
print("BERT Encoder는 두 방향 문맥을 함께 표현에 반영합니다.")
