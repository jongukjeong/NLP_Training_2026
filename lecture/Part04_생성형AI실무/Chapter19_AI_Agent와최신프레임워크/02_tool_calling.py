####################################################
# 19.2 Tool Calling: 읽기와 쓰기 권한 분리
####################################################
tools = {
    "get_order": {"effect": "read", "approval": False},
    "cancel_order": {"effect": "write", "approval": True},
}

for name, policy in tools.items():
    action = "사용자 승인 필요" if policy["approval"] else "자동 조회 가능"
    print(f"{name:14s}: {policy['effect']}, {action}")
