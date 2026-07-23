####################################################
# 14.3 Prompting: 작업 명세의 구성 요소 점검
####################################################
prompt = {
    "task": "배송 지연 안내문 작성",
    "audience": "고객",
    "tone": "정중하게",
    "format": "세 문장",
    "constraint": "보상 약속 금지",
}

print("=== Prompt 구성 ===")
for key, value in prompt.items():
    print(f"{key:10s}: {value}")
print("빠진 값:", [key for key, value in prompt.items() if not value])
