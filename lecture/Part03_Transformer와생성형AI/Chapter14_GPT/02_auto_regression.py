####################################################
# 14.2 Auto Regression: 생성 토큰을 다음 입력에 다시 추가
####################################################
transitions = {"배송": "이", "이": "빠르게", "빠르게": "도착했습니다"}
tokens = ["배송"]

print("=== 자기회귀 생성 ===")
for _ in range(3):
    next_token = transitions[tokens[-1]]
    tokens.append(next_token)
    print("현재 문장:", " ".join(tokens))
