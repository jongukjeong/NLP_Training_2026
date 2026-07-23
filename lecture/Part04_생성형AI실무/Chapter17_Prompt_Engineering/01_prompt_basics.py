####################################################
# 17.1 Prompt 기본: 목표·입력·제약·출력 계약
####################################################
parts = {
    "목표": "고객 문의 분류",
    "입력": "<inquiry>배송이 늦어요</inquiry>",
    "제약": "배송, 환불, 계정, 기타 중 하나",
    "출력": '{"category": "..."}',
}

print("=== Prompt 계약 ===")
for label, value in parts.items():
    print(f"{label}: {value}")
assert all(parts.values())
