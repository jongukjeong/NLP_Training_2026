import json


####################################################
# 14장 연결 예제: Prompt -> 생성 -> 구조 검증
####################################################
prompt = "배송 지연 안내를 JSON으로 작성하세요."
raw_output = '{"title": "배송 지연 안내", "message": "도착이 늦어 죄송합니다."}'

print("Prompt:", prompt)
try:
    result = json.loads(raw_output)
    required = {"title", "message"}
    missing = required - result.keys()
    assert not missing, f"필수 필드 누락: {missing}"
    print("검증된 결과:", result)
except (json.JSONDecodeError, AssertionError) as error:
    print("출력 검증 실패:", error)
