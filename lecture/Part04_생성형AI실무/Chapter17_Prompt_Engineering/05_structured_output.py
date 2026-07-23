import json


####################################################
# 17.5 Structured Output: JSON schema의 핵심 조건 검사
####################################################
raw_output = '{"category": "배송", "priority": "high"}'
allowed_categories = {"배송", "환불", "계정", "기타"}
required = {"category", "priority"}
result = json.loads(raw_output)

missing = required - result.keys()
valid_category = result.get("category") in allowed_categories
print("필수 필드 누락:", missing)
print("카테고리 허용값:", valid_category)
print("검증 성공:", not missing and valid_category)
