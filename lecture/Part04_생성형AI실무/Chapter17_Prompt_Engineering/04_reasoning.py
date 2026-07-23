####################################################
# 17.4 Reasoning: 내부 사고 대신 검증 가능한 계산 요청
####################################################
invoice = {"unit_price": 12000, "quantity": 3, "discount": 4000}
subtotal = invoice["unit_price"] * invoice["quantity"]
total = subtotal - invoice["discount"]
result = {
    "subtotal": subtotal,
    "discount": invoice["discount"],
    "total": total,
}

print("검증 가능한 계산 결과:", result)
assert result["subtotal"] - result["discount"] == result["total"]
