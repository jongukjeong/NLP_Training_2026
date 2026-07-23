####################################################
# 17.2 Zero-shot: 예시 없이 규칙만 제공
####################################################
instruction = "문의를 배송, 환불, 계정, 기타 중 하나로 분류하세요."
inquiry = "비밀번호를 잊어버렸어요."
keywords = {"배송": "배송", "환불": "환불", "비밀번호": "계정"}
category = next(
    (label for word, label in keywords.items() if word in inquiry),
    "기타",
)

print("지시:", instruction)
print("입력:", inquiry)
print("출력:", category)
