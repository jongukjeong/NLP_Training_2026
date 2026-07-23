####################################################
# 16.2 GPT 계열: 관리형 API 선택 기준 예
####################################################
requirements = {"tool_calling", "structured_output", "korean"}
models = [
    {"name": "api-small", "features": {"structured_output", "korean"}},
    {"name": "api-general", "features": {"tool_calling", "structured_output", "korean"}},
]

print("필수 기능:", requirements)
for model in models:
    missing = requirements - model["features"]
    print(model["name"], "적합" if not missing else f"누락={missing}")
