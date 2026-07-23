####################################################
# 19.3 MCP: Prompts, Resources, Tools 구분
####################################################
mcp_server = {
    "prompts": ["주문 조회 안내"],
    "resources": ["orders://policy"],
    "tools": ["get_order"],
}

print("=== MCP Server 제공 항목 ===")
for capability, items in mcp_server.items():
    print(f"{capability:10s}: {items}")
print("연결 규약과 서버 신뢰성·권한 검증은 별개의 문제입니다.")
