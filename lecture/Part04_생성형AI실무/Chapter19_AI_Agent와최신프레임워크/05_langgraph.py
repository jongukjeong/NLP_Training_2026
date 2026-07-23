####################################################
# 19.5 LangGraph: 상태와 조건에 따른 다음 Node 선택
####################################################
state = {"request": "주문 취소", "approved": False, "retries": 0}

if "취소" in state["request"] and not state["approved"]:
    next_node = "request_approval"
elif state["approved"]:
    next_node = "execute_cancellation"
else:
    next_node = "answer"

print("현재 상태:", state)
print("다음 Node:", next_node)
