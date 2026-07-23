####################################################
# 18장 연결 예제: 검색과 생성 오류를 분리
####################################################
cases = [
    {"retrieved": True, "grounded": True},
    {"retrieved": False, "grounded": False},
    {"retrieved": True, "grounded": False},
]

for index, case in enumerate(cases, 1):
    if not case["retrieved"]:
        error = "retrieval_error"
    elif not case["grounded"]:
        error = "generation_error"
    else:
        error = "success"
    print(f"{index}번 사례:", error)
