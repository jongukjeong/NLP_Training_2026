import json


####################################################
# 19.1 Function Calling: 함수명과 인수 제안 검증
####################################################
tool_call = '{"name": "get_order", "arguments": {"order_id": "A-1004"}}'
call = json.loads(tool_call)
allowed_tools = {"get_order"}
valid_id = call["arguments"].get("order_id", "").startswith("A-")

print("도구 허용:", call["name"] in allowed_tools)
print("인수 형식:", valid_id)
print("모델의 제안이며, 검증 후 애플리케이션이 실행합니다.")
