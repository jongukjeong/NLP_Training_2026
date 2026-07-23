####################################################
# 19장 연결 예제: Agent 도구 선택·승인·감사 로그
####################################################
request = {"tool": "cancel_order", "arguments": {"order_id": "A-1004"}}
write_tools = {"cancel_order", "send_email", "delete_file"}
approved = False
audit_log = []

if request["tool"] in write_tools and not approved:
    status = "blocked_for_approval"
else:
    status = "ready_to_execute"

audit_log.append({"request": request, "status": status})
print("상태:", status)
print("감사 로그:", audit_log)
